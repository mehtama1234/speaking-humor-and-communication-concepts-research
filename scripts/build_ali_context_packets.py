#!/usr/bin/env python3
"""Build bounded, provenance-preserving context packets for Ali wave-2 review."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "analysis/ali-siddiq-wave-2-context-review-queue.json"
INDEX = ROOT / "raw-material/youtube/transcripts/ali-siddiq-wave-2/transcript-index.json"
OUTPUT = ROOT / "analysis/ali-siddiq-wave-2-context-packets.json"

TERMS = {
    "consequence_first_orientation": ["when", "because", "then", "problem", "choice"],
    "scene_detail_as_compression": ["school", "house", "son", "wife", "dad", "mom"],
    "escalation_by_changed_conditions": ["then", "after", "next", "but", "problem"],
    "character_contrast_and_point_of_view": ["he", "she", "men", "women", "wife", "son"],
    "public_repair_as_relationship_maintenance": ["wait", "hold on", "let me", "I mean", "you know"],
    "repetition_callback_and_transformed_meaning": ["again", "remember", "every time", "same"],
    "difficulty_made_discussable_through_humor": ["funny", "laugh", "joke", "crazy", "marriage"],
}


def excerpt(text: str, terms: list[str]) -> list[dict[str, str]]:
    words = text.split()
    lower = text.lower()
    snippets: list[dict[str, str]] = []
    for term in terms:
        match = re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", lower)
        if not match:
            continue
        start = len(text[: match.start()].split())
        lo = max(0, start - 35)
        hi = min(len(words), start + 65)
        snippets.append({"matched_term": term, "text": " ".join(words[lo:hi])})
        if len(snippets) == 2:
            break
    return snippets


def main() -> int:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    records = {str(item["index"]): item for item in json.loads(INDEX.read_text(encoding="utf-8"))}
    packets = []
    for item in queue["items"]:
        references = []
        for ref in item["transcript_refs"]:
            index = ref.removeprefix("#")
            record = records.get(index)
            if not record:
                references.append({"ref": ref, "status": "missing_index_record"})
                continue
            if record.get("transcript_status") != "available":
                references.append({"ref": ref, "status": "transcript_unavailable", "video_id": record["id"]})
                continue
            text = (ROOT / record["clean_txt"]).read_text(encoding="utf-8", errors="ignore")
            references.append(
                {
                    "ref": ref,
                    "status": "available",
                    "video_id": record["id"],
                    "title": record["title"],
                    "url": record["url"],
                    "word_count": record["word_count"],
                    "clean_transcript": record["clean_txt"],
                    "cue_file": record["cue_json"],
                    "bounded_retrieval_excerpts": excerpt(text, TERMS[item["candidate_pattern"]]),
                }
            )
        packets.append(
            {
                "item_id": item["item_id"],
                "candidate_pattern": item["candidate_pattern"],
                "review_prompt": item["review_prompt"],
                "references": references,
                "review_status": "unreviewed",
                "claim_boundary": "Excerpts are retrieval aids. Reviewer decisions require reading the full linked transcript context and do not establish recurrence, transfer, or effectiveness.",
            }
        )
    output = {
        "schema_version": "1.0",
        "packet_id": "ali-siddiq-wave-2-context-packets",
        "source": "ali-siddiq-wave-2",
        "status": "machine_bounded_context_packets_not_human_review",
        "item_count": len(packets),
        "packets": packets,
    }
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(packets)} packets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
