# Speaking Practice — reading-experience review

This record is separate from the comparative manuscript review and the final release audit. It documents bounded checks, not accessibility certification.

## Navigation changes

The long reader previously offered contents navigation only at the end of each article. Every approach and learning path now has links to both contents lists above its title, plus previous/next links within its own sequence at the end. The first and last items omit nonexistent neighbors. Link text names the destination, rather than relying on an ambiguous “next.” These controls are hidden in print.

The main landmark now accepts programmatic focus with `tabindex="-1"`. The reader check activates the skip link with the keyboard and verifies that focus reaches main, rather than checking scrolling alone. All 27 chapter contents destinations are exercised at all four existing viewport widths, in addition to the eleven path routes and their chapter cross-links.

## Enlarged text

The new check enlarges root text to 200% at a 320-pixel viewport. Its first run found horizontal overflow outside the already wrapping article bodies. Extending `overflow-wrap: anywhere` to the body allows the cover and contents to wrap too. A separate post-fix browser check measured document width 320 against viewport width 320. The chapter 16 opening at this setting was visually inspected: navigation and the large title wrap within the viewport without overlapping. This is a text-enlargement check, not a claim to have simulated every browser zoom setting or assistive technology.

## Defined color pairs

Relative luminance calculations were performed for the CSS ink, muted text, link and focus-outline colors against paper, contents-panel, quotation and white backgrounds. The smallest ratio among the tested text pairs was 5.23:1 (muted text on the contents panel); the focus color's smallest tested ratio was 5.40:1. Links are also underlined. These calculations cover the defined solid-color pairs, not every possible browser override or a complete standards audit.

## Interior and print review

`scripts/review_speaking_reading_views.py` validates the previous/next target sets for all 38 articles, then exercises adjacent links and return-to-contents by keyboard at 390 and 1280 pixels. The run passed. Screen focus outlines were checked on the activated links. It also captured interior views in `/tmp/speaking-interior-review-9v055u67`.

Visually inspected: the business-path body at 390 pixels, chapter 16's worked example at 1280, chapter 16's end navigation at 390, and the source index at 1280. Paragraph measure, quotation styling, wrapping and article separation were legible without observed overlap in those samples. Together with the earlier cover/enlargement checks, these cover the guide's principal screen view types, not every scroll position.

PDF pages 1, 16, 44, 140 and 197 were rendered and inspected, covering the cover, changed business and multilingual examples, chapter 16's added demonstration and the final source page. This exposed a keyboard-focus outline around the printed main landmark. Print-only `:focus` styling now suppresses that outline while retaining screen focus styles. The exporter explicitly asserts the computed print outline is absent. A fresh export passed, and corrected pages 16 and 197 were visually inspected again: the extraneous page rectangle is gone and content remains intact. The final 197-page export checks all 2,283 substantive text blocks and page geometry; the five-page visual sample is not a page-by-page certification.

Disposition: the planned reading-experience review is complete with the above bounded evidence and the print defect corrected. Final first-edition labeling and the requirement audit have also passed; see `speaking-release-audit.md`.

## Release verification

The refreshed desktop (1280-pixel) and mobile (390-pixel) entry screens were visually inspected after the wrapping fix. Title, review status, navigation and the beginning of the learning-path panel are legible and contained. The complete enhanced reader check passed for 596 links, all 38 units, every chapter destination at four widths, no-JavaScript navigation, skip-link focus and 200% text. This does not cover all interior visual states.

First-edition reader/download labels are reconciled. The complete reader check and adjacent-navigation check passed again after relabeling. The new PDF cover was visually inspected; its first-edition label and scope note fit without clipping.

The current package is the first edition. See `deliverables/speaking-practice/export-check.json` for artifact fingerprints; subsequent manuscript, builder or stylesheet edits require a fresh export.
