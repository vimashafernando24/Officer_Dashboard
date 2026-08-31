# Final NYSC RAG Course Corpus V2

## Freeze decision

The versioned V2 corpus is ready for a subsequent RAG run. It contains **84 independently traceable course-parent documents**. It does not modify or replace the previously frozen 79-course corpus or any prototype that may currently use it.

The governing counts are:

| Count type | Total |
|---|---:|
| Catalogue course parents supported by screenshot validation | **88** |
| Previously approved/indexable parents | 79 |
| Approved manual-review recoveries | 5 |
| Final V2 AI/RAG-indexable parents | **84** |
| Explicitly excluded parents | **4** |
| Reconciliation | **84 + 4 = 88** |

Accordingly:

> **CATALOGUE COURSE PARENTS = 88**

> **AI/RAG-INDEXABLE COURSE PARENTS = 84**

The second number is a source-quality decision for AI use. It does not mean that NYSC has only 84 courses.

## Why the counts changed from 87 to 88

The structured course dataset contains **87 rows**. The original screenshot-extraction layer also had 87 course documents, but one of those raw documents combined two visibly separate Welder catalogue offerings:

- Welder Full Time
- Welder Part Time

Screenshot validation separated those offerings into COURSE-045 and COURSE-045B without inventing a course. That source-supported split produced **88 screenshot-derived course parents**.

The structured data contains a defensible Full Time Welder record but no defensible one-to-one Part Time Welder record. Therefore, the structured 87-row total is not used as a forced target for the screenshot-derived parent count.

Other duplicate/grouping corrections did not change the net count: repeated Full Time Automobile Mechanic, Part Time Beautician and Part Time Graphics Designer catalogue entries were reconciled using their source-visible parent/variant evidence.

## Manual-review promotion

Five of the nine formerly excluded documents were approved and promoted into V2:

| Course ID | Course | Final review status |
|---|---|---|
| COURSE-002 | PYTHON | `SAFE_TO_INDEX_WITH_UNCERTAINTY` |
| COURSE-004 | Professional English | `SAFE_TO_INDEX` |
| COURSE-005 | Automobile Mechanic | `SAFE_TO_INDEX` |
| COURSE-046 | Beautician Part Time | `SAFE_TO_INDEX` |
| COURSE-068 | Graphics Designer Part Time | `SAFE_TO_INDEX` |

The final documents were promoted from the separately reviewed candidate directory. The candidates and the original validated/manual-review documents remain unchanged.

## Remaining exclusions

Four catalogue parents remain present in the research record but absent from the AI/RAG-indexable directory:

| Course ID | Course | Source-integrity reason |
|---|---|---|
| COURSE-015 | Quantity Surveying Assistant | Catalogue card says Part Time while the captured detail says Full Time weekdays |
| COURSE-027 | Landscaping Technician | Catalogue card says Part Time while the captured detail says Full Time weekdays |
| COURSE-039 | Cook | Cook-titled source contains automobile-electrical image, modules and narrative |
| COURSE-045B | Welder Part Time | Part Time catalogue card conflicts with Full Time weekday detail text |

These parents are recorded in `final_rag_corpus_v2_exclusions.csv`, including the future source evidence required for reconsideration. They have not silently disappeared.

## Python uncertainty handling

Python is indexed as `SAFE_TO_INDEX_WITH_UNCERTAINTY`. Its two remaining `[UNCLEAR]` markers are preserved exactly. Its final document contains explicit `DOCUMENT STATUS: SAFE_TO_INDEX_WITH_UNCERTAINTY` metadata.

The operational evidence rule is:

- `[UNCLEAR]` passages are not factual recommendation evidence;
- no missing fact may be reconstructed from an `[UNCLEAR]` region;
- explanations may rely only on clearly readable source text;
- material uncertainty must be disclosed;
- the clearly supported Python facts—course name, Part Time mode, 03 Month duration and 20-student capacity—remain usable.

Among the five newly recovered documents, Python is the only one retaining approved uncertainty. Six previously approved V1 documents also retain their already-governed validation limitations and `[UNCLEAR]` markers; V2 preserves rather than erases those limitations. The same non-inference rule should apply to every `[UNCLEAR]` region in the corpus.

## Cook source-integrity finding

Cook was not excluded merely because an OCR result looked unusual. The original individual-course screenshot itself has a Cook page title but an automobile-electrical image, automobile modules and narrative explicitly naming Auto Electrical training. The raw extraction accurately reflects that corrupted source.

The supporting catalogue card confirms that a Cook entry exists, but supporting listing pages cannot substitute for a validated individual-course document or reconstruct missing curriculum. Cook therefore remains recorded as a catalogue parent and excluded from AI recommendation until corrected authoritative documentation is obtained.

## Provenance model

Every V2 manifest row preserves this chain:

`final V2 RAG document → validated document or approved manual-review candidate → raw source document(s) → original screenshot(s)`

The manifest records:

- final document path;
- validated/candidate source-document path;
- raw source IDs and raw document paths;
- original individual-course screenshots;
- supporting catalogue-page screenshots;
- review status and uncertainty count;
- provenance status;
- SHA-256 document hash.

All **84/84** manifest rows passed the provenance check.

## Validation results

| Validation check | Result |
|---|---|
| Final `.txt` course parents | 84 — PASS |
| Manifest rows | 84 — PASS |
| Exclusion-register rows | 4 — PASS |
| 84 + 4 equals 88 | PASS |
| Duplicate course IDs | 0 — PASS |
| Duplicate final document paths | 0 — PASS |
| Duplicate final document hashes | 0 — PASS |
| Missing final documents | 0 — PASS |
| Invalid provenance records | 0 — PASS |
| Supporting catalogue pages indexed as course parents | 0 — PASS |
| Newly recovered documents | 5 — PASS |
| Recovered documents with uncertainty other than Python | 0 — PASS |
| Excluded parents found in final corpus | 0 — PASS |
| Python uncertainty markers preserved | 2 — PASS |

## Files frozen for the next RAG run

- `outputs/rag_course_knowledge/final_rag_corpus_v2/`
- `outputs/rag_course_knowledge/final_rag_corpus_v2_manifest.csv`
- `outputs/rag_course_knowledge/final_rag_corpus_v2_exclusions.csv`
- `outputs/rag_course_knowledge/final_rag_corpus_v2_report.md`

No embeddings, chunks, model calls or recommendations were created. No current prototype or previous corpus was mutated.

## Limitations

- This is a validated source-document corpus, not proof that every course is currently accepting applications.
- Catalogue screenshots may represent a time-specific publication state.
- Card-only sources contain less descriptive evidence than full detail screenshots.
- Typos and awkward wording visible in authoritative source material are preserved rather than silently rewritten.
- `VALIDATED_WITH_LIMITATIONS` and `[UNCLEAR]` content must remain visible to downstream retrieval and explanation safeguards.
- The four excluded course parents require corrected authoritative source material before AI recommendation use.

FINAL RAG COURSE CORPUS V2 READY: 84/88 COURSE PARENTS INDEXABLE
