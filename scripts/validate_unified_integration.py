#!/usr/bin/env python3
"""Validate the bridge between the speaking atlas and best-speech-analysis."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "analysis" / "unified-integration-manifest.json"
STATUS_PATH = ROOT / "analysis" / "source-corpus-status.json"
BRIDGE_PATH = ROOT / "analysis" / "unified-integration-plan.md"
CROSSWALK_PATH = ROOT / "analysis" / "source-to-job-crosswalk.json"
APPROACH_CROSSWALK_PATH = ROOT / "analysis" / "source-to-approach-crosswalk.json"
PATTERN_LEADS_PATH = ROOT / "analysis" / "source-to-presentation-pattern-leads.json"
CONTEXT_QUEUE_PATH = ROOT / "analysis" / "source-pattern-context-review-queue.json"
PATTERN_REVIEW_BROWSER_PATH = ROOT / "site" / "pattern-review.html"
WAVE_2_REVIEW_BROWSER_PATH = ROOT / "site" / "pattern-review-wave-2.html"
WAVE_2_REVIEW_PACK_PATH = ROOT / "deliverables" / "wave-2-full-context-reviewer-pack.zip"
REVIEW_SCHEMA_PATH = ROOT / "analysis" / "source-pattern-review-record.schema.json"
REVIEW_SMOKE_PATH = ROOT / "analysis" / "source-pattern-review-browser-smoke.json"
VERTICAL_SLICE_PATH = ROOT / "analysis" / "vertical-slice-01-awkwardness-repair.md"
VERTICAL_SLICES_02_04_PATH = ROOT / "analysis" / "vertical-slices-02-to-04.md"
SITE_INTEGRATION_PATH = ROOT / "site" / "integration.html"
VALIDATION_HANDOFF_PATH = ROOT / "analysis" / "unified-validation-handoff.json"
RELEASE_RECEIPT_PATH = ROOT / "analysis" / "unified-release-receipt.json"
WAVE_2_CANDIDATES_PATH = ROOT / "analysis" / "wave-2-integration-candidates.json"
WAVE_2_REVIEW_QUEUE_PATH = ROOT / "analysis" / "ali-siddiq-wave-2-context-review-queue.json"
WAVE_2_PACKETS_PATH = ROOT / "analysis" / "ali-siddiq-wave-2-context-packets.json"
WAVE_2_CROSSWALK_PATH = ROOT / "analysis" / "wave-2-source-to-approach-crosswalk.json"
DRY_BAR_CANDIDATES_PATH = ROOT / "analysis" / "dry-bar-comedy-wave-2-starter-integration-candidates.json"
DRY_BAR_REVIEW_QUEUE_PATH = ROOT / "analysis" / "dry-bar-comedy-wave-2-starter-context-review-queue.json"
DRY_BAR_PACKETS_PATH = ROOT / "analysis" / "dry-bar-comedy-wave-2-starter-context-packets.json"
TED_CANDIDATES_PATH = ROOT / "analysis" / "ted-wave-2-starter-integration-candidates.json"
TED_REVIEW_QUEUE_PATH = ROOT / "analysis" / "ted-wave-2-starter-context-review-queue.json"
TED_PACKETS_PATH = ROOT / "analysis" / "ted-wave-2-starter-context-packets.json"
WAVE_2_UNIFIED_CROSSWALK_PATH = ROOT / "analysis" / "wave-2-unified-candidate-crosswalk.json"
WAVE_2_CONTEXT_REVIEW_REQUEST_PATH = ROOT / "analysis" / "wave-2-context-review-request.md"
WAVE_2_KEYWORD_LEADS_PATH = ROOT / "analysis" / "wave-2-keyword-leads.json"
BEST_SPEECH_ROOT = ROOT.parent / "best-speech-analysis"
CANONICAL_JOBS_PATH = BEST_SPEECH_ROOT / "research" / "communication-job-curriculum-index.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> list[str]:
    errors: list[str] = []
    if not MANIFEST_PATH.is_file():
        return [f"missing manifest: {MANIFEST_PATH}"]
    if not STATUS_PATH.is_file():
        errors.append(f"missing corpus status: {STATUS_PATH}")
    if not BRIDGE_PATH.is_file():
        errors.append(f"missing integration plan: {BRIDGE_PATH}")
    if not CROSSWALK_PATH.is_file():
        errors.append(f"missing source-to-job crosswalk: {CROSSWALK_PATH}")
    if not APPROACH_CROSSWALK_PATH.is_file():
        errors.append(f"missing source-to-approach crosswalk: {APPROACH_CROSSWALK_PATH}")
    if not PATTERN_LEADS_PATH.is_file():
        errors.append(f"missing source-to-presentation-pattern leads: {PATTERN_LEADS_PATH}")
    if not CONTEXT_QUEUE_PATH.is_file():
        errors.append(f"missing source-pattern context review queue: {CONTEXT_QUEUE_PATH}")
    if not PATTERN_REVIEW_BROWSER_PATH.is_file():
        errors.append(f"missing pattern review browser: {PATTERN_REVIEW_BROWSER_PATH}")
    if not REVIEW_SCHEMA_PATH.is_file():
        errors.append(f"missing source-pattern review schema: {REVIEW_SCHEMA_PATH}")
    if not REVIEW_SMOKE_PATH.is_file():
        errors.append(f"missing source-pattern browser smoke receipt: {REVIEW_SMOKE_PATH}")
    if not VERTICAL_SLICE_PATH.is_file():
        errors.append(f"missing first vertical slice: {VERTICAL_SLICE_PATH}")
    if not VERTICAL_SLICES_02_04_PATH.is_file():
        errors.append(f"missing slices 02-04: {VERTICAL_SLICES_02_04_PATH}")
    if not SITE_INTEGRATION_PATH.is_file():
        errors.append(f"missing site integration page: {SITE_INTEGRATION_PATH}")
    if not VALIDATION_HANDOFF_PATH.is_file():
        errors.append(f"missing validation handoff: {VALIDATION_HANDOFF_PATH}")
    if not RELEASE_RECEIPT_PATH.is_file():
        errors.append(f"missing unified release receipt: {RELEASE_RECEIPT_PATH}")
    if not WAVE_2_CANDIDATES_PATH.is_file():
        errors.append(f"missing wave-2 integration candidates: {WAVE_2_CANDIDATES_PATH}")
    if not WAVE_2_REVIEW_QUEUE_PATH.is_file():
        errors.append(f"missing wave-2 review queue: {WAVE_2_REVIEW_QUEUE_PATH}")
    if not WAVE_2_PACKETS_PATH.is_file():
        errors.append(f"missing wave-2 context packets: {WAVE_2_PACKETS_PATH}")
    if not WAVE_2_CROSSWALK_PATH.is_file():
        errors.append(f"missing wave-2 approach crosswalk: {WAVE_2_CROSSWALK_PATH}")
    if not DRY_BAR_CANDIDATES_PATH.is_file():
        errors.append(f"missing Dry Bar integration candidates: {DRY_BAR_CANDIDATES_PATH}")
    if not DRY_BAR_REVIEW_QUEUE_PATH.is_file():
        errors.append(f"missing Dry Bar review queue: {DRY_BAR_REVIEW_QUEUE_PATH}")
    if not DRY_BAR_PACKETS_PATH.is_file():
        errors.append(f"missing Dry Bar context packets: {DRY_BAR_PACKETS_PATH}")
    if not TED_CANDIDATES_PATH.is_file():
        errors.append(f"missing TED integration candidates: {TED_CANDIDATES_PATH}")
    if not TED_REVIEW_QUEUE_PATH.is_file():
        errors.append(f"missing TED review queue: {TED_REVIEW_QUEUE_PATH}")
    if not TED_PACKETS_PATH.is_file():
        errors.append(f"missing TED context packets: {TED_PACKETS_PATH}")
    if not WAVE_2_UNIFIED_CROSSWALK_PATH.is_file():
        errors.append(f"missing unified wave-2 candidate crosswalk: {WAVE_2_UNIFIED_CROSSWALK_PATH}")
    if not WAVE_2_CONTEXT_REVIEW_REQUEST_PATH.is_file():
        errors.append(f"missing wave-2 contextual review request: {WAVE_2_CONTEXT_REVIEW_REQUEST_PATH}")
    if not WAVE_2_KEYWORD_LEADS_PATH.is_file():
        errors.append(f"missing unified wave-2 keyword leads: {WAVE_2_KEYWORD_LEADS_PATH}")
    if not BEST_SPEECH_ROOT.is_dir():
        errors.append(f"missing sibling project: {BEST_SPEECH_ROOT}")

    manifest = load(MANIFEST_PATH)
    required_top = {
        "schema_version",
        "upstream_projects",
        "evidence_layers",
        "corpora",
        "crosswalk_targets",
        "next_actions",
    }
    errors.extend(
        f"manifest missing top-level field: {field}"
        for field in sorted(required_top - set(manifest))
    )

    all_statuses = load(STATUS_PATH).get("sources", []) if STATUS_PATH.is_file() else []
    # Keep the validated wave-1 release count separate from captured wave-2
    # candidates. Wave-2 records remain useful in source status, but are not
    # allowed to silently change the release checkpoint.
    statuses = [
        item for item in all_statuses
        if str(item.get("status", "")).startswith("ingested-as-")
    ]
    status_by_name = {
        item.get("title", "").removesuffix(" Videos"): item.get("videos_captured")
        for item in statuses
    }
    corpora = manifest.get("corpora", [])
    seen_sources: set[str] = set()
    for corpus in corpora:
        source = corpus.get("source")
        corpus_id = corpus.get("id")
        if not source or not corpus_id:
            errors.append(f"corpus missing source or id: {corpus}")
            continue
        if source in seen_sources:
            errors.append(f"duplicate corpus source: {source}")
        seen_sources.add(source)
        if source not in status_by_name:
            errors.append(f"corpus not present in source status: {source}")
        elif corpus.get("videos_captured") != status_by_name[source]:
            errors.append(f"video count mismatch for {source}")
        starter = ROOT / "raw-material" / "youtube" / "starter-manifests" / f"{corpus_id}.json"
        if not starter.is_file():
            errors.append(f"missing starter manifest for {corpus_id}: {starter}")

    if len(corpora) != len(statuses):
        errors.append(f"corpus/status count mismatch: {len(corpora)} != {len(statuses)}")
    if len(manifest.get("evidence_layers", [])) != 5:
        errors.append("expected five explicit evidence layers")
    if VERTICAL_SLICE_PATH.is_file():
        slice_text = VERTICAL_SLICE_PATH.read_text(encoding="utf-8")
        for required in ("charisma-on-command-wave-1", "chad-littlefield-wave-1", "jefferson-fisher-wave-1", "repair_or_self_correction", "listener restatement"):
            if required not in slice_text:
                errors.append(f"vertical slice missing required integration field: {required}")
        for relative in (
            "raw-material/youtube/transcripts/charisma-on-command-wave-1/clean/040-_2tXNCxg8hs.txt",
            "analysis/evidence-moments.md",
            "analysis/chad-littlefield-wave-1-drill-candidates.md",
            "analysis/jefferson-fisher-wave-1-drill-candidates.md",
        ):
            if not (ROOT / relative).is_file():
                errors.append(f"vertical slice source file missing: {relative}")
    if VERTICAL_SLICES_02_04_PATH.is_file():
        slice_text = VERTICAL_SLICES_02_04_PATH.read_text(encoding="utf-8")
        for required in ("story_or_personal_experience", "opening", "answer_or_response", "learner transfer records"):
            if required not in slice_text:
                errors.append(f"slices 02-04 missing required integration field: {required}")
        for relative in (
            "raw-material/youtube/transcripts/ultraspeaking-wave-1/clean/024-GFnmSoMfncw.txt",
            "raw-material/youtube/transcripts/vinh-giang-wave-1/clean/017-HYNXzKU92Qs.txt",
            "raw-material/youtube/transcripts/ultraspeaking-wave-1/clean/016-miL69223IOU.txt",
            "raw-material/youtube/transcripts/vinh-giang-wave-1/clean/006-sbNc5eL7xNA.txt",
            "raw-material/youtube/transcripts/think-fast-talk-smart-wave-1/clean/021-GtNid29h70s.txt",
        ):
            if not (ROOT / relative).is_file():
                errors.append(f"slices 02-04 source file missing: {relative}")
    if SITE_INTEGRATION_PATH.is_file():
        page = SITE_INTEGRATION_PATH.read_text(encoding="utf-8")
        for required in ("Unified End-to-End System", "Ten transcript-backed corpora", "Awkwardness and interruption repair", "unified-integration-plan.md", "Nine patterns need targeted source review", "Ali Siddiq is captured, but not silently promoted", "148,482 transcript words", "Dry Bar Comedy is represented", "bounded 40-video", "13 contextual-review items", "TED is represented", "81,429 transcript words", "19 contextual-review items", "Combined review queue"):
            if required not in page:
                errors.append(f"site integration page missing required content: {required}")
    if VALIDATION_HANDOFF_PATH.is_file():
        handoff = load(VALIDATION_HANDOFF_PATH)
        slices = handoff.get("slices", [])
        if handoff.get("status") != "instruments_ready_no_human_records_received":
            errors.append("validation handoff must preserve the no-human-records status")
        if len(slices) != 4:
            errors.append(f"expected four validation slices, found {len(slices)}")
        wave_handoff = handoff.get("wave_2_candidate_handoff", {})
        for field in ("queue", "context_packets", "approach_crosswalk", "review_request", "review_browser", "reviewer_pack", "promotion_rule"):
            if not wave_handoff.get(field):
                errors.append(f"wave-2 candidate handoff missing field: {field}")
        if wave_handoff.get("status") != "candidate_packets_ready_no_human_records_received":
            errors.append("wave-2 candidate handoff must preserve its no-human-records status")
        review_scope = wave_handoff.get("review_scope", {})
        if review_scope.get("target_item_count") != 19 or review_scope.get("context_reference_count") != 56 or review_scope.get("retrieved_excerpt_count") != 108:
            errors.append("wave-2 handoff must record the 19-item, 56-reference, 108-excerpt context scope")
        if review_scope.get("partial_export_supported") is not True or review_scope.get("omitted_items_recorded_as_unreviewed") is not True:
            errors.append("wave-2 review handoff must preserve partial export missingness")
        if review_scope.get("dedicated_browser_item_count") != 19 or review_scope.get("omitted_combined_queue_items") != 88:
            errors.append("wave-2 handoff must identify the focused 19-item surface and 88 omitted items")
        if review_scope.get("reviewer_pack_unique_transcript_count") != 43 or review_scope.get("reviewer_pack_unique_cue_file_count") != 43:
            errors.append("wave-2 reviewer pack context asset counts are stale")
        if review_scope.get("human_review_status") != "no_human_records_received":
            errors.append("wave-2 review handoff must not imply human decisions")
        if WAVE_2_CONTEXT_REVIEW_REQUEST_PATH.is_file():
            request = WAVE_2_CONTEXT_REVIEW_REQUEST_PATH.read_text(encoding="utf-8")
            for required in ("19 transcript-derived candidates", "other 88 IDs", "wave-2 coverage 19/19", "not a human"):
                if required not in request:
                    errors.append(f"wave-2 contextual review request missing boundary/instruction: {required}")
        for item in slices:
            path = item.get("path", "").split("#", 1)[0]
            if not path or not (ROOT / path).is_file():
                errors.append(f"validation slice document missing: {item.get('path')}")
            if item.get("review_status") != "not_reviewed":
                errors.append(f"validation slice must remain not_reviewed: {item.get('slice_id')}")
            if not item.get("gates"):
                errors.append(f"validation slice has no gates: {item.get('slice_id')}")
        for relative in (
            "research/validation-handoff.json",
            "research/shared-evidence-model.json",
            "research/communication-job-learner-check.json",
            "research/communication-job-listener-outcome-protocol.json",
            "research/external-review-launch-manifest.json",
        ):
            if not (BEST_SPEECH_ROOT / relative).is_file():
                errors.append(f"best-speech validation target missing: {relative}")
    if RELEASE_RECEIPT_PATH.is_file():
        receipt = load(RELEASE_RECEIPT_PATH)
        if receipt.get("status") != "release_candidate_reconciled_not_promotion_validated":
            errors.append("unified release receipt must remain a reconciled, non-promotional checkpoint")
        if receipt.get("speaking_atlas", {}).get("corpus_count") != len(corpora):
            errors.append("unified release receipt corpus count does not match manifest")
        best = receipt.get("best_speech_analysis", {})
        if best.get("release_audit_status") != "release_audit_passed":
            errors.append("unified release receipt does not contain a passing best-speech release audit")
        if best.get("promotion_ready_cards") != 0:
            errors.append("unified release receipt must keep promotion-ready card count at zero")
        external_review = best.get("external_review_launch", {})
        if external_review.get("status") != "operations_ready_no_human_records_received":
            errors.append("unified release receipt must preserve the external-review no-human-records status")
        if external_review.get("operation_count") != 8:
            errors.append("unified release receipt must reconcile all eight external-review operations")
        if external_review.get("first_action") != "priority_pattern_review":
            errors.append("unified release receipt must route the priority pattern review as the first action")
        if external_review.get("promotion_ready_cards") != 0:
            errors.append("unified release receipt must keep external-review promotion count at zero")
        if external_review.get("manifest_check", {}).get("return_code") != 0:
            errors.append("unified release receipt must contain a passing external-review manifest check")
        if external_review.get("wave2_snapshot_check", {}).get("return_code") != 0:
            errors.append("unified release receipt must contain a passing wave-2 snapshot check")
        speaking = receipt.get("speaking_atlas", {})
        if speaking.get("wave_2_source_count") != 3 or speaking.get("wave_2_review_queue_item_count") != 19:
            errors.append("unified release receipt must preserve the nineteen-item wave-2 queues")
        if speaking.get("combined_contextual_review_browser_item_count") != 107:
            errors.append("unified release receipt must reconcile the combined 107-item review browser")
        if speaking.get("wave_2_focused_review_browser_item_count") != 19:
            errors.append("unified release receipt must reconcile the focused 19-item wave-2 browser")
        if speaking.get("wave_2_reviewer_pack_reference_count") != 56 or speaking.get("wave_2_reviewer_pack_unique_transcripts") != 43 or speaking.get("wave_2_reviewer_pack_unique_cue_files") != 43:
            errors.append("unified release receipt must reconcile the wave-2 review context bundle")
        if speaking.get("wave_2_reviewer_pack_checksums_verified") is not True:
            errors.append("unified release receipt must verify the wave-2 reviewer pack checksums")
        if speaking.get("wave_2_candidate_pattern_count") != 19 or speaking.get("wave_2_transcript_count") != 277:
            errors.append("unified release receipt must reconcile the 19 wave-2 candidate rows and 277 transcripts")
        if speaking.get("wave_2_keyword_lead_row_count") != 19:
            errors.append("unified release receipt must reconcile 19 wave-2 keyword lead rows")
    if WAVE_2_CANDIDATES_PATH.is_file() and WAVE_2_REVIEW_QUEUE_PATH.is_file() and WAVE_2_PACKETS_PATH.is_file() and WAVE_2_CROSSWALK_PATH.is_file():
        wave = load(WAVE_2_CANDIDATES_PATH)
        queue = load(WAVE_2_REVIEW_QUEUE_PATH)
        packets = load(WAVE_2_PACKETS_PATH)
        crosswalk = load(WAVE_2_CROSSWALK_PATH)
        if wave.get("status") != "wave_2_candidate_evidence_not_promoted":
            errors.append("wave-2 candidates must remain explicitly unpromoted")
        if len(queue.get("items", [])) != 7:
            errors.append("Ali wave-2 review queue must contain seven candidate items")
        if any(item.get("decision") != "unreviewed" for item in queue.get("items", [])):
            errors.append("Ali wave-2 review queue must remain unreviewed")
        if packets.get("status") != "machine_bounded_context_packets_not_human_review" or packets.get("item_count") != 7:
            errors.append("Ali wave-2 context packets must remain bounded and cover seven items")
        if {item.get("item_id") for item in queue.get("items", [])} != {item.get("item_id") for item in packets.get("packets", [])}:
            errors.append("Ali wave-2 context packets must reconcile queue item IDs")
        if crosswalk.get("status") != "transcript_derived_mapping_not_independently_validated" or len(crosswalk.get("rows", [])) != 7:
            errors.append("Ali wave-2 approach crosswalk must remain provisional and cover seven items")
    if DRY_BAR_CANDIDATES_PATH.is_file() and DRY_BAR_REVIEW_QUEUE_PATH.is_file() and DRY_BAR_PACKETS_PATH.is_file():
        dry = load(DRY_BAR_CANDIDATES_PATH)
        dry_queue = load(DRY_BAR_REVIEW_QUEUE_PATH)
        dry_packets = load(DRY_BAR_PACKETS_PATH)
        if dry.get("status") != "wave_2_candidate_evidence_not_promoted" or len(dry_queue.get("items", [])) != 6:
            errors.append("Dry Bar wave-2 candidates must remain provisional and cover six items")
        if dry_packets.get("status") != "machine_bounded_context_packets_not_human_review" or dry_packets.get("item_count") != 6:
            errors.append("Dry Bar context packets must remain bounded and cover six items")
    if TED_CANDIDATES_PATH.is_file() and TED_REVIEW_QUEUE_PATH.is_file() and TED_PACKETS_PATH.is_file():
        ted = load(TED_CANDIDATES_PATH); ted_queue = load(TED_REVIEW_QUEUE_PATH); ted_packets = load(TED_PACKETS_PATH)
        if ted.get("status") != "wave_2_candidate_evidence_not_promoted" or len(ted_queue.get("items", [])) != 6:
            errors.append("TED wave-2 candidates must remain provisional and cover six items")
        if ted_packets.get("status") != "machine_bounded_context_packets_not_human_review" or ted_packets.get("item_count") != 6:
            errors.append("TED context packets must remain bounded and cover six items")
    if WAVE_2_UNIFIED_CROSSWALK_PATH.is_file():
        unified = load(WAVE_2_UNIFIED_CROSSWALK_PATH)
        if unified.get("status") != "transcript_derived_mapping_not_independently_validated":
            errors.append("unified wave-2 crosswalk must remain provisional")
        if len(unified.get("rows", [])) != 19:
            errors.append("unified wave-2 crosswalk must contain 19 candidate rows")
        expected_sources = {"ali-siddiq-wave-2", "dry-bar-comedy-wave-2-starter", "ted-wave-2-starter"}
        if set(unified.get("source_scope", {})) != expected_sources:
            errors.append("unified wave-2 crosswalk source scope mismatch")
    if WAVE_2_KEYWORD_LEADS_PATH.is_file():
        leads = load(WAVE_2_KEYWORD_LEADS_PATH)
        if leads.get("status") != "keyword_retrieval_leads_not_semantic_validation" or len(leads.get("rows", [])) != 19:
            errors.append("wave-2 keyword leads must remain retrieval-only and cover 19 rows")
        if any(row.get("status") != "keyword_retrieval_lead_requires_contextual_review" for row in leads.get("rows", [])):
            errors.append("wave-2 keyword lead rows must remain contextual-review leads")
    for target in manifest.get("crosswalk_targets", []):
        for field in ("atlas", "shared_target", "required_evidence"):
            if not target.get(field):
                errors.append(f"crosswalk target missing {field}: {target}")

    if CROSSWALK_PATH.is_file() and CANONICAL_JOBS_PATH.is_file():
        crosswalk = load(CROSSWALK_PATH)
        canonical = load(CANONICAL_JOBS_PATH)
        valid_jobs = {lesson["canonical_job"] for lesson in canonical.get("lessons", [])}
        crosswalk_rows = crosswalk.get("rows", [])
        crosswalk_ids = {row.get("corpus_id") for row in crosswalk_rows}
        manifest_ids = {corpus.get("id") for corpus in corpora}
        if crosswalk_ids != manifest_ids:
            errors.append("source-to-job crosswalk does not cover exactly the manifest corpora")
        for row in crosswalk_rows:
            for job in row.get("jobs", []):
                if job not in valid_jobs:
                    errors.append(f"unknown canonical job in crosswalk: {job}")
    if APPROACH_CROSSWALK_PATH.is_file():
        approach_crosswalk = load(APPROACH_CROSSWALK_PATH)
        approach_rows = approach_crosswalk.get("rows", [])
        if approach_crosswalk.get("status") != "transcript_derived_mapping_not_independently_validated":
            errors.append("source-to-approach crosswalk must preserve its provisional status")
        if len(approach_rows) != len(corpora):
            errors.append("source-to-approach crosswalk does not cover all manifest corpora")
        if approach_crosswalk.get("approach_definition_count") != 27:
            errors.append("expected the current 27 named approaches in the source crosswalk")
        for row in approach_rows:
            if not row.get("approaches"):
                errors.append(f"source has no named approach references: {row.get('source')}")
            for approach in row.get("approaches", []):
                if not approach.get("name") or not approach.get("evidence_refs"):
                    errors.append(f"incomplete named approach mapping: {row.get('source')} / {approach}")
    if PATTERN_LEADS_PATH.is_file():
        leads = load(PATTERN_LEADS_PATH)
        if leads.get("status") != "keyword_retrieval_leads_not_semantic_validation":
            errors.append("pattern lead map must preserve its retrieval-only status")
        if leads.get("pattern_count") != 55 or leads.get("corpus_count") != len(corpora):
            errors.append("pattern lead map must cover 55 patterns and all manifest corpora")
        if leads.get("patterns_with_any_lead") != 46 or len(leads.get("patterns_without_any_lead", [])) != 9:
            errors.append("pattern lead map must reconcile 46 covered and 9 globally uncovered patterns")
        for row in leads.get("rows", []):
            for lead in row.get("leads", []):
                if lead.get("status") != "keyword_lead_requires_contextual_review":
                    errors.append(f"pattern lead lacks contextual-review status: {row.get('source')} / {lead.get('pattern_id')}")
    if CONTEXT_QUEUE_PATH.is_file():
        queue = load(CONTEXT_QUEUE_PATH)
        if queue.get("status") != "unreviewed_contextual_review_queue":
            errors.append("context queue must remain explicitly unreviewed")
        if queue.get("pattern_count_with_leads") != 46:
            errors.append("context queue should cover the current 46 patterns with retrieval leads")
        if any(item.get("review_status") != "unreviewed" for item in queue.get("items", [])):
            errors.append("context queue contains a promoted or completed review status")
        for item in queue.get("items", []):
            if not item.get("source_files") or not item.get("review_instruction"):
                errors.append(f"context queue item lacks provenance/instruction: {item.get('review_item_id')}")
    if PATTERN_REVIEW_BROWSER_PATH.is_file():
        browser = PATTERN_REVIEW_BROWSER_PATH.read_text(encoding="utf-8")
        if browser.count('class="review-card"') != 107:
            errors.append("pattern review browser does not expose all 107 release and wave-2 queue items")
        for required in ("Pattern Context Review Queue", "does not establish recurrence", "id=\"search\"", "Export completed review items", "unreviewed_item_ids", "localStorage", "independence_confirmed"):
            if required not in browser:
                errors.append(f"pattern review browser missing boundary or control: {required}")
        wave_2_reviews = (
            (WAVE_2_REVIEW_QUEUE_PATH, WAVE_2_PACKETS_PATH),
            (DRY_BAR_REVIEW_QUEUE_PATH, DRY_BAR_PACKETS_PATH),
            (TED_REVIEW_QUEUE_PATH, TED_PACKETS_PATH),
        )
        expected_review_ids = set()
        total_references = 0
        total_excerpts = 0
        for queue_path, packet_path in wave_2_reviews:
            if not queue_path.is_file() or not packet_path.is_file():
                continue
            queue = load(queue_path)
            packets = load(packet_path)
            packets_by_id = {packet["item_id"]: packet for packet in packets.get("packets", [])}
            for item in queue.get("items", []):
                item_id = item["item_id"]
                expected_review_ids.add(item_id)
                packet = packets_by_id.get(item_id)
                if packet is None:
                    errors.append(f"wave-2 context packet missing for {item_id}")
                    continue
                marker = f'<article class="review-card" data-search="{item_id} '
                start = browser.find(marker)
                end = browser.find("</article>", start) if start >= 0 else -1
                if start < 0 or end < 0:
                    errors.append(f"wave-2 review card missing from browser: {item_id}")
                    continue
                article = browser[start:end]
                references = packet.get("references", [])
                if not references:
                    errors.append(f"wave-2 context packet has no references: {item_id}")
                total_references += len(references)
                for reference in references:
                    clean_transcript = "../" + quote(reference["clean_transcript"], safe="/")
                    cue_file = "../" + quote(reference["cue_file"], safe="/")
                    for required in (reference["url"], html.escape(clean_transcript, quote=True), html.escape(cue_file, quote=True)):
                        if required not in article:
                            errors.append(f"wave-2 card {item_id} lacks its source/transcript/cue link")
                    for excerpt in reference.get("bounded_retrieval_excerpts", []):
                        total_excerpts += 1
                        if html.escape(excerpt.get("text", "")) not in article:
                            errors.append(f"wave-2 card {item_id} lacks a retrieved context excerpt")
        if WAVE_2_UNIFIED_CROSSWALK_PATH.is_file():
            crosswalk_ids = {row.get("review_item_id") for row in load(WAVE_2_UNIFIED_CROSSWALK_PATH).get("rows", [])}
            if expected_review_ids != crosswalk_ids:
                errors.append("wave-2 review browser queues do not reconcile to the 19-row crosswalk")
        if browser.count('class="context-reference"') != total_references:
            errors.append("wave-2 browser source reference count does not match its context packets")
        if browser.count("<blockquote>") != total_excerpts:
            errors.append("wave-2 browser excerpt count does not match its context packets")
    if not WAVE_2_REVIEW_BROWSER_PATH.is_file():
        errors.append("focused 19-item wave-2 review browser is missing")
    else:
        focused = WAVE_2_REVIEW_BROWSER_PATH.read_text(encoding="utf-8")
        focused_ids = {
            match.split(" ", 1)[0]
            for match in re.findall(r'<article class="review-card" data-search="([^"]+)"', focused)
        }
        expected_ids = {
            row.get("review_item_id")
            for row in load(WAVE_2_UNIFIED_CROSSWALK_PATH).get("rows", [])
        } if WAVE_2_UNIFIED_CROSSWALK_PATH.is_file() else set()
        queue_ids_match = re.search(r'<script id="all-queue-ids" type="application/json">(.*?)</script>', focused, re.DOTALL)
        queue_ids = set(json.loads(queue_ids_match.group(1))) if queue_ids_match else set()
        if len(focused_ids) != 19 or focused_ids != expected_ids:
            errors.append("focused wave-2 browser must show exactly the 19 crosswalk target IDs")
        if len(queue_ids) != 107 or not expected_ids.issubset(queue_ids):
            errors.append("focused wave-2 browser must preserve all 107 combined queue IDs for missingness")
        if "other 88 combined-queue items are not displayed" not in focused:
            errors.append("focused wave-2 browser must state that the other 88 items remain unreviewed")
    if not WAVE_2_REVIEW_PACK_PATH.is_file():
        errors.append("portable wave-2 full-context reviewer pack is missing")
    else:
        try:
            with zipfile.ZipFile(WAVE_2_REVIEW_PACK_PATH) as archive:
                members = set(archive.namelist())
                required_members = {"README-reviewer.md", "SHA256SUMS", "site/pattern-review-wave-2.html", "site/styles.css", "analysis/wave-2-context-review-request.md"}
                if not required_members.issubset(members):
                    errors.append("wave-2 reviewer pack is missing required review files")
                if "site/pattern-review-wave-2.html" in members and archive.read("site/pattern-review-wave-2.html") != WAVE_2_REVIEW_BROWSER_PATH.read_bytes():
                    errors.append("wave-2 reviewer pack browser does not match the checked local page")
                for line in archive.read("SHA256SUMS").decode().splitlines():
                    digest, name = line.split("  ", 1)
                    if name not in members or hashlib.sha256(archive.read(name)).hexdigest() != digest:
                        errors.append(f"wave-2 reviewer pack checksum mismatch: {name}")
        except (OSError, zipfile.BadZipFile, ValueError) as exc:
            errors.append(f"wave-2 reviewer pack cannot be verified: {exc}")
    if REVIEW_SCHEMA_PATH.is_file():
        schema = load(REVIEW_SCHEMA_PATH)
        if schema.get("title") != "Source Pattern Context Review Export":
            errors.append("source-pattern review schema title mismatch")
    if REVIEW_SMOKE_PATH.is_file():
        smoke = load(REVIEW_SMOKE_PATH)
        if smoke.get("status") != "source_pattern_review_browser_smoke_passed":
            errors.append("source-pattern browser smoke is not passing")
        if smoke.get("queue_item_count") != 107:
            errors.append("source-pattern browser smoke queue count mismatch")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if not args.quiet:
        print("unified integration validation passed: 10 corpora, 10 source-job rows, 4 slices, 5 evidence layers, 4 crosswalk targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
