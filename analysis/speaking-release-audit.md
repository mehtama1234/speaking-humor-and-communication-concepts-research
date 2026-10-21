# Speaking Practice — first-edition release audit

## Scope

The goal is the detailed editorial product in this repository: all 27 approaches from [the original inventory](transcript-backed-concrete-speaking-approaches.md), all eleven curricula, reader integration, attribution, practical teaching and portable delivery. It is separate from best-speech-analysis's presentation fieldbook. Neither complete review of the wider video corpus nor acquisition of additional sources is a completion requirement for this editorial pass.

## Requirement evidence

| Requirement | Authoritative evidence | Disposition |
| --- | --- | --- |
| All 27 approaches, not a selected subset | `writeups/speaking-practice/01-*` through `27-*`; the technical audit maps every inventory number to its authored title and fingerprint | Scope check passes; substantive review covers every chapter |
| Eleven developed teaching paths | `writeups/speaking-curricula/01-*` through `11-*`; each maps to its own original curriculum and contains at least six developed sessions | Scope check passes; full path review covers continuing case, progression, outputs and transfer |
| First principles, source readings, concrete applications, limits and practice | [Comparative editorial review](speaking-editorial-review.md), with individual dispositions for all 38 units and book-level assessment | Complete; review made substantive corrections, not merely count checks |
| Real source material distinguished from invented applications | Each approach's source trail and local transcript; `analysis/speaking-source-catalog.json`; `writeups/speaking-book/sources-and-evidence.md` | Thirty cited video identities verified against acquisition metadata; inspection limits remain explicit. Original cases are labeled, not claimed as observed outcomes |
| Professional prose and coherent book-level treatment | Individual revisions and final book-level disposition in editorial review; orientation and evidence notes | Complete for the first edition; not external peer review or learner-effect validation |
| Usable frontend and existing-site entry points | `site/speaking-practice.html`, CSS, homepage link and curriculum reader/download links | Integrated; first-edition labels and final rebuild verified |
| Mobile/no-JavaScript/keyboard/enlarged-text reading | `scripts/check_speaking_practice_reader.py`, plus [reading-review record](speaking-reading-review.md) | Final first-edition run passes all chapter destinations, four widths, skip focus and 200% text |
| Interior navigation and visual inspection | `scripts/review_speaking_reading_views.py`; reading-review record | All 38 neighbor sets checked; desktop/mobile keyboard samples and principal visual types reviewed; no claim of all-device certification |
| PDF and offline ZIP | `scripts/export_speaking_practice.py`; `deliverables/speaking-practice/export-check.json` | Final first-edition full text-block, geometry, link and archive checks pass |
| Current artifacts, not stale snapshots | `scripts/audit_speaking_release.py`; `analysis/speaking-release-technical-audit.json` | Final input fingerprints, payload hashes, archive manifest, mappings, edition labels and links pass |
| Preserve research and avoid unauthorized publishing | Authored material is separate under `writeups`; portable archive contains only HTML, CSS, PDF, public source index, README and checksum manifest | No raw transcript/media redistribution, external sale, upload, commit or licensing claim performed |

## Boundaries

The source analysis is based on the local transcript passages named in the chapters. It does not claim audiovisual review of every cited video, verification of underlying research studies, current availability of public URLs, or complete coverage of hundreds of videos. Professional editorial packaging does not itself establish legal clearance, endorsement or market demand. The first edition is a deliverable for the owner, not an external sales transaction.

## Final verification

Completed on 2026-09-21. All commands below completed successfully against the first-edition artifacts:

- `python3 scripts/build_speaking_source_catalog.py`: 30 distinct sources across all 27 chapters.
- `python3 scripts/build_speaking_practice_reader.py`: all 27 approaches and 11 learning paths.
- `python3 scripts/check_speaking_practice_reader.py`: 596 links, unique IDs, four widths, every chapter destination, no-JavaScript reading, cross-navigation, skip focus and 200% text.
- `python3 scripts/export_speaking_practice.py`: 197 PDF pages, all 2,283 substantive text blocks, 514 portable HTML links, 316 PDF links, no text outside pages, no short-page flags, offline reading and verified ZIP payloads. Print focus regression assertion passes.
- `python3 scripts/audit_speaking_release.py`: all 38 inventory/curriculum mappings, source identities, manuscript links, edition labels, input fingerprints and exact archive contents.
- `python3 scripts/review_speaking_reading_views.py`: 38 adjacent-link sets and keyboard navigation at two widths. Final cover visually inspected after relabeling; interior layout/content is unchanged from the recorded sample review.
- `git diff --check`: passes. No TODO/TBD/PLACEHOLDER markers found in the authored manuscript directories.

Browser commands use `LD_LIBRARY_PATH="$(cat /tmp/playwright-libs-path)"` in this workspace. Main manuscript: 58,896 whitespace-delimited words, plus 1,041 words of orientation/evidence notes. ZIP SHA-256: `a8325e4443d6e8d9d2fc5b6d04e20b031ff1a7852cda45ff7f07d2496b309f26`.

Disposition: all requirements of this editorial goal are achieved. The first-edition reader, PDF and offline ZIP are ready for the owner's use. No required editorial or packaging work remains within this scope. External publication, commercial terms, permissions review, additional corpus analysis and learner studies are separate decisions, not outcomes claimed here.
