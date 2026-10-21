# Unified Speaking Analysis Integration Plan

This document is the bridge between this channel-and-curriculum atlas and
`../best-speech-analysis`. The two projects should become one end-to-end
speaking improvement system, but their evidence layers must remain explicit.

## Product goal

For a real communication problem, a learner should be able to move through:

```text
source channel/video
  -> transcript and surrounding context
  -> source theme and named speaking move
  -> cross-corpus pattern or communication job
  -> delivery evidence and limitations
  -> counterexample and non-fit boundary
  -> adaptable practice drill
  -> presentation or real-room application
  -> learner revision and listener check
```

The output is a traceable learning path, not a popularity ranking and not a
claim that every captured video has been independently analyzed.

## What each repository contributes

### This repository

- curated YouTube source selection;
- ten transcript-backed starter corpora;
- source-specific session inventories, briefs, theme maps, and drill candidates;
- cross-source concepts, evidence moments, curriculum pages, and learner paths;
- proposed next sources for storytelling, humor, and polished-talk exemplars.

### `best-speech-analysis`

- fixed inventory and canonical full-context review boundary;
- communication-job curriculum and shared evidence model;
- 55 presentation-pattern candidates and their evidence layers;
- delivery/media availability and proxy boundaries;
- counterexample, blinded review, learner, and listener instruments;
- fail-closed validators and reproducible release audits.

The second repository's current release candidate is internally runnable, but
its findings are not all independently validated. The bridge must preserve
that distinction.

## Shared identity contract

Every joined record must retain these stable fields:

| Field | Meaning |
|---|---|
| `corpus_id` | Source corpus, for example `charisma-on-command-wave-1`. |
| `video_id` | Stable platform or locally assigned video identifier. |
| `source_name` | Human-readable channel or publisher. |
| `transcript_ref` | Exact transcript path, segment, or line range. |
| `timestamp` | Start/end location when available. |
| `job_id` | Communication problem or function being solved. |
| `pattern_id` | Candidate pattern or named move; nullable until mapped. |
| `claim_status` | `inventory`, `transcript_candidate`, `cross_corpus_candidate`, `reviewed`, or `outcome_tested`. |
| `evidence_layer` | Which kind of evidence supports the record. |
| `limitations` | Missingness, confounds, transcript quality, and non-fit notes. |

No downstream page may silently replace `transcript_candidate` with
`reviewed` or `outcome_tested`.

## Integration order

1. **Inventory join.** Reconcile the ten corpora with the source map and the
   fixed speech-analysis inventory without copying raw files or inventing
   equivalence between video counts.
2. **Theme-to-job crosswalk.** Map each source's themes to communication jobs
   and to the 55 presentation-pattern candidates where the mapping is real.
3. **Evidence join.** Attach exact transcript references, timestamps, context,
   source URLs, and claim status to every crosswalk row.
4. **Practice join.** Connect each usable move to its drill, self-check,
   non-fit test, presentation adaptation, and listener-check prompt.
5. **Vertical-slice audit.** Select one example from Charisma on Command, one
   from storytelling, and one from workplace speaking; trace each from source
   to final learner-facing output.
6. **Validation handoff.** Export only blinded review items and clearly marked
   candidate records to the validation machinery in `best-speech-analysis`.
7. **Expansion.** Ali Siddiq is now captured and indexed as a wave-2 source;
   review its seven candidate patterns through the combined browser queue, but
   keep it outside the validated ten-corpus release until contextual and
   transfer gates close. Add Dry Bar Comedy only after this review slice shows
   which evidence fields and review burdens are real.

## First vertical slice

The first integration slice should cover the job **recover connection after an
awkward or difficult moment**:

- Charisma on Command: social recovery and visible appreciation;
- Chad Littlefield: conversation design and question quality;
- Jefferson Fisher: calm authority and direct boundary language;
- best-speech analysis: repair, qualification, rapport, and difficult-answer
  pattern candidates;
- final output: one evidence-bounded lesson with examples, a practice drill,
  a non-fit warning, and a listener restatement check.

This slice is complete only when every link is traceable and the lesson keeps
its provisional status where independent evidence is absent.

## Definition of done for the unified system

- All current source corpora have stable IDs and source-status records.
- Every promoted concept links back to exact source evidence.
- Cross-corpus recurrence includes denominators and preserves uncertainty.
- Presentation patterns, communication jobs, themes, and drills use a shared
  vocabulary or an explicit mapping.
- Candidate, reviewed, learner-tested, and listener-tested claims are visibly
  different in data and UI.
- A learner can start from a real problem and reach practice plus revision.
- A presentation maker can start from a theme and reach examples, structure,
  delivery notes, and non-fit boundaries.
- Reproducibility checks pass without being presented as effectiveness proof.

The authoritative machine-readable inventory for this bridge is
`analysis/unified-integration-manifest.json`.

The first implemented slice is documented in
`analysis/vertical-slice-01-awkwardness-repair.md`.

The next three implemented candidate slices are documented in
`analysis/vertical-slices-02-to-04.md`.

Their review packages are listed in
`analysis/unified-validation-handoff.json`. The handoff intentionally reports
`instruments_ready_no_human_records_received`; a packet or validator is not a
review result.

The first provisional source-to-job mapping is in
`analysis/source-to-job-crosswalk.json`. It is a routing index for the next
evidence pass, not a finding that every listed job recurs in every corpus.
