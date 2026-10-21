# Wave-2 full-context review request

Status: **review packet ready; no human review records received**.

Please review the 19 transcript-derived candidates in the unified crosswalk: 7
Ali Siddiq, 6 Dry Bar Comedy and 6 TED items. These are routing hypotheses, not
validated presentation lessons.

## Independence and task

The reviewer must be independent of the people who assembled the transcript
packets, proposed the candidate patterns, and created the crosswalk. Use a
pseudonymous reviewer code and confirm independence in the browser. For each
candidate, inspect all cited context: open the original video and the full
transcript/cue links, not only the bounded excerpts. Decide whether the cited
context supports the candidate as worded, does not support it, or is
indeterminate. Note mismatches, counterexamples, source/identity concerns, or
uncertainty. Do not infer recurrence, transfer, or effectiveness from these
items.

## Browser and export

Use the focused browser `site/pattern-review-wave-2.html` or the portable
`deliverables/wave-2-full-context-reviewer-pack.zip`. The focused page shows
only the 19 target items; it preserves the combined 107-item denominator and
lists the other 88 IDs explicitly as unreviewed. The package includes all 56
cited context references, 43 unique full transcripts and 43 unique cue/timing
files. Open the original source video and each cited full transcript/cue before
judging. Review these IDs:

- Ali Siddiq: `ali-001` through `ali-007`
- Dry Bar Comedy: `drybar-001` through `drybar-006`
- TED: `ted-001` through `ted-006`

Choose **Export completed review items** after the 19 target items are complete.
The export is partial for the combined 107-item queue: the other 88 IDs must
remain explicitly listed as unreviewed. Do not change decisions or omit the
unreviewed-ID list after export. Validate the returned JSON from the repository
root:

```text
python3 scripts/validate_source_pattern_review_export.py reviewer-wave-2.json
```

For this targeted pass, the validator should report `19/107`,
`partial; missingness preserved`, and `wave-2 coverage 19/19`. Preserve each
reviewer’s export as a separate record. Do not merge the results into the
55-pattern fieldbook or speaking guide: contextual fit alone does not establish
source identity, independent recurrence/function, delivery meaning, learner
transfer, listener outcomes, or effectiveness.

The local browser smoke test has exercised the 19-of-107 and full-export paths
with temporary synthetic decisions. It is technical evidence only, not a human
review record.
