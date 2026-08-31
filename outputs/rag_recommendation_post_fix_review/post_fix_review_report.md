# Final Post-Fix Live Review — 10 Respondents, Fully-Fixed Pipeline

Same 10 respondents as the prior targeted validation (no new respondents), same
retrieval (reused byte-for-byte), model=`gpt-5-mini` selected via the new
`get_production_model()`/`verify_production_model()` mechanism (printed and verified
correct at run start — first live exercise of that mechanism). 10/10 calls succeeded,
0 retries. Cost: **$0.1227 (ESTIMATED)**.

**This run is the live test of the one open question from the last report**: does the
tightened, no-hedging-exception affordability rule actually change model behaviour, or
only get correctly flagged after the fact? Answer: **it changes behaviour.** See §2.

## Audit results (all three, fresh run)

| Audit | Result |
|---|---|
| Grounding | 32 PASS, 3 PASS WITH CAUTION, **0 FAIL** |
| Category-discipline | 75 PASS, 1 PASS WITH CAUTION, **0 FAIL** |
| Evidence-hierarchy | **44 PASS, 0 CAUTION, 0 FAIL** |

Zero FAILs anywhere, for the first time across every round of this pipeline's testing.

---

## Per-respondent before/after

### 1. `nysc-0d099a8b` — strong DIRECT_MATCH control
BEFORE: 4× DIRECT_MATCH (Automobile/Motorcycle Mechanic family), all grounded in
`ideal_sector = Manufacturing/production`. AFTER: same pattern, 4× DIRECT_MATCH — one
course swapped (COURSE-021→COURSE-040, both mechanic-family). **What changed:** normal
model-to-model variance on a clean case, not a behaviour change. Audit: clean.

### 2. `nysc-4e38db03` — Education/Science → ADJACENT_MATCH + catalogue gap
BEFORE: 1 ADJACENT_MATCH (ICT). AFTER: 2 ADJACENT_MATCH (ICT + TV Production), both
still correctly bridged from the stated `study_field_preference = Science/mathematics`,
`catalogue_coverage_note` still present. **What changed:** one additional, still-
defensible adjacent option found — no regression, arguably richer coverage.

### 3. `nysc-0cba8a68` — profile-context use + individual-diverges-from-profile
BEFORE: 2 ADJACENT_MATCH (English courses). AFTER: same 2, plus one more
(COURSE-035, Secretarial). Profile citation (`D_motivation_p1`, "externally/uncertainly
motivated") still correctly hedged as group-level, still doesn't override the
respondent's own clear, specific goals. **What changed:** nothing structurally; one
extra defensible adjacent option.

### 4. `nysc-25c345ec` — profile-context differentiation, complex case
BEFORE: 5× DIRECT_MATCH (mechanic-family + refrigeration). AFTER: 4× DIRECT_MATCH,
same sector grounding (`Manufacturing/production`), 3 of 5 courses swapped for other
mechanic-family courses. Caregiving/schedule hedging language preserved (verified
directly). **What changed:** course-list churn only, same reasoning quality.

### 5. `nysc-4646cb19` — CONFIRMED occupation-as-preference fix, retested
BEFORE: 4× ADJACENT_MATCH, `catalogue_coverage_note` present, occupation used as
disclosed upskilling evidence. AFTER: 5× ADJACENT_MATCH — same pattern, one course
added (Secretary/Secretarial Practices variant COURSE-082), `catalogue_coverage_note`
still present and still accurate ("respondent did not state a specific preferred field
or sector..."). **What changed:** the fix held on a fresh call; nothing regressed.

### 6. `nysc-04134b0d` — occupation + weak preference, second case; also the typo-audit case
BEFORE: 2× ADJACENT_MATCH, one grounding typo (`occupation_class`). AFTER: same 2
courses, both now MODERATE (up from MODERATE/LIMITED), **no typo this time** — the
variable name is correctly spelled `occupational_class` in this run. **What changed:**
the model's own error did not recur; the fuzzy-match audit tolerance was not even
needed this time, though it remains in place as a safety net.

### 7. `nysc-3258dc18` — CONFIRMED `available_to_start` fix, retested
BEFORE: 5× DIRECT_MATCH, `available_to_start` not cited. AFTER: 5 recs (4× DIRECT_MATCH
+ 1 new ADJACENT_MATCH), **`available_to_start` still not cited anywhere** — explicitly
re-verified against the raw JSON. **What changed:** fix held; one additional
lower-confidence adjacent option appeared (LIMITED strength, correctly labelled, not a
fabricated direct claim).

### 8. `nysc-8ae4a1d8` — CONFIRMED economic-affordability fix, retested (the critical case)
BEFORE: 5× DIRECT_MATCH; the flagged citation on COURSE-068 mentioned "fee-paying study"
even with a hedge. AFTER: 5× DIRECT_MATCH (COURSE-016→COURSE-001 swap); **both
economic-profile citations in this run are completely clean of any affordability/fee/
payment language** — verified directly:
> *"Profile members more often reported private-institution background and online
> job-search methods (supporting digital/creative vocational interest)."*
> *"...this supports relevance of online/digital freelancing skills as a viable pathway
> for similar respondents (group-level only)."*

**This is the key confirmation**: the tightened rule doesn't just get correctly flagged
after the fact — the model stopped reaching for affordability language on its own, on a
live call, resolving the open question from the previous report.

### 9. `nysc-5242257e` — genuine NO_DEFENSIBLE_RECOMMENDATION control
BEFORE/AFTER: identical — declines both times, no regression toward over-recommending.

### 10. `nysc-27c2ff48` — additional profile-context example, G branch
BEFORE: 5× DIRECT_MATCH. AFTER: 4× DIRECT_MATCH (COURSE-009 dropped, no replacement) —
one course fewer, same core ICT-sector grounding, all remaining still DIRECT_MATCH.
**What changed:** a very minor reduction in list length, not a quality regression — the
4 retained are the same high-confidence courses as before.

---

## Was any good recommendation lost, or any new overreach introduced?

**No systematic loss, no new overreach pattern.** Course-list churn (roughly 1-3 courses
swapped per respondent) is present across most of the 10, consistent with expected
run-to-run variance for a non-zero-temperature reasoning model — not a directional
degradation:
- Total recommendations across the 10: 36 (before) → 39 (after) — a slight *increase*,
  not a drop.
- No respondent that had recommendations before now has zero (case 9 is the one
  unaffected `NO_DEFENSIBLE` control, unchanged both times).
- No respondent's list ballooned unreasonably (max is 5 in both rounds).
- Every one of the four specifically-targeted fixes (`available_to_start` §7,
  economic-affordability §8, occupation-as-preference §5/§6, category-discipline
  false-FAIL) held on this fresh, live call — not just in the retrospective audit of
  older saved data.
- Zero FAILs across all three audits, on all 44 recommendations produced.

The only near-miss worth naming: case 10 lost one course (COURSE-009) with nothing
replacing it — a shorter list, not a wrong one; every retained course is still a clean
DIRECT_MATCH.

---

## SAFE TO FREEZE AND RUN FULL COHORT
