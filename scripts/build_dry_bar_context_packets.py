#!/usr/bin/env python3
"""Build bounded provenance packets for the Dry Bar starter review queue."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "analysis/dry-bar-comedy-wave-2-starter-context-review-queue.json"
INDEX = ROOT / "raw-material/youtube/transcripts/dry-bar-comedy-wave-2-starter/transcript-index.json"
OUTPUT = ROOT / "analysis/dry-bar-comedy-wave-2-starter-context-packets.json"
TERMS = {
    "concrete_friction_before_generalization": ["school", "house", "job", "wife", "son", "parent"],
    "premise_promise_turn_payoff": ["why", "but", "then", "because", "problem"],
    "contrast_and_frame_replacement": ["but", "instead", "rather", "different", "than"],
    "character_specificity_and_point_of_view": ["he", "she", "my wife", "my son", "dad", "mom"],
    "room_awareness_and_recovery": ["you", "audience", "room", "laugh", "wait", "hold on"],
    "self_inclusion_as_safety_boundary": ["I", "my", "we", "our", "mistake", "wrong"],
}


def excerpts(text: str, terms: list[str]) -> list[dict[str, str]]:
    words = text.split()
    lower = text.lower()
    out = []
    for term in terms:
        match = re.search(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)", lower)
        if not match:
            continue
        pos = len(text[:match.start()].split())
        out.append({"matched_term": term, "text": " ".join(words[max(0, pos - 35): min(len(words), pos + 65)])})
        if len(out) == 2:
            break
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
                refs.append({"ref": ref, "status": "missing_index_record"})
                continue
            if record.get("transcript_status") != "available":
                refs.append({"ref": ref, "status": "transcript_unavailable", "video_id": record["id"]})
                continue
            text = (ROOT / record["clean_txt"]).read_text(encoding="utf-8", errors="ignore")
            refs.append({"ref": ref, "status": "available", "video_id": record["id"], "title": record["title"], "url": record["url"], "word_count": record["word_count"], "clean_transcript": record["clean_txt"], "cue_file": record["cue_json"], "bounded_retrieval_excerpts": excerpts(text, TERMS[item["candidate_pattern"]])})
        packets.append({"item_id": item["item_id"], "candidate_pattern": item["candidate_pattern"], "review_prompt": item["review_prompt"], "references": refs, "review_status": "unreviewed", "claim_boundary": "Excerpts are retrieval aids. Full linked transcript context and, where relevant, audio/video review are required; no transfer or effectiveness claim is established."})
    OUTPUT.write_text(json.dumps({"schema_version": "1.0", "packet_id": "dry-bar-comedy-wave-2-starter-context-packets", "source": "dry-bar-comedy-wave-2-starter", "status": "machine_bounded_context_packets_not_human_review", "item_count": len(packets), "packets": packets}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(packets)} packets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
