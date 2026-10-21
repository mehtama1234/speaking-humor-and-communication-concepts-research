#!/usr/bin/env python3
"""Select the performance-focused Stand-Up Studios starter slice."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "raw-material/youtube/manifests/stand-up-studios-wave-3.json"
OUTPUT = ROOT / "raw-material/youtube/manifests/stand-up-studios-wave-3-starter.json"
EXCLUDE = ("app", "instructional", "ad spot", "training video")

def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    selected = [entry for entry in source["videos"] if not any(term in entry.get("title", "").lower() for term in EXCLUDE)]
    output = {
        "slug": "stand-up-studios-wave-3-starter",
        "title": "Stand-Up Studios — Wave 3 Starter Slice",
        "url": source["url"],
        "category": "humor-exemplars",
        "source_manifest": "raw-material/youtube/manifests/stand-up-studios-wave-3.json",
        "selection_rule": "All channel videos whose titles are performance, showcase, comedy, spoof, story, or class content; app, advertising, and instructional uploads excluded.",
        "notes": "Bounded performance-focused slice. It is not a representative sample of other comedy channels and is not promotion validated.",
        "videos": [{"index": i, "id": e["id"], "title": e.get("title", f"Video {i}"), "url": e.get("url") or f"https://www.youtube.com/watch?v={e['id']}"} for i, e in enumerate(selected, 1)],
        "excluded_video_ids": [e["id"] for e in source["videos"] if e not in selected],
    }
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "channel_videos": len(source["videos"]), "starter_videos": len(selected), "excluded_videos": len(source["videos"]) - len(selected)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
