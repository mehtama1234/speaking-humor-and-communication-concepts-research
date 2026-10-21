#!/usr/bin/env python3
"""Build a reproducible corpus-to-named-approach evidence crosswalk."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "analysis" / "unified-integration-manifest.json"
APPROACHES = ROOT / "analysis" / "transcript-backed-concrete-speaking-approaches.md"
OUTPUT = ROOT / "analysis" / "source-to-approach-crosswalk.json"
APPROACH_HEADING = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
APPROACH_REF = re.compile(r"\bApproach\s+(\d+)\b")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    approach_text = APPROACHES.read_text(encoding="utf-8")
    approach_names = {
        int(match.group(1)): match.group(2)
        for line in approach_text.splitlines()
        if (match := APPROACH_HEADING.match(line))
    }
    if not approach_names:
        raise SystemExit("no numbered approaches found")

    rows = []
    for corpus in manifest["corpora"]:
        corpus_id = corpus["id"]
        prefix = corpus_id.removesuffix("-wave-1")
        files = sorted(ROOT.glob(f"analysis/{prefix}-wave-1-*.md"))
        occurrences: dict[int, list[dict[str, object]]] = {}
        for path in files:
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for match in APPROACH_REF.finditer(line):
                    number = int(match.group(1))
                    occurrences.setdefault(number, []).append(
                        {
                            "file": str(path.relative_to(ROOT)),
                            "line": line_number,
                        }
                    )
        approaches = []
        for number in sorted(occurrences):
            approaches.append(
                {
                    "approach_id": f"approach-{number:02d}",
                    "number": number,
                    "name": approach_names.get(number),
                    "occurrence_count": len(occurrences[number]),
                    "evidence_refs": occurrences[number],
                    "status": "transcript_derived_source_mapping",
                }
            )
        rows.append(
            {
                "corpus_id": corpus_id,
                "source": corpus["source"],
                "analysis_file_count": len(files),
                "approach_count": len(approaches),
                "approaches": approaches,
            }
        )

    result = {
        "schema_version": "1.0",
        "crosswalk_id": "source-to-approach-crosswalk",
        "generated_from": [
            "analysis/unified-integration-manifest.json",
            "analysis/transcript-backed-concrete-speaking-approaches.md",
            "analysis/*-wave-1-{corpus-brief,session-briefs,session-inventory,theme-map,drill-candidates}.md",
        ],
        "status": "transcript_derived_mapping_not_independently_validated",
        "claim_boundary": "Approach references show where the existing corpus notes connect a source to a named move. They do not prove semantic fit, recurrence, effectiveness, or independent review.",
        "approach_definition_count": len(approach_names),
        "corpus_count": len(rows),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.relative_to(ROOT)), "corpora": len(rows), "approaches": len(approach_names)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
