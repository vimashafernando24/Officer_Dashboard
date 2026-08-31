# NYSC course screenshot full-text extraction report

## Scope and outputs

- Total course-related screenshots found: **97**
- Screenshot folder: `CoursesSS/`
- Distinct course text documents created: **87**
- Whole-page catalogue listing transcriptions created: **8**
- Total text documents created: **95**
- Index rows created: **95**
- Course screenshots excluded as unrelated: **0**

This step preserves screenshot text only. It does not create chunks, embeddings, metadata features, classifications, summaries, recommendations, or LLM-generated course content.

## Grouping by course

- Single-course detail screenshots found: **89**
- Distinct courses represented by those detail screenshots after grouping overlaps: **85**
- Courses represented only by a visible catalogue card: **2** (`PYTHON` and `Professional English`)
- Final distinct course documents: **87**
- Multi-course catalogue listing screenshots that cannot truthfully be assigned to one course: **8**. Their full page text is preserved in separate `LISTING-*` documents and their index `course_name` is blank.

The following repeated/overlapping screenshots were grouped into one course document each, with exact repeated OCR lines removed and non-identical visible wording retained:

- Automobile Mechanic: Screenshot 2026-04-12 at 22.21.32.png; Screenshot 2026-04-12 at 22.23.26.png
- Beautician: Screenshot 2026-04-12 at 22.23.56.png; Screenshot 2026-04-12 at 23.01.50.png
- Graphics Designer: Screenshot 2026-04-12 at 22.28.35.png; Screenshot 2026-04-12 at 22.30.52.png
- Welder: Screenshot 2026-04-12 at 22.47.42.png; Screenshot 2026-04-12 at 23.01.39.png

## Course identification

- Course identifiable at the single-course/detail or course-card level: **87 documents**
- Screenshot whose content could not be identified at all: **0**
- Screenshots not attributable to one course because they display many course cards: **8 catalogue listing pages**

## Unreadable or uncertain areas

`[UNCLEAR]` is used instead of guessing. The main uncertainty is small Sinhala/Tamil/English poster text, tiny text embedded inside catalogue-card images, truncated text, and text partly covered by the operating-system screenshot overlay. Sinhala-aware OCR was used for the two detail pages with substantial Sinhala content; words below the confidence threshold remain `[UNCLEAR]`.

- Screenshot 2026-04-12 at 22.20.46.png: 1 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.25.19.png: 15 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.27.24.png: 1 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.31.50.png: 16 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.38.08.png: 14 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.47.42.png: 1 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.48.17.png: 8 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.52.40.png: 12 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.56.09.png: 1 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.57.21.png: 8 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 22.57.47.png: 1 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 23.00.22.png: 10 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 23.01.39.png: 1 `[UNCLEAR]` marker(s) across its preserved transcription(s)
- Screenshot 2026-04-12 at 23.02.00.png: 9 `[UNCLEAR]` marker(s) across its preserved transcription(s)

## Overlap and duplication handling

- Four course offerings had complementary or repeated detail screenshots and were combined as listed above.
- No byte-identical screenshot files were found.
- Only exact repeated OCR lines within a grouped course were removed. Similar but non-identical source wording was retained.
- Repeated site/navigation wording across different catalogue listing screenshots was retained because it is visibly present in each distinct source screenshot.

## Traceability and limitations

- Every document records its source screenshot filename(s).
- The index maps every document to its text file and extraction status.
- Two courses have only catalogue-card text because no detail screenshot was present; this is stated in their extraction status.
- The extraction is faithful to visible wording, including apparent spelling and website-content inconsistencies. It does not silently correct source text.
- Photographic content without readable wording is not described because this task is text preservation only.
