# What GPT-5-mini Actually Received — Full Snapshot Inspection
## Respondent `nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88` (Branch D)

Source of truth for this entire document: the literal saved API-call snapshot `outputs/rag_recommendation_post_fix_review/call_snapshots/nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88.json` (field `constructed_input_text`) from the final post-fix 10-respondent validation run, cross-referenced with the saved recommendation output in `api_recommendations_post_fix.jsonl`. **No API calls were made and nothing was regenerated to produce this document — every quoted block below is copied verbatim from the saved snapshot, not reconstructed.**

Model: `gpt-5-mini` | Response ID: `resp_007104089287a919006a913bc17cf887d0b10d9cbb6cfbc07a` | Total tokens: 38353 (input 34890, output 3463, reasoning 512)

Governance-instructions hash stored in the snapshot: `45f883053c208799...` — verified to match the current `context_pack_v2.GOVERNANCE_INSTRUCTIONS` constant (re-hashed just now, **MATCH**), confirming the governance text quoted in §5 below is exactly what this call used, byte-for-byte.

Why this respondent: 4 final recommendations (all DIRECT_MATCH), giving enough breadth to show both what was cited and what was available but unused.

---

## 1. RESPONDENT'S ACTUAL SURVEY ANSWERS GIVEN TO THE LLM

Every line below is copied verbatim from Section 1 of the constructed input text (nothing added, nothing omitted, nothing reordered). Each is labeled **[ACTUAL SURVEY ANSWER]**.

```
SECTION 1: DIRECT RESPONDENT EVIDENCE
(protected/proxy and technical fields already excluded; unlisted fields were missing, structurally not applicable, or routing-conditional — never treat an absence as 'No')

--- DIRECT PREFERENCE / INTENT (respondent explicitly stated what they want) ---
  ideal_work_type: Work for a multinational or large private company
  ideal_sector: Manufacturing or production
  plans_after_education: Look for a job
  expected_highest_edu_d: Post-graduate degree
  study_field_preference: Science or mathematics

--- FEASIBILITY / CONSTRAINT CONTEXT (respondent explicitly reported a circumstance) ---
  district: Badulla
  area_type: Metropolitan suburb
  has_children: No
  household_size: 4.0
  household_income: LKR 30,000 – 60,000
  household_workers: 1.0
  household_unemployed: 1.0
  primary_earner_status: No — someone else is the main provider
  primary_income_source: My parents or family
  edu_funding_source: Government-funded or free of charge

--- EDUCATION AND EXPERIENCE CONTEXT (actual background) ---
  edu_status: Currently in higher education (degree or diploma)
  worked_while_studying: Yes
  work_while_study_type: Informal or casual work
  work_while_study_paid: Paid
  work_while_study_hours: Less than 5 hours
  work_while_study_motivation: To earn money
  current_activity_status: Attending school, university, or a training programme
  already_job_searching: Yes — I am already searching
  re_entered_education: No
  institution_type: Government school or state university
  job_search_method_d: Online job ads (internet, social media)

--- INDIVIDUAL CONTEXT ONLY (explanation-supporting, must not independently drive ranking) ---
  age_group: 22 – 25 years
  moved_from_origin: No — I moved from somewhere else
  move_reason: For education or training
  employment_network_quality: Not really — I have very few useful contacts
  edu_min_for_decent_job: A/L level
  most_important_life_goal: Having financial security or earning a lot
  most_useful_quality_for_job: Scientific or technical qualifications
  social_capital_in_edu_access: I researched and applied entirely on my own initiative
  study_motivation_type: Because I am genuinely passionate about this subject
  autonomy_in_study: Some — there is flexibility within a mostly fixed curriculum
  competence_in_study_field: Very capable — confident and effective in my field
  relatedness_at_institution: Somewhat — I have some connections but am not deeply involved
```

**Total: 38 actual survey answers were given to the LLM for this respondent** (5 direct-preference/intent, 10 feasibility/constraint, 11 education/experience, 12 individual-context-only — as literally labeled in the text above).

---

## 2. SURVEY INFORMATION NOT GIVEN TO THE LLM

The snapshot's Section 1 header states this explicitly: *"protected/proxy and technical fields already excluded; unlisted fields were missing, structurally not applicable, or routing-conditional — never treat an absence as 'No'"*. Cross-checked against the frozen evidence-policy table (`outputs/rag_respondent_evidence/respondent_variable_policy.csv`), two categories are excluded from every respondent's LLM input by policy, not just this one:

- **PROTECTED_OR_PROXY_DO_NOT_USE** (6 variables) — fields that could let the model infer or reason about protected characteristics or family-background proxies. Category names only (this respondent's actual answers to these are not reproduced here): `father_edu, father_occ, gender, marital_status, mother_edu, mother_occ`.
- **TECHNICAL_DO_NOT_USE** (10 variables) — internal/system fields (record identifiers, branch-routing metadata, QA flags) that carry no substantive evidence about the respondent and could only introduce noise or leakage. Field-name categories only: record identifiers (e.g. respondent_id), branch-routing diagnostics (e.g. branch_changed, branch_integrity_issue, branch_path_disagreement, branch_routing_source, entry_branch), and QA/system metadata (feature_count, smoke_test, submitted_at).

Separately, a third kind of exclusion is per-respondent rather than category-wide: any field this specific respondent left unanswered, that was structurally not applicable to them (e.g. spell2/spell3 employment-history fields when they only reported one activity spell), or that was gated behind a routing question they answered in a way that skipped it (e.g. `reason_re_entered`, gated on `re_entered_education = No`). These are silently absent from Section 1 rather than shown as "No" or "N/A" — which is exactly what the governance instructions warn the model not to misread as a negative answer.

---

## 3. PROFILE CONTEXT GIVEN TO THE LLM

This respondent has **3 frozen profile memberships**, and the LLM received the **complete profile document** for each — not a summary. Every one is reproduced in full below, verbatim from the snapshot, labeled **[PROFILE/GROUP CONTEXT]**. Each document includes the exact cluster-definition facts, the pre-registered/FDR-screened "supported findings," and the complete observed distribution for every survey variable tested against that profile model (not only the highlighted ones) — this is the literal, un-summarized content sent to the model.

### [PROFILE/GROUP CONTEXT] `D_motivation_p2`

```
------ PROFILE DOCUMENT: D_motivation_p2 (Motivation and study experience) ------
====================================================================================================
NYSC YOUTH PROFILE KNOWLEDGE DOCUMENT
====================================================================================================

profile_key: D_motivation_p2
branch: D
retained_model_id: D_motivation
retained_dimension: Motivation and study experience
profile_id: 2
profile_label: Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support
profile_size_n: 75

SOURCE OF RECORD: This document is compiled only from the frozen, audited outputs of
the NYSC final clustering and post-cluster profiling stage (freeze date 26 August 2026):
  - NYSC_all_branches_clustering_final_report.md (Part I: clustering method, validation,
    decision register)
  - NYSC_Final_Clustering_and_Post_Cluster_Profiling_Report.docx / 
    final_cluster_profiling_report.md (Part II: post-cluster profiling)
  - outputs/final_cluster_programme_relevant_profiles.csv (17-row profile evidence summary)
  - outputs/final_cluster_profile_comparison_summary.csv (270-row variable-level statistics)
No fact in this document was invented, estimated, or extrapolated beyond these sources.

----------------------------------------------------------------------------------------------------
1. PROFILE_DEFINITION
----------------------------------------------------------------------------------------------------
Facts that define the cluster itself. These variables and diagnostics produced the
cluster; they are NOT re-tested as post-cluster findings (doing so would be circular).

Branch: D — strict final-path analytical cohort n=191 (of 362 total strict-cohort respondents: D=191, E=34, F=81, G=56).
Retained dimension: Motivation and study experience
Number of profiles in this retained model (k): 3
This profile's id and label: Profile 2 — "Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support"
This profile's exact frozen size: n=75 (cross-verified against the Part III freeze-verification table in the source report)

Exact cluster-forming variables (the only inputs used to build this clustering; all
other survey variables were deliberately excluded from distance calculation and are
only used descriptively in sections 2-3 below):
  - study_motivation_type
  - autonomy_in_study
  - competence_in_study_field
  - relatedness_at_institution

Theoretical basis and purpose: Self-Determination Theory (Deci & Ryan, 2000): autonomy, competence and relatedness in the study context, plus stated study-motivation type.

Clustering method: Gower distance over original mixed-type responses (no invented 0-100
scores), consensus of repeated K-medoids and spectral clustering across 100 matched
80% subsamples (200 base partitions), final clusters from K-medoids on (1 - co-association).

Validation diagnostics for this retained model: Gower silhouette 0.350; bootstrap/subsample ARI 0.981; ARI vs full K-medoids 0.968 and vs spectral 0.712; PAC (proportion of ambiguous clustering) 0.193; 7 of 8 mandatory validation checks passed.
Final decision status: Retained for exploratory use, with ambiguity and one-item-per-construct cautions.
Model-level caution (from the frozen decision register): Four single survey items represent motivation, autonomy, competence and relatedness; uncertain memberships must remain visible.

Additional definitional context: About 23.6% of respondents in this model had low Gower membership confidence (ambiguous cluster assignment); uncertain assignments must remain flagged. The three profile labels summarise four single-item questions only — they are not clinical or psychometrically validated SDT instrument types.

Interpretation of this specific profile (verbatim from the frozen report's per-model
profile table):
  Study direction was more goal-aligned, while competence and relatedness were mixed.

Reminder: this profile exists only WITHIN this one retained dimension. A respondent's
membership here says nothing about their membership in any other branch's or dimension's
profile system (see PROHIBITED_INFERENCES).

----------------------------------------------------------------------------------------------------
2. SUPPORTED_PROFILE_FINDINGS
----------------------------------------------------------------------------------------------------
Post-cluster comparisons that passed this model's pre-registered effect-size and
coverage reporting screen (i.e. explicitly retained/approved profiling findings, as
categorised in the frozen evidence summary). These are the findings that may inform a
later programme-matching stage. Directional statements are WITHIN-PROFILE percentages
compared against the other profile(s) in the same model.

FDR-correction context for this model: Among the findings that passed the effect-size/coverage reporting screen for this model, 0 of 1 remained significant after Benjamini-Hochberg FDR correction. The reported finding is descriptive/exploratory evidence only, not a confirmed statistical difference.

[Strongest additional characteristics (top approved differentiators)]
  - Useful employment/training contacts: less often reported ‘Yes — I know several people with useful connections’ (12/75, 16.0% vs 24.1% in other profile(s))

[Barriers, support and financial context]
  - Useful employment/training contacts: less often reported ‘Yes — I know several people with useful connections’ (12/75, 16.0% vs 24.1% in other profile(s))

[Aspirations and preferences]
  - No clear additional difference met the reporting screen for this category.

[Education, training and employment characteristics]
  - No clear additional difference met the reporting screen for this category.

[Programme-relevant evidence]
  - Useful employment/training contacts: less often reported ‘Yes — I know several people with useful connections’ (12/75, 16.0% vs 24.1% in other profile(s))

Statistical support detail for the variables named above (effect size is the primary
ranking evidence; p-values, raw and BH-adjusted, are supporting evidence only):

  - Useful employment/training contacts (employment_network_quality): coverage 100.0% of the model cohort; effect size epsilon-squared = 0.048; raw p = 0.004204; BH-adjusted p = 0.07778 (NOT significant at FDR<0.05 (descriptive only)); programme relevance rated 'high'.

----------------------------------------------------------------------------------------------------
3. DIRECT_GROUP_DISTRIBUTIONS
----------------------------------------------------------------------------------------------------
The complete observed distribution of THIS profile's survey answers for every
non-cluster-forming variable tested against this model (not only the ones highlighted
as approved findings above). Included so no descriptive detail is summarised away.
Entries marked [SCREENED FINDING] passed the reporting screen in section 2 above;
entries marked [tested, not highlighted] did not meet that screen and must be read as
raw descriptive data only, not as a vetted group difference.

* Area type [area_type] — type: categorical, theme: access, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=75): Metropolitan suburb: 34 (45.3%); Small town: 22 (29.3%); Large city: 11 (14.7%); Rural area: 8 (10.7%)

* District [district] — type: categorical, theme: access, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously; related model note: Many district categories can create sparse tables.)
    This profile's observed distribution (eligible n=75): Colombo: 20 (26.7%); Gampaha: 12 (16.0%); Kurunegala: 5 (6.7%); Kandy: 4 (5.3%); Kalutara: 4 (5.3%); Matara: 4 (5.3%); Puttalam: 3 (4.0%); Galle: 3 (4.0%); Jaffna: 3 (4.0%); Ratnapura: 3 (4.0%); Badulla: 2 (2.7%); Hambantota: 2 (2.7%); Anuradhapura: 2 (2.7%); Ampara: 2 (2.7%); Polonnaruwa: 2 (2.7%); Trincomalee: 1 (1.3%); Mullaitivu: 1 (1.3%); Kegalle: 1 (1.3%); Monaragala: 1 (1.3%)

* Current or preferred field of study [study_field_preference] — type: categorical, theme: aspiration, cohort coverage: 97.9% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=74): ICT or computing: 39 (52.7%); Science or mathematics: 8 (10.8%); Engineering: 7 (9.5%); Commerce, business, or management: 7 (9.5%); Other field: 4 (5.4%); Education or teaching: 3 (4.1%); Literature, arts, or social sciences: 2 (2.7%); Health sciences or nursing: 2 (2.7%); Industrial or technical studies: 2 (2.7%)

* Ideal sector [ideal_sector] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): Information technology and communications: 38 (50.7%); Education and teaching: 6 (8.0%); Manufacturing or production: 6 (8.0%); Finance, banking, and insurance: 5 (6.7%); Not sure: 5 (6.7%); Health, social work, and wellbeing: 4 (5.3%); Creative, media, and arts: 4 (5.3%); Hotels, restaurants, and hospitality: 2 (2.7%); Personal services (beauty, fitness, wellness): 2 (2.7%); Agriculture, forestry, and fishing: 1 (1.3%); Construction and building: 1 (1.3%); Transport, storage, and logistics: 1 (1.3%)

* Ideal work type [ideal_work_type] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): Work for a multinational or large private company: 29 (38.7%); Start my own business: 29 (38.7%); Not sure yet: 6 (8.0%); Work for the government or public sector: 5 (6.7%); Work for a local private Sri Lankan company: 5 (6.7%); Work on my own or family farm or land: 1 (1.3%)

* Most important life goal [most_important_life_goal] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): Being successful in work or my career: 30 (40.0%); Building self-confidence and personal fulfilment: 13 (17.3%); Having financial security or earning a lot: 12 (16.0%); Finding purpose and meaning in life: 6 (8.0%); Making a meaningful contribution to society: 5 (6.7%); Having leisure, freedom, and personal time: 4 (5.3%); Having a good family life: 4 (5.3%); Upholding my religious or cultural values: 1 (1.3%)

* Plans after current education [plans_after_education] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): Look for a job: 44 (58.7%); Immediately go on to further education or training: 21 (28.0%); Do not know yet: 5 (6.7%); Start my own business: 4 (5.3%); Stay at home: 1 (1.3%)

* Quality considered most useful for a good job [most_useful_quality_for_job] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): Communication and interpersonal skills: 26 (34.7%); Scientific or technical qualifications: 11 (14.7%); IT and digital skills: 10 (13.3%); Ambition and drive: 10 (13.3%); Command of languages (English, etc.): 4 (5.3%); Business and economic knowledge: 4 (5.3%); A good general education: 4 (5.3%); Teamwork and collaboration skills: 4 (5.3%); Completion of apprenticeship or vocational training: 2 (2.7%)

* Current institution type [institution_type] — type: categorical, theme: education, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously; related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=75): Private school or private degree-awarding institute: 39 (52.0%); Government school or state university: 25 (33.3%); International school or foreign university programme: 7 (9.3%); Online or distance learning programme: 2 (2.7%); Other: 1 (1.3%); Government vocational/technical institute (NYSC, NAITA, VTA, etc.): 1 (1.3%)

* Expected highest education [expected_highest_edu_d] — type: ordered, theme: education, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=75): median=7.00, IQR=6.00–7.00

* Father's education [father_edu] — type: ordered, theme: education, cohort coverage: 97.4% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=75): median=4.00, IQR=3.00–6.00

* Minimum education believed necessary for a decent job [edu_min_for_decent_job] — type: ordered, theme: education, cohort coverage: 96.9% [tested, not highlighted]
    This profile's observed distribution (eligible n=72): median=5.00, IQR=4.00–5.00

* Mother's education [mother_edu] — type: ordered, theme: education, cohort coverage: 95.8% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=73): median=5.00, IQR=3.00–6.00

* Re-entered education after interruption [re_entered_education] — type: categorical, theme: education, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=75): No: 62 (82.7%); Yes: 13 (17.3%)

* Reason for re-entering education [reason_re_entered] — type: categorical, theme: education, cohort coverage: 14.1% [tested, not highlighted] (conditional on: re_entered_education; sparse cells - interpret cautiously; small-sample flag; related model note: Follow-up to a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=13): Needed different qualifications for a different career: 4 (30.8%); Was not sure what I wanted to do: 2 (15.4%); Could not find suitable work: 2 (15.4%); Other reason: 2 (15.4%); Did not feel ready for the working world: 2 (15.4%); Finally had enough money to pay for education: 1 (7.7%)

* Already searching for work/business [already_job_searching] — type: categorical, theme: employment, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=75): Yes — I am already searching: 42 (56.0%); No — not yet: 33 (44.0%)

* Paid status of work while studying [work_while_study_paid] — type: categorical, theme: employment, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; small-sample flag; related model note: Conditional on a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=26): Paid: 19 (73.1%); Unpaid: 7 (26.9%)

* Type of work while studying [work_while_study_type] — type: categorical, theme: employment, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; sparse cells - interpret cautiously; small-sample flag; related model note: Conditional on a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=26): Internship or apprenticeship in a private company: 15 (57.7%); Internship or apprenticeship in the public sector: 5 (19.2%); Informal or casual work: 4 (15.4%); Other: 1 (3.8%); Paid work in a company (not internship): 1 (3.8%)

* Worked while studying [worked_while_studying] — type: categorical, theme: employment, cohort coverage: 98.4% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=74): No: 48 (64.9%); Yes: 26 (35.1%)

* Age group [age_group] — type: categorical, theme: equity, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): 22 – 25 years: 50 (66.7%); 18 – 21 years: 16 (21.3%); 26 – 29 years: 8 (10.7%); 15 – 17 years: 1 (1.3%)

* Gender [gender] — type: categorical, theme: equity, cohort coverage: 99.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=75): Male: 41 (54.7%); Female: 34 (45.3%)

* Has children [has_children] — type: categorical, theme: feasibility, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): No: 75 (100.0%)

* Hours band while studying [work_while_study_hours] — type: ordered, theme: feasibility, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; small-sample flag; related model note: Conditional on a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=26): median=2.00, IQR=2.00–4.00

* Marital status [marital_status] — type: categorical, theme: feasibility, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): Never married: 74 (98.7%); Engaged to be married: 1 (1.3%)

* Household income band [household_income] — type: ordered, theme: financial, cohort coverage: 84.8% [tested, not highlighted] (related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=61): median=4.00, IQR=3.00–5.00

* Household size [household_size] — type: numeric, theme: financial, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=75): median=4.00, IQR=4.00–5.00

* Household unemployed jobseekers [household_unemployed] — type: numeric, theme: financial, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=75): median=1.00, IQR=0.50–1.00

* Household workers [household_workers] — type: numeric, theme: financial, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=75): median=2.00, IQR=1.00–2.00

* Main education funding source [edu_funding_source] — type: categorical, theme: financial, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously; related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=75): Paid for by my family: 55 (73.3%); Government-funded or free of charge: 14 (18.7%); Other arrangement: 2 (2.7%); I pay from my own earnings: 2 (2.7%); Scholarship or grant: 1 (1.3%); Employer-sponsored: 1 (1.3%)

* Primary personal income source [primary_income_source] — type: categorical, theme: financial, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously; related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=75): My parents or family: 58 (77.3%); An education grant, scholarship, or training allowance: 5 (6.7%); My regular job or business: 5 (6.7%); Casual or informal work: 5 (6.7%); Other source: 2 (2.7%)

* Primary-earner status [primary_earner_status] — type: categorical, theme: financial, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously; related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=75): No — someone else is the main provider: 67 (89.3%); Yes — I provide the main household income: 4 (5.3%); Shared — several people contribute roughly equally: 4 (5.3%)

* Reason for working while studying [work_while_study_motivation] — type: categorical, theme: financial, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; sparse cells - interpret cautiously; small-sample flag; related model note: Conditional on a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=26): To gain work experience and build my CV: 14 (53.8%); To build connections that could lead to future employment: 6 (23.1%); To earn money: 5 (19.2%); Other reason: 1 (3.8%)

* Lives in the same area where they grew up [moved_from_origin] — type: categorical, theme: mobility, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=75): Yes — I grew up here and still live here: 51 (68.0%); No — I moved from somewhere else: 24 (32.0%)

* Reason for moving [move_reason] — type: categorical, theme: mobility, cohort coverage: 30.4% [tested, not highlighted] (conditional on: moved_from_origin; sparse cells - interpret cautiously; small-sample flag)
    This profile's observed distribution (eligible n=24): For education or training: 17 (70.8%); To accompany family: 3 (12.5%); Other reason: 3 (12.5%); For work or employment reasons: 1 (4.2%)

* How current programme was accessed [social_capital_in_edu_access] — type: categorical, theme: service, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=75): I researched and applied entirely on my own initiative: 35 (46.7%); Family members advised me or guided the choice: 30 (40.0%); A friend, teacher, or contact recommended it: 7 (9.3%); I was assigned or directed by a government programme: 3 (4.0%)

* Main job-search method while studying [job_search_method_d] — type: categorical, theme: service, cohort coverage: 58.1% [tested, not highlighted] (conditional on: already_job_searching; sparse cells - interpret cautiously; small-sample flag)
    This profile's observed distribution (eligible n=42): Online job ads (internet, social media): 24 (57.1%); Through education or training institution: 5 (11.9%); Direct application to employers: 4 (9.5%); Placing or answering job advertisements: 3 (7.1%); Checking at worksites / factory gates: 2 (4.8%); Attending job fairs: 2 (4.8%); Through friends, relatives, or colleagues: 1 (2.4%); Private employment agency: 1 (2.4%)

* Useful employment/training contacts [employment_network_quality] — type: ordered, theme: support, cohort coverage: 100.0% [SCREENED FINDING]
    This profile's observed distribution (eligible n=75): median=2.00, IQR=2.00–3.00

----------------------------------------------------------------------------------------------------
4. CAUTIONS
----------------------------------------------------------------------------------------------------
Model-level caution: Four single survey items represent motivation, autonomy, competence and relatedness; uncertain memberships must remain visible.
Additional model context: About 23.6% of respondents in this model had low Gower membership confidence (ambiguous cluster assignment); uncertain assignments must remain flagged. The three profile labels summarise four single-item questions only — they are not clinical or psychometrically validated SDT instrument types.
FDR-correction context: Among the findings that passed the effect-size/coverage reporting screen for this model, 0 of 1 remained significant after Benjamini-Hochberg FDR correction. The reported finding is descriptive/exploratory evidence only, not a confirmed statistical difference.

Profile-specific caution (verbatim from the frozen evidence summary): Four single survey items represent motivation, autonomy, competence and relatedness; uncertain memberships must remain visible. None of the selected comparisons remained below FDR 0.05; effect sizes are descriptive evidence.

Conditional-denominator caution: 7 of 37 variables tested against this model are conditional (asked only of an eligible subgroup via survey routing, e.g. only active jobseekers, only those who worked while studying). Their percentages use the eligible-subgroup denominator shown in section 3, not the full profile size. A blank caused by survey routing was never treated as a 'No' answer during profiling.

Cross-dimensional caution: the following variables tested against this model also form part of another retained clustering model; their relationship to this profile is descriptive only and is NOT independent statistical validation of this model:
  - Primary personal income source: Forms the separate D economic model.
  - Worked while studying: Forms the separate D educational/cultural model.
  - Re-entered education after interruption: Forms the separate D educational/cultural model.
  - Primary-earner status: Forms the separate D economic model.
  - Father's education: Forms the separate D educational/cultural model.
  - Main education funding source: Forms the separate D economic model.
  - Type of work while studying: Conditional on a variable forming the D educational/cultural model.
  - Household income band: Forms the separate D economic model.
  - Reason for working while studying: Conditional on a variable forming the D educational/cultural model.
  - Mother's education: Forms the separate D educational/cultural model.
  - Expected highest education: Forms the separate D educational/cultural model.
  - Hours band while studying: Conditional on a variable forming the D educational/cultural model.
  - District: Many district categories can create sparse tables.
  - Household size: Forms the separate D economic model.
  - Household workers: Forms the separate D economic model.
  - Household unemployed jobseekers: Forms the separate D economic model.
  - Current institution type: Forms the separate D educational/cultural model.
  - Reason for re-entering education: Follow-up to a variable forming the D educational/cultural model.
  - Paid status of work while studying: Conditional on a variable forming the D educational/cultural model.

Sparse-cell caution: 20 of 37 variables tested against this model contain sparse expected-cell counts (categorical tables with rare category combinations); percentages built from sparse tables are listed in section 3 and should be read with extra caution, especially for high-cardinality variables such as district, sector or stated obstacle.

General measurement cautions (apply to every profile in this knowledge base):
  - A reported percentage is a within-profile percentage in this 362-respondent strict
    cohort, not a population estimate for all Sri Lankan youth.
  - Effect sizes rank descriptive differences; they do not prove that cluster membership
    caused the characteristic.
  - Consensus clustering stability shows reproducibility under the specified procedure;
    it does not prove a natural, causal, or permanent youth type.
  - Profile names are descriptive and must not stigmatise respondents or be used to deny
    programme access.

----------------------------------------------------------------------------------------------------
5. PROHIBITED_INFERENCES
----------------------------------------------------------------------------------------------------
Statements that must NOT be assumed true for an individual merely because they belong
to this profile. These are hard constraints for any downstream system (including a RAG
recommendation layer) consuming this document.

Universal (applies to all 17 retained profiles):
  - Do not assume that a specific individual assigned to this profile personally holds any characteristic reported as a group percentage. A group finding such as 'X% of this profile reported Y' describes the profile as a whole; it is not a fact about any one person in it — a sizeable minority (and in close splits, close to half) of the profile did NOT report Y.
  - Do not treat profile membership as a diagnosis, permanent trait, or whole-person label. Profiles are exploratory response-pattern groups within ONE retained dimension only. The same respondent can simultaneously belong to different profiles across different retained dimensions (for example a Branch D respondent has independent motivation, economic and educational-trajectory profile memberships) — no single profile describes the whole person.
  - Do not use profile membership, alone, as an eligibility gate, a reason to deny access to a programme, or a reason to prioritise/deprioritise a youth for any service.
  - Do not treat effect sizes or association strength as evidence of causation. A reported association (e.g. 'Profile A more often reported X') describes a measured difference in this sample; it does not establish that being in Profile A caused X, or that X caused profile membership.
  - Do not treat a finding that did not pass this model's effect-size/coverage reporting screen (see DIRECT_GROUP_DISTRIBUTIONS) as an approved or reportable difference. Untagged distributions are raw descriptive data only, not vetted findings.
  - Do not treat a finding as statistically confirmed population evidence merely because it appears here. Most models in this knowledge base have few or zero findings that remain significant after Benjamini-Hochberg FDR correction (see this profile's CAUTIONS section and fdr_note) — effect sizes are the primary ranking evidence, and p-values (raw or adjusted) are supporting evidence only.
  - Do not generalise any percentage in this document to Sri Lankan youth generally, to NYSC's wider applicant pool, or to any group outside the 362-respondent strict analytical cohort (D=191, E=34, F=81, G=56) from which these profiles were derived.
  - Do not infer, invent, or assume any need, barrier, preference or characteristic for this profile that is not explicitly present in the source data below. If a data point is absent, it must be reported as absent/not tested, never filled in by assumption.
  - Do not use this document, on its own, to select or recommend a specific NYSC course or programme. Course/programme recommendation requires a separate, transparent, expert-reviewed matching stage that combines this profile information with the individual's own stated preferences, eligibility and the structured NYSC course catalogue.

Specific to the 'Motivation and study experience' model:
  - Do not treat the three motivation profile labels as clinical or psychometrically validated Self-Determination-Theory types; they summarise four single survey items only.
  - Do not assume an individual in the 'externally or uncertainly motivated' profile lacks motivation entirely, or that an individual in the 'highly self-directed' profile has no study difficulties — these are relative, not absolute, characterisations, and 23.6% of the model's respondents had low membership confidence.

Worked counter-example for this specific profile (do NOT do this):
  WRONG: "This youth is in profile 'Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support', so they must have this characteristic: Useful employment/training contacts: less often reported ‘Yes — I know several people with useful connections’ (12/75, 16.0% vs 24.1% in other profile(s))"
  RIGHT: "This youth is in profile 'Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support' (n=75). Within this profile, the group-level pattern was: Useful employment/training contacts: less often reported ‘Yes — I know several people with useful connections’ (12/75, 16.0% vs 24.1% in other profile(s)). This is evidence about the group, not a confirmed fact about this individual, who must be asked directly."

====================================================================================================
END OF DOCUMENT
====================================================================================================
```

### [PROFILE/GROUP CONTEXT] `D_economic_p1`

```
------ PROFILE DOCUMENT: D_economic_p1 (Economic resources and household pressure) ------
====================================================================================================
NYSC YOUTH PROFILE KNOWLEDGE DOCUMENT
====================================================================================================

profile_key: D_economic_p1
branch: D
retained_model_id: D_economic
retained_dimension: Economic resources and household pressure
profile_id: 1
profile_label: Economic profile 1: relatively lower household economic position
profile_size_n: 44

SOURCE OF RECORD: This document is compiled only from the frozen, audited outputs of
the NYSC final clustering and post-cluster profiling stage (freeze date 26 August 2026):
  - NYSC_all_branches_clustering_final_report.md (Part I: clustering method, validation,
    decision register)
  - NYSC_Final_Clustering_and_Post_Cluster_Profiling_Report.docx / 
    final_cluster_profiling_report.md (Part II: post-cluster profiling)
  - outputs/final_cluster_programme_relevant_profiles.csv (17-row profile evidence summary)
  - outputs/final_cluster_profile_comparison_summary.csv (270-row variable-level statistics)
No fact in this document was invented, estimated, or extrapolated beyond these sources.

----------------------------------------------------------------------------------------------------
1. PROFILE_DEFINITION
----------------------------------------------------------------------------------------------------
Facts that define the cluster itself. These variables and diagnostics produced the
cluster; they are NOT re-tested as post-cluster findings (doing so would be circular).

Branch: D — strict final-path analytical cohort n=191 (of 362 total strict-cohort respondents: D=191, E=34, F=81, G=56).
Retained dimension: Economic resources and household pressure
Number of profiles in this retained model (k): 2
This profile's id and label: Profile 1 — "Economic profile 1: relatively lower household economic position"
This profile's exact frozen size: n=44 (cross-verified against the Part III freeze-verification table in the source report)

Exact cluster-forming variables (the only inputs used to build this clustering; all
other survey variables were deliberately excluded from distance calculation and are
only used descriptively in sections 2-3 below):
  - edu_funding_source
  - household_income
  - household_size
  - household_unemployed
  - household_workers
  - primary_earner_status
  - primary_income_source

Theoretical basis and purpose: Bourdieu economic capital and ILO School-to-Work Transition Survey household/education-financing position.

Clustering method: Gower distance over original mixed-type responses (no invented 0-100
scores), consensus of repeated K-medoids and spectral clustering across 100 matched
80% subsamples (200 base partitions), final clusters from K-medoids on (1 - co-association).

Validation diagnostics for this retained model: Gower silhouette 0.436; bootstrap/subsample ARI 0.986; source-method ARIs 0.849 and 0.796; 7 of 8 mandatory validation checks passed.
Final decision status: Retained cautiously.
Model-level caution (from the frozen decision register): Income refusals and household-count inconsistencies were handled pairwise in clustering; profiles indicate relative position, not poverty status.

Additional definitional context: 29 of 191 Branch D respondents declined to report household income. 5 records had reported household workers plus unemployed members exceeding household size; their derived shares were treated as unavailable (missing) rather than silently corrected. Missing-aware Gower distance used only the remaining comparable components for these respondents.

Interpretation of this specific profile (verbatim from the frozen report's per-model
profile table):
  Lower relative position across the observed income, household-labour, earner-responsibility and education-funding pattern.

Reminder: this profile exists only WITHIN this one retained dimension. A respondent's
membership here says nothing about their membership in any other branch's or dimension's
profile system (see PROHIBITED_INFERENCES).

----------------------------------------------------------------------------------------------------
2. SUPPORTED_PROFILE_FINDINGS
----------------------------------------------------------------------------------------------------
Post-cluster comparisons that passed this model's pre-registered effect-size and
coverage reporting screen (i.e. explicitly retained/approved profiling findings, as
categorised in the frozen evidence summary). These are the findings that may inform a
later programme-matching stage. Directional statements are WITHIN-PROFILE percentages
compared against the other profile(s) in the same model.

FDR-correction context for this model: Among the findings that passed the effect-size/coverage reporting screen for this model, 4 of 5 remained significant after FDR correction; 1 did not.

[Strongest additional characteristics (top approved differentiators)]
  - Ideal sector: less often reported ‘Information technology and communications’ (18/44, 40.9% vs 63.3% in other profile(s)) [sparse table]
  - Current or preferred field of study: less often reported ‘ICT or computing’ (11/42, 26.2% vs 65.5% in other profile(s)) [sparse table]
  - Current institution type: less often reported ‘Private school or private degree-awarding institute’ (4/44, 9.1% vs 72.1% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - How current programme was accessed: less often reported ‘Family members advised me or guided the choice’ (6/44, 13.6% vs 41.5% in other profile(s)) [sparse table]
  - Main job-search method while studying: less often reported ‘Online job ads (internet, social media)’ (4/22, 18.2% vs 50.6% in other profile(s)) [conditional eligible n=111; sparse table]

[Barriers, support and financial context]
  - No clear additional difference met the reporting screen for this category.

[Aspirations and preferences]
  - Ideal sector: less often reported ‘Information technology and communications’ (18/44, 40.9% vs 63.3% in other profile(s)) [sparse table]
  - Current or preferred field of study: less often reported ‘ICT or computing’ (11/42, 26.2% vs 65.5% in other profile(s)) [sparse table]

[Education, training and employment characteristics]
  - Current institution type: less often reported ‘Private school or private degree-awarding institute’ (4/44, 9.1% vs 72.1% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - How current programme was accessed: less often reported ‘Family members advised me or guided the choice’ (6/44, 13.6% vs 41.5% in other profile(s)) [sparse table]
  - Main job-search method while studying: less often reported ‘Online job ads (internet, social media)’ (4/22, 18.2% vs 50.6% in other profile(s)) [conditional eligible n=111; sparse table]

[Programme-relevant evidence]
  - Ideal sector: less often reported ‘Information technology and communications’ (18/44, 40.9% vs 63.3% in other profile(s)) [sparse table]
  - Current or preferred field of study: less often reported ‘ICT or computing’ (11/42, 26.2% vs 65.5% in other profile(s)) [sparse table]
  - Current institution type: less often reported ‘Private school or private degree-awarding institute’ (4/44, 9.1% vs 72.1% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - Main job-search method while studying: less often reported ‘Online job ads (internet, social media)’ (4/22, 18.2% vs 50.6% in other profile(s)) [conditional eligible n=111; sparse table]

Statistical support detail for the variables named above (effect size is the primary
ranking evidence; p-values, raw and BH-adjusted, are supporting evidence only):

  - Ideal sector (ideal_sector): coverage 100.0% of the model cohort; effect size bias-corrected Cramér's V = 0.381; raw p = 0.0001102; BH-adjusted p = 0.0009369 (significant at FDR<0.05); programme relevance rated 'high'. [sparse cells]
  - Current or preferred field of study (study_field_preference): coverage 97.9% of the model cohort; effect size bias-corrected Cramér's V = 0.378; raw p = 3.15e-05; BH-adjusted p = 0.000357 (significant at FDR<0.05); programme relevance rated 'high'. [sparse cells]
  - Current institution type (institution_type): coverage 100.0% of the model cohort; effect size bias-corrected Cramér's V = 0.566; raw p = 6.976e-13; BH-adjusted p = 2.372e-11 (significant at FDR<0.05); programme relevance rated 'high'. [sparse cells, cross-dimensional: Forms the separate D educational/cultural model.]
  - How current programme was accessed (social_capital_in_edu_access): coverage 100.0% of the model cohort; effect size bias-corrected Cramér's V = 0.370; raw p = 4.966e-06; BH-adjusted p = 8.442e-05 (significant at FDR<0.05); programme relevance rated 'medium'. [sparse cells]
  - Main job-search method while studying (job_search_method_d): coverage 58.1% of the model cohort; effect size bias-corrected Cramér's V = 0.300; raw p = 0.02944; BH-adjusted p = 0.1122 (NOT significant at FDR<0.05 (descriptive only)); programme relevance rated 'high'. [sparse cells, conditional (gateway: already_job_searching)]

----------------------------------------------------------------------------------------------------
3. DIRECT_GROUP_DISTRIBUTIONS
----------------------------------------------------------------------------------------------------
The complete observed distribution of THIS profile's survey answers for every
non-cluster-forming variable tested against this model (not only the ones highlighted
as approved findings above). Included so no descriptive detail is summarised away.
Entries marked [SCREENED FINDING] passed the reporting screen in section 2 above;
entries marked [tested, not highlighted] did not meet that screen and must be read as
raw descriptive data only, not as a vetted group difference.

* Area type [area_type] — type: categorical, theme: access, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=44): Metropolitan suburb: 15 (34.1%); Small town: 13 (29.5%); Rural area: 9 (20.5%); Large city: 7 (15.9%)

* District [district] — type: categorical, theme: access, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously; related model note: Many district categories can create sparse tables.)
    This profile's observed distribution (eligible n=44): Colombo: 11 (25.0%); Puttalam: 5 (11.4%); Galle: 5 (11.4%); Trincomalee: 3 (6.8%); Gampaha: 3 (6.8%); Kandy: 3 (6.8%); Matara: 3 (6.8%); Kurunegala: 3 (6.8%); Kegalle: 1 (2.3%); Monaragala: 1 (2.3%); Kalutara: 1 (2.3%); Badulla: 1 (2.3%); Vavuniya: 1 (2.3%); Anuradhapura: 1 (2.3%); Hambantota: 1 (2.3%); Jaffna: 1 (2.3%)

* Current or preferred field of study [study_field_preference] — type: categorical, theme: aspiration, cohort coverage: 97.9% [SCREENED FINDING] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=42): Science or mathematics: 11 (26.2%); ICT or computing: 11 (26.2%); Engineering: 7 (16.7%); Other field: 4 (9.5%); Commerce, business, or management: 4 (9.5%); Education or teaching: 3 (7.1%); Health sciences or nursing: 2 (4.8%)

* Ideal sector [ideal_sector] — type: categorical, theme: aspiration, cohort coverage: 100.0% [SCREENED FINDING] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): Information technology and communications: 18 (40.9%); Manufacturing or production: 6 (13.6%); Agriculture, forestry, and fishing: 4 (9.1%); Health, social work, and wellbeing: 3 (6.8%); Education and teaching: 3 (6.8%); Not sure: 3 (6.8%); Finance, banking, and insurance: 2 (4.5%); Personal services (beauty, fitness, wellness): 2 (4.5%); Hotels, restaurants, and hospitality: 1 (2.3%); Construction and building: 1 (2.3%); Transport, storage, and logistics: 1 (2.3%)

* Ideal work type [ideal_work_type] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): Work for a multinational or large private company: 15 (34.1%); Start my own business: 14 (31.8%); Work for the government or public sector: 8 (18.2%); Work for a local private Sri Lankan company: 3 (6.8%); Not sure yet: 3 (6.8%); Work on my own or family farm or land: 1 (2.3%)

* Most important life goal [most_important_life_goal] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): Being successful in work or my career: 17 (38.6%); Having financial security or earning a lot: 12 (27.3%); Having leisure, freedom, and personal time: 6 (13.6%); Building self-confidence and personal fulfilment: 3 (6.8%); Having a good family life: 2 (4.5%); Finding purpose and meaning in life: 2 (4.5%); Making a meaningful contribution to society: 2 (4.5%)

* Plans after current education [plans_after_education] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): Look for a job: 29 (65.9%); Immediately go on to further education or training: 9 (20.5%); Start my own business: 3 (6.8%); Stay at home: 2 (4.5%); Do not know yet: 1 (2.3%)

* Quality considered most useful for a good job [most_useful_quality_for_job] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): Communication and interpersonal skills: 11 (25.0%); IT and digital skills: 10 (22.7%); Ambition and drive: 8 (18.2%); Command of languages (English, etc.): 5 (11.4%); Scientific or technical qualifications: 5 (11.4%); A good general education: 3 (6.8%); Business and economic knowledge: 2 (4.5%)

* Current institution type [institution_type] — type: categorical, theme: education, cohort coverage: 100.0% [SCREENED FINDING] (sparse cells - interpret cautiously; related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=44): Government school or state university: 33 (75.0%); International school or foreign university programme: 5 (11.4%); Private school or private degree-awarding institute: 4 (9.1%); Other: 2 (4.5%)

* Expected highest education [expected_highest_edu_d] — type: ordered, theme: education, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=44): median=7.00, IQR=6.00–7.00

* Father's education [father_edu] — type: ordered, theme: education, cohort coverage: 97.4% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=43): median=4.00, IQR=3.00–6.00

* Minimum education believed necessary for a decent job [edu_min_for_decent_job] — type: ordered, theme: education, cohort coverage: 96.9% [tested, not highlighted]
    This profile's observed distribution (eligible n=43): median=5.00, IQR=4.00–5.00

* Mother's education [mother_edu] — type: ordered, theme: education, cohort coverage: 95.8% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=43): median=3.00, IQR=3.00–5.00

* Re-entered education after interruption [re_entered_education] — type: categorical, theme: education, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=44): No: 36 (81.8%); Yes: 8 (18.2%)

* Reason for re-entering education [reason_re_entered] — type: categorical, theme: education, cohort coverage: 14.1% [tested, not highlighted] (conditional on: re_entered_education; sparse cells - interpret cautiously; small-sample flag; related model note: Follow-up to a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=8): Could not find suitable work: 4 (50.0%); Needed different qualifications for a different career: 1 (12.5%); Did not feel ready for the working world: 1 (12.5%); Finally had enough money to pay for education: 1 (12.5%); Was not sure what I wanted to do: 1 (12.5%)

* Already searching for work/business [already_job_searching] — type: categorical, theme: employment, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=44): Yes — I am already searching: 22 (50.0%); No — not yet: 22 (50.0%)

* Paid status of work while studying [work_while_study_paid] — type: categorical, theme: employment, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; sparse cells - interpret cautiously; small-sample flag; related model note: Conditional on a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=13): Paid: 13 (100.0%)

* Type of work while studying [work_while_study_type] — type: categorical, theme: employment, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; sparse cells - interpret cautiously; small-sample flag; related model note: Conditional on a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=13): Informal or casual work: 5 (38.5%); Internship or apprenticeship in a private company: 4 (30.8%); Other: 1 (7.7%); Internship or apprenticeship in the public sector: 1 (7.7%); Paid work in the public sector (not internship): 1 (7.7%); Paid work in a company (not internship): 1 (7.7%)

* Worked while studying [worked_while_studying] — type: categorical, theme: employment, cohort coverage: 98.4% [tested, not highlighted] (related model note: Forms the separate D educational/cultural model.)
    This profile's observed distribution (eligible n=42): No: 29 (69.0%); Yes: 13 (31.0%)

* Age group [age_group] — type: categorical, theme: equity, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): 22 – 25 years: 35 (79.5%); 26 – 29 years: 4 (9.1%); 18 – 21 years: 3 (6.8%); 15 – 17 years: 1 (2.3%); 30 – 35 years: 1 (2.3%)

* Gender [gender] — type: categorical, theme: equity, cohort coverage: 99.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=43): Male: 23 (53.5%); Female: 20 (46.5%)

* Has children [has_children] — type: categorical, theme: feasibility, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): No: 42 (95.5%); Yes: 2 (4.5%)

* Hours band while studying [work_while_study_hours] — type: ordered, theme: feasibility, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; small-sample flag; related model note: Conditional on a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=13): median=3.00, IQR=2.00–4.00

* Marital status [marital_status] — type: categorical, theme: feasibility, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): Never married: 41 (93.2%); Engaged to be married: 2 (4.5%); Married: 1 (2.3%)

* Reason for working while studying [work_while_study_motivation] — type: categorical, theme: financial, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; sparse cells - interpret cautiously; small-sample flag; related model note: Conditional on a variable forming the D educational/cultural model.)
    This profile's observed distribution (eligible n=13): To earn money: 8 (61.5%); To gain work experience and build my CV: 5 (38.5%)

* Lives in the same area where they grew up [moved_from_origin] — type: categorical, theme: mobility, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=44): Yes — I grew up here and still live here: 28 (63.6%); No — I moved from somewhere else: 16 (36.4%)

* Reason for moving [move_reason] — type: categorical, theme: mobility, cohort coverage: 30.4% [tested, not highlighted] (conditional on: moved_from_origin; sparse cells - interpret cautiously; small-sample flag)
    This profile's observed distribution (eligible n=16): For education or training: 14 (87.5%); For work or employment reasons: 1 (6.2%); To accompany family: 1 (6.2%)

* How current programme was accessed [social_capital_in_edu_access] — type: categorical, theme: service, cohort coverage: 100.0% [SCREENED FINDING] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=44): I researched and applied entirely on my own initiative: 25 (56.8%); I was assigned or directed by a government programme: 10 (22.7%); Family members advised me or guided the choice: 6 (13.6%); A friend, teacher, or contact recommended it: 2 (4.5%); My employer or a workplace contact directed me here: 1 (2.3%)

* Main job-search method while studying [job_search_method_d] — type: categorical, theme: service, cohort coverage: 58.1% [SCREENED FINDING] (conditional on: already_job_searching; sparse cells - interpret cautiously; small-sample flag)
    This profile's observed distribution (eligible n=22): Through education or training institution: 7 (31.8%); Online job ads (internet, social media): 4 (18.2%); Direct application to employers: 3 (13.6%); Attending job fairs: 3 (13.6%); Placing or answering job advertisements: 2 (9.1%); Checking at worksites / factory gates: 1 (4.5%); Private employment agency: 1 (4.5%); Public employment office registration: 1 (4.5%)

* Institutional belonging [relatedness_at_institution] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D motivation model.)
    This profile's observed distribution (eligible n=44): median=2.00, IQR=1.00–2.00

* Perceived competence in study field [competence_in_study_field] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D motivation model.)
    This profile's observed distribution (eligible n=44): median=2.00, IQR=1.00–2.25

* Study autonomy [autonomy_in_study] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D motivation model.)
    This profile's observed distribution (eligible n=44): median=2.00, IQR=1.00–2.00

* Study motivation type [study_motivation_type] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D motivation model.)
    This profile's observed distribution (eligible n=44): median=2.00, IQR=1.00–4.00

* Useful employment/training contacts [employment_network_quality] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=44): median=2.00, IQR=1.00–3.00

----------------------------------------------------------------------------------------------------
4. CAUTIONS
----------------------------------------------------------------------------------------------------
Model-level caution: Income refusals and household-count inconsistencies were handled pairwise in clustering; profiles indicate relative position, not poverty status.
Additional model context: 29 of 191 Branch D respondents declined to report household income. 5 records had reported household workers plus unemployed members exceeding household size; their derived shares were treated as unavailable (missing) rather than silently corrected. Missing-aware Gower distance used only the remaining comparable components for these respondents.
FDR-correction context: Among the findings that passed the effect-size/coverage reporting screen for this model, 4 of 5 remained significant after FDR correction; 1 did not.

Profile-specific caution (verbatim from the frozen evidence summary): Income refusals and household-count inconsistencies were handled pairwise in clustering; profiles indicate relative position, not poverty status. Some reported findings use eligible-subgroup denominators. Some categorical comparisons contain sparse cells.

Conditional-denominator caution: 7 of 34 variables tested against this model are conditional (asked only of an eligible subgroup via survey routing, e.g. only active jobseekers, only those who worked while studying). Their percentages use the eligible-subgroup denominator shown in section 3, not the full profile size. A blank caused by survey routing was never treated as a 'No' answer during profiling.

Cross-dimensional caution: the following variables tested against this model also form part of another retained clustering model; their relationship to this profile is descriptive only and is NOT independent statistical validation of this model:
  - Current institution type: Forms the separate D educational/cultural model.
  - Mother's education: Forms the separate D educational/cultural model.
  - Study autonomy: Forms the separate D motivation model.
  - Reason for working while studying: Conditional on a variable forming the D educational/cultural model.
  - Type of work while studying: Conditional on a variable forming the D educational/cultural model.
  - Expected highest education: Forms the separate D educational/cultural model.
  - Worked while studying: Forms the separate D educational/cultural model.
  - Paid status of work while studying: Conditional on a variable forming the D educational/cultural model.
  - Institutional belonging: Forms the separate D motivation model.
  - Study motivation type: Forms the separate D motivation model.
  - District: Many district categories can create sparse tables.
  - Reason for re-entering education: Follow-up to a variable forming the D educational/cultural model.
  - Perceived competence in study field: Forms the separate D motivation model.
  - Hours band while studying: Conditional on a variable forming the D educational/cultural model.
  - Father's education: Forms the separate D educational/cultural model.
  - Re-entered education after interruption: Forms the separate D educational/cultural model.

Sparse-cell caution: 18 of 34 variables tested against this model contain sparse expected-cell counts (categorical tables with rare category combinations); percentages built from sparse tables are listed in section 3 and should be read with extra caution, especially for high-cardinality variables such as district, sector or stated obstacle.

General measurement cautions (apply to every profile in this knowledge base):
  - A reported percentage is a within-profile percentage in this 362-respondent strict
    cohort, not a population estimate for all Sri Lankan youth.
  - Effect sizes rank descriptive differences; they do not prove that cluster membership
    caused the characteristic.
  - Consensus clustering stability shows reproducibility under the specified procedure;
    it does not prove a natural, causal, or permanent youth type.
  - Profile names are descriptive and must not stigmatise respondents or be used to deny
    programme access.

----------------------------------------------------------------------------------------------------
5. PROHIBITED_INFERENCES
----------------------------------------------------------------------------------------------------
Statements that must NOT be assumed true for an individual merely because they belong
to this profile. These are hard constraints for any downstream system (including a RAG
recommendation layer) consuming this document.

Universal (applies to all 17 retained profiles):
  - Do not assume that a specific individual assigned to this profile personally holds any characteristic reported as a group percentage. A group finding such as 'X% of this profile reported Y' describes the profile as a whole; it is not a fact about any one person in it — a sizeable minority (and in close splits, close to half) of the profile did NOT report Y.
  - Do not treat profile membership as a diagnosis, permanent trait, or whole-person label. Profiles are exploratory response-pattern groups within ONE retained dimension only. The same respondent can simultaneously belong to different profiles across different retained dimensions (for example a Branch D respondent has independent motivation, economic and educational-trajectory profile memberships) — no single profile describes the whole person.
  - Do not use profile membership, alone, as an eligibility gate, a reason to deny access to a programme, or a reason to prioritise/deprioritise a youth for any service.
  - Do not treat effect sizes or association strength as evidence of causation. A reported association (e.g. 'Profile A more often reported X') describes a measured difference in this sample; it does not establish that being in Profile A caused X, or that X caused profile membership.
  - Do not treat a finding that did not pass this model's effect-size/coverage reporting screen (see DIRECT_GROUP_DISTRIBUTIONS) as an approved or reportable difference. Untagged distributions are raw descriptive data only, not vetted findings.
  - Do not treat a finding as statistically confirmed population evidence merely because it appears here. Most models in this knowledge base have few or zero findings that remain significant after Benjamini-Hochberg FDR correction (see this profile's CAUTIONS section and fdr_note) — effect sizes are the primary ranking evidence, and p-values (raw or adjusted) are supporting evidence only.
  - Do not generalise any percentage in this document to Sri Lankan youth generally, to NYSC's wider applicant pool, or to any group outside the 362-respondent strict analytical cohort (D=191, E=34, F=81, G=56) from which these profiles were derived.
  - Do not infer, invent, or assume any need, barrier, preference or characteristic for this profile that is not explicitly present in the source data below. If a data point is absent, it must be reported as absent/not tested, never filled in by assumption.
  - Do not use this document, on its own, to select or recommend a specific NYSC course or programme. Course/programme recommendation requires a separate, transparent, expert-reviewed matching stage that combines this profile information with the individual's own stated preferences, eligibility and the structured NYSC course catalogue.

Specific to the 'Economic resources and household pressure' model:
  - Do not describe this profile using the word 'poverty' or treat it as a poverty classification — it indicates only a RELATIVE household economic position within this specific 191-respondent Branch D cohort, not an absolute income or poverty-line measurement.
  - Do not assume the 29 respondents who declined to report household income are evenly or randomly distributed across profiles, or backfill their income with an assumed value.

Worked counter-example for this specific profile (do NOT do this):
  WRONG: "This youth is in profile 'Economic profile 1: relatively lower household economic position', so they must have this characteristic: Ideal sector: less often reported ‘Information technology and communications’ (18/44, 40.9% vs 63.3% in other profile(s)) [sparse table]"
  RIGHT: "This youth is in profile 'Economic profile 1: relatively lower household economic position' (n=44). Within this profile, the group-level pattern was: Ideal sector: less often reported ‘Information technology and communications’ (18/44, 40.9% vs 63.3% in other profile(s)) [sparse table]. This is evidence about the group, not a confirmed fact about this individual, who must be asked directly."

====================================================================================================
END OF DOCUMENT
====================================================================================================
```

### [PROFILE/GROUP CONTEXT] `D_educational_cultural_p4`

```
------ PROFILE DOCUMENT: D_educational_cultural_p4 (Educational trajectory and cultural capital) ------
====================================================================================================
NYSC YOUTH PROFILE KNOWLEDGE DOCUMENT
====================================================================================================

profile_key: D_educational_cultural_p4
branch: D
retained_model_id: D_educational_cultural
retained_dimension: Educational trajectory and cultural capital
profile_id: 4
profile_label: Work-experienced students, mainly in private institutions
profile_size_n: 66

SOURCE OF RECORD: This document is compiled only from the frozen, audited outputs of
the NYSC final clustering and post-cluster profiling stage (freeze date 26 August 2026):
  - NYSC_all_branches_clustering_final_report.md (Part I: clustering method, validation,
    decision register)
  - NYSC_Final_Clustering_and_Post_Cluster_Profiling_Report.docx / 
    final_cluster_profiling_report.md (Part II: post-cluster profiling)
  - outputs/final_cluster_programme_relevant_profiles.csv (17-row profile evidence summary)
  - outputs/final_cluster_profile_comparison_summary.csv (270-row variable-level statistics)
No fact in this document was invented, estimated, or extrapolated beyond these sources.

----------------------------------------------------------------------------------------------------
1. PROFILE_DEFINITION
----------------------------------------------------------------------------------------------------
Facts that define the cluster itself. These variables and diagnostics produced the
cluster; they are NOT re-tested as post-cluster findings (doing so would be circular).

Branch: D — strict final-path analytical cohort n=191 (of 362 total strict-cohort respondents: D=191, E=34, F=81, G=56).
Retained dimension: Educational trajectory and cultural capital
Number of profiles in this retained model (k): 4
This profile's id and label: Profile 4 — "Work-experienced students, mainly in private institutions"
This profile's exact frozen size: n=66 (cross-verified against the Part III freeze-verification table in the source report)

Exact cluster-forming variables (the only inputs used to build this clustering; all
other survey variables were deliberately excluded from distance calculation and are
only used descriptively in sections 2-3 below):
  - expected_highest_edu_d
  - father_edu
  - institution_type
  - mother_edu
  - re_entered_education
  - worked_while_studying

Theoretical basis and purpose: Inherited educational background (Bourdieu cultural capital, proxied by parental education) plus current educational trajectory (institution type, work-while-studying, education re-entry).

Clustering method: Gower distance over original mixed-type responses (no invented 0-100
scores), consensus of repeated K-medoids and spectral clustering across 100 matched
80% subsamples (200 base partitions), final clusters from K-medoids on (1 - co-association).

Validation diagnostics for this retained model: Gower silhouette 0.427; bootstrap/subsample ARI 0.963; source-method ARIs 0.776 and 0.934; 8 of 8 mandatory validation checks passed.
Final decision status: Retained.
Model-level caution (from the frozen decision register): Parental education is a proxy only; work-experience and re-entry follow-ups are structurally linked to variables defining these profiles.

Additional definitional context: Parental education is only a proxy for family cultural capital; it is not a measure of intelligence or merit. Sensitivity analysis showed that work-while-studying experience and institution type are important drivers of the partition and must remain explicit in interpretation, not collapsed into a single 'cultural capital' score.

Interpretation of this specific profile (verbatim from the frozen report's per-model
profile table):
  Work while studying was prominent, with many respondents in private institutions.

Reminder: this profile exists only WITHIN this one retained dimension. A respondent's
membership here says nothing about their membership in any other branch's or dimension's
profile system (see PROHIBITED_INFERENCES).

----------------------------------------------------------------------------------------------------
2. SUPPORTED_PROFILE_FINDINGS
----------------------------------------------------------------------------------------------------
Post-cluster comparisons that passed this model's pre-registered effect-size and
coverage reporting screen (i.e. explicitly retained/approved profiling findings, as
categorised in the frozen evidence summary). These are the findings that may inform a
later programme-matching stage. Directional statements are WITHIN-PROFILE percentages
compared against the other profile(s) in the same model.

FDR-correction context for this model: Among the findings that passed the effect-size/coverage reporting screen for this model, 7 of 7 remained significant after FDR correction.

[Strongest additional characteristics (top approved differentiators)]
  - Already searching for work/business: less often reported ‘No — not yet’ (23/66, 34.8% vs 45.6% in other profile(s))
  - Primary personal income source: less often reported ‘My parents or family’ (40/66, 60.6% vs 87.2% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - Main education funding source: less often reported ‘Government-funded or free of charge’ (6/66, 9.1% vs 21.6% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - Household income band: more often reported ‘Above LKR 200,000’ (31/55, 56.4% vs 29.9% in other profile(s)) [cross-dimensional/related variable]
  - Primary-earner status: less often reported ‘Yes — I provide the main household income’ (1/66, 1.5% vs 7.2% in other profile(s)) [sparse table; cross-dimensional/related variable]

[Barriers, support and financial context]
  - Primary personal income source: less often reported ‘My parents or family’ (40/66, 60.6% vs 87.2% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - Main education funding source: less often reported ‘Government-funded or free of charge’ (6/66, 9.1% vs 21.6% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - Household income band: more often reported ‘Above LKR 200,000’ (31/55, 56.4% vs 29.9% in other profile(s)) [cross-dimensional/related variable]

[Aspirations and preferences]
  - No clear additional difference met the reporting screen for this category.

[Education, training and employment characteristics]
  - Already searching for work/business: less often reported ‘No — not yet’ (23/66, 34.8% vs 45.6% in other profile(s))

[Programme-relevant evidence]
  - Already searching for work/business: less often reported ‘No — not yet’ (23/66, 34.8% vs 45.6% in other profile(s))
  - Primary personal income source: less often reported ‘My parents or family’ (40/66, 60.6% vs 87.2% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - Main education funding source: less often reported ‘Government-funded or free of charge’ (6/66, 9.1% vs 21.6% in other profile(s)) [sparse table; cross-dimensional/related variable]
  - Household income band: more often reported ‘Above LKR 200,000’ (31/55, 56.4% vs 29.9% in other profile(s)) [cross-dimensional/related variable]

Statistical support detail for the variables named above (effect size is the primary
ranking evidence; p-values, raw and BH-adjusted, are supporting evidence only):

  - Already searching for work/business (already_job_searching): coverage 100.0% of the model cohort; effect size bias-corrected Cramér's V = 0.263; raw p = 0.001046; BH-adjusted p = 0.004112 (significant at FDR<0.05); programme relevance rated 'high'.
  - Primary personal income source (primary_income_source): coverage 100.0% of the model cohort; effect size bias-corrected Cramér's V = 0.365; raw p = 3.894e-12; BH-adjusted p = 1.285e-10 (significant at FDR<0.05); programme relevance rated 'high'. [sparse cells, cross-dimensional: Forms the separate D economic model.]
  - Main education funding source (edu_funding_source): coverage 100.0% of the model cohort; effect size bias-corrected Cramér's V = 0.322; raw p = 1.109e-09; BH-adjusted p = 1.831e-08 (significant at FDR<0.05); programme relevance rated 'high'. [sparse cells, cross-dimensional: Forms the separate D economic model.]
  - Household income band (household_income): coverage 84.8% of the model cohort; effect size epsilon-squared = 0.179; raw p = 7.53e-07; BH-adjusted p = 8.283e-06 (significant at FDR<0.05); programme relevance rated 'high'. [cross-dimensional: Forms the separate D economic model.]
  - Primary-earner status (primary_earner_status): coverage 100.0% of the model cohort; effect size bias-corrected Cramér's V = 0.265; raw p = 1.27e-05; BH-adjusted p = 0.0001048 (significant at FDR<0.05); programme relevance rated 'high'. [sparse cells, cross-dimensional: Forms the separate D economic model.]
  - Household unemployed jobseekers (household_unemployed): coverage 100.0% of the model cohort; effect size epsilon-squared = 0.084; raw p = 0.0003128; BH-adjusted p = 0.00172 (significant at FDR<0.05); programme relevance rated 'medium'. [cross-dimensional: Forms the separate D economic model.]
  - Household workers (household_workers): coverage 100.0% of the model cohort; effect size epsilon-squared = 0.042; raw p = 0.0129; BH-adjusted p = 0.03871 (significant at FDR<0.05); programme relevance rated 'medium'. [cross-dimensional: Forms the separate D economic model.]

----------------------------------------------------------------------------------------------------
3. DIRECT_GROUP_DISTRIBUTIONS
----------------------------------------------------------------------------------------------------
The complete observed distribution of THIS profile's survey answers for every
non-cluster-forming variable tested against this model (not only the ones highlighted
as approved findings above). Included so no descriptive detail is summarised away.
Entries marked [SCREENED FINDING] passed the reporting screen in section 2 above;
entries marked [tested, not highlighted] did not meet that screen and must be read as
raw descriptive data only, not as a vetted group difference.

* Area type [area_type] — type: categorical, theme: access, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=66): Metropolitan suburb: 32 (48.5%); Large city: 14 (21.2%); Small town: 13 (19.7%); Rural area: 7 (10.6%)

* District [district] — type: categorical, theme: access, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously; related model note: Many district categories can create sparse tables.)
    This profile's observed distribution (eligible n=66): Colombo: 28 (42.4%); Gampaha: 8 (12.1%); Kurunegala: 6 (9.1%); Galle: 5 (7.6%); Anuradhapura: 4 (6.1%); Kalutara: 3 (4.5%); Badulla: 2 (3.0%); Puttalam: 2 (3.0%); Trincomalee: 2 (3.0%); Kegalle: 2 (3.0%); Kandy: 1 (1.5%); Hambantota: 1 (1.5%); Matara: 1 (1.5%); Monaragala: 1 (1.5%)

* Current or preferred field of study [study_field_preference] — type: categorical, theme: aspiration, cohort coverage: 97.9% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): ICT or computing: 45 (68.2%); Science or mathematics: 10 (15.2%); Engineering: 4 (6.1%); Commerce, business, or management: 4 (6.1%); Literature, arts, or social sciences: 2 (3.0%); Industrial or technical studies: 1 (1.5%)

* Ideal sector [ideal_sector] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): Information technology and communications: 42 (63.6%); Not sure: 9 (13.6%); Manufacturing or production: 4 (6.1%); Education and teaching: 3 (4.5%); Wholesale, retail, or repair: 2 (3.0%); Agriculture, forestry, and fishing: 1 (1.5%); Creative, media, and arts: 1 (1.5%); Construction and building: 1 (1.5%); Finance, banking, and insurance: 1 (1.5%); Hotels, restaurants, and hospitality: 1 (1.5%); Health, social work, and wellbeing: 1 (1.5%)

* Ideal work type [ideal_work_type] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): Start my own business: 26 (39.4%); Work for a multinational or large private company: 24 (36.4%); Not sure yet: 7 (10.6%); Work for a local private Sri Lankan company: 5 (7.6%); Work for the government or public sector: 2 (3.0%); I do not wish to work: 1 (1.5%); Work on my own or family farm or land: 1 (1.5%)

* Most important life goal [most_important_life_goal] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): Being successful in work or my career: 24 (36.4%); Building self-confidence and personal fulfilment: 15 (22.7%); Having financial security or earning a lot: 13 (19.7%); Having leisure, freedom, and personal time: 5 (7.6%); Finding purpose and meaning in life: 4 (6.1%); Having a good family life: 3 (4.5%); Making a meaningful contribution to society: 2 (3.0%)

* Plans after current education [plans_after_education] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): Look for a job: 40 (60.6%); Immediately go on to further education or training: 18 (27.3%); Start my own business: 4 (6.1%); Do not know yet: 4 (6.1%)

* Quality considered most useful for a good job [most_useful_quality_for_job] — type: categorical, theme: aspiration, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): Communication and interpersonal skills: 26 (39.4%); IT and digital skills: 15 (22.7%); Ambition and drive: 11 (16.7%); Scientific or technical qualifications: 5 (7.6%); A good general education: 4 (6.1%); Teamwork and collaboration skills: 3 (4.5%); Business and economic knowledge: 2 (3.0%)

* Minimum education believed necessary for a decent job [edu_min_for_decent_job] — type: ordered, theme: education, cohort coverage: 96.9% [tested, not highlighted]
    This profile's observed distribution (eligible n=62): median=5.00, IQR=4.00–5.00

* Reason for re-entering education [reason_re_entered] — type: categorical, theme: education, cohort coverage: 14.1% [tested, not highlighted] (conditional on: re_entered_education; sparse cells - interpret cautiously; small-sample flag; related model note: Direct follow-up to a cluster-forming gateway.)
    This profile's observed distribution (eligible n=2): Was not sure what I wanted to do: 1 (50.0%); Could not find suitable work: 1 (50.0%)

* Already searching for work/business [already_job_searching] — type: categorical, theme: employment, cohort coverage: 100.0% [SCREENED FINDING]
    This profile's observed distribution (eligible n=66): Yes — I am already searching: 43 (65.2%); No — not yet: 23 (34.8%)

* Type of work while studying [work_while_study_type] — type: categorical, theme: employment, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; sparse cells - interpret cautiously; small-sample flag; related model note: Direct follow-up to a cluster-forming gateway.)
    This profile's observed distribution (eligible n=66): Internship or apprenticeship in a private company: 41 (62.1%); Informal or casual work: 8 (12.1%); Internship or apprenticeship in the public sector: 8 (12.1%); Paid work in a company (not internship): 5 (7.6%); Other: 2 (3.0%); Paid work in the public sector (not internship): 2 (3.0%)

* Age group [age_group] — type: categorical, theme: equity, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): 22 – 25 years: 45 (68.2%); 18 – 21 years: 12 (18.2%); 26 – 29 years: 6 (9.1%); 30 – 35 years: 2 (3.0%); 15 – 17 years: 1 (1.5%)

* Gender [gender] — type: categorical, theme: equity, cohort coverage: 99.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=65): Male: 38 (58.5%); Female: 27 (41.5%)

* Has children [has_children] — type: categorical, theme: feasibility, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): No: 65 (98.5%); Yes: 1 (1.5%)

* Marital status [marital_status] — type: categorical, theme: feasibility, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): Never married: 65 (98.5%); Married: 1 (1.5%)

* Household income band [household_income] — type: ordered, theme: financial, cohort coverage: 84.8% [SCREENED FINDING] (related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=55): median=5.00, IQR=3.50–5.00

* Household size [household_size] — type: numeric, theme: financial, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=66): median=4.00, IQR=4.00–5.00

* Household unemployed jobseekers [household_unemployed] — type: numeric, theme: financial, cohort coverage: 100.0% [SCREENED FINDING] (related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=66): median=1.00, IQR=0.00–1.00

* Household workers [household_workers] — type: numeric, theme: financial, cohort coverage: 100.0% [SCREENED FINDING] (related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=66): median=2.00, IQR=1.00–3.00

* Main education funding source [edu_funding_source] — type: categorical, theme: financial, cohort coverage: 100.0% [SCREENED FINDING] (sparse cells - interpret cautiously; related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=66): Paid for by my family: 51 (77.3%); Government-funded or free of charge: 6 (9.1%); I pay from my own earnings: 4 (6.1%); Other arrangement: 2 (3.0%); Scholarship or grant: 2 (3.0%); Employer-sponsored: 1 (1.5%)

* Primary personal income source [primary_income_source] — type: categorical, theme: financial, cohort coverage: 100.0% [SCREENED FINDING] (sparse cells - interpret cautiously; related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=66): My parents or family: 40 (60.6%); My regular job or business: 15 (22.7%); Casual or informal work: 6 (9.1%); Other source: 3 (4.5%); Unemployment or social security benefits: 1 (1.5%); My partner or spouse: 1 (1.5%)

* Primary-earner status [primary_earner_status] — type: categorical, theme: financial, cohort coverage: 100.0% [SCREENED FINDING] (sparse cells - interpret cautiously; related model note: Forms the separate D economic model.)
    This profile's observed distribution (eligible n=66): No — someone else is the main provider: 59 (89.4%); Shared — several people contribute roughly equally: 6 (9.1%); Yes — I provide the main household income: 1 (1.5%)

* Reason for working while studying [work_while_study_motivation] — type: categorical, theme: financial, cohort coverage: 38.7% [tested, not highlighted] (conditional on: worked_while_studying; sparse cells - interpret cautiously; small-sample flag; related model note: Direct follow-up to a cluster-forming gateway.)
    This profile's observed distribution (eligible n=66): To gain work experience and build my CV: 36 (54.5%); To earn money: 16 (24.2%); To build connections that could lead to future employment: 10 (15.2%); Other reason: 4 (6.1%)

* Lives in the same area where they grew up [moved_from_origin] — type: categorical, theme: mobility, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=66): Yes — I grew up here and still live here: 45 (68.2%); No — I moved from somewhere else: 21 (31.8%)

* Reason for moving [move_reason] — type: categorical, theme: mobility, cohort coverage: 30.4% [tested, not highlighted] (conditional on: moved_from_origin; sparse cells - interpret cautiously; small-sample flag)
    This profile's observed distribution (eligible n=21): For education or training: 14 (66.7%); Other reason: 6 (28.6%); To accompany family: 1 (4.8%)

* How current programme was accessed [social_capital_in_edu_access] — type: categorical, theme: service, cohort coverage: 100.0% [tested, not highlighted] (sparse cells - interpret cautiously)
    This profile's observed distribution (eligible n=66): I researched and applied entirely on my own initiative: 38 (57.6%); Family members advised me or guided the choice: 22 (33.3%); A friend, teacher, or contact recommended it: 3 (4.5%); My employer or a workplace contact directed me here: 2 (3.0%); I was assigned or directed by a government programme: 1 (1.5%)

* Main job-search method while studying [job_search_method_d] — type: categorical, theme: service, cohort coverage: 58.1% [tested, not highlighted] (conditional on: already_job_searching; sparse cells - interpret cautiously; small-sample flag)
    This profile's observed distribution (eligible n=43): Online job ads (internet, social media): 21 (48.8%); Attending job fairs: 6 (14.0%); Through education or training institution: 4 (9.3%); Checking at worksites / factory gates: 3 (7.0%); Direct application to employers: 3 (7.0%); Placing or answering job advertisements: 2 (4.7%); Other method: 1 (2.3%); Looking for resources to start own business: 1 (2.3%); Private employment agency: 1 (2.3%); Through friends, relatives, or colleagues: 1 (2.3%)

* Institutional belonging [relatedness_at_institution] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D motivation model.)
    This profile's observed distribution (eligible n=66): median=2.00, IQR=1.00–2.00

* Perceived competence in study field [competence_in_study_field] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D motivation model.)
    This profile's observed distribution (eligible n=66): median=2.00, IQR=1.00–2.00

* Study autonomy [autonomy_in_study] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D motivation model.)
    This profile's observed distribution (eligible n=66): median=1.00, IQR=1.00–2.00

* Study motivation type [study_motivation_type] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted] (related model note: Forms the separate D motivation model.)
    This profile's observed distribution (eligible n=66): median=2.00, IQR=1.25–3.00

* Useful employment/training contacts [employment_network_quality] — type: ordered, theme: support, cohort coverage: 100.0% [tested, not highlighted]
    This profile's observed distribution (eligible n=66): median=2.00, IQR=2.00–3.00

----------------------------------------------------------------------------------------------------
4. CAUTIONS
----------------------------------------------------------------------------------------------------
Model-level caution: Parental education is a proxy only; work-experience and re-entry follow-ups are structurally linked to variables defining these profiles.
Additional model context: Parental education is only a proxy for family cultural capital; it is not a measure of intelligence or merit. Sensitivity analysis showed that work-while-studying experience and institution type are important drivers of the partition and must remain explicit in interpretation, not collapsed into a single 'cultural capital' score.
FDR-correction context: Among the findings that passed the effect-size/coverage reporting screen for this model, 7 of 7 remained significant after FDR correction.

Profile-specific caution (verbatim from the frozen evidence summary): Parental education is a proxy only; work-experience and re-entry follow-ups are structurally linked to variables defining these profiles. Some categorical comparisons contain sparse cells.

Conditional-denominator caution: 5 of 33 variables tested against this model are conditional (asked only of an eligible subgroup via survey routing, e.g. only active jobseekers, only those who worked while studying). Their percentages use the eligible-subgroup denominator shown in section 3, not the full profile size. A blank caused by survey routing was never treated as a 'No' answer during profiling.

Cross-dimensional caution: the following variables tested against this model also form part of another retained clustering model; their relationship to this profile is descriptive only and is NOT independent statistical validation of this model:
  - Primary personal income source: Forms the separate D economic model.
  - Main education funding source: Forms the separate D economic model.
  - Household income band: Forms the separate D economic model.
  - Primary-earner status: Forms the separate D economic model.
  - District: Many district categories can create sparse tables.
  - Household unemployed jobseekers: Forms the separate D economic model.
  - Household workers: Forms the separate D economic model.
  - Perceived competence in study field: Forms the separate D motivation model.
  - Household size: Forms the separate D economic model.
  - Study motivation type: Forms the separate D motivation model.
  - Study autonomy: Forms the separate D motivation model.
  - Institutional belonging: Forms the separate D motivation model.
  - Reason for re-entering education: Direct follow-up to a cluster-forming gateway.
  - Type of work while studying: Direct follow-up to a cluster-forming gateway.
  - Reason for working while studying: Direct follow-up to a cluster-forming gateway.

Sparse-cell caution: 19 of 33 variables tested against this model contain sparse expected-cell counts (categorical tables with rare category combinations); percentages built from sparse tables are listed in section 3 and should be read with extra caution, especially for high-cardinality variables such as district, sector or stated obstacle.

General measurement cautions (apply to every profile in this knowledge base):
  - A reported percentage is a within-profile percentage in this 362-respondent strict
    cohort, not a population estimate for all Sri Lankan youth.
  - Effect sizes rank descriptive differences; they do not prove that cluster membership
    caused the characteristic.
  - Consensus clustering stability shows reproducibility under the specified procedure;
    it does not prove a natural, causal, or permanent youth type.
  - Profile names are descriptive and must not stigmatise respondents or be used to deny
    programme access.

----------------------------------------------------------------------------------------------------
5. PROHIBITED_INFERENCES
----------------------------------------------------------------------------------------------------
Statements that must NOT be assumed true for an individual merely because they belong
to this profile. These are hard constraints for any downstream system (including a RAG
recommendation layer) consuming this document.

Universal (applies to all 17 retained profiles):
  - Do not assume that a specific individual assigned to this profile personally holds any characteristic reported as a group percentage. A group finding such as 'X% of this profile reported Y' describes the profile as a whole; it is not a fact about any one person in it — a sizeable minority (and in close splits, close to half) of the profile did NOT report Y.
  - Do not treat profile membership as a diagnosis, permanent trait, or whole-person label. Profiles are exploratory response-pattern groups within ONE retained dimension only. The same respondent can simultaneously belong to different profiles across different retained dimensions (for example a Branch D respondent has independent motivation, economic and educational-trajectory profile memberships) — no single profile describes the whole person.
  - Do not use profile membership, alone, as an eligibility gate, a reason to deny access to a programme, or a reason to prioritise/deprioritise a youth for any service.
  - Do not treat effect sizes or association strength as evidence of causation. A reported association (e.g. 'Profile A more often reported X') describes a measured difference in this sample; it does not establish that being in Profile A caused X, or that X caused profile membership.
  - Do not treat a finding that did not pass this model's effect-size/coverage reporting screen (see DIRECT_GROUP_DISTRIBUTIONS) as an approved or reportable difference. Untagged distributions are raw descriptive data only, not vetted findings.
  - Do not treat a finding as statistically confirmed population evidence merely because it appears here. Most models in this knowledge base have few or zero findings that remain significant after Benjamini-Hochberg FDR correction (see this profile's CAUTIONS section and fdr_note) — effect sizes are the primary ranking evidence, and p-values (raw or adjusted) are supporting evidence only.
  - Do not generalise any percentage in this document to Sri Lankan youth generally, to NYSC's wider applicant pool, or to any group outside the 362-respondent strict analytical cohort (D=191, E=34, F=81, G=56) from which these profiles were derived.
  - Do not infer, invent, or assume any need, barrier, preference or characteristic for this profile that is not explicitly present in the source data below. If a data point is absent, it must be reported as absent/not tested, never filled in by assumption.
  - Do not use this document, on its own, to select or recommend a specific NYSC course or programme. Course/programme recommendation requires a separate, transparent, expert-reviewed matching stage that combines this profile information with the individual's own stated preferences, eligibility and the structured NYSC course catalogue.

Specific to the 'Educational trajectory and cultural capital' model:
  - Do not treat parental education (or this profile's implied 'cultural capital' framing) as a measure of a respondent's intelligence, merit, or worth.
  - Do not assume this profile's institution-type or work-experience pattern reflects individual choice alone — cost, geography and family circumstance are plausible unmeasured contributors not tested here.

Worked counter-example for this specific profile (do NOT do this):
  WRONG: "This youth is in profile 'Work-experienced students, mainly in private institutions', so they must have this characteristic: Already searching for work/business: less often reported ‘No — not yet’ (23/66, 34.8% vs 45.6% in other profile(s))"
  RIGHT: "This youth is in profile 'Work-experienced students, mainly in private institutions' (n=66). Within this profile, the group-level pattern was: Already searching for work/business: less often reported ‘No — not yet’ (23/66, 34.8% vs 45.6% in other profile(s)). This is evidence about the group, not a confirmed fact about this individual, who must be asked directly."

====================================================================================================
END OF DOCUMENT
====================================================================================================
```

---

## 4. COURSE INFORMATION GIVEN TO THE LLM

**15 courses were retrieved** (BM25 rank shown as sent to the model; the governance instructions explicitly tell the model retrieval rank is NOT suitability). For each, the complete extracted course document is reproduced below exactly as sent, labeled **[RETRIEVED COURSE EVIDENCE]** — including the raw OCR/extraction artefacts present in the underlying course text.

### [RETRIEVED COURSE EVIDENCE] Rank 1 (BM25 16.7772): `COURSE-012` — Refrigeration & Air Conditioning Technician (retrieved, not recommended)

```
------ RETRIEVAL RANK 1 (BM25 score 16.7772): COURSE-012 ------
COURSE DOCUMENT ID: COURSE-012

COURSE NAME: Refrigeration & Air Conditioning Technician

VALIDATION STATUS: VALIDATED_WITH_LIMITATIONS

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.26.56.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.31.50.png

RAW SOURCE DOCUMENT ID(S): COURSE-012

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Refrigeration & Air Conditioning Technician
LANGUAGE
MAX STUDENTS
Sinhala
20
→ APPLY NOW
Course Overview
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations.
1. Repair Refigerators, Deep freezers,
Display units, Bettle Coolers, Water
Refrigeration & Air Condition Technician courses will give you theoretical knowledge as well as job
Coolers
oriented practical skills that are necessary for employment and higher education. This is a part time
2. Prepare Estimates
course which will be held on weekends.
3. Repair Window and Split type A/C
It is our objective to show the correct path that will direct youth to their desired occupations while at
4. Operate and Maintain Central A/C
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
system
gentle attitudes within a dis Screenshot unment.
```

### [RETRIEVED COURSE EVIDENCE] Rank 2 (BM25 16.7772): `COURSE-034` — Refrigeration & Air Conditioning Technician **→ RECOMMENDED**

```
------ RETRIEVAL RANK 2 (BM25 score 16.7772): COURSE-034 ------
COURSE DOCUMENT ID: COURSE-034

COURSE NAME: Refrigeration & Air Conditioning Technician

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.37.22.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.38.08.png

RAW SOURCE DOCUMENT ID(S): COURSE-034

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Refrigeration & Air Conditioning Technician
LANGUAGE
MAX STUDENTS
sinhala
20
APPLY NOW
Course Overview
REFRIGER
1. Repair Refigerators, Deep freezers,
Display units, Bettle Coolers, Water
Coolers
2. Prepare Estimates
3. Repair Window and Split type A/C
4. Operate and Maintain Central A/C
System
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations.
Refrigeration & Air Conditioning Technician course will give you theoretical knowledge as well as job
oriented practical that is necessary for employment and higher education. This is a full time course
which will be held on weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , You can achieve competency Level 4 under the National Vocational
Qualifications Competency Standards.
```

### [RETRIEVED COURSE EVIDENCE] Rank 3 (BM25 13.1765): `COURSE-031` — National Diploma In Television Program Production (retrieved, not recommended)

```
------ RETRIEVAL RANK 3 (BM25 score 13.1765): COURSE-031 ------
COURSE DOCUMENT ID: COURSE-031

COURSE NAME: National Diploma In Television Program Production

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.36.17.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.38.08.png

RAW SOURCE DOCUMENT ID(S): COURSE-031

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

National Diploma In Television Program Production
LANGUAGE
MAX STUDENTS
sinhala
20
APPLY NOW
Course Overview
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations.
National Diploma in T V Programme & Production Technology course will give you theoretical
knowledge as well as job oriented practical that is necessary for employment and higher education.
This is a full time course which will be held on weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , You can achieve competency Level 5 under the National Vocational
Qualifications Competency Standards.
```

### [RETRIEVED COURSE EVIDENCE] Rank 4 (BM25 12.6474): `COURSE-028` — Lapiderist (Gem Cutting) (retrieved, not recommended)

```
------ RETRIEVAL RANK 4 (BM25 score 12.6474): COURSE-028 ------
COURSE DOCUMENT ID: COURSE-028

COURSE NAME: Lapiderist (Gem Cutting)

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.34.16.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.38.08.png

RAW SOURCE DOCUMENT ID(S): COURSE-028

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Lapiderist (Gem Cutting)
LANGUAGE
MAX STUDENTS
sinhala
20
H
APPLY NOW
Course Overview
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. The
Lapiderist (Gem Cutting) course will give you theoretical knowledge as well as job oriented practical
skills that are necessary for employment and higher education. This is a full time course which will be
held on weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , You can achieve competency Level 3 under the National Vocational
Qualifications Competency Standards.
```

### [RETRIEVED COURSE EVIDENCE] Rank 5 (BM25 12.0395): `COURSE-029` — Mobile Phone Repair Technician (retrieved, not recommended)

```
------ RETRIEVAL RANK 5 (BM25 score 12.0395): COURSE-029 ------
COURSE DOCUMENT ID: COURSE-029

COURSE NAME: Mobile Phone Repair Technician

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.34.31.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.38.08.png

RAW SOURCE DOCUMENT ID(S): COURSE-029

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Mobile Phone Repair Technician
LANGUAGE
MAX STUDENTS
sinhala
20
APPLY NOW
Course Overview
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. Mobile
Phone Repairing Craftsman course will give you theoretical knowledge as well as job oriented
practical that is necessary for employment and higher education. This is a full time course which will
be held on weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , You can achieve competency Level 4 under the National Vocational
Qualifications Competency Standards.
```

### [RETRIEVED COURSE EVIDENCE] Rank 6 (BM25 11.5258): `COURSE-030` — Motorcycle Mechanic **→ RECOMMENDED**

```
------ RETRIEVAL RANK 6 (BM25 score 11.5258): COURSE-030 ------
COURSE DOCUMENT ID: COURSE-030

COURSE NAME: Motorcycle Mechanic

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.35.56.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.38.08.png

RAW SOURCE DOCUMENT ID(S): COURSE-030

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Motorcycle Mechanic
LANGUAGE
MAX STUDENTS
sinhala
20
APPLY NOW
Course Overview
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations.
Motorcycle Mechanic course will give you theoretical knowledge as well as job oriented practical that
is necessary for employment and higher education. This is a full time course which will be held on
weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , You can achieve competency Level 3,4 under the National Vocational
Qualifications Competency Standards.
```

### [RETRIEVED COURSE EVIDENCE] Rank 7 (BM25 10.8103): `COURSE-077` — Mobile Phone Repair Technician (retrieved, not recommended)

```
------ RETRIEVAL RANK 7 (BM25 score 10.8103): COURSE-077 ------
COURSE DOCUMENT ID: COURSE-077

COURSE NAME: Mobile Phone Repair Technician

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.59.10.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 23.00.22.png

RAW SOURCE DOCUMENT ID(S): COURSE-077

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Mobile Phone Repair Technician
LANGUAGE
MAX STUDENTS
Sinhala
20
→ APPLY NOW
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. Mobile
Phone Repairing Craftsman courses will give you theoretical knowledge as well as job oriented
practical skills that are necessary for employment and higher education. This is a part time course
which will be held on weekends.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
```

### [RETRIEVED COURSE EVIDENCE] Rank 8 (BM25 10.0184): `COURSE-040` — Automobile Mechanic **→ RECOMMENDED**

```
------ RETRIEVAL RANK 8 (BM25 score 10.0184): COURSE-040 ------
COURSE DOCUMENT ID: COURSE-040

COURSE NAME: Automobile Mechanic

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.46.12.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.48.17.png

RAW SOURCE DOCUMENT ID(S): COURSE-040

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Automobile Mechanic
LANGUAGE
MAX STUDENTS
English
20
APPLY NOW
Course Overview
1. Overhead Engine (Petrol and Diesel)
2. Transmission System (Manual and
Auto)
3. Steering System (Power and Manual)
4. Breaking System
5. Suspension System
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. The
Automobile Mechanic course will give you theoretical knowledge as well as job oriented practical that
is necessary for employment and higher education.
This is a part time course which will be held on weekends.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
```

### [RETRIEVED COURSE EVIDENCE] Rank 9 (BM25 9.9116): `COURSE-005` — Automobile Mechanic **→ RECOMMENDED**

```
------ RETRIEVAL RANK 9 (BM25 score 9.9116): COURSE-005 ------
COURSE DOCUMENT ID: COURSE-005

COURSE NAME: Automobile Mechanic

DOCUMENT STATUS: SAFE_TO_INDEX

CORPUS VERSION: FINAL_RAG_CORPUS_V2

PROMOTED SOURCE DOCUMENT: outputs/rag_course_knowledge/manual_review_resolved_candidates/course-005_automobile_mechanic_candidate.txt

SOURCE TYPE: COURSE_DETAIL_SCREENSHOTS

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.21.32.png; Screenshot 2026-04-12 at 22.23.26.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.25.19.png

RAW SOURCE DOCUMENT ID(S): COURSE-005

REMAINING UNCERTAINTY MARKERS: 0

CORRECTION NOTE: Both detail screenshots visibly show the same course name, Sinhala language, 20-student capacity, Full Time weekday delivery and Level 4 outcome. The two corresponding catalogue cards also both show Full Time, 20 students and 01 year. They are therefore retained as one repeated screenshot-derived parent, not split using the conflicting structured English record.

COMPLETE EXTRACTED COURSE TEXT

Automobile Mechanic
LANGUAGE
MAX STUDENTS
Sinhala
20
APPLY NOW
Course Overview
The National Youth Service Council has initiated several Course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations.
Automobile Mechanic/Automobile Technician will give you theoretical knowledge as well as job
oriented practical that is necessary for employment and higher education. This is a full time course
which will be held on weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , can achieve Competency Level 4 under the National Vocational
Qualifications Competency Standards through following a variety of full time study programs covering
a variety of occupations.
1. Engine (Petrol and Diesel)
2. Transmission System (Manual and Auto)
3. Steering System (Power and Manual)
4. Breaking System
5. Electrical System
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. The
Automobile Mechanic/Automobile Technician course will give you theoretical knowledge as well as job
oriented practical skills that are necessary for employment and higher education. This is a full time
course which will be held on weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , You can achieve competency Level 4 under the National Vocational
Qualifications Competency Standards.
```

### [RETRIEVED COURSE EVIDENCE] Rank 10 (BM25 7.5634): `COURSE-078` — Motorcycle Mechanic (retrieved, not recommended)

```
------ RETRIEVAL RANK 10 (BM25 score 7.5634): COURSE-078 ------
COURSE DOCUMENT ID: COURSE-078

COURSE NAME: Motorcycle Mechanic

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.59.21.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 23.00.22.png

RAW SOURCE DOCUMENT ID(S): COURSE-078

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Motorcycle Mechanic
LANGUAGE
MAX STUDENTS
Sinhala
20
→ APPLY NOW
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations.
MotorBike Repair courses will give you theoretical knowledge as well as job oriented practical skills
that are necessary for employment and higher education. This is a part time course which will be
held on weekends.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
```

### [RETRIEVED COURSE EVIDENCE] Rank 11 (BM25 7.2529): `COURSE-042` — Automobile Electrician (retrieved, not recommended)

```
------ RETRIEVAL RANK 11 (BM25 score 7.2529): COURSE-042 ------
COURSE DOCUMENT ID: COURSE-042

COURSE NAME: Automobile Electrician

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.46.44.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.48.17.png

RAW SOURCE DOCUMENT ID(S): COURSE-042

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Automobile Electrician
LANGUAGE
MAX STUDENTS
sinhala
20
+
APPLY NOW
Course Overview
12.18
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. Auto
Electrical course will give you theoretical knowledge as well as job oriented practical skills that are
necessary for employment and higher education. This is a full time course which will be held on
weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
```

### [RETRIEVED COURSE EVIDENCE] Rank 12 (BM25 6.9185): `COURSE-081` — Radio, TV & Allied Equipment Repairer (retrieved, not recommended)

```
------ RETRIEVAL RANK 12 (BM25 score 6.9185): COURSE-081 ------
COURSE DOCUMENT ID: COURSE-081

COURSE NAME: Radio, TV & Allied Equipment Repairer

VALIDATION STATUS: VALIDATED_WITH_LIMITATIONS

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.59.53.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 23.00.22.png

RAW SOURCE DOCUMENT ID(S): COURSE-081

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Radio, TV & Allied Equipment Repairer
LANGUAGE
MAX STUDENTS
English
20
→ APPLY NOW
Course Overview
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. Radio,
1. CRT TV, Monitor, LCD / LED TV, DVD
Players Repair
TV & Allied Equipment Repairer courses will give you theoretical knowledge as well as job oriented
2. Basic Electricity and Electronics
practical skills that are necessary for employment and higher education. This is a part time course
which will be held on weekends.
3. Microcontroller Programming, LED
Display Boaet Programming
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
```

### [RETRIEVED COURSE EVIDENCE] Rank 13 (BM25 6.8168): `COURSE-006` — National Diploma In Information & Communication Technology (retrieved, not recommended)

```
------ RETRIEVAL RANK 13 (BM25 score 6.8168): COURSE-006 ------
COURSE DOCUMENT ID: COURSE-006

COURSE NAME: National Diploma In Information & Communication Technology

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.21.55.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.25.19.png

RAW SOURCE DOCUMENT ID(S): COURSE-006

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

National Diploma In Information & Communication
Technology
LANGUAGE
MAX STUDENTS
English
20
APPLY NOW
Course Overview
1. System Analysis & Design - Semester 1
2. Software Programming - Semester 1
3. Database System - Semester 1
4. Computer Graphics Design -
Semester 1
5. Manage Workplace Information -
6. Manage Workplace Communication -
7. Documents & Resource Level 5 -
8. Database Systems II - Semester 2
9. Software Testing - Semester 2
10. Web Programming - Semester 2
11. Local Area Network - Semester 2
12. Planing & Scheduling Work at
Workplace - Semester 2
The National Youth Service Council has initiated several Course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations.
Information & Communication Multimedia Technology will give you theoretical knowledge as well as
job oriented practical that is necessary for employment and higher education. This is a full time
course which will be held on weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , can achieve Competency Level 5 under the National Vocational
Qualifications Competency Standards through following a variety of full time study programs covering
a variety of occupations.
```

### [RETRIEVED COURSE EVIDENCE] Rank 14 (BM25 6.1148): `COURSE-021` — Automobile Electrician (retrieved, not recommended)

```
------ RETRIEVAL RANK 14 (BM25 score 6.1148): COURSE-021 ------
COURSE DOCUMENT ID: COURSE-021

COURSE NAME: Automobile Electrician

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.30.32.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.31.50.png

RAW SOURCE DOCUMENT ID(S): COURSE-021

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Automobile Electrician
LANGUAGE
MAX STUDENTS
English
20
→
APPLY NOW
Course Overview
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. The
Automobile Electrician course will give you theoretical knowledge as well as job oriented practical that
is necessary for employment and higher education. This is a full time course which will be held on
weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , You can achieve competency Level 4 under the National Vocational
Qualifications Competency Standards.
```

### [RETRIEVED COURSE EVIDENCE] Rank 15 (BM25 5.2473): `COURSE-038` — Three Wheeler Mechanic (retrieved, not recommended)

```
------ RETRIEVAL RANK 15 (BM25 score 5.2473): COURSE-038 ------
COURSE DOCUMENT ID: COURSE-038

COURSE NAME: Three Wheeler Mechanic

VALIDATION STATUS: VALIDATED

SOURCE TYPE: COURSE_DETAIL_SCREENSHOT

SOURCE SCREENSHOT FILENAME(S): Screenshot 2026-04-12 at 22.45.35.png

SUPPORTING CATALOGUE-PAGE SCREENSHOT(S): Screenshot 2026-04-12 at 22.48.17.png

RAW SOURCE DOCUMENT ID(S): COURSE-038

UNCERTAINTY MARKERS PRESENT: NO

PROVENANCE NOTE: Validated non-destructive copy of the corresponding raw course document.

SOURCE CONFLICT NOTE: NONE

COMPLETE EXTRACTED COURSE TEXT

Three Wheeler Mechanic
LANGUAGE
MAX STUDENTS
sinhala
20
APPLY NOW
Course Overview
Smiling
1443.
The National Youth Service Council has initiated several course programs to enable the youth to
develop their skills while also providing an opportunity to achieve their future job aspirations. The
Three Wheeler Mechanic course will give you theoretical knowledge as well as job oriented practical
skills that are necessary for employment and higher education.
This is a full time course which will be held on weekdays.
It is our objective to show the correct path that will direct youth to their desired occupations while at
the same time developing entrepreneurial abilities by obtaining the necessary knowledge, skills and
gentle attitudes within a disciplined environment.
By completing this course , You can achieve competency Level 3 under the National Vocational
Qualifications Competency Standards.
```

---

## 5. GOVERNANCE / REASONING INSTRUCTIONS

These are verbatim excerpts of `GOVERNANCE_INSTRUCTIONS` (sent as the API's `instructions` parameter, hash-verified above to match this exact call), pulled from the specific sections that govern the six topics requested. The full instructions text is ~23,600 characters; only the passages directly answering each topic are quoted here.

### On individual evidence vs. profile context (the evidence hierarchy)

```
A. INDIVIDUAL SURVEY EVIDENCE (Section 1) — PRIMARY. This is what is actually known about this specific respondent. It is the foundation of any claim about what THIS person wants, needs, or faces.
B. PROFILE/GROUP CONTEXT (Section 2) — SUPPORTING CONTEXT ONLY. This describes a broader empirical pattern discovered among OTHER respondents who share a statistical cluster assignment with this respondent. It is valuable background, never a substitute for A.
C. COURSE DOCUMENTS (Section 3) — AUTHORITATIVE PROGRAMME EVIDENCE. This is what a programme actually contains/offers. Course claims must come only from this text.

Individual answers (A) establish what is actually known about the respondent. Profile membership (B) describes a broader empirical pattern among similar respondents — it does not describe this respondent. Course documents (C) establish what the programme actually contains. Never allow profile context (B) to override a direct individual answer (A). When they conflict, A always wins.
```

### On correct use of profile/group context

```
GROUP-LEVEL RESEARCH CONTEXT. DO NOT ASSUME THESE CHARACTERISTICS APPLY TO THIS INDIVIDUAL. A group percentage or tendency is evidence about the group, never a fact about this specific person. If a group tendency and this respondent's own Section 1 answer ever point in different directions, the respondent's own Section 1 answer always wins. You may say something like "the respondent's own answer is consistent with a broader pattern observed in this profile" ONLY when both the individual evidence and the group finding genuinely support that statement.
```

### On DIRECT_MATCH

```
DIRECT_MATCH: direct INDIVIDUAL evidence (Section 1 — a stated field, goal, training interest, work intention, or clearly relevant preference) connects the respondent to this programme. Example: a stated finance/business interest -> Computer Based Accounting.
```

### On ADJACENT_MATCH

```
ADJACENT_MATCH: the programme does NOT directly correspond to a stated field, but has a defensible, EXPLAINED relationship to the respondent's goals/circumstances. Example: a respondent who states an Education-sector goal and a Science-related study-field preference, where no education/teaching-specific programme exists in the catalogue, but an ICT programme is defensibly relevant as a general STEM-adjacent/technical-skill option.

Adjacent recommendations are allowed and encouraged when genuinely defensible. However: clearly label the match_relationship field; ALWAYS fill in adjacent_match_bridge_explanation for an ADJACENT_MATCH, stating the specific inferential bridge; never present an ADJACENT_MATCH as equivalent in strength to a DIRECT_MATCH; and never manufacture a bridge merely to avoid returning NO_DEFENSIBLE_RECOMMENDATION or to avoid a short list — a bridge must be genuinely defensible on the actual evidence, not invented to fill space.
```

### On unsupported inference

```
The goal of all the rules above is NOT "no inference." Inference is allowed and wanted. The goal is SUPPORTED + TRANSPARENT + HEDGED inference. [...] Every claim must still be clearly labelled as one of: [ACTUAL INDIVIDUAL EVIDENCE], [PROFILE/GROUP CONTEXT], [COURSE FACT], or [LLM INFERENCE] in substance (via the structured fields provided), even when you are confident.

STRICTLY PROHIBITED, under all circumstances: [...] 8. Inferring a technical field from economic hardship, job insecurity, household circumstances, or any other circumstantial variable alone — content recommendations still need real preference/interest/skill evidence, not just hardship. This includes general opinion/perception answers (e.g. most_useful_quality_for_job): they must never substitute for a genuine DIRECT PREFERENCE/INTENT answer as the basis for selecting a programme's field/content.

CONFLICT RULE: if a genuine direct-preference/intent answer points one way and a general opinion/context answer points a different way, the respondent's own DIRECT stated preference always takes precedence for content/field selection.

NO-SUBSTITUTION RULE: if the respondent has not given any usable DIRECT PREFERENCE/INTENT answer naming a field, sector, or skill, that is missing preference evidence [...] it is NOT license to manufacture a preference from a feasibility, experience, or opinion variable instead.
```

### On NO_DEFENSIBLE_RECOMMENDATION

```
YOUR TASK: recommend between 0 and 5 of the retrieved courses for this respondent. Do not force a number — if evidence supports only 1-2, return only 1-2. If no course is defensible, return recommendation_status = "NO_DEFENSIBLE_RECOMMENDATION" with zero items in recommendations and a clear reason. This is a normal, correct, and important possible output, not a failure.

If neither a DIRECT_MATCH nor a defensible ADJACENT_MATCH exists, the correct output is recommendation_status = "NO_DEFENSIBLE_RECOMMENDATION", not a manufactured adjacent match.
```

---

## 6. WHAT GPT-5-MINI ACTUALLY USED

Taken directly from this respondent's record in `api_recommendations_post_fix.jsonl` — the structured fields the model itself returned, not a re-interpretation.

### Course: `COURSE-005` — Automobile Mechanic
**Match type:** DIRECT_MATCH
**Evidence strength:** STRONG — Direct match between the respondent's stated Manufacturing/production sector preference and the course's clear mechanical/manufacturing-relevant content (explicit practical skills and vocational competency).

**[ACTUAL SURVEY ANSWERS CITED]**
- `ideal_sector` = Manufacturing or production — The course teaches core mechanical skills used in vehicle production and servicing, which maps to the respondent's stated Manufacturing/production sector interest.
- `study_field_preference` = Science or mathematics — Mechanical and vehicle-technology training is a technical/engineering-adjacent application of science and mathematics study preference.
- `plans_after_education` = Look for a job — The course is vocational and explicitly framed for employment, matching the respondent's intention to seek work after education.

**[PROFILE CONTEXT CITED]**
- `D_educational_cultural_p4`: Many profile members worked while studying and were already searching for work; vocational, work-oriented programmes are common in this profile (supporting-context-only).

**[COURSE FACTS CITED]**
- "Course gives theoretical knowledge and job-oriented practical skills; full time course held on weekdays; competency Level 4 under National Vocational Qualifications." (source: COURSE-005)
- "Covers engine, transmission, steering, braking, electrical systems (practical mechanical skills)." (source: COURSE-005)

**[LLM INFERENCE]**
- "This vocational mechanical programme may support the respondent's stated preference for Manufacturing/production and their plan to look for a job because it provides job-oriented practical skills aligned with production/maintenance roles."
- "Because the respondent is already searching for work and has experience working while studying, a competency-level vocational credential (Level 4) may be immediately useful in applying to technical roles in manufacturing or large private companies."

**Why the model connected this person to this course, in one sentence:** Direct sector alignment: the respondent named Manufacturing/production and this course provides practical mechanical skills and a recognised vocational competency relevant to manufacturing, vehicle maintenance, and related technical roles that can support immediate job search.


### Course: `COURSE-040` — Automobile Mechanic
**Match type:** DIRECT_MATCH
**Evidence strength:** STRONG — Direct sector match with explicit mechanical skills taught and a stated employment orientation; additional feasibility support because a part-time weekend variant is documented.

**[ACTUAL SURVEY ANSWERS CITED]**
- `ideal_sector` = Manufacturing or production — Course content (engine, transmission, braking, suspension) aligns with manufacturing/production and vehicle-technology technical roles.
- `plans_after_education` = Look for a job — The course is vocational and described as intended to enable employment, matching the respondent's immediate job-seeking plan.

**[PROFILE CONTEXT CITED]**
- `D_educational_cultural_p4`: Profile members commonly combined study with work experience and were actively searching for employment (supporting-context-only).

**[COURSE FACTS CITED]**
- "Course covers overhead engines, transmission, steering, braking, suspension; described as part time held on weekends in this document." (source: COURSE-040)

**[LLM INFERENCE]**
- "Because this particular course instance is described as part-time on weekends, it may be easier for the respondent to combine with ongoing studies or part-time work compared with a weekday full-time course."

**Why the model connected this person to this course, in one sentence:** Technical/mechanical content aligns with the respondent's Manufacturing/production sector preference and employment-focused plan; the documented weekend/part-time format may also improve feasibility while studying.


### Course: `COURSE-034` — Refrigeration & Air Conditioning Technician
**Match type:** DIRECT_MATCH
**Evidence strength:** MODERATE — Direct sector and technical-skill alignment is clear, but catalogue inconsistency about delivery format and lack of specific local-offering details reduce certainty about immediate feasibility.

**[ACTUAL SURVEY ANSWERS CITED]**
- `ideal_sector` = Manufacturing or production — Refrigeration/AC technician skills are industrial/technical and commonly used in manufacturing, production facilities, and maintenance roles, matching the respondent's sector interest.
- `study_field_preference` = Science or mathematics — The course involves technical, applied physical science skills (systems operation, repair) compatible with a science/maths study preference.

**[PROFILE CONTEXT CITED]**
- `D_motivation_p2`: Profile members value scientific or technical qualifications as useful for jobs (supporting-context-only).

**[COURSE FACTS CITED]**
- "Course teaches repair of refrigerators, deep freezers, display units, water coolers, repair of window and split A/C, operate and maintain central A/C systems; described as full time on weekdays in one document and part time on weekends in another (catalogue shows both variants)." (source: COURSE-012 / COURSE-034)
- "Course description frames training as job-oriented practical skills and entrepreneurial ability development." (source: COURSE-034)

**[LLM INFERENCE]**
- "Training in refrigeration and AC maintenance may support the respondent's objective to work in Production/Manufacturing because many large companies require in-house HVAC and refrigeration maintenance staff, and the course explicitly provides practical job-oriented skills."
- "There is some catalogue inconsistency about whether the course is offered weekday full time or weekend part time; if a weekend variant is available it may be easier to combine with the respondent's continuing studies."

**Why the model connected this person to this course, in one sentence:** The course provides technical, industrial maintenance skills that directly map to Manufacturing/production-sector work and the respondent's science/maths interest; it is framed for employment and practical competency.


### Course: `COURSE-030` — Motorcycle Mechanic
**Match type:** DIRECT_MATCH
**Evidence strength:** MODERATE — Clear vocational/mechanical alignment with the respondent's stated sector, but narrower occupational focus and missing local/delivery details reduce overall certainty.

**[ACTUAL SURVEY ANSWERS CITED]**
- `ideal_sector` = Manufacturing or production — Mechanical repair and maintenance skills are relevant to production, small-scale manufacturing supply chains, and technical roles within manufacturing firms.
- `plans_after_education` = Look for a job — The course is vocational and explicitly job-oriented, aligning with the respondent's plan to seek employment.

**[PROFILE CONTEXT CITED]**
- `D_educational_cultural_p4`: Profile members often worked while studying and sought employment; short vocational courses are commonly used to enter the labour market (supporting-context-only).

**[COURSE FACTS CITED]**
- "MotorCycle Mechanic course provides practical job-oriented skills; documented as a part-time weekend course in one listing and as full time in another (catalogue shows part time weekends for some records)." (source: COURSE-030 / COURSE-078)

**[LLM INFERENCE]**
- "This vocational mechanic training may be directly useful for immediate employment opportunities in technical/production support roles, consistent with the respondent's plan to look for a job."

**Why the model connected this person to this course, in one sentence:** Direct technical/mechanical content maps to the respondent's Manufacturing/production sector preference and employment-focused intentions; some course instances are part-time which could suit students working while studying.


---

## 7. UNUSED INFORMATION

Everything below was present in the constructed input the model received, but does not appear in any `direct_respondent_evidence_used`, `profile_context_used`, or course-citation field of any of the 4 final recommendations above.

**Unused actual survey answers (35 of 38 given):**
`ideal_work_type`, `expected_highest_edu_d`, `district`, `area_type`, `has_children`, `household_size`, `household_income`, `household_workers`, `household_unemployed`, `primary_earner_status`, `primary_income_source`, `edu_funding_source`, `edu_status`, `worked_while_studying`, `work_while_study_type`, `work_while_study_paid`, `work_while_study_hours`, `work_while_study_motivation`, `current_activity_status`, `already_job_searching`, `re_entered_education`, `institution_type`, `job_search_method_d`, `age_group`, `moved_from_origin`, `move_reason`, `employment_network_quality`, `edu_min_for_decent_job`, `most_important_life_goal`, `most_useful_quality_for_job`, `social_capital_in_edu_access`, `study_motivation_type`, `autonomy_in_study`, `competence_in_study_field`, `relatedness_at_institution`

Notably, `ideal_work_type` (Work for a multinational or large private company) and `expected_highest_edu_d` (Post-graduate degree) — both DIRECT_PREFERENCE_OR_INTENT answers — were given to the model but never cited in any of the 4 recommendations; the model relied on `ideal_sector`, `study_field_preference`, and `plans_after_education` as sufficient direct grounding instead.

**Unused profile membership:** `D_economic_p1` — this respondent's third frozen profile (economic resources and household pressure) was supplied in full but not cited in any of the 4 recommendations' `profile_context_used` fields.

**Unused retrieved courses (11 of 15 retrieved):** the model was given the complete document for every course below but did not recommend any of them:
- `COURSE-012` — Refrigeration & Air Conditioning Technician
- `COURSE-031` — National Diploma In Television Program Production
- `COURSE-028` — Lapiderist (Gem Cutting)
- `COURSE-029` — Mobile Phone Repair Technician
- `COURSE-077` — Mobile Phone Repair Technician
- `COURSE-078` — Motorcycle Mechanic
- `COURSE-042` — Automobile Electrician
- `COURSE-081` — Radio, TV & Allied Equipment Repairer
- `COURSE-006` — National Diploma In Information & Communication Technology
- `COURSE-021` — Automobile Electrician
- `COURSE-038` — Three Wheeler Mechanic