#!/usr/bin/env python3
"""Index sources cited by the authored chapters; do not infer review coverage."""

from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "writeups" / "speaking-practice"
OUTPUT = ROOT / "analysis" / "speaking-source-catalog.json"


def collect_sources():
    sources = {}
    chapters = []
    for chapter in sorted(CHAPTERS.glob("[0-9][0-9]-*.md")):
        text = chapter.read_text()
        cited = []
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "raw-material/youtube/transcripts/" not in target:
                continue
            transcript = (chapter.parent / target).resolve()
            relative = transcript.relative_to(ROOT).as_posix()
            if not transcript.is_file():
                raise ValueError(f"Missing transcript: {relative}")
            match = re.fullmatch(r"\d{3}-([A-Za-z0-9_-]{11})", transcript.stem)
            if not match:
                raise ValueError(f"Unrecognized source identifier: {relative}")
            video_id = match[1]
            if relative not in sources:
                directory = ROOT / "raw-material" / "youtube" / "metadata" / transcript.parent.parent.name
                matches = []
                for candidate in directory.glob(f"*-{video_id}-*.info.json"):
                    data = json.loads(candidate.read_text())
                    if data.get("id") == video_id:
                        matches.append((candidate, data))
                if len(matches) != 1:
                    raise ValueError(f"Expected one metadata record for {relative}, got {len(matches)}")
                metadata, data = matches[0]
                url = data.get("webpage_url", "")
                parts = urlsplit(url)
                if (parts.scheme != "https" or parts.hostname not in ("youtube.com", "www.youtube.com")
                        or parse_qs(parts.query).get("v") != [video_id]):
                    raise ValueError(f"Unexpected public source URL: {url}")
                if not data.get("title") or not data.get("channel"):
                    raise ValueError(f"Missing source attribution: {metadata}")
                sources[relative] = {
                    "video_id": video_id,
                    "title": data["title"],
                    "channel": data["channel"],
                    "url": url,
                    "transcript": relative,
                    "transcript_sha256": sha256(transcript.read_bytes()).hexdigest(),
                    "metadata": metadata.relative_to(ROOT).as_posix(),
                    "chapters": [],
                }
            number = chapter.stem.split("-", 1)[0]
            if number not in sources[relative]["chapters"]:
                sources[relative]["chapters"].append(number)
            cited.append(relative)
        if not cited:
            raise ValueError(f"Chapter has no transcript citation: {chapter.name}")
        sections = re.split(r"^## Source[^\n]*\n", text, flags=re.M)
        if len(sections) != 2:
            raise ValueError(f"Expected one source trail: {chapter.name}")
        chapters.append({
            "number": chapter.stem.split("-", 1)[0],
            "file": chapter.relative_to(ROOT).as_posix(),
            "title": text.splitlines()[0][2:],
            "sources": sorted(set(cited)),
            "source_trail_markdown": sections[1].strip(),
        })
    return {
        "description": "Sources cited by the authored approach chapters, not a full-corpus review certificate.",
        "coverage_rule": "Read each chapter's source trail for inspected passages and limits. A citation does not imply complete-video or audiovisual review.",
        "url_status": "Public URLs and titles match local acquisition metadata; current online availability is not verified by this build.",
        "chapter_count": len(chapters),
        "source_count": len(sources),
        "sources": sorted(sources.values(), key=lambda row: (row["channel"], row["title"])),
        "chapters": chapters,
    }


def main():
    catalog = collect_sources()
    OUTPUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    print(f"Indexed {catalog['source_count']} distinct sources across {catalog['chapter_count']} chapters")


if __name__ == "__main__":
    main()
