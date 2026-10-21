#!/usr/bin/env python3
"""Select a bounded distinct-speaker TED starter slice."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "raw-material/youtube/manifests/ted-wave-2.json"
OUTPUT = ROOT / "raw-material/youtube/manifests/ted-wave-2-starter.json"


def speaker_key(title: str) -> str:
    parts = [part.strip() for part in title.split("|")]
    if len(parts) < 2:
        return title.lower()
    speaker = parts[-2] if parts[-1].lower() == "ted" else parts[-1]
    speaker = re.sub(r"\b(TED Intersections|TED Talks|TED)\b", "", speaker, flags=re.I)
    return re.sub(r"\s+", " ", speaker).strip().lower() or title.lower()


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    chosen = []
    seen: set[str] = set()
    for entry in source["videos"]:
        title = entry.get("title", "")
        if "TED" not in title:
            continue
        key = speaker_key(title)
        if key in seen:
            continue
        seen.add(key)
        chosen.append(entry)
        if len(chosen) == 40:
            break
    output = {
        "slug": "ted-wave-2-starter",
        "title": "TED — Wave 2 Starter Slice",
        "url": source["url"],
        "category": "polished-talks",
        "source_manifest": "raw-material/youtube/manifests/ted-wave-2.json",
        "selection_rule": "First 40 title-qualified talks with distinct speaker keys; channel-level manifest remains 4,842 videos.",
        "notes": "Transcript-backed starter slice only. It is not a representative sample of the full channel and is not promotion validated.",
        "videos": [
            {"index": index, "id": entry["id"], "title": entry.get("title", f"Video {index}"), "url": entry.get("url") or f"https://www.youtube.com/watch?v={entry['id']}"}
            for index, entry in enumerate(chosen, 1)
        ],
    }
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "channel_videos": len(source["videos"]), "starter_videos": len(chosen)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
