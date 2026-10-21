#!/usr/bin/env python3
"""Export the portable first edition; technical checks do not replace editorial review."""

from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile

import pymupdf as fitz
from playwright.sync_api import sync_playwright

from build_speaking_practice_reader import ROOT, SOURCE, CURRICULA, BOOK, build
from build_speaking_source_catalog import collect_sources

OUT = ROOT / "deliverables" / "speaking-practice"


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "href" in attrs:
            self.links.append(attrs["href"])
        if "src" in attrs:
            self.assets.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.assets.append(attrs["href"])


def normalized(text):
    text = " ".join(unicodedata.normalize("NFKC", text).replace("\u00ad", "").split())
    # PDF extraction inserts spaces at line wraps before/after dashes, including
    # "five-\nminute" and headings wrapped before an em dash. Preserve every
    # visible character while comparing those typographic breaks consistently.
    return re.sub(r"(?<=[\-–—])\s+|\s+(?=[\-–—])", "", text)


def check_local_document(path):
    document = Document()
    document.feed(path.read_text())
    assert len(document.ids) == len(set(document.ids)), "Duplicate HTML IDs"
    for href in document.links + document.assets:
        parts = urlsplit(href)
        if parts.scheme:
            assert parts.scheme == "https", href
            continue
        assert not parts.netloc, href
        if parts.path:
            target = (path.parent / unquote(parts.path)).resolve()
            assert target.is_relative_to(path.parent.resolve()), href
            assert target.is_file(), href
        if parts.fragment:
            assert unquote(parts.fragment) in document.ids, href
    assert all(not urlsplit(asset).scheme for asset in document.assets), "Remote rendering dependency"
    assert "raw-material/" not in path.read_text(), "Workspace transcript link leaked into portable HTML"
    return document


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    catalog = collect_sources()
    approaches = sorted(SOURCE.glob("[0-9][0-9]-*.md"))
    curricula = sorted(CURRICULA.glob("[0-9][0-9]-*.md"))
    assert len(approaches) == 27 and len(curricula) == 11, "Incomplete authored scope"
    inputs = approaches + curricula + sorted(BOOK.glob("*.md")) + [
        ROOT / "site" / "speaking-practice.css",
        ROOT / "scripts" / "build_speaking_practice_reader.py",
        ROOT / "scripts" / "build_speaking_source_catalog.py",
        Path(__file__).resolve(),
    ]
    input_hashes = {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest() for path in inputs}
    reader = OUT / "speaking-practice.html"
    pdf = OUT / "speaking-practice.pdf"
    build(output=reader, portable=True, catalog=catalog)
    shutil.copy2(ROOT / "site" / "speaking-practice.css", OUT / "speaking-practice.css")
    document = check_local_document(reader)
    preview = Path(tempfile.mkdtemp(prefix="speaking-practice-print-"))
    print("Checking offline reader and rendering PDF", flush=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(java_script_enabled=False, offline=True)
        page = context.new_page()
        for width in (320, 390, 768, 1280):
            print(f"Checking offline width {width}", flush=True)
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(reader.as_uri())
            assert page.locator("article.approach").count() == 27
            assert page.locator("article.learning-path").count() == 11
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
            page.keyboard.press("Tab")
            assert page.locator(".skip").evaluate("el => el === document.activeElement")
            page.keyboard.press("Enter")
            page.wait_for_url("**#main", timeout=10000)
            assert page.url.endswith("#main")
        # Collect every substantive rendered text block, not only titles.
        blocks = page.locator("article h2, article h3, article p, article li, .book-matter h2, .book-matter h3, .book-matter p, .book-matter li").evaluate_all(
            "els => els.filter(el => !el.classList.contains('back') && !el.classList.contains('reader-jump')).map(el => el.innerText)"
        )
        page.emulate_media(media="print")
        assert page.locator("#main").evaluate("el => getComputedStyle(el).outlineStyle === 'none'"), "Keyboard focus outline leaked into print"
        # Print styling lives in the stylesheet. Injecting it with add_style_tag
        # waits for an onload callback that cannot run with JavaScript disabled.
        print("Rendering paginated PDF", flush=True)
        page.pdf(path=str(pdf), format="A4", print_background=True,
                 display_header_footer=True, header_template="<span></span>",
                 footer_template='<div style="width:100%;text-align:center;font-size:8px;color:#555">Speaking Practice · First edition · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                 margin={"top":"18mm", "bottom":"18mm", "left":"19mm", "right":"19mm"},
                 tagged=True, outline=True)
        browser.close()
    print("Checking PDF text, links and page geometry", flush=True)
    with fitz.open(pdf) as print_document:
        text = normalized(" ".join(page.get_text(sort=True) for page in print_document))
        # Running footers may fall inside paragraphs split across pages.
        text = re.sub(r"Speaking Practice · First edition · \d+ / \d+", "", text)
        text = normalized(text)
        missing = [block for block in blocks if normalized(block) not in text]
        (OUT / "pdf-missing-blocks.json").write_text(json.dumps(missing, ensure_ascii=False, indent=2))
        assert not missing, f"PDF lost or reordered {len(missing)} text blocks; inspect pdf-missing-blocks.json"
        short_pages = []
        outside = []
        for index, printed_page in enumerate(print_document):
            if len(printed_page.get_text().split()) < 30:
                short_pages.append(index + 1)
            for word in printed_page.get_text("words"):
                x0, y0, x1, y1 = word[:4]
                if x0 < -1 or y0 < -1 or x1 > printed_page.rect.width + 1 or y1 > printed_page.rect.height + 1:
                    outside.append(index + 1)
            for link in printed_page.get_links():
                assert not link.get("uri", "").startswith("file:"), link
                assert link.get("kind") not in (fitz.LINK_GOTOR, fitz.LINK_LAUNCH), link
        assert not outside, f"Text outside page: {sorted(set(outside))}"
        for index in sorted({0, 5, len(print_document)//2, len(print_document)-1}):
            print_document[index].get_pixmap(matrix=fitz.Matrix(1, 1)).save(preview / f"page-{index+1}.png")
        page_count = len(print_document)
        pdf_link_count = sum(len(page.get_links()) for page in print_document)
    public_catalog = {
        "coverage_rule": catalog["coverage_rule"], "url_status": catalog["url_status"],
        "sources": [{key: row[key] for key in ("video_id", "title", "channel", "url", "chapters")} for row in catalog["sources"]],
    }
    (OUT / "sources.json").write_text(json.dumps(public_catalog, ensure_ascii=False, indent=2) + "\n")
    (OUT / "README.txt").write_text(
        "SPEAKING PRACTICE — PORTABLE FIRST EDITION\n\n"
        "Unzip the whole package, then open speaking-practice.html. It works offline, without JavaScript or an account. "
        "Keep speaking-practice.css beside it. Original video links require internet access.\n\n"
        "speaking-practice.pdf is the paginated reading edition. Both editions contain 27 approach chapters, "
        "11 learning paths, reader guidance and source notes. sources.json identifies the cited videos. "
        "Raw transcripts, audio, video and third-party imagery are not included. Research-note references "
        "remain as text; transcript citations lead to the source index.\n\n"
        "The authored chapters and learning paths have received editorial review. This is not a claim of licensing clearance, endorsement, "
        "complete-corpus review or measured learning outcomes. No sale or hosting is authorized by this export.\n"
    )
    assets = [reader, OUT / "speaking-practice.css", pdf, OUT / "sources.json", OUT / "README.txt"]
    manifest = {path.name: sha256(path.read_bytes()).hexdigest() for path in assets}
    archive = OUT / "speaking-practice.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in assets:
            bundle.write(path, path.name)
        bundle.writestr("manifest.json", json.dumps(manifest, indent=2) + "\n")
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        for name, digest in manifest.items():
            assert sha256(bundle.read(name)).hexdigest() == digest
        extraction = Path(tempfile.mkdtemp(prefix="speaking-practice-bundle-"))
        bundle.extractall(extraction)  # Only the fixed local assets above are written.
        check_local_document(extraction / reader.name)
    receipt = {
        "status": "portable_first_edition_technical_checks_pass",
        "chapters":27, "learning_paths":11, "sources":catalog["source_count"],
        "html_links_checked":len(document.links), "pdf_pages":page_count,
        "pdf_text_blocks_checked":len(blocks), "pdf_links":pdf_link_count,
        "pages_under_30_words_for_visual_review":short_pages,
        "pdf_text_outside_page":outside, "preview_directory":str(preview),
        "offline_no_js_widths":[320,390,768,1280], "archive_payload_hashes":manifest,
        "archive_sha256":sha256(archive.read_bytes()).hexdigest(),
        "extracted_bundle_directory":str(extraction),
        "authored_input_hashes":input_hashes,
    }
    assert all(sha256((ROOT / path).read_bytes()).hexdigest() == digest for path, digest in input_hashes.items()), "Inputs changed during export"
    (OUT / "export-check.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
