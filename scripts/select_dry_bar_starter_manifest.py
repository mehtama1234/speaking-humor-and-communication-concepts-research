#!/usr/bin/env python3
"""Select a diverse Dry Bar Comedy starter slice from a channel manifest."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "raw-material/youtube/manifests/dry-bar-comedy-wave-2.json"
OUTPUT = ROOT / "raw-material/youtube/manifests/dry-bar-comedy-wave-2-starter.json"


def performer(title: str) -> str:
    parts = [part.strip() for part in title.split("|")]
    if len(parts) > 1:
        candidate = parts[-1]
        candidate = re.sub(r"\b(FULL SPECIAL|Double Feature|Stand-Up Comedy|Stand Up Comedy)\b", "", candidate, flags=re.I)
        if candidate.strip():
            return candidate.strip().lower()
    return title.lower()


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    entries = source["videos"]
    chosen = []
    seen: set[str] = set()
    priority = ("full special", "double feature", "stand-up", "stand up")
    for entry in entries:
        title = entry.get("title", "")
        lower = title.lower()
        if not any(marker in lower for marker in priority):
            continue
        key = performer(title)
        if key in seen:
            continue
        seen.add(key)
        chosen.append(entry)
        if len(chosen) == 40:
            break
    output = {
        "slug": "dry-bar-comedy-wave-2-starter",
        "title": "Dry Bar Comedy — Wave 2 Starter Slice",
        "url": source["url"],
        "category": "humor-exemplars",
        "source_manifest": "raw-material/youtube/manifests/dry-bar-comedy-wave-2.json",
        "selection_rule": "First 40 title-qualified exemplars with distinct performer keys; channel-level manifest remains 2,829 videos.",
        "notes": "Transcript-backed starter slice only. It is not a representative sample of the full channel and is not promotion validated.",
        "videos": [
            {
                "index": index,
                "id": entry["id"],
                "title": entry.get("title", f"Video {index}"),
                "url": entry.get("url") or f"https://www.youtube.com/watch?v={entry['id']}",
            }
            for index, entry in enumerate(chosen, 1)
        ],
    }
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "channel_videos": len(entries), "starter_videos": len(chosen)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
