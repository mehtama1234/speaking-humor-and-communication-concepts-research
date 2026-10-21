#!/usr/bin/env python3
"""Build the no-JavaScript first-edition reader. Requires pandoc on PATH."""

from html import escape
from pathlib import Path
import re
import subprocess
from urllib.parse import quote
from build_speaking_source_catalog import collect_sources

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "writeups" / "speaking-practice"
CURRICULA = ROOT / "writeups" / "speaking-curricula"
OUTPUT = ROOT / "site" / "speaking-practice.html"
BOOK = ROOT / "writeups" / "speaking-book"


def render_book_section(name, anchor):
    text = (BOOK / name).read_text()
    heading, body = text.split("\n", 1)
    if not heading.startswith("# "):
        raise ValueError(f"Missing book section title: {name}")
    body = re.sub(r"^(#{2,5}) ", r"\1# ", body, flags=re.M)
    rendered = subprocess.run(
        ["pandoc", "--from=markdown", "--to=html5", "--wrap=none", f"--id-prefix={anchor}-"],
        input=body, text=True, capture_output=True, check=True,
    ).stdout
    return (f'<section class="book-matter" id="{anchor}" aria-labelledby="{anchor}-title">'
            f'<h2 id="{anchor}-title">{escape(heading[2:])}</h2>{rendered}</section>')


def chapter_id(path):
    prefix = "path-" if path.parent == CURRICULA else "chapter-"
    return prefix + path.stem.split("-", 1)[0]


def build(output=OUTPUT, portable=False, catalog=None):
    catalog = catalog or collect_sources()
    source_by_path = {row["transcript"]: row for row in catalog["sources"]}
    chapter_sources = {row["number"]: row["sources"] for row in catalog["chapters"]}
    approach_files = sorted(SOURCE.glob("[0-9][0-9]-*.md"))
    curriculum_files = sorted(CURRICULA.glob("[0-9][0-9]-*.md"))
    files = approach_files + curriculum_files
    if not approach_files:
        raise ValueError("No chapters found")
    ids = [chapter_id(path) for path in files]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate chapter numbers")
    contents, chapters, path_contents, paths = [], [], [], []
    for path in files:
        text = path.read_text()
        heading, body = text.split("\n", 1)
        if not heading.startswith("# "):
            raise ValueError(f"Missing chapter title: {path}")
        title = heading[2:]
        anchor = chapter_id(path)

        def rewrite_link(match):
            label, target = match.groups()
            if "://" in target or target.startswith("#"):
                return match.group(0)
            target_path = (path.parent / target).resolve()
            if not target_path.is_file():
                raise ValueError(f"Broken source link: {path}: {target}")
            if target_path in files:
                href = "#" + chapter_id(target_path)
            elif portable:
                relative = target_path.relative_to(ROOT).as_posix()
                if relative in source_by_path:
                    href = "#source-" + source_by_path[relative]["video_id"]
                elif relative.startswith("analysis/"):
                    # Keep historical research-note references as plain text;
                    # the portable edition contains the developed lessons, not
                    # an incomplete copy of the research workspace.
                    return label
                else:
                    raise ValueError(f"No portable target for {relative}")
            else:
                href = "../" + quote(target_path.relative_to(ROOT).as_posix())
            return f"[{label}]({href})"

        body = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", rewrite_link, body)
        # Chapter titles become h2, their sections h3. Prefix heading IDs so
        # repeated section labels remain unique across the combined reader.
        body = re.sub(r"^(#{2,5}) ", r"\1# ", body, flags=re.M)
        rendered = subprocess.run(
            ["pandoc", "--from=markdown", "--to=html5", "--wrap=none",
             f"--id-prefix={anchor}-"],
            input=body, text=True, capture_output=True, check=True,
        ).stdout
        # Pandoc also prefixes internal link destinations; restore our global
        # chapter links while keeping its locally scoped heading IDs.
        for prefix in ("chapter-", "path-", "source-"):
            rendered = rendered.replace(f'href="#{anchor}-{prefix}', f'href="#{prefix}')
        is_path = path in curriculum_files
        toc = path_contents if is_path else contents
        articles = paths if is_path else chapters
        kind = "learning-path" if is_path else "approach"
        source_links = ""
        if not is_path:
            entries = [source_by_path[target] for target in chapter_sources[path.stem.split("-", 1)[0]]]
            links = [f'<a href="#source-{row["video_id"]}">{escape(row["channel"])} — {escape(row["title"])}</a>' for row in entries]
            source_links = '<p class="source-note">Original video sources: ' + ' · '.join(links) + '</p>'
            source_heading = re.search(r'<h3 id="[^"]*source-trail[^"]*">', rendered)
            if not source_heading:
                raise ValueError(f"Missing rendered source trail: {path}")
            split_at = source_heading.start()
            rendered = (rendered[:split_at] + '<section class="chapter-sources">'
                        + rendered[split_at:] + source_links + '</section>')
            source_links = ""
        back_target = "learning-paths" if is_path else "contents"
        back_label = "learning paths" if is_path else "chapters"
        siblings = curriculum_files if is_path else approach_files
        position = siblings.index(path)
        adjacent = []
        for offset, label in ((-1, "Previous"), (1, "Next")):
            neighbor = position + offset
            if 0 <= neighbor < len(siblings):
                target = siblings[neighbor]
                target_title = target.read_text().splitlines()[0][2:]
                adjacent.append(f'<a href="#{chapter_id(target)}">{label}: {escape(target_title)}</a>')
        onward = ('<nav class="chapter-navigation" aria-label="Adjacent reading">'
                  + ''.join(adjacent) + '</nav>')
        toc.append(f'<li><a href="#{anchor}">{escape(title)}</a></li>')
        articles.append(
            f'<article class="{kind}" id="{anchor}" aria-labelledby="{anchor}-title">'
            '<p class="reader-jump"><a href="#learning-paths">All learning paths</a> · '
            '<a href="#contents">All approach chapters</a></p>'
            f'<h2 id="{anchor}-title">{escape(title)}</h2>{rendered}{source_links}'
            f'<p class="back"><a href="#{back_target}">Back to {back_label}</a> · '
            f'<a href="#using-the-guide">Using the guide</a></p>{onward}</article>'
        )
    source_entries = []
    for row in catalog["sources"]:
        chapter_links = ' · '.join(f'<a href="#chapter-{number}">Chapter {number}</a>' for number in row["chapters"])
        local_link = "" if portable else f'<a href="../{quote(row["transcript"])}">Local research transcript</a>.'
        source_entries.append(
            f'<li id="source-{row["video_id"]}"><h3><a href="{escape(row["url"], quote=True)}">{escape(row["title"])}</a></h3>'
            f'<p>{escape(row["channel"])}</p><p class="source-note">Used in: {chapter_links}. '
            f'{local_link}</p></li>'
        )
    orientation = render_book_section("how-to-use.md", "using-the-guide")
    evidence = render_book_section("sources-and-evidence.md", "source-notes")
    if portable:
        navigation = '<a href="#using-the-guide">Speaking Practice</a><a href="#learning-paths">Learning paths</a>'
        footer = '<a href="#source-notes">Sources and evidence</a> · <a href="#contents">Approach chapters</a>'
        edition_note = '<p class="source-note">Portable first edition. Research-note references are retained as text; source citations lead to the video index. No raw transcripts are included.</p>'
    else:
        navigation = '<a href="./index.html">Speaking Research Atlas</a><a href="./curriculum.html">Curricula</a>'
        footer = '<a href="../analysis/speaking-release-audit.md">Edition scope and release audit</a> · <a href="./curriculum.html">Existing curriculum atlas</a>'
        edition_note = ""
    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Speaking Practice — The Detailed Guide</title>
  <meta name="description" content="Source-grounded lessons in presentation and conversation, with worked examples and practical exercises. First edition.">
  <link rel="stylesheet" href="./speaking-practice.css">
</head>
<body>
  <a class="skip" href="#main">Skip to the guide</a>
  <div class="shell">
    <nav class="top" aria-label="Atlas navigation">
      {navigation}
    </nav>
    <header>
      <p class="eyebrow">The detailed guide · First edition</p>
      <h1>Speaking practice,<br>one real situation at a time.</h1>
      <p class="intro">Understand the principle. See the move in context. Try it in your next conversation or presentation.</p>
      <p class="status">{len(approach_files)} of 27 approach chapters and {len(curriculum_files)} of 11 learning paths developed and editorially reviewed. Source readings, original worked examples and practical exercises. See the evidence notes for the limits of the source review.</p>
      {edition_note}
      <p class="reader-jump"><a href="#learning-paths">Follow a learning path</a> · <a href="#contents">Explore the approaches</a> · <a href="#using-the-guide">How to use this guide</a> · <a href="#source-notes">Sources and evidence</a></p>
    </header>
    <main id="main" tabindex="-1">
      <section class="contents-panel" id="learning-paths" aria-labelledby="paths-title">
        <p class="eyebrow">Put the approaches together</p>
        <h2 id="paths-title">Prepare for a real speaking situation.</h2>
        <p>Develop one piece of work through a sequence of practice sessions, worked examples and review. Choose the path closest to your next real occasion.</p>
        <ul>{''.join(path_contents)}</ul>
      </section>
      <section class="contents-panel" id="contents" aria-labelledby="contents-title">
        <p class="eyebrow">Choose a chapter</p>
        <h2 id="contents-title">Start with the situation you recognize.</h2>
        <p>Numbering follows the original research inventory. Read an approach on its own or follow it from a learning path.</p>
        <ol>{''.join(contents)}</ol>
        <p class="source-note">Source readings are drawn from the local transcripts. Invented application dialogues are labeled explicitly. Each chapter ends with its source trail and the scope of inspection.</p>
      </section>
      {orientation}
      {''.join(paths)}
      {''.join(chapters)}
      {evidence}
      <section class="book-matter" id="source-index" aria-labelledby="source-index-title">
        <p class="eyebrow">Original video sources</p>
        <h2 id="source-index-title">Source index</h2>
        <p>{catalog['source_count']} distinct sources cited across the 27 approach chapters. See each chapter's source trail for inspection scope; this count is not a full-corpus coverage claim.</p>
        <ol class="source-index">{''.join(source_entries)}</ol>
      </section>
    </main>
    <footer>{footer}</footer>
  </div>
</body>
</html>
'''
    output.write_text(page)
    print(f"Built {output.relative_to(ROOT)}: {len(approach_files)} chapters, {len(curriculum_files)} learning paths", flush=True)


if __name__ == "__main__":
    build()
