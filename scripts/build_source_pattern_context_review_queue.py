#!/usr/bin/env python3
"""Select a bounded, source-diverse contextual review queue from pattern leads."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADS = ROOT / "analysis" / "source-to-presentation-pattern-leads.json"
OUTPUT = ROOT / "analysis" / "source-pattern-context-review-queue.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-pattern", type=int, default=2)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.per_pattern < 1:
        raise SystemExit("--per-pattern must be positive")

    source_map = json.loads(LEADS.read_text(encoding="utf-8"))
    candidates: dict[str, list[dict]] = defaultdict(list)
    for row in source_map["rows"]:
        for lead in row["leads"]:
            candidates[lead["pattern_id"]].append(
                {
                    "corpus_id": row["corpus_id"],
                    "source": row["source"],
                    "candidate_form": lead["candidate_form"],
                    "category": lead["category"],
                    "matched_terms": lead["matched_terms"],
                    "source_files": lead["source_files"],
                }
            )

    items = []
    for pattern_id in sorted(candidates):
        selected = []
        seen_corpora = set()
        pool = sorted(
            candidates[pattern_id],
            key=lambda item: (-len(item["matched_terms"]), item["source"]),
        )
        for candidate in pool:
            if candidate["corpus_id"] in seen_corpora:
                continue
            seen_corpora.add(candidate["corpus_id"])
            selected.append(candidate)
            if len(selected) >= args.per_pattern:
                break
        for index, candidate in enumerate(selected, 1):
            item = dict(candidate)
            item.update(
                {
                    "review_item_id": f"source-pattern-{pattern_id}-{index:02d}",
                    "pattern_id": pattern_id,
                    "review_status": "unreviewed",
                    "review_instruction": "Read the cited analysis note, locate the underlying transcript/session evidence, and decide whether the source actually demonstrates the candidate form in context. Use indeterminate when the note or source context is insufficient.",
                    "does_not_establish": [
                        "semantic pattern validity",
                        "cross-speaker recurrence",
                        "delivery meaning",
                        "learner transfer",
                        "listener outcome",
                        "effectiveness",
                    ],
                }
            )
            items.append(item)

    result = {
        "schema_version": "1.0",
        "queue_id": "source-pattern-context-review-queue",
        "generated_from": ["analysis/source-to-presentation-pattern-leads.json"],
        "status": "unreviewed_contextual_review_queue",
        "claim_boundary": "This queue selects source-diverse review leads. It contains no reviewer judgment and does not validate any pattern.",
        "selection_rule": f"Select up to {args.per_pattern} distinct corpora per pattern, prioritizing distinct matched-term count.",
        "pattern_count_with_leads": len(candidates),
        "item_count": len(items),
        "review_status_counts": {"unreviewed": len(items)},
        "items": items,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.relative_to(ROOT)), "patterns": len(candidates), "items": len(items)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
