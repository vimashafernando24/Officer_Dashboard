# NYSC course knowledge validation report

## Final readiness decision

**READY WITH DOCUMENTED LIMITATIONS**

The corpus is structurally ready for a controlled RAG indexing step because validated documents and complete provenance are now available. However, **9 documents must be excluded from normal indexing until manual review**, and the eight multi-course listing pages must remain supporting sources rather than competing course records.

## What was audited

- Source screenshots verified: **97**
- Raw indexed documents verified: **95**
- Raw course documents audited: **87**
- Multi-course catalogue-page documents audited: **8**
- Empty raw course documents: **0**
- Suspiciously short raw course documents: **2**
- Raw course documents with valid screenshot/index provenance: **87 / 87**
- Raw course documents with unexpected cross-course screenshot reuse: **0**

## Corrected course-document count

Validated unique screenshot-derived course offerings: **88**.

The eight listing pages show **91 course-card entries**. After reconciling visibly duplicated offerings and attendance variants, these support 88 validated screenshot-derived parents.

This is one higher than the raw 87 because the raw Welder document combined a visibly **Full Time** card and a visibly **Part Time** card. The validation stage split them without changing either source. Two other incorrect raw groupings were safely reorganized without changing the net count:

- Beautician: full-time kept separate; two part-time card sources grouped together.
- Graphics Designer: full-time kept separate; two part-time card sources grouped together.

The two Automobile Mechanic full-time sources remain grouped because their screenshot-derived detail headers both say Sinhala and the visible cards show the same attendance/duration. The structured dataset disagrees by claiming separate Sinhala and English records; that disagreement is documented for manual review rather than silently resolved.

## Manual review and exclusion from initial indexing

Documents requiring manual review: **9**.

- `COURSE-002` — PYTHON: Only a short catalogue card is available and two portions remain [UNCLEAR].
- `COURSE-004` — Professional English: Only a short catalogue card is available and its attendance conflicts with the structured catalogue record.
- `COURSE-005` — Automobile Mechanic: Two full-time Automobile Mechanic cards/details were grouped because both visible detail headers say Sinhala and both listing cards show one year; the structured cross-check instead contains separate Sinhala and English full-time records.
- `COURSE-015` — Quantity Surveying Assistant: The catalogue card says Part Time, while the course-detail text says full time; the structured cross-check contains only a Full Time Quantity Surveying record.
- `COURSE-027` — Landscaping Technician: The catalogue card says Part Time, while the course-detail text says full time; the structured cross-check contains both full-time and part-time Landscaping Technician records although only one screenshot-derived record exists.
- `COURSE-039` — Cook: The visible title is Cook, but the modules and overview describe automobile/auto-electrical training.
- `COURSE-045B` — Welder: The catalogue card says Part Time, while the course-detail text says full time; no part-time Welder record exists in the structured cross-check.
- `COURSE-046` — Beautician: Both linked catalogue cards are Part Time, but one of their detail screenshots states full time.
- `COURSE-068` — Graphics Designer: Both linked catalogue cards are Part Time, but one of their detail screenshots states full time.

The most serious issue is `COURSE-039`: the title says **Cook**, while the modules and narrative describe automobile/auto-electrical content. It must not enter course retrieval as currently written.

## Uncertainty, corruption and truncation

- Validated documents containing `[UNCLEAR]`: **7**
- Remaining `[UNCLEAR]` markers: **9**
- Raw documents with a truncated/covered section flag: **9**
- Raw documents with malformed-character or obvious-corruption flags: **8**

Safe cleaning removed encoding artifacts such as `Â` and a non-text CJK icon, removed unmatched terminal bracket artifacts, and changed two corrupted software-version fragments to `[UNCLEAR]`. No missing wording was invented. Ambiguous reading order remains documented rather than aggressively rewritten.

## Structured course-data cross-check

- Defensible one-to-one matches to the 87-row matching dataset: **85**
- Validated screenshot-derived offerings without a defensible structured match: **3**
- Structured rows without a defensible screenshot-derived match: **2**
- Validated documents with a recorded source/structured conflict: **8**
- Validated documents with at least one possible information-loss flag: **88**

Field-level cross-check absences among defensibly matched records:

- course name: **0**
- attendance: **3**
- duration: **84**
- language: **1**
- NVQ/qualification: **3**
- modules: **2**
- maximum students: **0**

Screenshot-derived offerings without a structured match:

- `COURSE-004` — Professional English (Full Time)
- `COURSE-015` — Quantity Surveying Assistant (Part Time)
- `COURSE-045B` — Welder (Part Time)

Structured rows without a screenshot-derived match:

- `NYSC-C020` — Automobile Mechanic (Full Time – English)
- `NYSC-C068` — Landscaping Technician (Full Time)

Duration is the most common apparent loss from individual detail documents because it is usually visible on the catalogue card rather than inside the captured detail page. The eight catalogue-page transcriptions preserve those card values, but they cannot safely be indexed as ordinary course records until card text is reconciled to the correct parent course.

The structured dataset was used only as a cross-check. Conflicts were retained; it did not replace screenshot text.

## Multi-course catalogue-page decision

All eight multi-course page documents are classified **SUPPORTING_SOURCE**. They contain useful card-level attendance, capacity, duration and snippets, but embedding them as ordinary courses would create duplicate and cross-course contamination. Keep them separate from the semantic course collection or later attach manually verified card snippets to the correct parent.

## Recommended retrieval architecture

Use parent-child retrieval: retrieve a whole course or a reliable section-aware child, deduplicate by course ID, and send the **full validated parent document** for final reasoning. Do not use fixed-size chunks as the default. Do not index documents marked `NEEDS_MANUAL_REVIEW_DO_NOT_INDEX`.

## Outputs

- `validated_documents/`: **88** source-preserving course parents
- `course_knowledge_quality_audit.csv`: one row for each of the 87 raw course documents
- `course_source_traceability.csv`: one row for each validated course parent
- `multi_course_document_audit.csv`: one row for each supporting catalogue page
- `rag_chunking_strategy.md`: future chunking/retrieval design only; no chunks created

No embeddings, chunks, recommendations, course scoring, survey changes, clustering changes or LLM calls were created in this stage.

## Final readiness declaration

**READY WITH DOCUMENTED LIMITATIONS**
