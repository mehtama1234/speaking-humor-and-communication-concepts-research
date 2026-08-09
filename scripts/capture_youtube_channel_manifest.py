#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


def run_json(url: str, cwd: Path) -> dict[str, Any]:
    output = subprocess.check_output(
        ["yt-dlp", "--flat-playlist", "--dump-single-json", url],
        cwd=cwd,
        text=True,
    )
    return json.loads(output)


def stable_payload(data: dict[str, Any]) -> dict[str, Any]:
    out = dict(data)
    out.pop("epoch", None)
    return out


def normalize_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for index, entry in enumerate(entries, 1):
        video_id = entry.get("id")
        if not video_id:
            continue
        normalized.append(
            {
                "index": index,
                "id": video_id,
                "title": entry.get("title") or f"Video {index}",
                "url": entry.get("url") or f"https://www.youtube.com/watch?v={video_id}",
            }
        )
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture a stable flat-playlist manifest for a YouTube channel or playlist.")
    parser.add_argument("--workspace-root", type=Path, default=Path(__file__).resolve().parents[1], help="Repo root.")
    parser.add_argument("--slug", required=True, help="Stable slug for the source.")
    parser.add_argument("--title", required=True, help="Human-readable title for the source.")
    parser.add_argument("--url", required=True, help="Channel, playlist, or videos-tab URL.")
    parser.add_argument("--category", required=True, help="Source category, such as framework, examples, or charisma.")
    parser.add_argument("--notes", default="", help="Optional notes about why this source matters.")
    args = parser.parse_args()

    workspace_root = args.workspace_root.resolve()
    raw_root = workspace_root / "raw-material" / "youtube"
    channels_dir = raw_root / "channels"
    manifests_dir = raw_root / "manifests"
    channels_dir.mkdir(parents=True, exist_ok=True)
    manifests_dir.mkdir(parents=True, exist_ok=True)

    data = stable_payload(run_json(args.url, workspace_root))
    entries = normalize_entries(data.get("entries", []))

    raw_path = channels_dir / f"{args.slug}.json"
    manifest_path = manifests_dir / f"{args.slug}.json"

    raw_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest = {
        "slug": args.slug,
        "title": args.title,
        "url": args.url,
        "category": args.category,
        "notes": args.notes,
        "captured_on": "2026-08-09",
        "videos": entries,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {raw_path}")
    print(f"Wrote {manifest_path}")
    print(f"Captured {len(entries)} videos")


if __name__ == "__main__":
    main()
