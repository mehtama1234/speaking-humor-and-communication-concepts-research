#!/usr/bin/env python3
"""Package the 19 full-context candidate review without marking others reviewed."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from build_source_pattern_review_browser import load_review_items, load_wave_2_ids


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "site/pattern-review-wave-2.html"
CSS = ROOT / "site/styles.css"
REQUEST = ROOT / "analysis/wave-2-context-review-request.md"
OUTPUT = ROOT / "deliverables/wave-2-full-context-reviewer-pack.zip"


def build(output: Path = OUTPUT) -> dict:
    all_items, _ = load_review_items()
    wave_ids = load_wave_2_ids()
    targets = [item for item in all_items if item["review_item_id"] in wave_ids]
    page = PAGE.read_bytes()
    html_text = page.decode("utf-8")
    css = CSS.read_bytes()
    request = REQUEST.read_bytes()
    if len(targets) != 19 or len(all_items) != 107 or len(wave_ids) != 19:
        raise ValueError("expected 19 wave-2 candidates in a 107-item combined queue")
    if html_text.count('class="review-card"') != 19:
        raise ValueError("focused browser must render exactly the 19 target cards")
    id_match = re.search(r'<script id="all-queue-ids" type="application/json">(.*?)</script>', html_text, re.DOTALL)
    if not id_match or set(json.loads(id_match.group(1))) != {item["review_item_id"] for item in all_items}:
        raise ValueError("focused browser does not retain exact combined-queue IDs")
    if "other 88 combined-queue items are not displayed" not in html_text:
        raise ValueError("focused browser must disclose the 88 omitted items")
    reference_count = sum(len(item["context_references"]) for item in targets)
    if reference_count != 56:
        raise ValueError(f"expected 56 target context references, got {reference_count}")

    local_paths = {"site/pattern-review-wave-2.html": page, "site/styles.css": css, "analysis/wave-2-context-review-request.md": request}
    for item in targets:
        for reference in item["context_references"]:
            for field in ("clean_transcript", "cue_file"):
                relative = reference.get(field)
                if not isinstance(relative, str):
                    raise ValueError(f"{field} missing for {item['review_item_id']}")
                source = (ROOT / relative).resolve()
                if ROOT not in source.parents or not source.is_file():
                    raise ValueError(f"unsafe or missing context asset: {relative}")
                local_paths[Path(relative).as_posix()] = source.read_bytes()
    transcript_count = sum("/clean/" in name and "/transcripts/" in name for name in local_paths)
    cue_count = sum("/cues/" in name for name in local_paths)
    if transcript_count != 43 or cue_count != 43:
        raise ValueError(f"expected 43 unique transcripts and cues, got {transcript_count} and {cue_count}")

    readme = f"""# Wave-2 full-context candidate review

This focused reviewer pack contains exactly 19 provisional candidates: seven
Ali Siddiq, six Dry Bar Comedy, and six TED. The other 88 IDs in the combined
review queue are not shown and remain explicitly unreviewed in exports. The pack
includes all 56 cited transcript references, their {transcript_count} unique
full transcripts and {cue_count} unique cue/timing files, plus direct links to
the source videos.

## Independence and task

Review independently of the people who assembled the transcript packets,
proposed these candidate patterns, and created the crosswalk. Do not view or
discuss another reviewer's decisions before returning yours. Use a pseudonymous
reviewer code. For each displayed candidate, inspect the original source video
and all cited full-transcript/cue context, not only the retrieved excerpts.
Choose supports, does not support, or indeterminate and record uncertainty,
identity concerns, and counterexamples. Do not infer recurrence, transfer, or
effectiveness.

## Browser and export

Unzip while preserving the folder structure, then open
`site/pattern-review-wave-2.html`. Review the 19 displayed items and export the
completed records. The exported denominator remains 107, with the other 88 IDs
explicitly listed as unreviewed. Return the JSON unchanged. From the project
repository, validate it with:

```text
python3 scripts/validate_source_pattern_review_export.py reviewer-wave-2.json
```

Expected targeted coverage is `19/107`, partial with missingness preserved,
and wave-2 coverage `19/19`. Preserve reviewer exports separately. Contextual
fit does not establish source identity across events, recurrence, delivery
meaning, learner transfer, listener outcomes, or effectiveness. No review
decisions are included in this pack.
""".encode()
    files = {**local_paths, "README-reviewer.md": readme}
    sums = "".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in sorted(files.items())).encode()
    files["SHA256SUMS"] = sums

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(output) as archive:
        if set(archive.namelist()) != set(files):
            raise ValueError("reviewer archive members do not match the checked file set")
        for name, data in files.items():
            if archive.read(name) != data:
                raise ValueError(f"archive content mismatch: {name}")
        for line in archive.read("SHA256SUMS").decode().splitlines():
            digest, name = line.split("  ", 1)
            if hashlib.sha256(archive.read(name)).hexdigest() != digest:
                raise ValueError(f"archive checksum mismatch: {name}")

    return {
        "output": str(output),
        "target_item_count": 19,
        "combined_queue_denominator": 107,
        "explicitly_unreviewed_other_items": 88,
        "context_references": reference_count,
        "unique_transcripts": transcript_count,
        "unique_cue_files": cue_count,
        "private_or_unreviewed_records_included": False,
        "checksums_verified": True,
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
