# 30-Respondent Validation Batch Report

**Frozen and unchanged in this run:** `gpt-5-mini`, the evidence-category-disciplined
governance prompt (`context_pack_v2.GOVERNANCE_INSTRUCTIONS`), the 84-course V2 corpus,
the BM25 retrieval architecture and query-construction logic (imported directly from
`retrieval_v2.py`, not reimplemented), the respondent/profile/course evidence rules, both
audits, and the recommendation schema. The only thing that changed was the **sample**:
30 new respondents, never used in the frozen 10-person v3 baseline, with retrieval
computed fresh for them (there was no prior bundle to reuse, since they're new).

30/30 API calls succeeded, 0 retries, 0 timeouts — the most operationally clean run of
this pipeline so far.

---

## 1. Sample selection — how the 30 were chosen

Selected from the 352 remaining respondents (362 total − 10 already used in the frozen
baseline), deliberately for stress-testing rather than ease of recommendation. Full
rationale per respondent in `validation_sample_30_selection_rationale.csv`. Method:

1. Built compact characterisation cards for all 352 remaining respondents (branch,
   frozen profile memberships, `ideal_sector`/`study_field_preference`/`job_type_sought`,
   feasibility/context signals, education/employment status).
2. Allocated by branch **not proportionally** but weighted toward stress-testing value:
   D=11, F=8, G=6, E=5. E has only 33 remaining respondents (the smallest, most
   sample-constrained branch per the frozen clustering report itself); 5/33 ≈ 15% is a
   deliberately *higher* sampling rate than the other branches (~5-6%) to ensure
   meaningful E representation without distorting the batch with a forced equal count.
3. Within each branch, hand-picked for:
   - **Profile-membership diversity**: every G economic-role×future-engagement combo
     represented (including the rare `p2/p2` combo, only 3 respondents in the whole
     remaining pool); both E profiles; both F profiles (4 insecure / 4 secure — a
     deliberately more even split than the ~2:1 population ratio, to stress-test the
     insecure-employment profile adequately); 10 distinct D profile combos across 11
     picks (D has 24 possible combos; not all could be covered, but repeats were
     avoided except once).
   - **Sector diversity**: Education/teaching, Manufacturing, Finance/banking,
     Health/social work, Creative arts, Agriculture, Hospitality, Public
     administration/government, Retail/repair, Personal services/beauty, plus ICT
     (unavoidably the modal sector in this survey population, but represented with
     different profiles/contexts each time, not repeats of the original 10's cases).
   - **Evidence-strength spread**: clear strong direct-sector preferences; moderate
     cases; and explicitly weak/sparse cases selected by checking for `ideal_sector` =
     "Not sure" *combined with* no other usable field-specific signal (`nysc-b556590a`,
     `nysc-04134b0d`, `nysc-5242257e`) — a stricter weak-evidence filter than "has any
     answered field," since most respondents answer *something*.
   - **Deliberately complex/conflicting cases**: `nysc-25c345ec` (has children, never
     studied, O/L-level, states "stay at home" intent, yet also names a sector
     preference); `nysc-49b62c9a` (provider with children, wants postgraduate study,
     but also says they don't want to work); `nysc-cab6cf5f` (sector "Not sure" but
     other direct-preference signals present) — none of these were selected because
     they looked easy.

## 2. Branch and profile composition

| Branch | n | Profile combos represented |
|---|---:|---|
| D | 11 | 10 distinct combos (of 24 possible) — 1 repeat |
| E | 5 | Both profiles: 2×p1, 3×p2 |
| F | 8 | Both profiles: 4×p1 (insecure), 4×p2 (secure) |
| G | 6 | All 4 combos: 3×p1/p1, 1×p1/p2, — wait, see exact counts below |

Exact G combo counts observed: `economic_role:p1;future_engagement:p1`=1,
`p1;p2`=1, `p2;p1`=2, `p2;p2`=2 (the rare combo, deliberately over-represented
relative to its ~5.7% population share, since it had only 3 members in the entire
remaining pool).

## 3. Headline results

| Metric | 30-batch | Frozen 10 (v3) |
|---|---:|---:|
| Respondents | 30 | 10 |
| Total recommendations | **102** | 30 |
| Respondents with ≥1 recommendation | **26/30 (86.7%)** | 8/10 (80%) |
| `NO_DEFENSIBLE_RECOMMENDATION` | **4/30 (13.3%)** | 2/10 (20%) |
| Recommendations per respondent (distribution) | 0×4, 3×9, 4×10, 5×7 | 0×2, 2×1, 3×3, 4×4 |
| Evidence-strength distribution | STRONG 34, MODERATE 51, LIMITED 17 | not separately tabulated before; comparable mix observed on spot-check |
| Grounding audit | **92 PASS, 14 PASS WITH CAUTION, 0 FAIL** | 29 PASS, 3 PASS WITH CAUTION, 0 FAIL |
| Category-discipline audit | **243 PASS, 3 PASS WITH CAUTION, 0 FAIL** | 72 PASS, 1 PASS WITH CAUTION, 0 FAIL |
| API calls / retries / timeouts | 30 / **0** / **0** | 10 / 1 / 0 |
| Avg. call duration | 22.0s | 32.0s |
| Cost (this batch) | **$0.3359 (ESTIMATED)** | $0.1018 (ESTIMATED) |

Coverage and decline rates are close to the frozen baseline (86.7% vs. 80% coverage;
13.3% vs. 20% decline) — no dramatic shift in either direction. Grounding CAUTION rate
is somewhat higher in the larger batch (13.2% of rows vs. 9.4%), driven entirely by the
same low-severity word-overlap/paraphrase pattern already documented, not by new issue
types (see §5). Category-discipline CAUTION rate is essentially identical (1.2% vs.
1.4%) — strong evidence the prompt fix generalises beyond the original 10.

## 4. A bug found and fixed in the audit itself (not the model)

The first pass of the grounding audit flagged 1 FAIL: `nysc-3258dc18` / COURSE-005,
"prohibited phrase pattern: 'guaranteed job'". The actual text was: *"No explicit
information about placements, local employer links, or guaranteed job outcomes is
provided in the course text."* — a correct disclaimer, not a violation. The negation cue
("No explicit") was 67 characters before the flagged phrase, just past the audit's
60-character negation-detection window from the previous experiment. **Fixed by
widening the window to 120 characters** in `grounding_audit_v2.py`, then the audit was
re-run (no new API calls — pure re-analysis of already-saved text) against both this
batch and the frozen v3 baseline to confirm no regression. Result: **30-batch grounding
now 92 PASS / 14 CAUTION / 0 FAIL; v3 baseline unchanged at 29/3/0.** This is the second
negation-window false positive found across the two batches — both were audit-tooling
bugs, not model failures, and both are now fixed for future runs.

## 5. Grounding audit — the 14 PASS WITH CAUTION rows

All 14 are the same word-overlap/paraphrase-detection heuristic flagging a
`course_evidence_used` citation whose wording doesn't closely match the source course
text — deliberately lenient-but-flagging, not a fail, because paraphrase is legitimate.
Spot-checked several by hand:
- `nysc-0cba8a68`/COURSE-003, `nysc-8ae4a1d8`/COURSE-001, `nysc-515dbda4`/COURSE-001,
  `nysc-0566257f`/COURSE-001: all legitimate paraphrases of the actual course text
  (verified accurate, not fabricated).
- `nysc-25c345ec`/COURSE-034: an inference flagged for missing hedge-word text despite
  being marked `uncertainty_language_used=True` — the inference compares two
  near-duplicate Refrigeration/AC course records in the corpus (cross-referencing
  COURSE-012 while discussing COURSE-034), the same benign pattern noted for a similar
  case in the earlier v2 experiment.

No new caution *type* appeared beyond what was already characterised in prior runs.

## 6. Category-discipline audit — the 3 PASS WITH CAUTION rows

All 3 are the same low-severity pattern already seen once in the frozen v3 run (the
single `most_important_life_goal`-at-position-3 case): a secondary (non-primary)
citation of an `EDUCATION_AND_EXPERIENCE_CONTEXT` variable given mildly preference-like
phrasing, always at position 3 (tertiary supporting evidence, never the primary driver):

- `nysc-2e8a4c77` / COURSE-049: `activity_while_searching` at position 3.
- `nysc-0a92b28f` / COURSE-005: `edu_status` at position 3.
- `nysc-04134b0d` (decline): `training_type_received` co-occurring with content-judgement
  language in the decline reason — flagged for review, not a confirmed violation (the
  decline itself is correct; this variable's value happening to appear in the same
  paragraph as a field-relevance judgement doesn't establish it caused that judgement).

**Zero instances of the systematic `most_useful_quality_for_job`-style failure that
originally motivated the prompt fix.** The fix's effect held up at 3x the original
sample size.

## 7. Was the corpus-limitation decline (`nysc-4e38db03`) a system failure?

**No — this is the report's most important positive finding.** `nysc-4e38db03` was
selected specifically because they have a clear, unambiguous, STRONG direct-preference
signal: `ideal_sector = "Health, social work, and wellbeing"`, `study_field_preference =
"Science or mathematics"`. Only 2 courses were retrieved for them at all (BM25 correctly
found almost nothing relevant, because **the 84-course V2 corpus has no health,
social-work, or wellbeing course**): National Diploma in Television Program Production,
and the National Diploma in ICT. The model's decline reason explicitly names both
retrieved courses and explains neither teaches the respondent's stated field — a
transparent, correct application of the decision rules even though the respondent's
*own* evidence was strong. This is exactly the "recommendation unsupported by retrieved
courses" and "excessive recommendation behaviour" failure modes the task asked to watch
for — and the system correctly avoided both by declining rather than forcing an
irrelevant match. This is a genuine catalogue-coverage gap (worth flagging to NYSC
separately), not a pipeline defect.

## 8. Were weak-evidence respondents handled appropriately?

Yes, across all four types tested:
- `nysc-b556590a`, `nysc-5242257e` (fully weak/unsure, no usable field signal at all) →
  correctly declined, with reasons explicitly citing the no-substitution rule.
- `nysc-04134b0d` (weak sector but some contextual signal — professional occupational
  class) → correctly declined rather than stretching the contextual signal into a
  content driver.
- `nysc-cab6cf5f` (sector "Not sure" but `job_type_sought`/`training_type_would_help`
  present — a genuine, if partial, direct-preference signal) → **received
  recommendations**, correctly distinguishing "no direct preference at all" from
  "sector unstated but another direct-preference field is." This is a meaningful,
  correct nuance the earlier binary weak/strong framing hadn't explicitly tested.

## 9. Did contextual reasoning remain useful?

Yes, with good examples beyond what the frozen 10 showed:
- `nysc-25c345ec` (has children, low education, ambivalent "stay at home" intent):
  correctly used their genuine `ideal_sector` preference to recommend vocational
  trades courses appropriate to their O/L-level education, and **correctly hedged**
  the caregiving/schedule concern as an uncertainty ("may make weekday full-time
  attendance harder — schedule suitability is uncertain") rather than asserting it as
  a fact — textbook-correct application of the permitted-inference rules on a
  deliberately conflicting-signal case.
- `nysc-49b62c9a` (Education-sector aspirant based in Trincomalee): used their district
  (a legitimate `FEASIBILITY_OR_CONSTRAINT_CONTEXT` variable) to suggest a Tamil-language
  course as secondary, MODERATE-strength support for teaching-related communication
  skills in a Tamil-speaking area — a genuinely useful, non-obvious connection that a
  sector-only filter could never produce, correctly kept secondary to the primary
  Education-sector-and-further-study evidence.

## 10. Any new systematic failure pattern?

**None identified.** Both audits' issue types are consistent in kind and rate with the
frozen baseline (word-overlap paraphrase caution; secondary-citation category caution);
no new failure category appeared across 3x the sample size, and the one prior systematic
issue (opinion-variable misuse) did not recur even once in 246 category-discipline rows.

## 11. API usage and cost

| | 30-batch | Frozen 10 (v3) |
|---|---:|---:|
| Input tokens | 734,777 | 240,942 |
| Cached input tokens | 76,032 | 45,824 |
| Output tokens (incl. reasoning) | 84,669 | 25,936 |
| Reasoning tokens | 9,920 | — (not separately reported before) |
| Total tokens | 819,446 | 266,878 |
| Retries | 0 | 1 |
| Timeouts (hard-timeout triggered) | 0 | 1 (recovered) |

**Cost: $0.3359 (ESTIMATED)** for this batch, from actual recorded token usage against
`gpt-5-mini`'s published list pricing ($0.25/1M input, $2.00/1M output, ~$0.025/1M
cached) — not a live-billed figure.

**Updated per-respondent average: $0.0112** (30-respondent sample, more representative
than the 10-person estimate). Projected costs, all **ESTIMATED**:
- Remaining 322 respondents (362 − 10 − 30 already run): **~$3.61**
- Full 362-respondent cohort (all runs combined): **~$4.05**

---

## Verdict

**A. Coverage/decline behaviour** stayed close to the frozen baseline (86.7% vs. 80%
coverage) with no evidence of drift toward either excessive recommending or excessive
refusal — and correctly declined even a strong-evidence respondent when the corpus
genuinely had no matching course (§7), which is exactly the discipline a larger run
needs.

**B. Grounding quality** held at 0 FAIL across 106 audited items (after fixing a
confirmed audit-tooling bug, not a model issue) — the same clean result as the frozen
baseline, at 3x the scale.

**C. Evidence-category discipline** held at 0 FAIL across 246 audited citations, with
the CAUTION rate essentially unchanged from the frozen baseline (1.2% vs. 1.4%) and zero
recurrence of the original systematic failure — the strongest evidence yet that the
prompt fix generalises.

**D. Contextual reasoning** remained useful and appropriately hedged on genuinely
difficult, conflicting-signal cases that weren't in the original 10.

**E. Operationally**, this was the cleanest run yet: 0 retries, 0 timeouts, faster
average latency than the frozen baseline.

The system is stable across a 3x larger, deliberately harder sample than the frozen
baseline, with no new failure modes and both audits confirming the prior fixes hold.

## READY FOR FULL COHORT RUN
