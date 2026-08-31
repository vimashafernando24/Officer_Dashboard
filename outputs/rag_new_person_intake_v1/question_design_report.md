# §1 — Additional Course-Matching Question Design

Grounded in a direct inspection of the validated 84-course RAG corpus and its structured companion dataset (`outputs/nysc_course_matching_dataset.csv`, 87 rows, 83 of which crosswalk 1:1 to an indexable RAG document — see §2), cross-checked against the existing 362-respondent survey instrument so nothing already collected is asked twice. No question below was added because it "sounds useful" — each is backed by real population/variance numbers from the corpus, shown inline.

## Catalogue attribute inventory (real numbers, all 87 structured rows)

| Attribute | Populated | Variance | Verdict |
|---|---:|---|---|
| `skill_area` | 87/87 (100%) | 10 categories, 5–18 courses each | Usable, but see overlap note below |
| `attendance_type`/`attendance_days` | 87/87 (100%) | 50 Part-Time/Weekends vs 37 Full-Time/Weekdays | Usable — strong discriminator |
| `instruction_languages` | 87/87 (100%) | 43 Sinhala-only, 39 English-only, 5 bilingual | Usable — strong discriminator |
| `duration_months` | 87/87 (100%) | 65/87 (75%) are 6 months; rest scattered (12, 8, 3, 24) | Too skewed to discriminate — see rejection below |
| `nvq_level` | 32/87 (37%) | Level 4 (24), Level 5 (3), Level 3 (3), Level 3/4 (2) | Usable only as a soft signal |
| `qualification_type` | 34/87 (39%) | NVQ (32), Certificate (2) | Usable only as a soft signal |
| `target_occupations` | 55/87 (63%) | Mostly a single-item list that just restates `course_name` | Not independently useful |
| `course_modules` | 36/87 (41%) | Free text, real module names when present | Too sparse for a structured filter |
| `technical_skills` | 36/87 (41%) | Same source as `course_modules` | Too sparse for a structured filter |
| `soft_skills` | 4/87 (5%) | — | Too sparse to use at all |
| `entrepreneurship_content` | 7/87 (8%) | Inspected the 7 values directly — several are just ordinary module names ("Business Management", "Baker Management"), not reliably entrepreneurship-specific | Too sparse and too noisy for a structured filter |
| `sector_tags` | 87/87 (100%) | Mirrors `skill_area` at the same grain | Redundant with `skill_area` |
| `subcategory` | 0/87 (0%) | — | Unusable |

## Existing survey questions already covering part of this ground

- `ideal_sector` (12 options, e.g. "Manufacturing or production", "Information technology and communications") is already asked of every respondent and already has a working bridge to the catalogue's `skill_area` taxonomy: `SECTOR_BRIDGE` in `src/rag_prototype/retrieval_v2.py` maps 11 of 14 `ideal_sector` values to one or more `skill_area` values (the 3 unmapped — "Not sure", "Public administration, government, and defence", "Health, social work, and wellbeing" — have no clean catalogue equivalent, a genuine catalogue gap, not a bridge-table gap).
- `study_field_preference` (academic subject area) and `plans_after_education` (life-stage plan: job / further study / start a business / etc.) already exist and provide useful context but ask a different question from any of the candidates below.
- **Conclusion: "desired training area/field" is NOT re-asked.** `ideal_sector` is reused directly as the PRIMARY field signal via the existing bridge. What's missing, and genuinely new, is a finer-grained follow-up *within* that already-known sector — several `ideal_sector` values map to more than one `skill_area` (e.g. "Manufacturing or production" → both Automotive & Mechanical Engineering *and* Electrical & Electronics, 23 courses combined), and even a single `skill_area` contains many distinct occupations (Automotive & Mechanical Engineering alone spans Automobile Mechanic, Motorcycle Mechanic, Three Wheeler Mechanic, Automobile Electrician...). That gap becomes Q1 below.

## Final question set (5)

### Q1 — Occupation / course focus (new; refines, does not duplicate, `ideal_sector`)
- **Question**: "Within [the respondent's own `ideal_sector` answer], which of these is closest to what you want to train in?"
- **Answer options**: the distinct course names available in the RAG corpus under the `skill_area`(s) bridged from the respondent's `ideal_sector` (generated programmatically from the structured matching layer, §2, so it never drifts out of sync with the real catalogue), plus "Not sure / open to more than one." Skipped entirely if `ideal_sector = "Not sure"`.
- **Why needed**: `ideal_sector` alone is too coarse — it's compatible with many, sometimes a dozen or more, real courses.
- **Catalogue match**: `skill_area` (100% populated) narrows the field; `course_name` (100% populated, 84 distinct names in the indexable corpus) is the actual selection.
- **Sufficiently available?** Yes — both fields are 100% populated across the corpus.
- **Existing question overlap?** No — `ideal_sector` exists but at a much coarser grain; this is a genuinely new refinement, not a repeat.
- **How it influences retrieval**: hard filter to the bridged `skill_area`(s); soft-scores toward the named course when a specific one is chosen; falls back to sector-only matching (no course-name scoring) when "Not sure" is chosen.

### Q2 — Main reason/goal for this training (new)
- **Question**: "What's the main reason you want this training?"
- **Answer options**: Get a job / Improve skills in my current job / Start my own business / Continue on to further education / Build general skills, not sure about the next step yet.
- **Why needed**: distinguishes course *purpose* — a genuinely different dimension from `plans_after_education` (which is about the respondent's life stage generally, not why they want *this specific training*).
- **Catalogue match**: no single clean structured field supports this as a hard filter — `entrepreneurship_content` looked promising but is only 8% populated and, on direct inspection, inconsistently labeled (several values are just ordinary module names, not entrepreneurship-specific content). **This question is retained for reasoning/explanation quality, not as a retrieval filter**: it shapes whether the LLM frames a recommendation around job-readiness, upskilling, or entrepreneurial relevance when the course's own text supports that framing, and helps the DIRECT/ADJACENT-MATCH and "why recommended" explanation stay honest about what the respondent is actually trying to achieve.
- **Sufficiently available?** No structured field is well-populated enough to hard-filter on this — disclosed explicitly rather than pretending otherwise.
- **Existing question overlap?** No — genuinely new dimension.
- **How it influences retrieval**: does not filter or score candidates; passed to the LLM as explicit respondent evidence to shape explanation framing only.

### Q3 — Attendance / schedule preference (new)
- **Question**: "Which training schedule works best for you?"
- **Answer options**: Full-time, weekdays / Part-time, weekends / No strong preference.
- **Why needed**: this is the single strongest resolver of the catalogue's duplicate-course-name pairs (the same course offered in two schedule variants).
- **Catalogue match**: `attendance_type`/`attendance_days`, 100% populated, real variance (50 Part-Time vs 37 Full-Time).
- **Sufficiently available?** Yes.
- **Existing question overlap?** No — the existing `work_while_study_hours` question is about *current* work hours, not a training-schedule *preference*.
- **How it influences retrieval**: soft score boost toward matching courses; "No strong preference" applies no boost either way; never a hard filter (a respondent should still see a good course even if only one schedule variant exists for it).

### Q4 — Language of instruction (new)
- **Question**: "Which language would you prefer to study in?"
- **Answer options**: Sinhala / English / No strong preference.
- **Why needed**: resolves the catalogue's language-differentiated duplicate pairs (e.g. Automobile Electrician offered separately in Sinhala and English).
- **Catalogue match**: `instruction_languages`, 100% populated, meaningful split (43 Sinhala-only / 39 English-only / 5 bilingual).
- **Sufficiently available?** Yes.
- **Existing question overlap?** No equivalent question exists in the current survey.
- **How it influences retrieval**: soft score boost; never a hard filter (bilingual courses always satisfy either preference; "No strong preference" applies no boost).

### Q5 — Qualification / NVQ preference (new, soft signal only)
- **Question**: "Is it important to you that the training leads to a formal NVQ or vocational qualification?"
- **Answer options**: Yes, I want a formal NVQ or qualification / Not necessarily — I mainly want the practical skills / Not sure.
- **Why needed**: a real, if partial, distinguishing feature — some courses explicitly lead to an NVQ level, most don't state one either way.
- **Catalogue match**: `nvq_level`/`qualification_type`, only 37–39% populated.
- **Sufficiently available?** Only partially — **this is why it is a soft scoring signal, never a hard filter**. A course with a blank `qualification_type` is treated as "not documented," not as "does not offer a qualification" — the governance rules (§4) explicitly forbid treating catalogue silence as a negative fact.
- **Existing question overlap?** No.
- **How it influences retrieval**: small score boost when `qualification_type` is populated and matches the stated preference; zero effect (neither reward nor penalty) when the course's qualification field is blank or the respondent answered "Not sure."

## Candidates investigated and explicitly rejected

| Candidate | Verdict | Why |
|---|---|---|
| Specific skills/topics (free text) | **Rejected** | `course_modules`/`technical_skills` only 41% populated; a dedicated question would create expectations the catalogue can't reliably answer for the majority of courses. Module/skill text is still shown descriptively in the final course-evidence section when present — just not turned into a matching question. |
| Preferred course duration | **Rejected** | 100% populated but heavily skewed (75% of all courses are 6 months) — too little real variance to meaningfully discriminate; duration is instead surfaced as a plain course fact in the output. |
| A separate "target occupation" question | **Rejected** | `target_occupations` (63% populated) turns out, on inspection, to just restate `course_name` in almost every case — no independent information beyond what Q1 already captures. |
| Affordability / fees | **Rejected** | No clean structured field exists anywhere in the catalogue (confirmed in earlier corpus research); asking a question the catalogue can't answer would be a governance violation, not a matching aid. |
| Location / branch | **Rejected** | Same reason — not a clean structured catalogue field. |
| Eligibility / entry requirements | **Rejected** | Same reason. |
| Childcare / other personal constraints | **Rejected** | Explicitly out of scope per the governance brief — these must never be inferred from profile data either, and the catalogue has no structured field to match them against regardless. |

## Summary

5 new questions, all backed by real catalogue population/variance numbers, none duplicating an existing survey question. Two (Q1, "occupation/course focus") reuse the existing `ideal_sector` answer rather than re-asking it. One (Q2, "reason for training") is retained for explanation quality despite having no reliable structured catalogue field to filter on — disclosed as such, not silently treated as a hard filter. Two (Q3 schedule, Q4 language) are strong, well-populated hard-scoring discriminators. One (Q5 qualification) is an explicitly soft, partial-coverage signal.
