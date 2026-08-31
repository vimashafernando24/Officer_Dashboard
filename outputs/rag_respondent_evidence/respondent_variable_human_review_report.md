# Respondent-Variable Human-Review Audit

**Purpose:** a focused re-examination of the evidence-policy classifications assigned in
`respondent_variable_policy.csv`, specifically targeting the ambiguities flagged in §8 of
`respondent_evidence_report.md` plus every variable matching the fourteen themes named in this
audit request (household-provider/economic responsibility, household income/financial pressure,
current employment, employment security, contract type/formality, working hours, job-change
intention, previous training, education status, barriers to employment, care/family
responsibilities, motivation/autonomy/competence, social support/networks, future
education/training intention).

**This is a review, not a change.** `respondent_variable_policy.csv` and
`respondent_evidence.jsonl` have **not** been modified. No retrieval, embeddings, LLM calls, or
recommendation logic were built. Every recommendation below is a proposal awaiting your
approval.

**Method:** every variable was re-tested against the definitions given in this audit request —
in particular the distinction between a respondent *explicitly stating* something (a preference,
a circumstance) versus the system *inferring* something plausible-but-unstated from it — and
against the critical rule that correlation or plausible reasoning is never sufficient
justification on its own. 28 variables required a documented decision; the remaining themed
variables (listed in §9) were reviewed and found already correctly and conservatively scoped, so
they are reported briefly rather than audited in full.

---

## 1. Household-provider / time-autonomy: "provider ≠ cannot attend full-time"

The task's own worked example — *"primary household provider does NOT automatically mean cannot
attend full-time"* — applies directly to three variables that were previously marked
drive-eligible on the strength of *plausible* association with a schedule constraint, without any
respondent ever stating that constraint.

| Variable | Branches | Issue |
|---|---|---|
| `primary_earner_status` | all | States an economic ROLE, not a time/schedule fact. |
| `time_use_decision_maker` | G | States who controls the respondent's time, but not what that implies for training attendance. |
| `support_for_engagement` | G | Measures expected support, inconsistently classified relative to every other social-support variable (all of which are already `INDIVIDUAL_CONTEXT_ONLY`). |

**Recommendation for all three:** move to non-driving (`INDIVIDUAL_CONTEXT_ONLY`, or
`FEASIBILITY_OR_CONSTRAINT_CONTEXT` with `may_drive=False`). The legitimate driver of schedule
ranking should be the respondent's own direct answer to the new intake questionnaire's schedule
question (full-time/weekday vs. part-time/weekend), not an inference from these three variables.
They remain available to *explain* a recommendation and to prompt that direct question, but must
not move a ranking score on their own.

---

## 2. Household income and financial pressure: no catalogue-side cost mechanism exists

Eight variables report income, funding, or wage-related facts. The critical rule states this
almost verbatim: *"low household income must NOT automatically mean recommend a shorter course...
unless... the catalogue provides the necessary cost/feasibility information."* **The V2 course
matching dataset (87 courses) has no fee, cost, scholarship, or subsidy field at all.** There is
therefore currently no legitimate mechanism connecting any of these variables to a course
attribute — the classification should track catalogue capability, not merely whether the
respondent answered directly.

| Variable | Branches | Note |
|---|---|---|
| `household_income` | all | Explicit critical-rule example. |
| `household_workers` | all | Structural component of household_income. |
| `household_unemployed` | all | Structural component of household_income. |
| `primary_income_source` | all | No funding-eligibility mechanism exists. |
| `edu_funding_source` | D | Describes *current* education's funding, not the new course's. |
| `monthly_income_band` | F | Personal income, same catalogue gap. |
| `who_paid_training` | F | Historical training-funding fact; should match its already-correctly-scoped siblings (`training_provider`, `training_duration`, `training_type_received`), all `EDUCATION_AND_EXPERIENCE_CONTEXT`, non-driving. |
| `has_minimum_wage` / `minimum_wage_band` | E | A JOB wage floor, not a course attribute — no course-side wage-outcome field exists. |

**One exception:** `income_urgency` (E) *does* have a real matching catalogue field
(`duration_months`), so it is not part of this "no mechanism exists" group — see §3.

**Recommendation:** reclassify all eight to non-driving (`INDIVIDUAL_CONTEXT_ONLY` for the
income/funding/wage group; `EDUCATION_AND_EXPERIENCE_CONTEXT` non-driving for `who_paid_training`
specifically, to match its siblings). Revisit if/when the catalogue gains a documented cost or
wage-outcome field.

---

## 3. `income_urgency` — the one financial variable with a real target field

Unlike the rest of the income group, `income_urgency` ("How urgently do you need to start earning
income?") could legitimately inform a preference for shorter `duration_months` courses — that
field genuinely exists in the catalogue. The risk is not the variable itself but *how* it gets
used: an LLM silently weighting urgency against duration without a documented, explainable rule
is exactly the "plausible-sounding but unsupported reasoning" this audit exists to prevent.

**Recommendation:** keep drive-eligible, but require the future scoring design to encode the
urgency→duration relationship as an explicit, stated rule (visible in generated explanations),
never an implicit LLM inference.

---

## 4. Care/family responsibilities: `has_children` / `num_children`

These were explicitly named as legitimate examples in the original task brief ("relevant...
care constraints where directly answered"), so they are *not* pure proxies — but on reflection
they share the same structural problem as household-provider status: knowing someone has children
does not itself state that they need a part-time or weekend course. It is suggestive, not
declarative.

**Recommendation:** retain the category but set `may_drive=False` for both. They remain strong
candidates to *corroborate* a direct schedule preference and to support explanation text (e.g.
"this respondent has caregiving responsibilities"), but the schedule decision itself should come
from the respondent's own direct answer to the new intake's schedule question.

---

## 5. Working hours / availability: current-job facts are not future-training facts

Four variables describe the respondent's *current job* or *current job-search* availability, and
were previously treated as though they answered a *future training-schedule* question. They do
not — the two commitments are not interchangeable, and the approved intake questionnaire already
asks about training schedule directly (Q3: weekday/full-time vs. weekend/part-time).

| Variable | Branch | Problem |
|---|---|---|
| `usual_hours_per_week` | F | Current job hours ≠ future training availability. |
| `actual_hours_last_week` | F | Same, plus single-week snapshot volatility. |
| `income_hours_preference` | F | A genuine direct preference — but about current-job hours, not course schedule. Category (A) stays correct; drive-eligibility for course scheduling does not. |
| `available_to_start` | E | Availability to start a JOB last week ≠ availability to attend training now. |

**Recommendation:** set `may_drive=False` for all four (for course-schedule purposes
specifically). They remain useful for explanation (e.g. "currently works full-time hours") and as
context that could prompt the direct schedule question, but must not silently substitute for it.

---

## 6. Mobility: no catalogue-side location field exists

`willing_to_relocate` (E) and `willing_to_relocate_f` (F) directly state a real geographic
willingness — but the V2 course catalogue has no district/location field for any of the 87
courses, so there is nothing to legitimately match this against yet.

**Recommendation:** reclassify both to non-driving (`INDIVIDUAL_CONTEXT_ONLY`) until the
catalogue documents course location/delivery-site data. Revisit at that point.

---

## 7. Qualification/education matching: no catalogue-side eligibility field exists

`highest_edu_completed` (all branches) and `qualification_job_match` (F) were flagged as explicit
exceptions in the prior report's policy (drive-eligible despite their category being
`EDUCATION_AND_EXPERIENCE_CONTEXT`, which is otherwise non-driving). On closer review:

- `highest_edu_completed` *could* legitimately gate NVQ-level/minimum-qualification eligibility
  — but the V2 catalogue documents no entry-requirement or minimum-prior-qualification field for
  any course. The connecting rule does not exist yet.
- `qualification_job_match` measures how well the respondent's *current job* uses their
  qualifications — it describes employment quality, not training need, and was over-classified as
  an exception in the original build. It should not have been treated the same as
  `highest_edu_completed`.

**Recommendation:** set `may_drive=False` for both. `highest_edu_completed` should be revisited
once/if the catalogue gains a documented entry-requirement field — at that point it would become
a legitimate, non-proxy eligibility driver, not an inference. `qualification_job_match` should
remain explanation-only regardless.

---

## 8. Barriers to employment: legitimate first-person evidence, but must not select content alone

Four variables are the clearest case of genuine, directly self-reported barrier evidence
(`main_obstacle_finding_work` E, `obstacle_finding_this_job` F, `main_business_obstacle` F,
`reason_not_in_labour_force` G). Unlike the groups above, these are **not** proxies or
topic-mismatches — the respondent is directly naming their own obstacle. The critical rule's
warning here is different: *"employment insecurity must NOT automatically mean this person needs
course X. It may provide context, but programme content should still require relevant
preference/interest/skill evidence."*

`reason_not_in_labour_force` deserves particular care: the frozen clustering report itself found
that removing this variable reproduced the Branch G future-engagement profiles *exactly* (ARI
1.000) — confirming it is genuinely descriptive of circumstance, not a hidden driver of anything.
The same restraint that the clustering methodology applied to it should apply to any future
content-recommendation use.

**Recommendation:** do **not** change the category for any of these four — they are legitimate,
directly-answered evidence. Instead, adopt an explicit **usage-scope rule** at the future scoring
stage: these variables may adjust feasibility/prioritisation and support explanation, but must
**never independently select programme field/content** without corroborating
`DIRECT_PREFERENCE_OR_INTENT` evidence from the same respondent (e.g. a stated `ideal_sector` or
`training_type_would_help` answer). This is a policy/scope decision, not a reclassification.

---

## 9. Themed variables reviewed and found already correctly scoped (no change proposed)

For completeness, every variable matching the fourteen named themes was checked. These were
already conservatively and correctly classified and do not require a decision:

- **Motivation/autonomy/competence** (all single-item SDT-style indicators): `study_motivation_type`,
  `autonomy_in_study`, `competence_in_study_field`, `relatedness_at_institution` (D);
  `work_autonomy`, `competence_growth_at_work`, `relatedness_at_work`, `work_motivation_type`,
  `job_satisfaction`, `insecurity_bothers` (F); `job_search_self_efficacy`,
  `job_search_autonomy_orientation`, `future_planning_orientation` (E); `future_orientation_g`,
  `employment_self_efficacy` (G) — all `INDIVIDUAL_CONTEXT_ONLY`, non-driving. Correct.
- **Social support/networks** (besides `support_for_engagement`, moved in §1):
  `employment_network_quality` (all), `knows_people_in_target_sector`, `network_helpfulness`
  (E), `labour_market_connection` (G), `professional_network_growth` (F) — all
  `INDIVIDUAL_CONTEXT_ONLY`. Correct and consistent.
- **Future education/training intention**: `plans_further_edu`/`plans_further_edu_f`,
  `wants_further_edu`, `expected_highest_edu_d`/`_e`/`_f`/`_g`, `study_field_preference`,
  `training_type_would_help` — all `DIRECT_PREFERENCE_OR_INTENT`, drive-eligible. These are the
  clean, legitimate cases the critical rule contrasts *against*: explicit first-person statements
  of what the respondent wants. Correct.
- **Job-change intention**: `hopes_to_change_job` (F, direct intent) and `reason_wants_to_change`
  (F, elaborates that intent) — `DIRECT_PREFERENCE_OR_INTENT`. Correct; note that neither
  specifies *which* field to change to, so field-selection still requires `ideal_sector`/
  `ideal_work_type` as corroborating evidence, not `hopes_to_change_job` alone.
- **Previous training** (besides `who_paid_training`, moved in §2): `received_training`,
  `training_type_received`, `training_provider`, `training_duration` (F) — all
  `EDUCATION_AND_EXPERIENCE_CONTEXT`, non-driving. Correct.
- **Education status**: `edu_status`, `edu_end_year`, `spell1_activity`/`spell2_activity`,
  `current_activity_status`, `worked_while_studying` — all `EDUCATION_AND_EXPERIENCE_CONTEXT`,
  non-driving. Correct.
- **Current employment / contract type / formality / employment security**:
  `employment_status`, `work_arrangement`, `contract_type`, `sector_formality`,
  `occupational_class`, `enterprise_registered`, `paid_taxes`, `job_security_12months`,
  `union_member`, `enterprise_size`, `has_second_job` — all `EDUCATION_AND_EXPERIENCE_CONTEXT`,
  non-driving (context/explanation only, consistent with the frozen research report's own caution
  that this dimension "describes employment conditions, not respondent worth or employability").
  Correct.

---

## 10. Concise decision table

Only the 28 variables requiring your decision are listed. Full detail for each (exact question,
all twelve audit points) is in `respondent_variable_human_review.csv`.

| VARIABLE | CURRENT CLASS | RECOMMENDED CLASS | ALLOW TO DRIVE RECOMMENDATION? | ALLOW IN EXPLANATION? | MAIN RISK | DECISION NEEDED |
|---|---|---|---|---|---|---|
| `primary_earner_status` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Task's own named forbidden inference (provider ≠ can't attend full-time) | Approve reclassification |
| `time_use_decision_maker` | FEASIBILITY (drive) | FEASIBILITY, drive=False | No | Yes | Infers a schedule constraint not actually stated | Approve drive-flag change |
| `support_for_engagement` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Inconsistent with sibling social-support variables; penalises respondent for family attitude | Approve reclassification |
| `household_income` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | No catalogue cost field — fabricated cost reasoning | Approve reclassification |
| `household_workers` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Same as household_income | Approve reclassification |
| `household_unemployed` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Same as household_income | Approve reclassification |
| `primary_income_source` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | No funding-eligibility mechanism | Approve reclassification |
| `edu_funding_source` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Describes a different (current) programme's funding | Approve reclassification |
| `monthly_income_band` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Same as household_income | Approve reclassification |
| `who_paid_training` | FEASIBILITY (drive) | EDUCATION_CONTEXT, drive=False | No | Yes | Historical fact wrongly treated as live constraint | Approve reclassification |
| `has_minimum_wage` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | No course-side wage-outcome field | Approve reclassification |
| `minimum_wage_band` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Same as has_minimum_wage | Approve reclassification |
| `income_urgency` | FEASIBILITY (drive) | FEASIBILITY (drive), scoped | Yes, via explicit rule only | Yes | Implicit urgency→duration weighting if not made explicit | Approve usage-scope rule |
| `has_children` | FEASIBILITY (drive) | FEASIBILITY, drive=False | No (standalone) | Yes | Task's own named forbidden inference (children ≠ needs part-time) | Approve drive-flag change |
| `num_children` | FEASIBILITY (drive) | FEASIBILITY, drive=False | No (standalone) | Yes | Same as has_children | Approve drive-flag change |
| `usual_hours_per_week` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Current-job hours ≠ future training availability | Approve reclassification |
| `actual_hours_last_week` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Same, plus single-week volatility | Approve reclassification |
| `income_hours_preference` | DIRECT_PREFERENCE (drive) | DIRECT_PREFERENCE, drive=False for schedule | No (for course schedule) | Yes | Topic mismatch: job-hours preference ≠ course-schedule preference | Approve drive-flag change |
| `available_to_start` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Job-start availability ≠ training availability | Approve reclassification |
| `willing_to_relocate` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | No catalogue location field | Approve reclassification |
| `willing_to_relocate_f` | FEASIBILITY (drive) | INDIVIDUAL_CONTEXT_ONLY | No | Yes | Same as willing_to_relocate | Approve reclassification |
| `highest_edu_completed` | EDUCATION_CONTEXT (drive, exception) | EDUCATION_CONTEXT, drive=False | No | Yes | No catalogue entry-requirement field yet | Approve drive-flag change |
| `qualification_job_match` | EDUCATION_CONTEXT (drive, exception) | EDUCATION_CONTEXT, drive=False | No | Yes | Describes current job quality, not training need | Approve drive-flag change |
| `main_obstacle_finding_work` | FEASIBILITY (drive) | FEASIBILITY (drive), scoped | Yes, feasibility only, not content | Yes | Barrier used to auto-select programme content without preference evidence | Approve usage-scope rule |
| `obstacle_finding_this_job` | FEASIBILITY (drive) | FEASIBILITY (drive), scoped | Yes, feasibility only, not content | Yes | Same, plus historical framing | Approve usage-scope rule |
| `main_business_obstacle` | FEASIBILITY (drive) | FEASIBILITY (drive), scoped | Yes, feasibility only, not content | Yes | Same, plus small sample (n=14) | Approve usage-scope rule |
| `reason_not_in_labour_force` | FEASIBILITY (drive) | FEASIBILITY (drive), scoped | Yes, feasibility only, not content | Yes | Highest-stakes content-substitution risk for inactive youth | Approve usage-scope rule |
| `age_group` | INDIVIDUAL_CONTEXT_ONLY | No change | No | Yes | None currently; revisit only if catalogue gains age-eligibility data | Confirm no action needed |

**Nothing in this table has been applied.** `respondent_variable_policy.csv` and
`respondent_evidence.jsonl` remain exactly as originally built. Awaiting your decision on each row
before any file is modified.
