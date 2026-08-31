# RAG chunking and retrieval strategy for the NYSC course catalogue

## Corpus measured in this audit

- Validated screenshot-derived course offerings: **88**
- Character length: median **874**, minimum **62**, 95th percentile **1215**, maximum **1595**
- Word length: median **132**, minimum **10**, maximum **236**
- Multi-course catalogue pages: **8 supporting sources**, not course records

No chunks or embeddings are created in this stage.

## Strategy comparison

| Option | Fit for this catalogue | Main risk |
|---|---|---|
| A. One whole course document = one chunk | Good baseline because most documents are short. Preserves all context. | Long or multilingual pages may match less precisely, and one noisy section can affect retrieval. |
| B. Fixed-size chunks | Poor default. | Splits headings, module lists and qualifications from the course identity and can mix context at arbitrary boundaries. |
| C. Heading/section-aware chunks | Useful only where clear sections exist, such as overview, modules, qualification or schedule. | Some screenshots have broken two-column reading order or no reliable headings. |
| D. Parent-child retrieval | Best fit. Small section-aware children can retrieve a course, but final reasoning receives the full validated parent. | Requires stable parent IDs and careful exclusion of review-only/supporting documents. |

## Recommended architecture

Use **parent-child retrieval with a whole-course parent**:

1. Keep each validated course file as the authoritative parent document.
2. For short, coherent documents, allow the whole parent to act as the only retrieval chunk.
3. Where reliable headings/lists exist, later create section-aware child chunks. Never split a module item or paragraph solely to meet a token count.
4. Retrieve child or whole-document candidates, deduplicate by `course_document_id`, then provide the **full validated parent course document** to the reasoning model.
5. Do not embed `NEEDS_MANUAL_REVIEW_DO_NOT_INDEX` records until resolved.
6. Keep the eight `SUPPORTING_SOURCE` listing pages outside the course-document semantic collection. They may be retained in a separate provenance collection but must not compete as courses.
7. Never use fixed-size chunking as the first pass. If a future unusually long parent requires a size cap, split only at verified section/paragraph boundaries with a small overlap and retain the parent link.

## Minimal future retrieval metadata

| Metadata | Purpose |
|---|---|
| `course_document_id` | Stable identity and deduplication. |
| `course_name` | Human-readable retrieval result. |
| `parent_document_id` | Links any future child chunk to the full validated course. |
| `source_type` | Distinguishes `COURSE_DOCUMENT` from `SUPPORTING_SOURCE`. |
| `source_screenshot_filenames` | Exact provenance. |
| `validation_status` | Prevents review-only documents from entering normal retrieval. |
| `uncertainty_present` / `uncertainty_count` | Allows cautious handling of `[UNCLEAR]`. |
| `source_conflict_present` | Prevents conflicting schedule/language facts being treated as settled. |
| `section_heading` | Only for future section-aware child chunks. |

Do not replace the full parent text with metadata or a recommendation feature table.
