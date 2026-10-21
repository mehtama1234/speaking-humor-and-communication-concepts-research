#!/usr/bin/env python3
"""Count bounded lexical retrieval leads for all unified wave-2 candidates."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "analysis/wave-2-unified-candidate-crosswalk.json"
OUTPUT = ROOT / "analysis/wave-2-keyword-leads.json"
INDEXES = {
    "ali-siddiq-wave-2": ROOT / "raw-material/youtube/transcripts/ali-siddiq-wave-2/transcript-index.json",
    "dry-bar-comedy-wave-2-starter": ROOT / "raw-material/youtube/transcripts/dry-bar-comedy-wave-2-starter/transcript-index.json",
    "ted-wave-2-starter": ROOT / "raw-material/youtube/transcripts/ted-wave-2-starter/transcript-index.json",
}
TERMS = {
    "consequence_first_orientation": ["when", "because", "then", "problem", "choice"],
    "scene_detail_as_compression": ["school", "house", "son", "wife", "dad", "mom"],
    "escalation_by_changed_conditions": ["then", "after", "next", "but", "problem"],
    "character_contrast_and_point_of_view": ["he", "she", "men", "women", "wife", "son"],
    "public_repair_as_relationship_maintenance": ["wait", "hold on", "let me", "I mean", "you know"],
    "repetition_callback_and_transformed_meaning": ["again", "remember", "every time", "same"],
    "difficulty_made_discussable_through_humor": ["funny", "laugh", "joke", "crazy", "marriage"],
    "concrete_friction_before_generalization": ["school", "house", "job", "wife", "son", "parent"],
    "premise_promise_turn_payoff": ["why", "but", "then", "because", "problem"],
    "contrast_and_frame_replacement": ["but", "instead", "rather", "different", "than"],
    "character_specificity_and_point_of_view": ["he", "she", "my wife", "my son", "dad", "mom"],
    "room_awareness_and_recovery": ["you", "audience", "room", "laugh", "wait", "hold on"],
    "self_inclusion_as_safety_boundary": ["I", "my", "we", "our", "mistake", "wrong"],
    "concrete_opening_before_abstraction": ["when", "one day", "years ago", "today", "story"],
    "question_to_thesis_orientation": ["what if", "why", "how", "question", "idea"],
    "analogy_or_explanation_bridge": ["like", "imagine", "think of", "means", "example"],
    "contrast_before_after_reframe": ["but", "instead", "however", "before", "after"],
    "story_to_principle_transition": ["so", "because", "lesson", "learned", "therefore"],
    "audience_orientation_and_close": ["you", "we", "together", "remember", "thank you"],
}

def count_terms(text: str, terms: list[str]) -> tuple[int, int]:
    lower = text.lower()
    occurrences = 0
    matched = 0
    for term in terms:
        count = len(re.findall(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)", lower))
        occurrences += count
        matched += bool(count)
    return occurrences, int(occurrences > 0)

def main() -> int:
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    patterns = [(row["source"], row["candidate_pattern"], row["review_item_id"]) for row in crosswalk["rows"]]
    rows = []
    for source, pattern, review_item_id in patterns:
        index = json.loads(INDEXES[source].read_text(encoding="utf-8"))
        total_words = 0; available = 0; occurrences = 0; hit_videos = 0; refs = []
        for record in index:
            if record.get("transcript_status") != "available": continue
            text = (ROOT / record["clean_txt"]).read_text(encoding="utf-8", errors="ignore")
            count, hit = count_terms(text, TERMS[pattern])
            available += 1; total_words += int(record.get("word_count", 0)); occurrences += count; hit_videos += hit
            if hit and len(refs) < 8: refs.append({"ref": f"#{record['index']}", "video_id": record["id"], "title": record["title"], "occurrences": count})
        rows.append({"source": source, "candidate_pattern": pattern, "review_item_id": review_item_id, "transcripts_available": available, "total_words": total_words, "keyword_occurrences": occurrences, "transcripts_with_keyword_hits": hit_videos, "bounded_example_refs": refs, "status": "keyword_retrieval_lead_requires_contextual_review"})
    OUTPUT.write_text(json.dumps({"schema_version": "1.0", "status": "keyword_retrieval_leads_not_semantic_validation", "claim_boundary": "Counts locate candidate contexts and do not establish semantic fit, recurrence, delivery meaning, transfer, or effectiveness.", "rows": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(rows)} rows)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
