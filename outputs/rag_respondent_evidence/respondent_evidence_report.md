# Respondent Evidence Layer — Build Report (RAG Step 3)

**Purpose of this build:** construct source (1) of the three evidence sources the RAG
recommendation system will eventually reason over — the respondent's own actual survey
answers — and link it safely to source (2), the frozen profile membership(s). **No survey,
clustering, profiling, course, or RAG-knowledge file was modified.** No embeddings were
created, no LLM was called, and no course recommendation logic was written.

---

## 1. Respondents represented

| Branch | Expected strict cohort | Respondents in `respondent_evidence.jsonl` |
|---|---|---|
| D | 191 | 191 |
| E | 34 | 34 |
| F | 81 | 81 |
| G | 56 | 56 |
| **Total** | **362** | **362** |

All 362 records match the frozen strict-cohort sizes exactly. No reclustering, recomputation,
or reassignment was performed — every profile membership was read directly from the seven
frozen `*_consensus_assignments.csv` files produced by the original clustering notebooks.

---

## 2. Where the data came from, and a data-integrity issue that had to be resolved first

Two respondent-ID schemes exist in this project's outputs:

- An older **ObjectId-style** scheme (e.g. `69fac94d4a154e3795d7a181`), used in the general
  `outputs/nysc_survey_*` master/analysis-ready files (392 respondents).
- The **frozen `nysc-<uuid>` scheme** actually used by the clustering and post-cluster
  profiling stage (363 "new-structure" respondents, one of which was later excluded for a
  Branch F path-integrity issue, leaving the 362-respondent strict cohort).

Both ID schemes turned out to coexist **within the same file**:
`outputs/nysc_survey_cleaned_values.csv` and `outputs/nysc_survey_cleaned_labels.csv` each
contain 392 rows, of which exactly 363 use the `nysc-` scheme — and those 363 rows' branch
distribution (D=191, E=34, F=82, G=56) matches the clustering report's "new-structure" cohort
exactly. This was verified before use, not assumed:

- The `nysc-` respondent_id sets in all three Branch D assignment files are **identical**
  (same 191 IDs in the motivation, economic, and educational-cultural models).
- The `nysc-` respondent_id sets in both Branch G assignment files are **identical** (same 56
  IDs).
- The Branch F assignment file's 81 IDs are a strict subset of the 82 `nysc-`-scheme Branch F
  rows in the cleaned survey data; the one respondent present in the data but absent from the
  frozen assignment is `nysc-d7da89a3-4c8d-4e5a-83ff-b2793774fdce` — this matches the report's
  statement that "one invalid employed-path record was excluded."

This respondent was therefore **excluded from `respondent_evidence.jsonl`**: they have no
frozen profile membership to link, and inventing one would violate the "do not recompute
assignments" instruction. This is the only respondent record that could not be linked safely
(see §7).

Source files used (all read-only):

| File | Role |
|---|---|
| `outputs/nysc_survey_cleaned_values.csv` | Coded survey answers (363 `nysc-`-scheme rows used) |
| `outputs/nysc_survey_cleaned_labels.csv` | Human-readable answer text, joined 1:1 by `respondent_id` |
| `outputs/nysc_survey_feature_manifest.csv` | 131-variable manifest: type, applicable branch, question text |
| `outputs/nysc_survey_missingness.csv` | Cohort-wide (392-respondent) per-variable missingness aggregate, used only in the policy audit, not per-respondent |
| `outputs/final_cluster_profile_comparison_summary.csv` | Source of the 21 documented variable→gateway routing relationships reused here for missingness classification |
| `outputs/branch_d_motivation_consensus/motivation_consensus_assignments.csv` | D motivation profile membership |
| `outputs/branch_d_economic_resources_clusters/economic_consensus_assignments.csv` | D economic profile membership |
| `outputs/branch_d_educational_cultural_capital_clusters/educational_cultural_consensus_assignments.csv` | D educational/cultural profile membership |
| `outputs/branch_e_all_dimensions_clusters/e4/consensus_assignments.csv` | E learning-orientation profile membership |
| `outputs/branch_f_employment_security_clusters/employment_security_consensus_assignments.csv` | F employment-security profile membership |
| `outputs/branch_g_household_economic_resources_clusters/household_economic_consensus_assignments.csv` | G economic-role profile membership |
| `outputs/branch_g_inactivity_pathway_future_engagement_clusters/pathway_engagement_consensus_assignments.csv` | G future-engagement profile membership |

---

## 3. Profile memberships linked

| Branch | Retained models | Expected memberships/respondent | Result |
|---|---|---|---|
| D | Motivation; Economic resources; Educational/cultural | 3 | 191/191 respondents have exactly 3 |
| E | Education usefulness/further-learning orientation | 1 | 34/34 respondents have exactly 1 |
| F | Employment security and formality | 1 | 81/81 respondents have exactly 1 |
| G | Household economic role; Future engagement | 2 | 56/56 respondents have exactly 2 |

Total membership links written: 191×3 + 34×1 + 81×1 + 56×2 = **916**. No respondent was
collapsed into a single synthetic profile — every membership is stored as its own object with
`model_id`, `retained_dimension`, `profile_id`, and `profile_label`, exactly as specified.

---

## 4. Variable evidence-policy audit

All **171** columns present in the cleaned survey data (131 manifest variables + 30 additional
substantive conditional/follow-up variables found in the data but absent from the manifest +
10 technical/system fields) were individually classified. Full detail, one row per variable,
is in `respondent_variable_policy.csv`.

| Evidence category | Variables | May drive ranking | May support explanation only |
|---|---:|---|---|
| A. DIRECT_PREFERENCE_OR_INTENT | 20 | Yes | Yes |
| B. FEASIBILITY_OR_CONSTRAINT_CONTEXT | 29 | Yes | Yes |
| C. EDUCATION_AND_EXPERIENCE_CONTEXT | 75 | No (context only, except `highest_edu_completed` and `qualification_job_match`, marked drive-eligible as they are directly answered qualification facts) | Yes |
| D. INDIVIDUAL_CONTEXT_ONLY | 31 | No | Yes |
| E. PROTECTED_OR_PROXY_DO_NOT_USE | 6 | No | No |
| F. TECHNICAL_DO_NOT_USE | 10 | No | No |
| **Total** | **171** | | |

The 6 PROTECTED_OR_PROXY variables are: `gender`, `marital_status`, `father_edu`, `mother_edu`,
`father_occ`, `mother_occ` — `father_edu`/`mother_edu`/`father_occ`/`mother_occ` match the
task's own "family-background proxies" example exactly; `gender` matches the task's own example
exactly; `marital_status` was added because, unlike `has_children`/`num_children` (which state
an actual care constraint and were classified as feasibility context), marital status on its own
states no constraint and functions only as a family/social-status proxy.

The 10 TECHNICAL_DO_NOT_USE fields are: `respondent_id`, `submitted_at`, `entry_branch`,
`branch`, `branch_routing_source`, `branch_changed`, `branch_path_disagreement`,
`branch_integrity_issue`, `feature_count`, `smoke_test`.

### Branch-specific variable availability

Because Branches D/E/F/G each have their own conditional question set (plus ~40 shared
all-branch variables), the number of *applicable* variables differs by branch:

| Branch | Applicable variables (incl. technical) | A | B | C | D | E(protected) | F(technical) |
|---|---:|---:|---:|---:|---:|---:|---:|
| D | 74 | 5 | 11 | 28 | 14 | 6 | 10 |
| E | 87 | 8 | 17 | 31 | 15 | 6 | 10 |
| F | 112 | 8 | 18 | 53 | 17 | 6 | 10 |
| G | 66 | 5 | 13 | 20 | 12 | 6 | 10 |

Branch F has the largest applicable variable set (112) because it carries both the common
all-branch questions and the largest branch-specific block (current-employment detail,
business/self-employment sub-branch questions, and training-history follow-ups).

---

## 5. Missingness and structural-N/A handling

Every applicable variable, for every respondent, was classified into exactly one of five
states — the record never collapses a routing skip into "No," and no answer is ever inferred
from another variable's content:

| Status | Meaning | How it was determined |
|---|---|---|
| `answered` | The respondent actually answered this question. | Non-blank value in both the coded and labelled survey files. |
| `prefer_not_to_say` | The respondent was offered and chose an explicit refusal option. | Label text matched `"prefer not to say"` (case-insensitive) — a real answer choice, not a blank. |
| `structural_na_branch` | The question is not part of this respondent's branch questionnaire at all. | The manifest's own `applicable_branch` field for that variable does not include the respondent's branch. Deterministic — no content was inferred. |
| `conditional_routing_linked` | The field is blank *and* is a documented conditional follow-up of another variable. | Matched against the 21 variable→gateway relationships already documented in the frozen post-cluster comparison table (e.g. `work_while_study_type` depends on `worked_while_studying`; `who_paid_training` depends on `received_training`). |
| `ordinary_missing` | The field is blank, is applicable to this respondent's branch, and has no documented gateway. | Reported as simply missing — no reason is asserted, because none is independently documented. |

**Important methodological choice:** for `conditional_routing_linked` fields, the record stores
the gateway variable's name *and the respondent's own actual recorded answer to that gateway
variable* (e.g. `"gateway_variable": "wants_further_edu", "gateway_variable_recorded_answer":
"Not sure yet"`) rather than asserting whether that answer "should" have triggered a skip. This
was a deliberate choice: the 21 gateway relationships are documented only as *which* variable
depends on *which* other variable, not always the exact triggering condition for every category
value (e.g. `employment_status` gates different follow-ups differently depending on
self-employed vs. wage-worker category). Asserting the exact trigger logic myself would risk
violating the instruction against inferring from another variable unless the relationship is
explicitly deterministic in the frozen design. Surfacing the real recorded fact and letting the
downstream reasoning system evaluate it is the safer, fully faithful choice.

`missingness_notes` in each JSONL record carries this detail only for non-`answered` fields (to
avoid duplicating the same information already tagged inline in each evidence category), giving
an auditable trail without bloating every record with restated "answered" markers.

---

## 6. Excluded/protected variables — audit trail

Rather than silently dropping PROTECTED_OR_PROXY / TECHNICAL variables, every record carries an
`excluded_fields_present` list naming which of those variables the respondent actually answered
(status only — `answered` or `prefer_not_to_say` — no value is copied into this list). This
makes it possible to audit, per respondent, exactly what protected data existed and was
deliberately withheld from the four usable evidence categories, without that data ever being
exposed inside `direct_preference_or_intent`, `feasibility_or_constraint_context`,
`education_and_experience_context`, or `individual_context_only`.

---

## 7. Linkage validation results

`respondent_profile_linkage_audit.csv` contains one row per of the 362 linked respondents,
comparing `expected_membership_count` (3/1/1/2 by branch) against `actual_membership_count`.

**Result: 362/362 = OK. Zero mismatches.**

**Respondent records that could not be linked safely:** exactly one —
`nysc-d7da89a3-4c8d-4e5a-83ff-b2793774fdce` (Branch F). This respondent has full survey answers
in the cleaned data but no frozen profile assignment (the report's documented "one invalid
employed-path record" exclusion). It was correctly **omitted** from `respondent_evidence.jsonl`
and from the linkage audit, rather than given a fabricated or zero-length membership list.

---

## 8. Ambiguities flagged for human review

- **`highest_edu_completed` and `qualification_job_match`** were classified as
  EDUCATION_AND_EXPERIENCE_CONTEXT but marked `may_drive_recommendation = True` (unlike the rest
  of that category), because they are directly answered qualification facts that a course-eligibility
  rule could legitimately use. A domain reviewer should confirm this is the intended treatment
  before the scoring stage relies on it.
- **`age_group`** was placed in INDIVIDUAL_CONTEXT_ONLY rather than
  FEASIBILITY_OR_CONSTRAINT_CONTEXT or PROTECTED_OR_PROXY_DO_NOT_USE. Age could plausibly gate
  course eligibility (many youth programmes have age bands), but the current NYSC course
  dataset (`nysc_course_matching_dataset.csv`) has no documented age-eligibility field, so there
  is no legitimate rule to attach it to yet. This should be revisited once/if course-level age
  eligibility is documented.
- **`marital_status`, `spouse_activity`, `age_first_married`, `moved_from_origin`,
  `move_reason`, `edu_min_for_decent_job`, `most_important_life_goal`,
  `most_useful_quality_for_job`** sit near a genuine category boundary (context vs. proxy vs.
  feasibility). The reasoning for each specific placement is recorded in
  `respondent_variable_policy.csv`'s `reason` column; a domain/ethics reviewer should sanity-check
  these borderline calls before the scoring stage is built.
- **Conditional-routing coverage is partial.** Only 21 variable→gateway relationships are
  documented in the frozen research outputs and reused here. Several other clearly-conditional
  variables in the raw data (e.g. `spell2_*`, `has_job_to_return`, `reason_temp_absence`) have no
  documented gateway and are therefore reported as `ordinary_missing` even though a routing
  explanation plausibly exists. This is a conservative under-statement (never a false
  structural-N/A claim), but a reviewer with access to the original survey skip-logic could tighten
  it further.

---

## READINESS FOR RAG RECOMMENDATION

The next stage needs three components. Status of each, as of this build:

1. **Respondent-level evidence** — ✅ **Ready.** `outputs/rag_respondent_evidence/respondent_evidence.jsonl`
   holds one record per each of the 362 frozen-cohort respondents, with actual survey answers
   (not just clustering variables) classified into an auditable evidence policy, correct
   missingness/routing distinctions, and frozen profile memberships explicitly linked by
   `model_id`/`retained_dimension`/`profile_id`/`profile_label` — with zero group-level
   percentages copied into any individual record.

2. **Frozen profile knowledge** — ✅ **Ready** (built in the prior stage). 17 full-text documents
   under `outputs/rag_profile_knowledge/documents/`, one per retained profile, indexed by
   `outputs/rag_profile_knowledge/profile_document_index.csv`. The `model_id` + `profile_id`
   values stored in every respondent record's `frozen_profile_memberships` match this index's
   `model` + `profile_id` columns exactly, so retrieval can join the two directly.

3. **Full-text NYSC course knowledge** — ✅ **Present.** 87 course text documents under
   `outputs/rag_course_knowledge/raw_course_text/`, indexed by
   `outputs/rag_course_knowledge/raw_course_text_index.csv`, covering all 87 catalogue courses
   (plus 8 whole-page catalogue-listing transcriptions). This is raw extracted text, not yet
   chunked or embedded — sufficient as a knowledge source for the next stage, but retrieval-ready
   chunking/embedding work has not been done.

**All three components needed for the next stage exist.** What remains before recommendation
logic can be built (explicitly out of scope for this task and not started): retrieval indexing
or embeddings over the profile and course documents, the actual evidence-weighted scoring/ranking
method, and the explanation-generation layer. No such logic exists anywhere in this build.
