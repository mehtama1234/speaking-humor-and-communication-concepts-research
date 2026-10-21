#!/usr/bin/env python3
"""Fail-closed validator for exported source-pattern contextual reviews."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "analysis" / "source-pattern-context-review-queue.json"
WAVE_2_QUEUE = ROOT / "analysis" / "ali-siddiq-wave-2-context-review-queue.json"
DRY_BAR_QUEUE = ROOT / "analysis" / "dry-bar-comedy-wave-2-starter-context-review-queue.json"
TED_QUEUE = ROOT / "analysis" / "ted-wave-2-starter-context-review-queue.json"
CROSSWALK = ROOT / "analysis" / "wave-2-unified-candidate-crosswalk.json"


def validate_export(export: dict) -> tuple[list[str], int, int, int]:
    if not isinstance(export, dict):
        return ["export must be an object"], 0, 0, 0
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    expected = {item["review_item_id"] for item in queue["items"]}
    wave2_ids = set()
    errors = []
    for path in (WAVE_2_QUEUE, DRY_BAR_QUEUE, TED_QUEUE):
        if path.is_file():
            wave = json.loads(path.read_text(encoding="utf-8"))
            wave2_ids.update(item["item_id"] for item in wave.get("items", []))
            expected.update(item["item_id"] for item in wave.get("items", []))
    if CROSSWALK.is_file():
        crosswalk_ids = {
            row.get("review_item_id")
            for row in json.loads(CROSSWALK.read_text(encoding="utf-8")).get("rows", [])
        }
        if crosswalk_ids != wave2_ids:
            errors.append("wave-2 queue IDs do not match the unified crosswalk")
            wave2_ids = set()

    records = export.get("records")
    if not isinstance(records, list):
        records = []
        errors.append("records must be an array")
    record_ids = [record.get("review_item_id") for record in records if isinstance(record, dict)]
    if any(not isinstance(item_id, str) or not item_id for item_id in record_ids):
        errors.append("review_item_id must be a nonempty string")
    valid_record_ids = [item_id for item_id in record_ids if isinstance(item_id, str) and item_id]
    actual = set(valid_record_ids)
    if len(actual) != len(valid_record_ids):
        errors.append("duplicate review_item_id")
    unreviewed_value = export.get("unreviewed_item_ids")
    if not isinstance(unreviewed_value, list):
        unreviewed_value = []
        errors.append("unreviewed_item_ids must be an array")
    if any(not isinstance(item_id, str) or not item_id for item_id in unreviewed_value):
        errors.append("unreviewed_item_id must be a nonempty string")
    valid_unreviewed_ids = [item_id for item_id in unreviewed_value if isinstance(item_id, str) and item_id]
    unreviewed = set(valid_unreviewed_ids)
    if len(unreviewed) != len(valid_unreviewed_ids):
        errors.append("duplicate unreviewed_item_id")
    if not actual:
        errors.append("at least one completed item is required")
    unknown = actual - expected
    if unknown:
        errors.append(f"unknown item_ids: {sorted(unknown)}")
    if actual & unreviewed:
        errors.append("reviewed and unreviewed item IDs overlap")
    if actual | unreviewed != expected:
        errors.append(f"coverage partition expected {len(expected)} items; reviewed {len(actual)} and explicitly unreviewed {len(unreviewed)}")
    if export.get("queue_item_count") != len(expected):
        errors.append(f"queue_item_count expected {len(expected)}")
    expected_status = "complete" if actual == expected and not unreviewed else "partial"
    if export.get("review_status") != expected_status:
        errors.append(f"review_status expected {expected_status}")
    if export.get("schema_version") != "1.0": errors.append("schema_version")
    if export.get("queue_id") != "source-pattern-context-review-queue": errors.append("queue_id")
    if not isinstance(export.get("reviewer_code"), str) or not export["reviewer_code"].strip(): errors.append("reviewer_code")
    if export.get("independence_confirmed") is not True: errors.append("independence_confirmed")
    if not isinstance(export.get("claim_boundary"), str) or not export["claim_boundary"].strip(): errors.append("claim_boundary")
    for record in records:
        if not isinstance(record, dict):
            errors.append("record must be an object")
            continue
        if not isinstance(record.get("decision"), str) or record["decision"] not in {"supports_candidate", "does_not_support", "indeterminate"}:
            errors.append(f"decision:{record.get('review_item_id')}")
        if record.get("context_inspected") is not True:
            errors.append(f"context_inspected:{record.get('review_item_id')}")
        if not isinstance(record.get("note", ""), str):
            errors.append(f"note:{record.get('review_item_id')}")
    return errors, len(actual), len(expected), len(actual & wave2_ids)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("export", type=Path)
    args = parser.parse_args()
    export = json.loads(args.export.read_text(encoding="utf-8"))
    errors, reviewed_count, queue_count, wave2_reviewed = validate_export(export)
    if errors:
        print("source-pattern review export invalid:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    coverage = "complete" if reviewed_count == queue_count else "partial; missingness preserved"
    print(f"source-pattern review export valid: {reviewed_count}/{queue_count} records; {coverage}; wave-2 coverage {wave2_reviewed}/19; no promotion implied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
