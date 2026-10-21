#!/usr/bin/env python3
"""Build bounded provenance packets for the TED starter review queue."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "analysis/ted-wave-2-starter-context-review-queue.json"
INDEX = ROOT / "raw-material/youtube/transcripts/ted-wave-2-starter/transcript-index.json"
OUTPUT = ROOT / "analysis/ted-wave-2-starter-context-packets.json"
TERMS = {
    "concrete_opening_before_abstraction": ["when", "one day", "years ago", "today", "story"],
    "question_to_thesis_orientation": ["what if", "why", "how", "question", "idea"],
    "analogy_or_explanation_bridge": ["like", "imagine", "think of", "means", "example"],
    "contrast_before_after_reframe": ["but", "instead", "however", "before", "after"],
    "story_to_principle_transition": ["so", "because", "lesson", "learned", "therefore"],
    "audience_orientation_and_close": ["you", "we", "together", "remember", "thank you"],
}

def excerpts(text: str, terms: list[str]) -> list[dict[str, str]]:
    words = text.split(); lower = text.lower(); out = []
    for term in terms:
        match = re.search(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)", lower)
        if not match: continue
        pos = len(text[:match.start()].split())
        out.append({"matched_term": term, "text": " ".join(words[max(0, pos - 35): min(len(words), pos + 65)])})
        if len(out) == 2: break
    return out

def main() -> int:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    records = {str(item["index"]): item for item in json.loads(INDEX.read_text(encoding="utf-8"))}
    packets = []
    for item in queue["items"]:
        refs = []
        for ref in item["transcript_refs"]:
            record = records.get(ref.removeprefix("#"))
            if not record:
                refs.append({"ref": ref, "status": "missing_index_record"}); continue
            if record.get("transcript_status") != "available":
                refs.append({"ref": ref, "status": "transcript_unavailable", "video_id": record["id"]}); continue
            text = (ROOT / record["clean_txt"]).read_text(encoding="utf-8", errors="ignore")
            refs.append({"ref": ref, "status": "available", "video_id": record["id"], "title": record["title"], "url": record["url"], "word_count": record["word_count"], "clean_transcript": record["clean_txt"], "cue_file": record["cue_json"], "bounded_retrieval_excerpts": excerpts(text, TERMS[item["candidate_pattern"]])})
        packets.append({"item_id": item["item_id"], "candidate_pattern": item["candidate_pattern"], "review_prompt": item["review_prompt"], "references": refs, "review_status": "unreviewed", "claim_boundary": "Excerpts are retrieval aids. Full linked transcript context and, where relevant, audio/video review are required; no transfer or effectiveness claim is established."})
    OUTPUT.write_text(json.dumps({"schema_version": "1.0", "packet_id": "ted-wave-2-starter-context-packets", "source": "ted-wave-2-starter", "status": "machine_bounded_context_packets_not_human_review", "item_count": len(packets), "packets": packets}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(packets)} packets)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
