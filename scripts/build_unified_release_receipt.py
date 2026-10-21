#!/usr/bin/env python3
"""Join the two repositories' current release and claim-boundary receipts."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEST_ROOT = ROOT.parent / "best-speech-analysis"
OUTPUT = ROOT / "analysis" / "unified-release-receipt.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(command: list[str], cwd: Path) -> dict:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": " ".join(command),
        "return_code": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    site_check = run(["node", "scripts/validate_site_data.js"], ROOT)
    integration_check = run(["python3", "scripts/validate_unified_integration.py"], ROOT)
    external_review_check = run(["python3", "scripts/validate_external_review_launch_manifest.py"], BEST_ROOT)
    wave2_snapshot_check = run(["python3", "scripts/validate_wave2_crosswalk_snapshot.py"], BEST_ROOT)
    best_audit = load(BEST_ROOT / "research" / "autonomous-release-audit.json")
    best_end_to_end = load(BEST_ROOT / "research" / "autonomous-end-to-end-audit.json")
    readiness = load(BEST_ROOT / "research" / "communication-job-promotion-readiness.json")
    external_review = load(BEST_ROOT / "research" / "external-review-launch-manifest.json")
    browser_smoke = load(BEST_ROOT / "research" / "autonomous-browser-smoke.json")
    approach_crosswalk = load(ROOT / "analysis" / "source-to-approach-crosswalk.json")
    pattern_leads = load(ROOT / "analysis" / "source-to-presentation-pattern-leads.json")
    context_queue = load(ROOT / "analysis" / "source-pattern-context-review-queue.json")
    wave_2_queue = load(ROOT / "analysis" / "ali-siddiq-wave-2-context-review-queue.json")
    dry_bar_queue = load(ROOT / "analysis" / "dry-bar-comedy-wave-2-starter-context-review-queue.json")
    ted_queue = load(ROOT / "analysis" / "ted-wave-2-starter-context-review-queue.json")
    wave_2_crosswalk = load(ROOT / "analysis" / "wave-2-unified-candidate-crosswalk.json")
    wave_2_leads = load(ROOT / "analysis" / "wave-2-keyword-leads.json")
    review_smoke = load(ROOT / "analysis" / "source-pattern-review-browser-smoke.json")
    wave_2_handoff = load(ROOT / "analysis" / "unified-validation-handoff.json").get("wave_2_candidate_handoff", {})
    focused_review_html = (ROOT / "site" / "pattern-review-wave-2.html").read_text(encoding="utf-8")

    receipt = {
        "schema_version": "1.0",
        "receipt_id": "unified-speaking-system-release",
        "generated_on": date.today().isoformat(),
        "status": "release_candidate_reconciled_not_promotion_validated",
        "claim_boundary": "This joins repository-local artifact and runtime checks. It does not establish independent human review, learner transfer, listener outcomes, or communication effectiveness.",
        "speaking_atlas": {
            "corpus_count": 10,
            "vertical_slice_count": 4,
            "named_approach_definition_count": approach_crosswalk.get("approach_definition_count"),
            "source_to_approach_row_count": len(approach_crosswalk.get("rows", [])),
            "presentation_pattern_candidate_count": pattern_leads.get("pattern_count"),
            "presentation_patterns_with_keyword_leads": pattern_leads.get("patterns_with_any_lead"),
            "presentation_patterns_without_any_lead": len(pattern_leads.get("patterns_without_any_lead", [])),
            "contextual_review_queue_item_count": context_queue.get("item_count"),
            "contextual_review_queue_status": context_queue.get("status"),
            "wave_2_source_count": 3,
            "wave_2_review_queue_item_count": len(wave_2_queue.get("items", [])) + len(dry_bar_queue.get("items", [])) + len(ted_queue.get("items", [])),
            "wave_2_candidate_pattern_count": len(wave_2_crosswalk.get("rows", [])),
            "wave_2_keyword_lead_row_count": len(wave_2_leads.get("rows", [])),
            "wave_2_transcript_count": sum(item.get("transcripts_available", 0) for item in wave_2_crosswalk.get("source_scope", {}).values()),
            "combined_contextual_review_browser_item_count": context_queue.get("item_count", 0) + len(wave_2_queue.get("items", [])) + len(dry_bar_queue.get("items", [])) + len(ted_queue.get("items", [])),
            "wave_2_focused_review_browser_item_count": focused_review_html.count('class="review-card"'),
            "wave_2_reviewer_pack": wave_2_handoff.get("reviewer_pack"),
            "wave_2_reviewer_pack_reference_count": wave_2_handoff.get("review_scope", {}).get("context_reference_count"),
            "wave_2_reviewer_pack_unique_transcripts": wave_2_handoff.get("review_scope", {}).get("reviewer_pack_unique_transcript_count"),
            "wave_2_reviewer_pack_unique_cue_files": wave_2_handoff.get("review_scope", {}).get("reviewer_pack_unique_cue_file_count"),
            "wave_2_reviewer_pack_checksums_verified": wave_2_handoff.get("review_scope", {}).get("reviewer_pack_checksums_verified"),
            "contextual_review_browser_smoke_status": review_smoke.get("status"),
            "site_data_check": site_check,
            "integration_check": integration_check,
        },
        "best_speech_analysis": {
            "release_audit_status": best_audit.get("status"),
            "release_audit_steps": {
                "passed": best_audit.get("passed_step_count"),
                "total": best_audit.get("step_count"),
            },
            "browser_smoke_status": browser_smoke.get("status"),
            "end_to_end_status": best_end_to_end.get("status"),
            "promotion_status": readiness.get("status"),
            "promotion_ready_cards": readiness.get("promotion_ready_count"),
            "promotion_card_count": readiness.get("card_count"),
            "external_review_launch": {
                "status": external_review.get("status"),
                "operation_count": len(external_review.get("operations", [])),
                "first_action": external_review.get("first_action"),
                "promotion_ready_cards": external_review.get("promotion_ready_cards"),
                "claim_boundary": external_review.get("claim_boundary"),
                "manifest_check": external_review_check,
                "wave2_snapshot_check": wave2_snapshot_check,
            },
        },
        "required_external_evidence": [
            "independent identity, function, recurrence, phrase-form and multimodal review records",
            "reviewed counterexamples and misuse boundaries",
            "consented learner teachability and transfer records",
            "locked listener stimuli and blinded listener outcome records",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.relative_to(ROOT)), "status": receipt["status"]}, indent=2))
    return 0 if site_check["return_code"] == 0 and integration_check["return_code"] == 0 and external_review_check["return_code"] == 0 and wave2_snapshot_check["return_code"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
