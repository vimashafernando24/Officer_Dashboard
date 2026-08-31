# Prompt-Fix Verification Report — Evidence-Category-Discipline Fix

**Question this experiment answers:** did the targeted prompt fix (§9 of
`evidence_category_discipline_report.md`) solve the systematic category-misuse problem
found in the v2 run, without bringing back the earlier excessive
under-recommendation problem? **Answer: yes, on both counts.**

Retrieval, the 84-course corpus, the 10 respondents, and the model (`gpt-5-mini`) were
all held identical to the v2 run — the v1 run's saved retrieval bundle was reused
byte-for-byte, not recomputed. The only change was the governance prompt
(`context_pack_v2.GOVERNANCE_INSTRUCTIONS`), which now includes an explicit
EVIDENCE-CATEGORY DISCIPLINE section, a CONFLICT RULE (direct preference beats general
opinion), and a NO-SUBSTITUTION RULE (missing preference evidence = uncertainty, not
license to manufacture one). Full fix text in `context_pack_v2.py`.

A note on how this run went operationally: the first attempt hung on two separate calls
well past their configured SDK-level timeout, with no other explanation (isolated
diagnostic calls confirmed it wasn't a broad connectivity or auth issue — a trivial call
succeeded in ~5s throughout). Rather than keep debugging httpx/SDK internals, a hard,
Python-level daemon-thread timeout was added to `openai_client.py` that cannot be
defeated by SDK behavior, and the run script was changed to write results
incrementally so no progress is lost if a future run has to be interrupted. The
full 10-respondent run below used that fix and completed cleanly (1 retry used across
all 10 calls, 10/10 succeeded).

---

## 1. Headline comparison

| Metric | v2 (before fix) | **v3 (after fix)** | Manual (reference) |
|---|---:|---:|---:|
| Total recommendations | 35 | **30** | 19 |
| Respondents with ≥1 recommendation | 10/10 | **8/10** | 8/10 |
| `NO_DEFENSIBLE_RECOMMENDATION` count | 0/10 | **2/10** | 2/10 |
| Category-discipline audit — FAIL | 4 | **0** | n/a |
| Category-discipline audit — PASS WITH CAUTION | 6 | **1** (new, minor, unrelated to the fixed pattern) | n/a |
| Category-discipline audit — PASS | 95 | **72** | n/a |
| Fabrication/eligibility/etc. audit — FAIL | 0 (after negation fix) | **0** | n/a |
| Cost (10 respondents) | $0.075 (ESTIMATED) | $0.102 (ESTIMATED) | $0 |
| Cost projection (362) | ~$2.72 (ESTIMATED) | ~$3.69 (ESTIMATED) | — |

**v3's coverage pattern (8/10 respondents, 2 correct declines) now matches the manual
reference almost exactly**, rather than the v2 run's 10/10-with-zero-declines pattern
that was itself a symptom of the category-misuse problem (both weak-evidence
respondents had been getting a recommendation built on an opinion variable instead of
correctly declining).

## 2. The two respondents whose STRONG recommendations were flagged for downgrade

| Respondent | Before (v2) | After (v3) |
|---|---|---|
| `nysc-465701ee` | STRONG recommendation for COURSE-006, primary-justified by the opinion variable `most_useful_quality_for_job` | **`NO_DEFENSIBLE_RECOMMENDATION`.** The model's own stated reason: *"The respondent did not state any direct content preference... Other answers available (feasibility, education background, or general opinions such as valuing IT skills) are not permitted to substitute for a stated field preference."* This is a direct, explicit application of the new rule. |
| `nysc-33aaf2f7` | STRONG recommendation for COURSE-006, same misuse; entire 5-course set had no legitimate content anchor once the opinion variable was discounted | **3 recommendations, all cleanly grounded.** COURSE-008 (Computer Hardware Technician) and COURSE-029 (Mobile Phone Repair Technician) are now primary-justified by `ideal_sector = "Wholesale, retail, **or repair**"` — the model correctly recognised that "repair" is literally part of this respondent's stated sector, a genuine connection this analysis had not even surfaced. `occupational_class` (their current technical occupation) now appears only as *secondary*, correctly-hedged supporting evidence, not the primary driver. |

`33aaf2f7`'s new recommendations are, if anything, **better grounded than the original
manual-reasoning baseline** (which had picked the same two courses, COURSE-008 and
COURSE-029, by a different reasoning path) — the fix didn't just remove a bad citation,
it let the model find the legitimate one that was there all along.

## 3. All 4 previously-affected respondents, confirmed clean

| Respondent | `most_useful_quality_for_job` citations before | After |
|---|---:|---|
| `nysc-465701ee` | 1 FAIL (primary, STRONG) | Not cited at all — correctly declined |
| `nysc-33aaf2f7` | 3 FAILs + 2 CAUTIONs (across 4 of 5 recommendations) | Not cited at all |
| `nysc-acaf63b5` | 1 CAUTION | Not cited at all — leads with `study_field_preference` |
| `nysc-0c6c34a2` | 2 CAUTIONs | Not cited at all — leads with `ideal_sector` |

Zero remaining citations of `most_useful_quality_for_job` anywhere in the v3 run. The
one new PASS WITH CAUTION in v3 (`nysc-3a86d117` / COURSE-001, citing
`most_important_life_goal` as a *tertiary* (position-3) supporting citation) is a
different, much lower-severity instance — not primary, not the systematic pattern, and
correctly self-limited by the audit's own severity rules (LOW severity, secondary
citation, category rules explicitly allow this as acceptable secondary framing).

## 4. Was legitimate contextual reasoning accidentally suppressed?

**No — checked directly.** The 5 respondents whose v2 recommendations had zero
category-discipline issues were re-compared against v3 course-by-course:

| Respondent | v2 course set | v3 course set |
|---|---|---|
| `3a86d117` | COURSE-001, 006, 073, 002, 057 | COURSE-001, 006, 073, 002 |
| `131a2b60` | COURSE-006, 073, 052, 002 | COURSE-073, 052, 002, 006 |
| `346623df` | COURSE-006, 001, 073, 057 | COURSE-001, 006, 073, 057 |
| `00e2c251` | COURSE-019, 023, 060, 065 | COURSE-023, 019, 060, 024 |
| `55bdfdcc` | COURSE-049, 007, 011, 050 | COURSE-049, 007, 047, 050 |

All five retain their core matches (the ICT diploma/Java/networking cluster for the
ICT-interested respondents, Construction Site Supervisor + Quantity Surveying for the
construction-interested respondent, Business Management + Cookery + Baker for the
hospitality-interested respondent). Only minor single-course substitutions occurred
(one dropped duplicate, a few swaps to near-identical alternative courses in the same
sub-field) — consistent with normal LLM output variance between calls, not a
suppression of legitimate reasoning. The core finding from the v2 experiment (retrieval
correctly surfaces the right courses; the earlier gpt-4o-mini run's problem was the
model, not retrieval) still stands and was not undone by this fix.

## 5. Fabrication/eligibility/protected-field audit (the original grounding audit)

Re-run on the v3 output using the same extended audit from the previous experiment
(covers course-ID safety, respondent/profile claim grounding, course-text grounding,
inference labelling, and the negation-aware banned-phrase and unsupported-eligibility
checks): **29 PASS, 3 PASS WITH CAUTION (low-severity paraphrase/word-overlap flags,
same nature as before), 0 FAIL.** No new fabrication or eligibility-claim issues were
introduced by the prompt change.

## 6. Cost and operational notes

- $0.1018 for this 10-respondent run (**ESTIMATED**, from actual recorded token usage —
  240,942 input / 25,936 output tokens — against `gpt-5-mini`'s published list pricing;
  not a live-billed figure). ~$3.69 projected for 362 respondents, also **ESTIMATED**.
  Somewhat higher than the v2 run's $0.075/~$2.72, consistent with the longer prompt
  (12,436 chars of instructions vs. the earlier ~9,000).
- Average call duration 32s (max 47s) — faster on average than the v2 run's 41s
  avg/74s max, though this run also hit one hard-timeout-triggered retry (1 total across
  10 calls) that the incremental-write safeguard absorbed without losing any progress.
- The hard-timeout fix and incremental-write safeguard are now permanent parts of
  `openai_client.py` / the run-script pattern and will apply to any future run using
  this pipeline, including a larger validation batch.

---

## Verdict

The targeted fix worked as intended, verified against every dimension requested:

- **Systematic category-misuse problem: resolved.** 0 FAILs (down from 4), the
  `most_useful_quality_for_job` pattern is completely gone, and the model now
  articulates the correct rule in its own decline reasoning.
- **Both flagged STRONG recommendations: correctly resolved**, not merely downgraded —
  one became a correct decline, the other found a genuinely stronger, previously
  unnoticed legitimate justification.
- **No return of the excessive under-recommendation problem.** Coverage (8/10) and
  decline count (2/10) now match the manual reference pattern; the specific
  previously-missing matches recovered by the v2 fix (Business Management, Construction
  courses, Cookery/Baking, etc.) are all still present.
- **No regression in legitimate contextual reasoning** across the 5 respondents that
  were already clean.
- **No new fabrication, eligibility, or protected-field issues** introduced.

## READY FOR NEXT VALIDATION BATCH
