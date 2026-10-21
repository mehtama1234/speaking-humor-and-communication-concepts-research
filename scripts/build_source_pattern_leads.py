#!/usr/bin/env python3
"""Build keyword retrieval leads from the ten source corpora to 55 patterns."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEST_ROOT = ROOT.parent / "best-speech-analysis"
MANIFEST = ROOT / "analysis" / "unified-integration-manifest.json"
INVENTORY = BEST_ROOT / "research" / "exhaustive-pattern-inventory.json"
OUTPUT = ROOT / "analysis" / "source-to-presentation-pattern-leads.json"
WORD = re.compile(r"[a-z][a-z0-9_-]{2,}")
STOPWORDS = {
    "and", "the", "for", "with", "from", "that", "this", "into", "then",
    "when", "where", "what", "your", "their", "they", "will", "can", "may",
    "one", "not", "without", "before", "after", "through", "over", "about",
    "make", "more", "less", "use", "used", "using", "give", "get", "room",
    "speaker", "speaking", "audience", "communication", "talk", "idea",
}


def tokens(text: str) -> set[str]:
    return {word for word in WORD.findall(text.lower()) if word not in STOPWORDS}


def pattern_records(inventory: dict) -> list[dict]:
    records = []
    for item in inventory["themes"]:
        records.append({
            "pattern_id": item["theme_id"],
            "category": "core_theme",
            "candidate_form": item["candidate_form"],
            "keywords": tokens(item.get("matching_rule", "")) | tokens(item["theme_id"]),
        })
    for item in inventory["relation_patterns"]:
        records.append({
            "pattern_id": item["relation_type"],
            "category": "structural_relation",
            "candidate_form": item["candidate_form"],
            "keywords": tokens(item["relation_type"]) | tokens(item["candidate_form"]),
        })
    for item in inventory["unmatched_clusters"]:
        records.append({
            "pattern_id": item["cluster_id"],
            "category": "additional_cluster",
            "candidate_form": item["candidate_form"],
            "keywords": tokens(item.get("matching_rule", "")) | tokens(item["cluster_id"]),
        })
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    patterns = pattern_records(json.loads(INVENTORY.read_text(encoding="utf-8")))
    rows = []
    for corpus in manifest["corpora"]:
        prefix = corpus["id"].removesuffix("-wave-1")
        files = sorted(ROOT.glob(f"analysis/{prefix}-wave-1-*.md"))
        documents = [(path, path.read_text(encoding="utf-8")) for path in files]
        leads = []
        for pattern in patterns:
            hits = []
            all_terms: set[str] = set()
            for path, text in documents:
                matched = sorted(pattern["keywords"] & tokens(text))
                if matched:
                    hits.append({"file": str(path.relative_to(ROOT)), "matched_terms": matched})
                    all_terms.update(matched)
            # One generic token is not enough to create a lead. Keep the rule
            # deliberately conservative; zero leads remain visible below.
            if len(all_terms) >= 2:
                leads.append({
                    "pattern_id": pattern["pattern_id"],
                    "category": pattern["category"],
                    "candidate_form": pattern["candidate_form"],
                    "matched_term_count": len(all_terms),
                    "matched_terms": sorted(all_terms),
                    "source_files": hits,
                    "status": "keyword_lead_requires_contextual_review",
                })
        rows.append({
            "corpus_id": corpus["id"],
            "source": corpus["source"],
            "analysis_file_count": len(files),
            "lead_count": len(leads),
            "leads": sorted(leads, key=lambda item: (-item["matched_term_count"], item["pattern_id"])),
            "patterns_without_lead": sorted({p["pattern_id"] for p in patterns} - {l["pattern_id"] for l in leads}),
        })

    result = {
        "schema_version": "1.0",
        "lead_map_id": "source-to-presentation-pattern-leads",
        "generated_from": ["analysis/unified-integration-manifest.json", "../best-speech-analysis/research/exhaustive-pattern-inventory.json", "analysis/*-wave-1-*.md"],
        "status": "keyword_retrieval_leads_not_semantic_validation",
        "claim_boundary": "Keyword overlap is a retrieval aid. A lead is not evidence that a source teaches a pattern, that the pattern recurs, or that it is effective.",
        "pattern_count": len(patterns),
        "corpus_count": len(rows),
        "patterns_with_any_lead": len({lead["pattern_id"] for row in rows for lead in row["leads"]}),
        "patterns_without_any_lead": [
            {"pattern_id": pattern["pattern_id"], "category": pattern["category"], "candidate_form": pattern["candidate_form"]}
            for pattern in patterns
            if pattern["pattern_id"] not in {lead["pattern_id"] for row in rows for lead in row["leads"]}
        ],
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.relative_to(ROOT)), "corpora": len(rows), "patterns": len(patterns), "patterns_with_any_lead": result["patterns_with_any_lead"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
