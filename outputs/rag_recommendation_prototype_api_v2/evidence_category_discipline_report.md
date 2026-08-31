# Evidence-Category-Discipline Audit Report

**Scope:** a new, additive mechanical check on top of the existing grounding audit — does
each cited respondent variable get *used* in a way consistent with its evidence-policy
category (`outputs/rag_respondent_evidence/respondent_variable_policy.csv`), not merely
whether the variable/value exists and matches what the respondent actually answered
(the existing audit already checks that part and still passes).

**No retrieval, corpus, respondent selection, model, or knowledge base was touched.
No new API calls were made.** This is pure re-analysis of the two already-saved JSONL
files (`outputs/rag_recommendation_prototype_api_v2/api_test_recommendations.jsonl`,
the gpt-5-mini run; `outputs/rag_recommendation_prototype_api/api_test_recommendations.jsonl`,
the gpt-4o-mini run — audited too since it's one of the files this task named, and
because it makes the "also check decline reasons" requirement testable: the gpt-5-mini
run has zero declines). **No saved recommendation file was modified.**

---

## 1. Method

For each `direct_respondent_evidence_used` citation in a recommendation, this audit:

1. Looks up the variable's authoritative category in the **current, unmodified**
   `respondent_variable_policy.csv` (the human-review recommendations from an earlier
   audit were never applied to this file, so it still reflects the original build).
2. Infers the **role** the LLM actually gave that citation — PREFERENCE-framing
   (implies the respondent wants/prefers this, i.e. driving programme content
   selection), FEASIBILITY-framing (schedule/format/practical-combination language),
   EXPERIENCE-framing (builds-on-background language), or unclear — from simple,
   transparent keyword patterns in the citation's own `relevance` text.
3. Uses list position (1 = first-listed) as a proxy for "primary/leading" evidence,
   consistent with the observed pattern that the model lists its strongest
   justification first.
4. Applies the five category rules given in this task verbatim (§2 below) to produce
   PASS / PASS WITH CAUTION / FAIL.

**This is a mechanical pattern-match, not semantic understanding.** It can misclassify
novel phrasing. Every FAIL and CAUTION reported below was manually re-read against the
actual JSONL text before being included in this report's conclusions — the mechanical
flags matched what a human read confirms, with one noted exception of ambiguous
confidence (§4).

## 2. Rules applied

| Category | Rule |
|---|---|
| A. DIRECT_PREFERENCE_OR_INTENT | May drive content/field selection — always PASS regardless of role/position. |
| B. FEASIBILITY_OR_CONSTRAINT_CONTEXT | May support feasibility reasoning only; FAIL if it is the primary (position-1) justification for content match, PASS WITH CAUTION if secondary. |
| C. EDUCATION_AND_EXPERIENCE_CONTEXT | May support "builds on experience" reasoning; FAIL if framed as a stated preference at position 1 without an explicit respondent preference, PASS WITH CAUTION if secondary. |
| D. INDIVIDUAL_CONTEXT_ONLY | Explanation only; FAIL if it is the primary reason with preference-like framing, PASS WITH CAUTION if merely primary-position (regardless of framing) or preference-framed-but-secondary. |
| E/F. PROTECTED_OR_PROXY_DO_NOT_USE / TECHNICAL_DO_NOT_USE | FAIL immediately if cited at all — no role nuance. |

Decline (`NO_DEFENSIBLE_RECOMMENDATION`) reasons were separately scanned for co-occurrence
of a B/C/D-category answer's exact value text with content/field-relevance judgement
language, flagged PASS WITH CAUTION (not FAIL — text co-occurrence alone isn't proof of
misuse for free-text reasons).

## 3. Headline results

| Model | Rows audited | PASS | PASS WITH CAUTION | FAIL |
|---|---:|---:|---:|---:|
| gpt-5-mini (35 recommendations, 0 declines) | 105 citation rows | 95 | 6 | **4** |
| gpt-4o-mini (4 recommendations, 8 declines) | 18 rows | 18 | 0 | 0 |

**4 confirmed category violations, all in the gpt-5-mini run.** The gpt-4o-mini run has
zero — consistent with it citing very little evidence at all given how conservative it
was.

## 4. The violations, in detail

**The dominant, systematic pattern: `most_useful_quality_for_job` treated as a stated
preference.** This variable ("Which quality do you think is most useful for finding a
good job?") is a general opinion/belief question — its own policy-file reason states
*"Opinion, not an actionable personal preference"* — and is correctly categorised
`INDIVIDUAL_CONTEXT_ONLY`. It accounts for **8 of the 10 flagged rows** (3 of 4 FAILs, 5
of 6 CAUTIONs), across **4 different respondents**:

| Respondent | Course | Strength | Position | Status |
|---|---|---|---|---|
| `465701ee` | COURSE-006 (ICT Diploma) | **STRONG** | 1 | **FAIL** |
| `33aaf2f7` | COURSE-006 (ICT Diploma) | **STRONG** | 1 | **FAIL** |
| `33aaf2f7` | COURSE-053 (Computer Applications Assistant) | MODERATE | 1 | **FAIL** |
| `33aaf2f7` | COURSE-022 (Computer Network Technician) | MODERATE | 1 | CAUTION |
| `33aaf2f7` | COURSE-001 (Freelancer Web Design) | LIMITED | 1 | CAUTION |
| `acaf63b5` | COURSE-006 (ICT Diploma) | MODERATE | 1 | CAUTION |
| `0c6c34a2` | COURSE-034 (Refrigeration & AC) | MODERATE | 2 | CAUTION |
| `0c6c34a2` | COURSE-042 (Automobile Electrician) | MODERATE | 2 | CAUTION |

Two secondary instances of a different variable:
- `33aaf2f7` / COURSE-006 also cites `edu_status` (EDUCATION_AND_EXPERIENCE_CONTEXT) at
  position 2 with preference-like framing ("aligns with that trajectory") — CAUTION.
- `33aaf2f7` / COURSE-008 (Computer Hardware Technician) cites `occupational_class`
  (EDUCATION_AND_EXPERIENCE_CONTEXT: "currently works in Technical work (IT technician,
  lab technician, etc.)") at position 1 with the phrase "aligns with that occupational
  class" — flagged **FAIL**. On manual review this one is lower-confidence than the
  others: `occupational_class` genuinely is a legitimate *experience*-based signal for
  this specific course (the respondent already works in a technical occupation, a real
  "builds on existing background" connection), and "aligns with" is ambiguous between
  preference-framing and experience-framing in this context. This FAIL should be read as
  **borderline/needs-human-judgment**, not as clear-cut as the other three.

## 5. The severe case: `nysc-33aaf2f7-dc2a-4530-ae73-3bfdf5be63ab`

This respondent's **entire 5-course recommendation set is affected**, and the underlying
data shows why this matters beyond a labelling technicality. Their actual
`DIRECT_PREFERENCE_OR_INTENT` answers are:

```
ideal_sector          = Wholesale, retail, or repair
ideal_work_type        = Work for a multinational or large private company
reason_wants_to_change  = To get better career prospects and advancement
plans_further_edu_f     = Yes
willing_to_relocate_f   = Yes — to another country
```

**None of these name ICT, computing, or any technical field.** Yet all five recommended
courses are ICT courses (ICT Diploma, Computer Hardware Technician, Computer Network
Technician, Computer Applications Assistant, Web Design/Freelancer), and for four of the
five, the *only* field-specific justification is `most_useful_quality_for_job = "IT and
digital skills"` — the misclassified opinion variable. Once that variable is discounted,
COURSE-006, COURSE-022, COURSE-053, and COURSE-001 have **no remaining
content-specific evidence connecting them to this respondent's stated interests at
all** — the other citations used (`reason_wants_to_change`, `willing_to_relocate_f`,
`ideal_work_type`, `plans_further_edu_f`) are all generic and would apply to almost any
course. COURSE-008 (Computer Hardware Technician) is the one exception with a plausible
independent basis (`occupational_class` showing genuine prior technical-work
experience), though its own citation is also flagged as ambiguous (§4).

This respondent's stated sector (Wholesale, retail, or repair) has no strong course
match in the 84-course corpus, which likely explains why the model reached for a
tangentially-related opinion answer instead of returning
`NO_DEFENSIBLE_RECOMMENDATION` or a much shorter, better-anchored list — exactly the
risk flagged in the prior report's §8.2 (watch for the under-recommendation fix
becoming an over-recommendation bias).

## 6. Should any STRONG recommendations be downgraded?

**Yes, two:**

| Respondent | Course | Current rating | Recommendation |
|---|---|---|---|
| `465701ee` | COURSE-006 | STRONG | **Downgrade to LIMITED** (or below) — its only field-specific evidence is the misclassified opinion variable; the STRONG rating is not earned by legitimate DIRECT_PREFERENCE_OR_INTENT evidence. |
| `33aaf2f7` | COURSE-006 | STRONG | **Downgrade to LIMITED** (or below) — same reason, compounded by directly contradicting the respondent's own stated sector (Wholesale/retail/repair). |

## 7. Should any recommendations be invalidated?

**Yes:** `nysc-33aaf2f7-dc2a-4530-ae73-3bfdf5be63ab`'s recommendation set (COURSE-006,
COURSE-022, COURSE-053, COURSE-001 — 4 of its 5 courses) should be treated as
**invalidated pending regeneration**, not merely downgraded — they rest on evidence that
both fails the category rule and, once discounted, leaves no field-specific connection
to this respondent's actual stated interests, which point to a different sector the
current 84-course corpus may simply not serve well. COURSE-008 for the same respondent
is a judgment call (§4) — defensible on experience grounds but should be re-justified
with `occupational_class` framed correctly (experience/background, not preference) if
kept.

No other respondent's recommendation set requires invalidation; `acaf63b5` and
`0c6c34a2`'s flagged citations are secondary (not the sole or primary basis) and each of
those recommendations retains independent, correctly-used DIRECT_PREFERENCE_OR_INTENT
grounding from other citations.

## 8. Decline reasons

The gpt-5-mini run has **zero** declines (0/10), so there was nothing to check there.
The gpt-4o-mini run's 8 declines were scanned under the same co-occurrence heuristic:
**no category-discipline concerns found** — the one issue previously known in that run
(the `nysc-00e2c251` self-contradicting eligibility claim) is a different failure mode,
already caught by the existing grounding audit, and is unaffected by this check.

## 9. Should the prompt be updated?

**Yes — this is a systematic pattern (4 respondents, 8 of 10 flagged citations sharing
one root cause), not an isolated one-off, and should be fixed at the prompt level
before any larger run.** Recommended addition to `context_pack_v2.GOVERNANCE_INSTRUCTIONS`:

> Some Section 1 answers are *opinions about the job market in general* (e.g. "which
> quality do you think is most useful for finding a good job?"), not statements of what
> the respondent personally wants to study or do. These are labelled INDIVIDUAL CONTEXT
> ONLY in Section 1 for exactly this reason. Do not treat a general-opinion answer as
> equivalent to the respondent naming a preferred subject, sector, or skill area — only
> a DIRECT PREFERENCE / INTENT-labelled answer (e.g. `ideal_sector`, `study_field_preference`,
> `training_type_would_help`) may independently justify a content/field match. If the
> respondent has stated no clear direct field/sector preference at all, that is itself
> a reason to lean toward a shorter list or `NO_DEFENSIBLE_RECOMMENDATION`, not a reason
> to substitute an opinion-question answer for a preference.

This directly targets the failure mode found (opinion-as-preference), while preserving
the rest of the rebalanced prompt that successfully fixed the under-recommendation
problem in the prior experiment.

## 10. What this does *not* undo

The prior experiment's core finding stands: retrieval was unaffected by any of this
(held constant, unaudited by this check), and 6 of the 10 respondents' recommendation
sets (`3a86d117`, `a04f7d96`, `131a2b60`, `346623df`, `00e2c251`, `55bdfdcc`) have **zero**
category-discipline issues at all, including the previously-documented recovery of every
course the gpt-4o-mini run had inaccurately declined. The problem found here is narrower
and specific: one opinion-type variable being over-used as if it were a stated
preference, concentrated in weak-evidence/off-corpus cases where the model reached for
a substitute justification rather than declining or shortening the list.

---

## NOT READY

Two respondents in the gpt-5-mini run (`465701ee`, `33aaf2f7`) contain confirmed
category-discipline violations serious enough to require a downgrade (STRONG→LIMITED,
§6) and, for `33aaf2f7`, invalidation of most of its recommendation set (§7). The root
cause is systematic (one mislabelled-as-preference variable, 4 respondents affected) and
has a clear, targeted prompt fix (§9) that has not yet been applied or tested. Before any
larger validation batch: apply the §9 prompt addition, re-run these same 10 respondents
(no new respondents, no retrieval changes) to confirm the fix resolves the pattern
without reintroducing the original under-recommendation problem, then re-run this same
evidence-category-discipline audit against the new output.
