#!/usr/bin/env python3
"""Build a local, non-promotional browser for the source-pattern review queue."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "analysis" / "source-pattern-context-review-queue.json"
WAVE_2_QUEUE = ROOT / "analysis" / "ali-siddiq-wave-2-context-review-queue.json"
DRY_BAR_QUEUE = ROOT / "analysis" / "dry-bar-comedy-wave-2-starter-context-review-queue.json"
TED_QUEUE = ROOT / "analysis" / "ted-wave-2-starter-context-review-queue.json"
OUTPUT = ROOT / "site" / "pattern-review.html"


def render_context_references(item: dict) -> str:
    rendered = []
    for reference in item.get("context_references", []):
        excerpts = "".join(
            "<blockquote><p><strong>Retrieved context — term: "
            + html.escape(excerpt.get("matched_term", "unspecified"))
            + "</strong></p><p>"
            + html.escape(excerpt.get("text", ""))
            + "</p></blockquote>"
            for excerpt in reference.get("bounded_retrieval_excerpts", [])
        )
        rendered.append(
            f"""<section class="context-reference">
              <h3>{html.escape(reference.get('ref', 'Transcript reference'))}: {html.escape(reference.get('title') or reference['video_id'])}</h3>
              <p>{reference.get('word_count', 'unknown')} transcript words ·
                <a href="{html.escape(reference['url'], quote=True)}" target="_blank" rel="noreferrer">Open source video</a> ·
                <a href="{html.escape(reference['transcript_url'], quote=True)}">Open full local transcript</a> ·
                <a href="{html.escape(reference['cue_url'], quote=True)}">Open cue/timing data</a>
              </p>
              <details><summary>Retrieved context excerpts</summary>{excerpts}</details>
            </section>"""
        )
    if not rendered:
        return ""
    return "<details class=\"full-context\"><summary>Source and transcript context</summary>" + "".join(rendered) + "</details>"


def card(item: dict) -> str:
    refs = "".join(
        f"<li><code>{html.escape(ref['file'])}</code>{' (matched: ' + html.escape(', '.join(ref['matched_terms'])) + ')' if ref.get('matched_terms') else ''}</li>"
        for source_file in item.get("source_files", [])
        for ref in [source_file]
    )
    searchable = html.escape(
        " ".join(
            [
                item.get("review_item_id", ""),
                item.get("source", ""),
                item.get("pattern_id", ""),
                item.get("candidate_form", ""),
                " ".join(item.get("matched_terms", [])),
                " ".join(
                    excerpt.get("text", "")
                    for reference in item.get("context_references", [])
                    for excerpt in reference.get("bounded_retrieval_excerpts", [])
                ),
            ]
        ),
        quote=True,
    )
    matched_terms = (
        f"<p><strong>Matched terms:</strong> {html.escape(', '.join(item['matched_terms']))}</p>"
        if item.get("matched_terms") else ""
    )
    return f"""
      <article class=\"review-card\" data-search=\"{searchable}\">
        <div class=\"card-topline\"><span class=\"status\">{html.escape(item['review_status'])}</span><code>{html.escape(item['review_item_id'])}</code></div>
        <p class=\"eyebrow\">{html.escape(item['source'])} · {html.escape(item['category'])}</p>
        <h2>{html.escape(item['pattern_id'])}</h2>
        <p><strong>Candidate form:</strong> {html.escape(item['candidate_form'])}</p>
        {matched_terms}
        {render_context_references(item)}
        <details><summary>Analysis-note provenance</summary><ul>{refs}</ul></details>
        <p class=\"instruction\">{html.escape(item['review_instruction'])}</p>
        <div class=\"review-controls\">
          <label>Decision <select class=\"review-decision\" data-item=\"{html.escape(item['review_item_id'])}\"><option value=\"\">Choose…</option><option value=\"supports_candidate\">Supports candidate</option><option value=\"does_not_support\">Does not support</option><option value=\"indeterminate\">Indeterminate</option></select></label>
          <label><input type=\"checkbox\" class=\"context-inspected\" data-item=\"{html.escape(item['review_item_id'])}\"> I inspected the underlying transcript/context</label>
          <label class=\"note-label\">Reviewer note <textarea class=\"review-note\" data-item=\"{html.escape(item['review_item_id'])}\" rows=\"2\" placeholder=\"Record context, mismatch, or uncertainty…\"></textarea></label>
        </div>
      </article>
    """


def load_review_items() -> tuple[list[dict], int]:
    """Normalize release and wave-2 queues into one review surface."""
    base = json.loads(QUEUE.read_text(encoding="utf-8"))
    items = list(base["items"])
    pattern_ids = {item.get("pattern_id") for item in items}
    for queue_path, source_label, packet_path in (
        (WAVE_2_QUEUE, "Ali Siddiq (wave 2)", ROOT / "analysis" / "ali-siddiq-wave-2-context-packets.json"),
        (DRY_BAR_QUEUE, "Dry Bar Comedy (wave 2 starter)", ROOT / "analysis" / "dry-bar-comedy-wave-2-starter-context-packets.json"),
        (TED_QUEUE, "TED (wave 2 starter)", ROOT / "analysis" / "ted-wave-2-starter-context-packets.json"),
    ):
        if queue_path.is_file():
            wave = json.loads(queue_path.read_text(encoding="utf-8"))
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            packet_by_id = {packet_item["item_id"]: packet_item for packet_item in packet.get("packets", [])}
            for item in wave.get("items", []):
                refs = item.get("transcript_refs", [])
                context_packet = packet_by_id.get(item["item_id"])
                if context_packet is None:
                    raise ValueError(f"missing context packet for review item {item['item_id']}")
                context_references = []
                for reference in context_packet.get("references", []):
                    transcript_path = (ROOT / reference["clean_transcript"]).resolve()
                    cue_path = (ROOT / reference["cue_file"]).resolve()
                    if ROOT not in transcript_path.parents or not transcript_path.is_file():
                        raise ValueError(f"missing or unsafe full transcript for {item['item_id']}: {reference.get('clean_transcript')}")
                    if ROOT not in cue_path.parents or not cue_path.is_file():
                        raise ValueError(f"missing or unsafe cue file for {item['item_id']}: {reference.get('cue_file')}")
                    context_references.append({
                        **reference,
                        "transcript_url": "../" + quote(reference["clean_transcript"], safe="/"),
                        "cue_url": "../" + quote(reference["cue_file"], safe="/"),
                    })
                if not context_references:
                    raise ValueError(f"review item {item['item_id']} has no source references")
                normalized = {
                    "review_item_id": item["item_id"],
                    "review_status": item.get("decision", "unreviewed"),
                    "source": source_label,
                    "category": "humor-storytelling",
                    "pattern_id": item["candidate_pattern"],
                    "candidate_form": item.get("review_prompt", ""),
                    "matched_terms": [],
                    "source_files": [
                        {"file": packet_path.relative_to(ROOT).as_posix() + "#" + item["item_id"], "matched_terms": []},
                        {"file": "transcript refs: " + ", ".join(refs), "matched_terms": []},
                    ],
                    "review_instruction": (
                        item.get("review_prompt", "")
                        + " Inspect the linked full transcript and source video, not the retrieved excerpts alone; "
                        + "record counterexamples, identity problems, or uncertainty in the reviewer note."
                    ),
                    "context_references": context_references,
                }
                items.append(normalized)
                pattern_ids.add(normalized["pattern_id"])
    return items, len(pattern_ids)


def load_wave_2_ids() -> set[str]:
    return {
        item["item_id"]
        for queue_path in (WAVE_2_QUEUE, DRY_BAR_QUEUE, TED_QUEUE)
        if queue_path.is_file()
        for item in json.loads(queue_path.read_text(encoding="utf-8")).get("items", [])
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--wave-2-only", action="store_true", help="render only the 19 wave-2 targets while retaining the combined queue denominator")
    args = parser.parse_args()
    all_items, _ = load_review_items()
    all_queue_ids = [item["review_item_id"] for item in all_items]
    wave_2_ids = load_wave_2_ids()
    items = [item for item in all_items if item["review_item_id"] in wave_2_ids] if args.wave_2_only else all_items
    if args.wave_2_only and len(items) != 19:
        raise ValueError(f"expected 19 wave-2 cards, got {len(items)}")
    pattern_count = len({item["pattern_id"] for item in items})
    cards = "\n".join(card(item) for item in items)
    all_ids_json = json.dumps(all_queue_ids).replace("<", "\\u003c")
    page_title = "Wave-2 Full-Context Review" if args.wave_2_only else "Pattern Context Review Queue"
    hero_text = (
        "This focused page shows the 19 wave-2 targets only: 7 Ali Siddiq, 6 Dry Bar Comedy, and 6 TED candidates. "
        "The other 88 combined-queue items are not displayed and remain explicitly unreviewed in any partial export. "
        "Each target includes retrieved passages, video links, and local full-transcript/cue links. Inspect full context; "
        "candidates are not independently validated."
        if args.wave_2_only
        else f"{len(items)} items across {pattern_count} presentation-pattern candidates, including the Ali Siddiq, Dry Bar, and TED wave-2 queues. Wave-2 cards include retrieved passages, source-video links, and local full-transcript/cue links. Inspect the full context before making any judgment; transcripts and candidate patterns are not independently validated."
    )
    reviewer_instruction = (
        "Review the 19 displayed wave-2 targets. The other 88 combined-queue IDs are intentionally not shown and will remain unreviewed. "
        "Every exported decision requires context-inspection confirmation."
        if args.wave_2_only
        else "For the 19 wave-2 candidates, search for ‘wave 2’ and export only completed items. Omitted items are explicitly retained as unreviewed; each exported item must have a decision and context-inspection confirmation."
    )
    navigation = "" if args.wave_2_only else '<nav class="topnav"><a class="brand" href="./index.html">Speaking Research Atlas</a><div class="navlinks"><a href="./integration.html">Integration</a><a href="./corpora.html">Corpora</a><a href="./evidence.html">Evidence</a></div></nav>'
    page = f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>{page_title} | Speaking Research Atlas</title>
<link rel=\"stylesheet\" href=\"./styles.css\">
<style>
  .review-toolbar {{ display:flex; gap:1rem; flex-wrap:wrap; margin:2rem 0; }}
  .review-toolbar input {{ flex:1 1 22rem; padding:.8rem 1rem; border:1px solid #c7c0b5; border-radius:.4rem; font:inherit; }}
  .review-card {{ background:#fff; border:1px solid #ded7ca; border-radius:.75rem; padding:1.25rem; margin:1rem 0; box-shadow:0 4px 14px rgba(37,31,24,.05); }}
  .context-reference {{ border-top:1px solid #e5dfd4; margin:.8rem 0; padding:.5rem 0; }}
  .full-context {{ background:#f7f3ec; padding:.8rem; border-radius:.4rem; margin:1rem 0; }}
  blockquote {{ margin:.5rem 0; padding:.2rem .9rem; border-left:3px solid #c59a62; background:#fff; }}
  .card-topline {{ display:flex; justify-content:space-between; gap:1rem; color:#665f55; font-size:.85rem; }}
  .status {{ background:#f4ead1; color:#765717; border-radius:999px; padding:.25rem .6rem; }}
  .review-card h2 {{ margin:.5rem 0; }}
  .instruction {{ border-left:3px solid #aa7132; padding-left:1rem; }}
  .review-controls {{ display:grid; gap:.7rem; border-top:1px solid #ded7ca; padding-top:1rem; margin-top:1rem; }}
  .review-controls label {{ display:flex; gap:.6rem; align-items:center; flex-wrap:wrap; }}
  .review-controls select, .review-controls textarea, .reviewer-bar input {{ font:inherit; padding:.45rem .6rem; border:1px solid #c7c0b5; border-radius:.35rem; }}
  .review-controls textarea {{ width:100%; box-sizing:border-box; }}
  .note-label {{ display:block !important; }}
  .reviewer-bar {{ display:grid; gap:.7rem; background:#f7f3ec; padding:1rem; border-radius:.6rem; margin-bottom:1rem; }}
  .reviewer-bar-actions {{ display:flex; gap:.7rem; flex-wrap:wrap; }}
  .reviewer-bar button {{ cursor:pointer; padding:.55rem .8rem; border:1px solid #7a4b21; border-radius:.35rem; background:#7a4b21; color:#fff; font:inherit; }}
  .reviewer-bar button.secondary {{ background:#fff; color:#7a4b21; }}
  #export-status {{ min-height:1.4em; }}
  .empty {{ display:none; padding:2rem 0; }}
</style></head>
<body><div class=\"page-shell\"><nav class=\"topnav\"><a class=\"brand\" href=\"./index.html\">Speaking Research Atlas</a><div class=\"navlinks\"><a href=\"./integration.html\">Integration</a><a href=\"./corpora.html\">Corpora</a><a href=\"./evidence.html\">Evidence</a></div></nav>
{navigation}<main><header class=\"hero\"><div class=\"hero-copy\"><p class=\"eyebrow\">Unreviewed Retrieval Leads</p><h1>{page_title}</h1><p class=\"hero-text\">{hero_text}</p></div><aside class=\"hero-panel\"><h2>Claim boundary</h2><p>This browser is a review aid. It contains no reviewer decisions and does not establish recurrence, delivery meaning, learner transfer, listener outcomes, or effectiveness.</p></aside></header>
<section class=\"section\"><div class=\"reviewer-bar\"><label>Reviewer code <input id=\"reviewer-code\" autocomplete=\"off\" placeholder=\"pseudonymous code\"></label><label><input id=\"independence\" type=\"checkbox\"> I did not assemble the transcript packets, propose these candidates, or create the crosswalk, and I have not seen another review</label><p>{reviewer_instruction}</p><div class=\"reviewer-bar-actions\"><button id=\"save\" type=\"button\">Save draft locally</button><button id=\"export\" class=\"secondary\" type=\"button\">Export completed review items</button></div><div id=\"export-status\" aria-live=\"polite\"></div></div><div class=\"review-toolbar\"><label for=\"search\">Search source, pattern, or term</label><input id=\"search\" type=\"search\" placeholder=\"e.g. wave 2, Charisma, repair, story...\"><span id=\"count\" aria-live=\"polite\"></span></div><p class=\"empty\" id=\"empty\">No queue item matches that search.</p><div id=\"queue\">{cards}</div></section></main></div>
<script id=\"all-queue-ids\" type=\"application/json\">{all_ids_json}</script>
<script>
const input=document.getElementById('search'), cards=[...document.querySelectorAll('.review-card')], count=document.getElementById('count'), empty=document.getElementById('empty'), storageKey='speaking-pattern-context-review-draft-v1', allQueueIds=JSON.parse(document.getElementById('all-queue-ids').textContent);
function filter() {{ const q=input.value.trim().toLowerCase(); let visible=0; cards.forEach(card=>{{const show=!q||card.dataset.search.toLowerCase().includes(q); card.hidden=!show; if(show) visible++;}}); count.textContent=`${{visible}} of ${{cards.length}} items`; empty.style.display=visible?'none':'block'; }}
input.addEventListener('input',filter); filter();
function collect() {{ const records=cards.map(card=>{{const id=card.querySelector('.review-decision').dataset.item; return {{review_item_id:id, decision:card.querySelector('.review-decision').value, context_inspected:card.querySelector('.context-inspected').checked, note:card.querySelector('.review-note').value}};}}); return {{schema_version:'1.0', queue_id:'source-pattern-context-review-queue', reviewer_code:document.getElementById('reviewer-code').value.trim(), independence_confirmed:document.getElementById('independence').checked, records, claim_boundary:'Review records describe contextual fit only; omissions remain unreviewed. The queue does not establish recurrence, delivery meaning, learner transfer, listener outcomes, or effectiveness.'}}; }}
function restore() {{ const raw=localStorage.getItem(storageKey); if(!raw) return; try {{ const data=JSON.parse(raw); document.getElementById('reviewer-code').value=data.reviewer_code||''; document.getElementById('independence').checked=!!data.independence_confirmed; (data.records||[]).forEach(record=>{{const card=cards.find(c=>c.querySelector('.review-decision').dataset.item===record.review_item_id); if(!card)return; card.querySelector('.review-decision').value=record.decision||''; card.querySelector('.context-inspected').checked=!!record.context_inspected; card.querySelector('.review-note').value=record.note||'';}}); }} catch(e) {{}} }}
function saveDraft() {{ localStorage.setItem(storageKey,JSON.stringify(collect())); document.getElementById('export-status').textContent='Draft saved in this browser only.'; }}
function exportReview() {{ const draft=collect(); if(!draft.reviewer_code||!draft.independence_confirmed) {{ document.getElementById('export-status').textContent='Enter a reviewer code and confirm independence before export.'; return; }} const started=draft.records.filter(r=>r.decision||r.context_inspected||r.note.trim()); if(!started.length) {{ document.getElementById('export-status').textContent='Complete at least one item and confirm its context before export.'; return; }} if(started.some(r=>!r.decision||!r.context_inspected)) {{ document.getElementById('export-status').textContent='Finish or clear each started item: every exported decision needs context inspection.'; return; }} const reviewed=new Set(started.map(r=>r.review_item_id)), data={{...draft, queue_item_count:allQueueIds.length, review_status:reviewed.size===allQueueIds.length?'complete':'partial', unreviewed_item_ids:allQueueIds.filter(id=>!reviewed.has(id)), records:started}}; const blob=new Blob([JSON.stringify(data,null,2)+'\\n'],{{type:'application/json'}}), url=URL.createObjectURL(blob), link=document.createElement('a'); link.href=url; link.download='source-pattern-context-review.json'; link.click(); URL.revokeObjectURL(url); document.getElementById('export-status').textContent=`Exported ${{started.length}} of ${{allQueueIds.length}} combined queue items. Omitted items are explicitly marked unreviewed; validate coverage before returning it.`; }}
document.getElementById('save').addEventListener('click',saveDraft); document.getElementById('export').addEventListener('click',exportReview); restore();
</script></body></html>"""
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    try:
        display_output = str(output.relative_to(ROOT))
    except ValueError:
        display_output = str(output)
    print(json.dumps({"output": display_output, "items": len(items), "combined_queue_items": len(all_items), "pattern_count": pattern_count, "wave_2_only": args.wave_2_only}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
