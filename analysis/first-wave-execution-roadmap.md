# First-Wave Execution Roadmap

Operational sequence for turning the first three speaking source slices into
transcript-backed research assets.

Date: August 10, 2026.

If the operational goal is not only corpus capture but usable move extraction,
pair this roadmap with `analysis/transcript-backed-concrete-speaking-approaches.md`
so each wave is judged partly by which exact approaches it strengthens.

## Objective of this wave

Build the first real working corpus in this repo, starting with
`Ultraspeaking`, then extending the same workflow to `Vinh Giang` and
`Think Fast Talk Smart`.

This wave is successful when each starter corpus has:

- transcript capture completed or attempted across the curated slice
- a corpus summary
- a transcript index
- a session inventory
- a clear list of missing transcripts, if any
- enough material to begin session briefs and theme extraction
- enough material to map high-value sessions into exact transcript-backed
  approaches

## Corpus order

1. `ultraspeaking-wave-1`
2. `vinh-giang-wave-1`
3. `think-fast-talk-smart-wave-1`

## Why this order

`Ultraspeaking` is the best first full slice because it is compact, highly
aligned with spontaneous speaking and audience connection, and likely to give
the fastest payoff in theme extraction.

`Vinh Giang` then adds stronger material on articulation, presence, and
high-energy delivery.

`Think Fast Talk Smart` adds a more structured, academic, and
workplace-oriented communication layer that should balance the first two.

Wave-level exact-approach priorities:

- `ultraspeaking-wave-1`:
  `Approach 1`, `Approach 3`, `Approach 10`, `Approach 15`
- `vinh-giang-wave-1`:
  `Approach 2`, `Approach 7`, `Approach 21`
- `think-fast-talk-smart-wave-1`:
  `Approach 5`, `Approach 14`, `Approach 19`

## Runbook

### Step 1: Capture transcripts for the first slice

```bash
python3 scripts/download_youtube_playlist_transcripts.py \
  --course-root . \
  --manifest raw-material/youtube/starter-manifests/ultraspeaking-wave-1.json
```

Expected outputs:

- `raw-material/youtube/playlists/ultraspeaking-wave-1.json`
- `raw-material/youtube/transcripts/ultraspeaking-wave-1/course-manifest.json`
- `raw-material/youtube/transcripts/ultraspeaking-wave-1/summary.json`
- `raw-material/youtube/transcripts/ultraspeaking-wave-1/transcript-index.json`
- `raw-material/youtube/transcripts/ultraspeaking-wave-1/raw-vtt/`
- `raw-material/youtube/transcripts/ultraspeaking-wave-1/clean/`
- `raw-material/youtube/transcripts/ultraspeaking-wave-1/cues/`

### Step 2: Build the session inventory

```bash
python3 scripts/build_course_session_inventory.py \
  --course-root . \
  --manifest raw-material/youtube/starter-manifests/ultraspeaking-wave-1.json \
  --output analysis/ultraspeaking-wave-1-session-inventory.md
```

### Step 3: Inspect gaps

Check:

- how many transcripts were actually captured
- which videos are missing transcripts
- which sessions are dense enough for early concept extraction

Primary evidence files:

- `raw-material/youtube/transcripts/ultraspeaking-wave-1/summary.json`
- `raw-material/youtube/transcripts/ultraspeaking-wave-1/transcript-index.json`

### Step 4: Write first-pass synthesis

Using the session inventory and transcripts, produce:

- session briefs
- early theme groupings
- subtheme candidates
- drill candidates
- strongest example candidates
- strongest exact-approach candidates for
  `analysis/transcript-backed-concrete-speaking-approaches.md`

### Step 5: Repeat for the next two starter corpora

Repeat the same two script calls with:

- `raw-material/youtube/starter-manifests/vinh-giang-wave-1.json`
- `raw-material/youtube/starter-manifests/think-fast-talk-smart-wave-1.json`

## Acceptance checks

For each corpus, verify:

- the manifest slug has a matching transcript folder
- `summary.json` exists
- `transcript-index.json` exists
- the session inventory markdown exists
- transcript availability counts are visible
- missing items are identifiable by title and video id

## Immediate deliverables after transcript capture

Once `ultraspeaking-wave-1` is captured, the next analysis files to create are:

- `analysis/ultraspeaking-wave-1-session-briefs.md`
- `analysis/ultraspeaking-wave-1-theme-map.md`
- `analysis/ultraspeaking-wave-1-drill-candidates.md`
- `analysis/example-library.md`
- `analysis/featured-sessions.md`
- updates or additions to
  `analysis/transcript-backed-concrete-speaking-approaches.md`

## Notes on quality

This wave should favor useful coverage over fake completeness.

If a transcript is unavailable:

- keep the session in the corpus
- mark it clearly as missing
- do not invent content
- use title-level placement until transcript-backed review is possible
