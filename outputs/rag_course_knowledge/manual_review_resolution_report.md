# NYSC course manual-review resolution report

## Scope and safeguard

This review investigated only the nine documents currently marked `NEEDS_MANUAL_REVIEW_DO_NOT_INDEX`. Every decision was checked against the original screenshot at its native resolution, then compared with the raw extraction, validated document, supporting catalogue page and structured course data. The screenshots remained authoritative; structured records were used only as a cross-check.

No production file under `validated_documents/` was changed. No current RAG/index output was changed. The five proposed recovered documents are isolated in `manual_review_resolved_candidates/` and are not approved production inputs unless reviewed separately.

## Outcome

- Excluded documents reviewed: **9**
- Proposed as `SAFE_TO_INDEX`: **4**
- Proposed as `SAFE_TO_INDEX_WITH_UNCERTAINTY`: **1**
- Proposed recoveries in total: **5**
- Proposed to remain excluded: **4**
- Currently approved/indexable parents before this review: **79 of 88**
- Proposed indexable parents if all five recoveries are approved: **84 of 88**
- Existing and final evidence-supported screenshot-derived parent count: **88**
- Production corpus changed: **No**

## Decision table

| Course | Original problem | Resolution | Remaining uncertainty | Proposed status |
|---|---|---|---|---|
| COURSE-002 — PYTHON | Card-only source with two `[UNCLEAR]` placeholders | Recovered the clearly visible line `Python මුල සිට ඉගෙන ගන්න`; kept unreadable promotional-image and corrupted/truncated text marked | Two localized markers remain; course identity, Part Time mode, 03 Month duration and 20-student capacity are clear | `SAFE_TO_INDEX_WITH_UNCERTAINTY` |
| COURSE-004 — Professional English | Short card only; screenshot says Full Time while structured data only has a separate Part Time record | Preserved the complete Full Time screenshot card and did not overwrite it from structured data | Card is sparse but not ambiguous | `SAFE_TO_INDEX` |
| COURSE-005 — Automobile Mechanic | Two apparent source entries grouped; structured data implies Sinhala and English variants | Both original detail captures say Sinhala, Full Time weekdays, 20 students and Level 4; both catalogue cards say Full Time, 20 students and 01 year, so one repeated screenshot-derived parent is retained | Structured English/6-month record is unsupported by these screenshots, but the screenshot parent itself is reliable | `SAFE_TO_INDEX` |
| COURSE-015 — Quantity Surveying Assistant | Part Time catalogue card conflicts with Full Time weekday detail text | Kept unresolved; did not choose one schedule and did not merge it with the separately captured Full Time COURSE-019 | Attendance and delivery days are materially contradictory | `KEEP_EXCLUDED` |
| COURSE-027 — Landscaping Technician | Part Time catalogue card conflicts with Full Time weekday detail text | Encoding artefacts were identifiable, but the schedule conflict could not be resolved | Attendance/delivery pattern remains unreliable | `KEEP_EXCLUDED` |
| COURSE-039 — Cook | Cook title but automobile image, modules and Auto Electrical narrative | Confirmed the contamination exists in the original Cook-titled detail screenshot itself; the supporting listing card cannot reconstruct the missing Cook detail content | Curriculum and descriptive content remain invalid for Cook | `KEEP_EXCLUDED` |
| COURSE-045B — Welder | Part Time card conflicts with Full Time weekday detail text | Kept the parent separate from the valid Full Time COURSE-045, but no source-supported Part Time detail reconstruction exists | Attendance/delivery pattern remains unreliable | `KEEP_EXCLUDED` |
| COURSE-046 — Beautician | Two Part Time cards had one correct Part Time detail capture and one conflicting Full Time detail capture | Built the candidate from the complete Part Time 22.48.00 screenshot only; retained COURSE-010 as the independent Full Time parent | None material | `SAFE_TO_INDEX` |
| COURSE-068 — Graphics Designer | A Full Time variant detail source had been included in the Part Time parent | Built the candidate from the complete English Part Time 22.55.38 screenshot only; the Sinhala/English Full Time Level 4 source remains with COURSE-016 | None material | `SAFE_TO_INDEX` |

The row-level evidence, paths and structured cross-check identifiers are in `manual_review_course_audit.csv`. Every proposed textual deletion, recovery or reading-order correction is in `manual_review_change_log.csv`.

## `[UNCLEAR]` review

Only COURSE-002 among these nine documents contained `[UNCLEAR]` markers: **2 original markers**.

The original-resolution Python card makes the first catalogue-description line readable: `Python මුල සිට ඉගෙන ගන්න`. That readable fragment was recovered. However, the promotional-image wording and a following corrupted/truncated catalogue line are still not fully legible. They remain localized as two `[UNCLEAR]` markers rather than being guessed.

Therefore:

- Fully resolved original markers: **0**
- Original marker regions partially narrowed: **1**
- Remaining `[UNCLEAR]` markers in the proposed candidate: **2**
- Remaining uncertainty impact: **Medium**, because detailed promotional wording may include schedule/contact details, while the card's core course identity, attendance, duration and capacity are independently clear.

## Cook investigation

The Cook trace is:

1. Individual-course screenshot: `Screenshot 2026-04-12 at 22.45.50.png`
2. Raw document: `raw_course_text/course-039_cook.txt`
3. Validated document: `validated_documents/course-039_cook.txt`
4. Supporting catalogue page: `Screenshot 2026-04-12 at 22.48.17.png`
5. Structured cross-check: `NYSC-C053`

The individual screenshot itself is internally contaminated. Its visible page title is **Cook**, but it shows:

- an automobile-electrical photograph;
- engine, transmission, steering, braking and electrical-system modules;
- narrative explicitly naming an **Auto Electrical** course.

The raw extraction accurately preserved what the screenshot shows. No neighbouring screenshot text was accidentally appended, no two raw documents were merged, and the course boundary is not an OCR artefact. The supported diagnosis is therefore **D: the original source itself genuinely contains the wrong-course content**—most plausibly a source-site content/linking fault, without asserting its technical cause.

The catalogue listing card confirms only a Cook card with Part Time, 20 students and 06 Month. Because the eight listing pages must remain supporting sources, that card cannot replace the corrupted individual detail page or supply missing Cook curriculum. Cook therefore remains excluded.

## Variant and grouping decisions

### Automobile Mechanic

The catalogue shows two Full Time cards, but both visible cards show the same name, 20 students and 01 year, and both captured detail pages show Sinhala, Full Time weekday delivery and Level 4 content. No screenshot-visible attribute supports separating these into Sinhala and English parents. They remain one repeated screenshot-derived parent. The structured English/6-month record is reported as a conflict but is not authoritative for this screenshot corpus.

### Quantity Surveying Assistant

The catalogue visibly contains a Part Time card and a separate Full Time card. COURSE-019 remains the separately supported Full Time parent. COURSE-015 cannot be safely assigned to the Part Time parent because its individual detail page says Full Time; it is not merged with COURSE-019 and remains excluded.

### Welder

The catalogue visibly contains Full Time and Part Time cards, so COURSE-045 and COURSE-045B remain separate parents. COURSE-045B is not collapsed into the Full Time parent merely because its detail text says Full Time. Its own source inconsistency keeps it excluded.

### Beautician

Full Time COURSE-010 and Part Time COURSE-046 remain separate parents. The complete 22.48.00 screenshot independently supports Part Time COURSE-046. The conflicting 23.01.50 Full Time capture is not used in the Part Time candidate.

### Graphics Designer

Full Time COURSE-016 and Part Time COURSE-068 remain separate parents. Screenshot 22.30.52 explicitly supports the Full Time Sinhala/English Level 4 parent. Screenshot 22.55.38 explicitly supports the English Part Time parent and is the only detail source used in its repaired candidate.

## Cross-course and safe-corpus review

The only confirmed different-course content contamination among the nine documents is COURSE-039 Cook.

The Beautician and Graphics Designer problems were same-title delivery-variant source grouping problems, not text from an unrelated course. The Automobile Mechanic issue was repeated/variant ambiguity rather than cross-course contamination. No neighbouring-card text was found inside the other excluded documents.

No newly discovered problem requires a currently indexable parent to be reconsidered. In particular:

- Full Time Beautician COURSE-010 has its own supporting Full Time detail evidence.
- Full Time Graphics Designer COURSE-016 has its own supporting Full Time detail evidence.
- Full Time Welder COURSE-045 remains distinct from the unresolved Part Time COURSE-045B.
- Full Time Quantity Surveying Assistant COURSE-019 remains distinct from unresolved COURSE-015.

## Course-count reconciliation

The source evidence continues to support **88 unique screenshot-derived course parents**.

The eight listing pages contain **91 visible course-card entries**. Three repeated same-offering card entries reconcile those 91 entries to 88 parents: the repeated Full Time Automobile Mechanic entry, the repeated Part Time Beautician entry and the repeated Part Time Graphics Designer entry. Separately, the visibly Full Time and Part Time Welder entries remain two parents; their split is why the validated screenshot-derived count is one higher than the 87 raw course documents.

The 87-row structured dataset is not used as a target count. It has 85 defensible one-to-one screenshot matches and known source/variant differences. None of the nine manual-review resolutions supplies evidence for adding or removing another parent, so **88** remains the defensible count.

## Files created

- `manual_review_course_audit.csv` — explicit nine-course working table and decision evidence
- `manual_review_change_log.csv` — source-visible proposed text changes only
- `manual_review_resolution_report.md` — this report
- `manual_review_resolved_candidates/course-002_python_candidate.txt`
- `manual_review_resolved_candidates/course-004_professional_english_candidate.txt`
- `manual_review_resolved_candidates/course-005_automobile_mechanic_candidate.txt`
- `manual_review_resolved_candidates/course-046_beautician_part_time_candidate.txt`
- `manual_review_resolved_candidates/course-068_graphics_designer_part_time_candidate.txt`

These five candidates are proposals only. The current production/index corpus remains unchanged and must continue excluding all nine original manual-review documents until the proposed statuses are approved.
