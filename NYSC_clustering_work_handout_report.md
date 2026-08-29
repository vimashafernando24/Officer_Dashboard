# NYSC Youth Transition Survey

## Data preparation and clustering work completed to date

**Handout report**  
**Project:** Youth Labour Market Programme Matching through Unsupervised Clustering of School-to-Work Transition Profiles  
**Researcher:** Fernando W. S. V. — IT22166456 — R26-DS-014  
**Partner:** National Youth Services Council (NYSC), Sri Lanka  
**Status date:** 25 August 2026

---

## 1. Purpose of this handout

This document records the complete analysis journey so far: what data were received, how the survey export was cleaned, how the correct final branch was reconstructed, which clustering approaches were tried, which results were retained or rejected, what the current method is, and what work remains.

The most important conclusion is that a visually attractive or internally stable clustering is not automatically a valid youth typology. A result is retained only when the variables form a defensible theoretical dimension, the solution is reasonably stable across samples and algorithms, no single question simply dictates membership, the profiles are large enough to interpret, and the profiles have a coherent programme-relevant meaning.

This handout distinguishes three statuses:

- **Retained:** suitable for cautious exploratory reporting.
- **Excluded/rejected:** analysed, but the evidence was not strong enough to use it as a youth profile system.
- **Historical/provisional:** an earlier method that helped the analysis develop but is no longer the adopted final approach.

---

## 2. Research purpose and theoretical plan

The supervisor preparation document proposed identifying youth transition profiles and later mapping them to NYSC's 95-course catalogue. It combines three complementary frameworks.

| Framework | Contribution to the survey and analysis |
|---|---|
| ILO School-to-Work Transition Survey (SWTS) | Labour-market position, education-to-work pathway, employment conditions, job search, barriers and branch structure. |
| Bourdieu's forms of capital | Economic resources, cultural/educational capital, social-network resources and labour-market field position. |
| Self-Determination Theory (SDT) | Autonomy, competence, relatedness and the type of motivation guiding study, search or work. |

The survey first places respondents into a current transition branch and then asks branch-specific questions:

| Research branch | Meaning |
|---|---|
| D | In education |
| E | Unemployed and actively seeking/transitioning |
| F | Employed, including temporary absence with a job to return to |
| G | Inactive/not currently seeking work |

The original plan mentioned clustering many encoded variables and using PCA. The work showed that this can produce weak or uninterpretable groups. The adopted approach therefore became **dimension-specific clustering on original questionnaire responses**, followed only later—if justified—by richer integrated profiles.

---

## 3. Data received and reconstruction problem

### 3.1 Raw export

The raw CSV contained **481 submissions and 2,547 flattened columns**. The large column count occurred because several generations of the application export were present:

- newer `answers.<question>.*` fields;
- intermediate `analysis.items[...]` fields;
- explicit `analysis.values.*` and `analysis.labels.*` dictionaries; and
- older top-level survey fields.

The notebook reconstructed one canonical survey row per submission across these formats. Only answers identified as belonging to the active survey path were used; audit copies and off-path payloads were not treated as genuine answers.

### 3.2 Where readable and numbered values came from

The readable values were **not manually invented**. For newer records:

- `answers.<question>.value` supplied the internal value/code; and
- `answers.<question>.label` supplied the readable response wording.

Equivalent value and label fields were recovered from the intermediate and legacy layouts. Two parallel datasets were preserved:

- `nysc_survey_cleaned_values.csv` for reproducible transformations; and
- `nysc_survey_cleaned_labels.csv` for readable interpretation.

Ordinal numbers were used only when the questionnaire itself defined an order. Binary yes/no fields became 1/0. Nominal categories such as occupation, sector, obstacle and contract-reason categories were not given invented rankings. For the general ML-ready export, nominal variables were one-hot encoded. In the final dimension-specific clustering, nominal responses were compared directly using Gower same/different distance.

Explicit compatibility mappings were needed for a few old textual values, such as age bands and residence type. These mappings harmonised equivalent historical labels; they did not create new substantive scores.

---

## 4. Cleaning and quality filtering

### 4.1 Cleaning operations

The cleaning notebook performed the following operations:

1. Standardised blank and missing tokens such as empty strings, `NA`, `null`, `undefined` and `missing`.
2. Reconstructed canonical response variables across all export layouts.
3. Used only active-path responses.
4. Preserved both internal values and readable labels.
5. Reconstructed entry branch and final active branch separately.
6. Removed known test/debug/smoke records.
7. Required a recognised D/E/F/G branch, an in-scope age of 15–35 and at least ten recovered answers.
8. Treated repeated session IDs as resubmissions and retained the latest submission.
9. Preserved legacy submissions with distinct database IDs.
10. Kept possible outliers for review rather than deleting them automatically.
11. Produced missingness, numeric-conversion, outlier, branch-correction and quality-audit files.

### 4.2 Record accounting

Quality-rule counts can overlap; therefore, they should not be added together as independent deletions.

| Stage or audit flag | Records |
|---|---:|
| Raw submissions | 481 |
| Known test submissions | 11 |
| Outside the target age range | 30 |
| Unrecognised or missing branch | 10 |
| Too few recovered answers | 14 |
| Eligible before deduplication | 443 |
| Duplicate/resubmission records removed | 51 |
| Final cleaned master dataset | 392 |

No record was flagged as explicitly incomplete by the export status. The final cleaned master file contains 392 rows and 171 canonical/admin columns.

### 4.3 Three analytical populations that must not be confused

| Population | D | E | F | G | Total | Use |
|---|---:|---:|---:|---:|---:|---|
| Cleaned master, including historical routing fallbacks | 195 | 38 | 90 | 69 | 392 | Data preservation and audit |
| New-structure translated final-active-branch records | 191 | 34 | 82 | 56 | 363 | New survey structure analyses |
| Strict new-structure records after integrity exclusion | 191 | 34 | 81 | 56 | 362 | Current valid clustering cohorts |

The additional 29 cleaned records outside the new-structure cohort consist of **six legacy final-active-branch records** and **23 entry-branch fallback records**. They remain in the cleaned master data but are not mixed into strict final-path clustering.

---

## 5. Correct final-branch logic

### 5.1 Why the entry branch was insufficient

The answer to the initial activity gateway records where a person first entered the branch system. A respondent can later switch branch—for example, an apparently unemployed respondent may reveal that they are not actively seeking work and move to inactivity. Therefore, the entry branch cannot always be the analytical branch.

### 5.2 Final branch rule used

The newer application used implementation section letters that were one position earlier than the research report. They were translated as follows:

| Application section | Research branch |
|---|---|
| C | D — In education |
| D | E — Unemployed |
| E | F — Employed |
| F | G — Inactive |

For new survey records, the last branch-specific section in `path.active_sections` was treated as authoritative. This corrects cases where `path.active_branch` remained stale after a mid-survey branch switch. If final-path metadata was absent, a legacy final branch was used; the initial entry branch was the last fallback only.

The logic retained:

- 31 records whose final branch differed from their entry branch;
- 11 mid-survey path disagreements that were explicitly corrected; and
- one Branch F integrity problem for audit but exclusion from employed clustering.

The integrity case had final Branch F and current activity recorded as working, but no `employment_status`. Because a valid employed path should contain that core response, the record was not allowed into Branch F clustering.

**Conclusion:** the correct final analytical branch is being used for the new survey structure, including respondents who switched branches during the survey. Historical fallback records remain separately identifiable and are not silently treated as equally reliable final-path records.

---

## 6. General preprocessing outputs

The cleaning notebook created a general-purpose analysis-ready layer and ML-ready alternatives.

| Operation | Rule used |
|---|---|
| Structural missingness | Off-branch unanswered fields recorded as `not_applicable`. |
| Genuine missingness | Applicable but unanswered fields recorded as `missing`. |
| Ordinal variables | Questionnaire order preserved. |
| Binary variables | 0/1 mapping. |
| Nominal variables | One-hot encoding in ML-ready matrices. |
| Numeric imputation | Median, after quality filtering. |
| Nominal imputation | Explicit/mode category in ML-ready pipeline. |
| Scaling | StandardScaler after imputation. |
| PCA | Components retained until at least 85% variance. |
| Outliers | Diagnosed with audit tables; not automatically deleted. |

The complete cleaned dataset had 131 model variables present, expanded to 621 encoded features. Thirty-six PCA components retained 85.32% of the variance.

| Branch master matrix | Rows | Input variables | Encoded features | PCA components | Variance retained |
|---|---:|---:|---:|---:|---:|
| D | 195 | 48 | 204 | 33 | 85.31% |
| E | 38 | 60 | 205 | 20 | 86.41% |
| F | 90 | 84 | 284 | 34 | 85.22% |
| G | 69 | 49 | 200 | 24 | 85.14% |

These counts describe the broad cleaned master matrices. The later clustering notebooks rebuild stricter final-path cohorts and generally use original responses with Gower distance instead of the imputed/PCA matrices.

---

## 7. Why the analysis moved to dimension-specific clustering

### 7.1 First Branch D all-variable experiment

The initial Branch D experiment used 191 strict final-Branch-D respondents, 48 candidate input variables, 197 expanded features and 71 PCA components. K-means tested `k=2–5`, with holdout and comparison diagnostics.

No acceptable solution was found. The diagnostic `k=2` result contained 183 respondents in one cluster and only 8 in the other. Although the training silhouette was 0.410, only one cluster appeared in the holdout data. This demonstrated that a good-looking single metric can coexist with an unusable typology.

### 7.2 Proposed Level 1 and Level 2 strategy

The analysis then proposed:

- **Level 1:** group theoretically related variables into dimensions and identify dimension-specific response profiles.
- **Level 2:** represent each dimension once and create integrated whole-person transition profiles.

An early Level 1 notebook constructed five 0–100 dimension scores using researcher-defined mappings and equal weights. A Level 2 k-means analysis produced a provisional three-profile solution of sizes 52, 87 and 52. However, it passed only two of five quality checks: silhouette 0.186, bootstrap ARI mean 0.574, bootstrap ARI 10th percentile 0.299, K-medoids agreement ARI 0.505 and Ward agreement ARI 0.408. Forty-seven memberships were low-confidence.

More importantly, the lecturer's criticism was correct: a researcher cannot claim a validated theoretical score merely by inventing numerical category mappings and averaging them. The agency diagnostic alpha was also only approximately 0.551. Consequently:

> The constructed-score Level 1/Level 2 solution is retained only as a historical experiment and must not be reported as the final youth typology.

The current method clusters original responses inside theoretically defensible dimensions and does not invent total-score formulas.

---

## 8. Current adopted clustering method, in simple terms

### 8.1 Feature selection

Choosing which survey questions belong to each dimension is a form of **theory-guided feature selection**. Fewer variables do not automatically make clusters more stable. The aim is to use enough relevant, non-duplicative variables to represent one coherent concept.

Theory proposes a candidate grouping, but data-quality checks decide whether each variable has enough coverage and variation. Stability tests then decide whether the respondent groups are reproducible. Neither theory nor a high score alone is sufficient.

### 8.2 Gower distance

For each question, the method measures how different two respondents are:

- ordered response: difference in rank divided by the possible rank range;
- numeric response: absolute difference divided by its observed/theoretical range;
- nominal response: 0 if the answers match and 1 if they differ;
- missing response: that question is omitted for that respondent pair.

The overall distance is the equal-weight mean of the available question-level differences:

\[
d(i,j)=\frac{\sum_p w_{ijp}\,\delta_{ijp}}{\sum_p w_{ijp}}
\]

No respondent receives an invented motivation, capital or readiness score. Gower distance only expresses how different two original response patterns are.

### 8.3 K-medoids, spectral clustering and consensus

- **K-medoids** groups respondents around actual respondents called medoids. It is compatible with Gower distance and keeps profiles interpretable.
- **Spectral clustering** provides a different way of partitioning the same Gower-based relationships.
- For retained consensus analyses, each method is run on 100 matched 80% respondent subsamples, creating 200 base partitions.
- For every respondent pair, the consensus value is:

\[
C_{ij}=\frac{\text{times respondents }i,j\text{ were clustered together}}
{\text{times both were sampled}}
\]

- Final profiles are obtained by K-medoids on `1 − C`.

Consensus is not automatically superior. It is accepted only if it is reproducible, has clear within-profile blocks, agrees reasonably with both source methods and produces meaningful profiles.

### 8.4 Validation evidence used

| Diagnostic | Meaning |
|---|---|
| Silhouette | Whether respondents are closer to their own profile than alternatives. |
| Adjusted Rand Index (ARI) | Agreement between two partitions, corrected for chance; 1 means identical, around 0 means little agreement beyond chance. |
| Subsample/bootstrap stability | Whether broadly the same grouping returns when respondents are resampled. |
| Cross-algorithm ARI | Whether the result depends heavily on one algorithm. |
| Minimum profile size | Prevents tiny groups being overinterpreted. Most dimension analyses used at least 15. |
| Leave-one-feature-out ARI | Tests whether removing one variable destroys the solution. |
| Encoding sensitivity | Tests reasonable alternative treatments of ambiguous variable types. |
| Respondent confidence | Flags respondents near a profile boundary. |
| PAC | Proportion of pairwise consensus values lying in an ambiguous middle interval. Lower is clearer, but it is used comparatively. |
| Prediction strength | Tests whether clusters learned in training data reproduce in held-out respondents. |
| Permutation-null calibration | Checks whether the best result found after searching many combinations is better than results from independently shuffled variables. |

There is no universally justified rule that `PAC ≤ 0.20` proves validity. The earlier discussion therefore led to a correction: PAC is now reported comparatively across candidate solutions and is not used as a universal pass/fail threshold.

Scatterplots are two-dimensional displays of a higher-dimensional distance structure. Their horizontal and vertical axes are display coordinates such as MDS/PCA axes, not questionnaire scores and not the variables used to create the clusters. Cluster validity comes from the diagnostics and original-response profiles, not from how separated coloured dots appear.

---

## 9. Branch D — In Education

### 9.1 Strict cohort

All current Branch D dimension analyses use 191 new-structure respondents whose final translated active branch is D.

The broad Branch D analysis-ready manifest contains 48 variables:

`age_group`, `gender`, `district`, `area_type`, `moved_from_origin`, `move_reason`, `marital_status`, `age_first_married`, `spouse_activity`, `has_children`, `num_children`, `father_edu`, `mother_edu`, `father_occ`, `mother_occ`, `household_size`, `household_income`, `household_workers`, `household_unemployed`, `primary_earner_status`, `employment_network_quality`, `edu_status`, `highest_edu_completed`, `edu_end_year`, `spell1_activity`, `spell1_is_current`, `worked_while_studying`, `edu_min_for_decent_job`, `most_important_life_goal`, `most_useful_quality_for_job`, `ideal_work_type`, `ideal_sector`, `primary_income_source`, `current_activity_status`, `plans_after_education`, `already_job_searching`, `re_entered_education`, `reason_re_entered`, `expected_highest_edu_d`, `study_field_preference`, `institution_type`, `edu_funding_source`, `social_capital_in_edu_access`, `study_motivation_type`, `autonomy_in_study`, `competence_in_study_field`, `relatedness_at_institution`, `job_search_method_d`.

Not all 48 variables were placed in clustering distances. Demographics and programme-mapping variables remain descriptors; conditional variables are used only where applicable.

### 9.2 Branch D dimension results

| Dimension | Variables/components used | Profiles and evidence | Current decision |
|---|---|---|---|
| Motivation and study experience | `study_motivation_type`, `autonomy_in_study`, `competence_in_study_field`, `relatedness_at_institution` | Consensus k=3; sizes 47, 75, 69; Gower silhouette 0.350; bootstrap ARI mean 0.981; ARI against K-medoids 0.968 and spectral 0.712; PAC 0.193. | **Retained for exploratory dimension-specific profiling, with ambiguity and single-item/ordinal-spacing cautions.** |
| Economic resources and household pressure | Household income; worker and unemployed household proportions; primary-earner responsibility; primary income source; education funding source | k=2; sizes 44 and 147; Gower silhouette 0.436; bootstrap ARI mean 0.986; K-medoids/spectral agreements 0.849/0.796; seven of eight checks passed. | **Retained with caution.** Profiles indicate relatively lower versus relatively higher household economic position. |
| Educational trajectory and cultural capital | Parental education, expected education, institution type, work while studying, re-entry into education | k=4; sizes 15, 53, 57, 66; Gower silhouette 0.427; bootstrap ARI mean 0.963; K-medoids/spectral agreements 0.776/0.934; all eight checks passed. | **Retained.** Stable, cross-method-supported exploratory segmentation. |
| Transition planning and direction | `plans_after_education`, `ideal_work_type`, `ideal_sector`, `study_field_preference` | Diagnostic k=2; sizes 120 and 71; Gower silhouette 0.245; spectral agreement ARI 0.137; PAC 0.751; only five of eight checks passed. | **Rejected.** No sufficiently robust transition-planning profiles. |
| Social connectedness and support pathways | `employment_network_quality`, `relatedness_at_institution` | Statistically stable k=3; sizes 51, 83, 57; algorithms agreed perfectly in this discrete two-item pattern. | **Excluded from the final dimension set.** `relatedness_at_institution` is already used in motivation; retaining this dimension would double-count it. |

### 9.3 Retained Branch D profile interpretations

**Motivation/study experience:**

1. Externally or uncertainly motivated, with moderate study support — 47.
2. Goal-aligned motivation with mixed confidence and support — 75.
3. Highly self-directed, capable and connected — 69.

These names describe four questionnaire responses only; they are not psychological diagnoses or validated SDT types. Approximately 23.6% had low Gower membership confidence, so individual classification must preserve uncertainty.

**Economic resources:**

1. Relatively lower household economic position — 44.
2. Relatively higher household economic position — 147.

Twenty-nine respondents declined household income. Five records had workers plus unemployed greater than household size. Those inconsistent proportions were treated as unavailable rather than silently corrected; the remaining components were compared through missing-aware Gower distance.

**Educational trajectory/cultural capital:**

1. Re-entered students, often with degree-educated parents — 15.
2. State-institution students without work exposure — 53.
3. Private-institution students without work exposure — 57.
4. Work-experienced students, mainly in private institutions — 66.

Parental education is used as a proxy/indicator of family cultural capital, not as a measure of intelligence or respondent merit.

### 9.4 `highest_edu_completed` and related education issue

`highest_edu_completed` was not generally missing because of a cleaning error. It was observed for only 3 of the 191 current-student respondents because the question is conditional on having completed or left education. It was therefore excluded from Branch D distance. `edu_status` was also excluded: it was more than 90% one category and contained six answers conflicting with the final current-attendance route. The final branch remained authoritative.

### 9.5 Candidate dimensions deliberately not created

- **Parental occupation:** Bourdieu makes parental social position relevant, but father/mother occupation alone is not a ready-made validated capital scale. A defensible occupational-class crosswalk would be required. The variables remain descriptors and were not silently ignored.
- **Family responsibilities:** responsibility is partly represented through household structure and primary-earner status. Sparse conditional marital/child questions did not support a separate all-respondent dimension.
- **Life goals and plans:** `most_important_life_goal` and `plans_after_education` are meaningful descriptors, but combining two nominal questions into a single score or claiming one latent construct was not sufficiently grounded.
- **Beliefs:** proposed belief items did not form a published, validated multi-item scale in this survey. They were retained descriptively rather than combined through invented formulas.
- **Social connectedness:** excluded despite statistical stability because it overlapped with the retained motivation dimension.

---

## 10. Attempted global household-economic clustering

The idea was to cluster all new-structure branches together using common household questions, then examine the same dimension within each branch. The global analysis included 363 respondents: D=191, E=34, F=82 and G=56. Branch identity was not used as a clustering input.

The four distance inputs were household income, household size, household workers and household unemployed. Primary-earner status and primary income source were moved to descriptors because they tended to recreate direct questionnaire/branch splits.

The diagnostic k=2 result had groups of 135 and 228 and Gower silhouette 0.365. However, agreement with full K-medoids was ARI 0.011, raw-count sensitivity was also ARI 0.011, and PAC was 0.609. Only six of nine checks passed.

**Decision:** the global household-economic segmentation was rejected. The global approach was paused, and the analysis returned to branch-by-branch dimensions.

---

## 11. Branch F — Employed

### 11.1 Cohort and survey-variable accounting

There are 82 new-structure final-Branch-F records. One routing-integrity record lacks `employment_status`, leaving **81 valid employed respondents** for clustering.

The branch-specific modelling manifest originally showed 84 variables: 39 common variables plus 45 retained employed variables. A later full active-path audit found **105 collectively answerable Branch F variables**, because it also counted conditional follow-ups and employee/self-employed subgroup questions. This is not a contradiction; the two counts describe different inventories.

Among the 81 valid employed respondents:

- wage-worker subgroup: 70;
- self-employed subgroup: 11.

### 11.2 Theory-led Branch F dimensions

| Code | Proposed dimension | Variables | Theory/rationale |
|---|---|---|---|
| D1 | Household economic resources and responsibility | `household_income`, `household_size`, `household_workers`, `household_unemployed`, `primary_earner_status`, `primary_income_source` | Bourdieu economic capital plus SWTS household position. Raw indicators, not a published scale. |
| D2 | Educational and inherited cultural capital | `father_edu`, `mother_edu`, `edu_status`, `worked_while_studying` | Family education and education/work trajectory. Parental education is only a proxy. |
| D3 | Employment security and formality | `contract_type`, `job_security_12months`, `sector_formality` | SWTS employment quality and labour-market field position. |
| D4 | Earnings and working-time adequacy | `monthly_income_band`, `usual_hours_per_week`, `income_hours_preference` | SWTS employment conditions and under/over-employment preference. |
| D5 | Job satisfaction and mobility intention | `job_satisfaction`, `contract_satisfaction`, `hopes_to_change_job` | SWTS satisfactory employment and intention to change jobs. Contract reasons remain nominal. |
| D6 | Qualification use and skill development | `qualification_job_match`, `past_edu_useful_for_job`, `received_training` | Cultural-capital utilisation and education/training relevance. |
| D7 | Professional social capital | `employment_network_quality`, `professional_network_growth` | Access to useful contacts and network expansion. |
| D8 | Work motivation and psychological need experience | `work_autonomy`, `competence_growth_at_work`, `relatedness_at_work`, `work_motivation_type` | SDT autonomy, competence, relatedness and motivation style. One item per construct; not a validated scale. |
| D9 | Transition-to-work search pathway and barriers | `registered_as_jobseeker`, `employment_service_help_f`, `jobs_applied_before_hire`, `interviews_before_hire`, `search_duration_before_hire`, `obstacle_finding_this_job` | SWTS search intensity, duration, institutional help and barriers. |

### 11.3 Branch F dimension decisions

| Dimension/attempt | Main empirical result | Final decision |
|---|---|---|
| D1 Household economic resources and responsibility | Dedicated k=2 consensus produced sizes 21/60, silhouette 0.470 and bootstrap ARI mean 0.994, but the single `primary_income_source` partition agreed at ARI 0.845; removing that item changed the result to ARI −0.036; the three structural-resource components agreed at ARI 0.000; searched permutation p=0.059. | **Rejected for clustering; retain indicators for descriptive/programme-feasibility analysis.** The result mainly distinguished family-supported from own-job-supported income rather than two broad economic-resource positions. |
| D2 Educational and inherited cultural capital | No k=2–4 candidate kept at least 15 respondents per cluster under both algorithms. Diagnostic k=2 produced K-medoids sizes 21/60 but spectral minimum size 14; mean silhouette 0.461; cross-algorithm ARI 0.647; K-medoids/spectral stability means 0.898/0.713; permutation p=0.683. `worked_while_studying` was the strongest driver (single-item ARI 0.571; leave-out ARI 0.243). | **Rejected for clustering; retain parental education, education status and work exposure for descriptive/programme-mapping analysis.** Diagnostic groups must not be named as profiles. |
| Broad six-variable employment-quality attempt | k=3, sizes 29/25/27, silhouette 0.263, spectral agreement ARI 0.444, six of eight checks. | **Rejected.** Too broad and not sufficiently cross-method robust; replaced by clearer D3 and D4 dimensions. |
| D3 Employment security and formality | k=2, sizes 29/52; silhouette 0.368; bootstrap ARI mean 0.953; K-medoids and spectral agreements 0.854/0.950; seven of eight checks. | **Retained with PAC/ambiguity caution.** |
| D4 Earnings and working-time preference | k=2, sizes 51/30; silhouette 0.525; bootstrap ARI mean 0.995; eight of eight checks; leave-out preference ARI −0.013. | **Excluded from the final dimension set by researcher decision.** Retain only as a descriptive diagnostic because it mainly repeats the working-hours/income preference answer rather than forming a multidimensional employed-youth profile. |
| D5 Job satisfaction and mobility intention | Apparent k=2 sizes 34/47 and good internal stability, but removing `hopes_to_change_job` produced ARI −0.007; PAC 0.519; detailed/binary contract encoding ARI 0.488. | **Rejected for clustering; keep for descriptive analysis.** It mostly reproduced one intention question. |
| D6 Qualification use and skill development | Initial k=2 sizes 65/16 appeared perfectly stable, but exactly reproduced `received_training`; removing it gave ARI 0.014. The two-variable retest had weak source-algorithm agreement, ARI 0.097–0.212. | **Rejected for clustering; keep for descriptive analysis.** |
| D7 Professional social capital | Two direct indicators available. | **Skipped/excluded under the prior no-overlapping-social-connectedness decision.** Keep as descriptors unless scope is revised. |
| D8 Work motivation/psychological needs | No k=2–4 solution met the cross-algorithm minimum-size rule. Diagnostic k=3 spectral agreement ARI 0.330; alternative motivation encoding ARI 0.248. | **Rejected for clustering; keep for descriptive analysis.** |
| D9 Search pathway and barriers | Diagnostic k=2 sizes 48/33; silhouette 0.165; bootstrap ARI mean 0.532; spectral agreement ARI 0.038; 35.8% low-confidence. Raw/log count agreement ARI 0.902. | **Rejected for clustering; count preprocessing was not the main problem.** |

### 11.4 Retained Branch F profile system and excluded D4 diagnostic

**D3 Employment security and formality**

1. Temporary/no-contract employment with uncertain security — 29.
2. Predominantly permanent employment with stronger security — 52.

This is a defensible employment-condition pattern, but it is still exploratory and should be checked with more data and expert interpretation.

**D4 Earnings and working-time preference — excluded from the final clustering set**

1. Mostly current-hours preference — 51 (63.0%): 47 wanted to keep hours/income the same and 4 preferred fewer hours/lower income.
2. More-hours/more-income preference — 30 (37.0%): 28 wanted more hours/more income and 2 preferred fewer hours/lower income.

Both profiles had a median monthly-income-band code of 4 and median usual working hours of 40. Therefore, this result must **not** be labelled low income versus high income. It is primarily a preference segmentation and is retained only as a descriptive diagnostic, not as a final Branch F clustering.

### 11.5 Branch F `highest_edu_completed`

In Branch F, `highest_edu_completed` was observed for 21 of 81 respondents. This was caused by conditional education-history routing, not automatic evidence of 60 incomplete surveys. It remains a conditional descriptor and is not placed in an all-Branch-F distance calculation.

---

## 12. Branch F complete 105-variable role audit

The complete audit ensures that no variable was silently forgotten. Only 34 were eligible theory-proposed clustering inputs. The other 71 remain available for interpretation, subgroup analysis, validation or routing audits.

| Role | Count | Variables |
|---|---:|---|
| Proposed clustering inputs | 34 | `household_size`, `household_income`, `household_workers`, `household_unemployed`, `primary_earner_status`, `primary_income_source`, `father_edu`, `mother_edu`, `edu_status`, `worked_while_studying`, `sector_formality`, `contract_type`, `job_security_12months`, `usual_hours_per_week`, `income_hours_preference`, `monthly_income_band`, `contract_satisfaction`, `job_satisfaction`, `hopes_to_change_job`, `qualification_job_match`, `received_training`, `past_edu_useful_for_job`, `employment_network_quality`, `professional_network_growth`, `work_autonomy`, `competence_growth_at_work`, `relatedness_at_work`, `work_motivation_type`, `registered_as_jobseeker`, `employment_service_help_f`, `jobs_applied_before_hire`, `interviews_before_hire`, `search_duration_before_hire`, `obstacle_finding_this_job` |
| Programme/profile descriptors | 30 | `age_group`, `gender`, `district`, `area_type`, `moved_from_origin`, `move_reason`, `marital_status`, `has_children`, `father_occ`, `mother_occ`, `work_while_study_type`, `work_while_study_paid`, `work_while_study_hours`, `work_while_study_motivation`, `edu_min_for_decent_job`, `most_important_life_goal`, `most_useful_quality_for_job`, `ideal_work_type`, `ideal_sector`, `enterprise_location_type`, `occupational_class`, `has_second_job`, `willing_to_relocate_f`, `plans_further_edu_f`, `expected_highest_edu_f`, `union_member`, `ever_refused_job_f`, `acceptance_conditions_search`, `had_min_wage_during_search`, `employment_status` |
| Conditional descriptors | 27 | `age_first_married`, `spouse_activity`, `num_children`, `reason_left_edu`, `highest_edu_completed`, `edu_end_year`, `spell1_activity`, `spell2_activity`, `spell3_activity`, `spell1_is_current`, `spell2_is_current`, `spell1_contract`, `spell2_contract`, `spell1_satisfaction`, `spell2_satisfaction`, `spell1_end_reason`, `spell2_end_reason`, `reason_temp_absence`, `reason_below_normal_hours`, `reason_wants_to_change`, `insecurity_bothers`, `reason_not_union`, `training_type_received`, `training_provider`, `training_duration`, `who_paid_training`, `reason_refused_job_f` |
| Validation/profile descriptors | 4 | `enterprise_registered`, `paid_taxes`, `actual_hours_last_week`, `hours_below_normal` |
| Wage-worker subgroup descriptors | 3 | `job_recruitment_method`, `enterprise_size`, `gender_equality_at_work` |
| Self-employed subgroup descriptors | 5 | `reason_self_employed`, `business_helpers`, `business_funding_source`, `business_profitability`, `main_business_obstacle` |
| Routing/audit only | 2 | `current_activity_status`, `has_job_to_return` |

Why variables were not used directly in every clustering:

- demographics are better used to describe and check equity across profiles than to define needs automatically;
- conditional questions would make distance depend on which follow-up path a person saw;
- subgroup questions cannot fairly compare 70 wage workers with 11 self-employed respondents in one all-Branch-F distance;
- enterprise registration/tax and actual/usual hours can duplicate formality and hours information;
- programme-preference descriptors are most useful after clustering for mapping profiles to interventions;
- routing variables should validate cohort membership, not recreate the known branch.

The detailed question-by-question table, with question IDs, wording, coverage and framework metadata, is preserved in `branch_f_variable_dimension_selection_report.md` and `outputs/branch_f_variable_dimension_audit/branch_f_all_105_variables.csv`.

---

## 13. Branch G — Inactive: variable and dimension audit

The next branch selected for analysis was Branch G because it contains 56 strict final-path respondents, compared with only 34 in Branch E. A complete active-path audit identified 62 collectively answerable variables. The first requested clustering test, G1 household economic resources and dependency, has now also been completed.

| Variable role | Count |
|---|---:|
| Proposed clustering inputs | 19 |
| Profile/programme-mapping descriptors | 21 |
| Conditional descriptors | 13 |
| Routing/audit variables | 9 |

Five candidate dimensions were proposed:

| Code | Candidate dimension | Variables | Main caution |
|---|---|---|---|
| G1 | Household economic resources and dependency | `household_income`, `household_size`, `household_workers`, `household_unemployed`, `primary_earner_status`, `primary_income_source` | Five household-count conflicts; income source could dominate. |
| G2 | Educational and inherited cultural capital | `father_edu`, `mother_edu`, `edu_status`, `worked_while_studying` | Parental education is a proxy; prior branches produced weak/work-exposure-led solutions. |
| G3 | Inactivity pathway and future engagement intention | `reason_not_in_labour_force`, `ever_worked`, `wants_to_work_future`, `wants_further_edu` | The 13-category inactivity reason may directly control the partition. |
| G4 | Psychological readiness and support for engagement | `future_orientation_g`, `employment_self_efficacy`, `support_for_engagement` | One item per component; original answers must be clustered without claiming a validated SDT scale. |
| G5 | Labour-market social connection | `employment_network_quality`, `labour_market_connection` | Only two closely related indicators; a cross-tab may be more appropriate than clustering. |

All 19 proposed inputs have complete canonical coverage. Three respondents declined household income and five household-count records require pairwise unavailability rather than silent correction. `time_use_decision_maker`, `expected_highest_edu_g`, parental occupations, demographics and conditional histories remain descriptors. Nine unemployment/temporary-absence gateway variables encountered before final rerouting remain audit fields and do not enter all-Branch-G distances.

### 13.1 G1 household economic resources and dependency result

G1 used the six audited source variables without constructing an economic-capital score. Household size formed worker and unemployed shares and therefore did not receive a second independent weight. Missing-aware Gower distance compared five equal-weight components, and a 200-partition K-medoids/spectral consensus selected two profiles.

| Profile | Records | Percent | Main pattern |
|---|---:|---:|---|
| Predominantly family/partner-supported non-provider | 41 | 73.2% | 90.2% were not the main household provider; 75.6% relied mainly on parents/family and 14.6% on a partner/spouse. |
| Predominantly self-income provider/contributor | 15 | 26.8% | 86.7% were the main or a shared earner; 66.7% reported a regular job/business as their main personal income source. |

All nine prespecified screening checks passed: Gower silhouette 0.372, ensemble bootstrap mean ARI 1.000, agreement with full K-medoids 0.854 and spectral clustering 0.718, minimum profile size 15, and a 100-repetition permutation p-value of 0.012. The result is not exactly reproduced by one item, although primary income source is the strongest item (ARI 0.640).

The interpretation is deliberately narrower than the original title. Structural resources alone—income position and household worker/unemployed shares—had ARI -0.016 with the final grouping. Removing income source also reduced agreement to ARI 0.356. The result is therefore retained cautiously as a **household economic role/dependency segmentation**, not a low-versus-high household-resource or validated economic-capital classification.

### 13.2 G4 psychological readiness and support result

G4 used `future_orientation_g`, `employment_self_efficacy`, and `support_for_engagement` as three equal-weight ordered responses. All 56 respondents answered all three, and no combined psychological score was created. No k=2–4 candidate met the cross-algorithm minimum-profile-size rule. The diagnostic k=2 solution formed groups of 45 and 11. It had good separation (silhouette 0.539), high ensemble stability (mean ARI 0.984) and permutation p=0.010, but K-medoids agreement was only ARI 0.590. Removing self-efficacy changed the grouping almost completely (ARI -0.017), and the smaller group was below the minimum size of 15.

G4 is therefore **excluded from clustering**. The three answers remain useful as descriptive indicators for programme planning, but the diagnostic groups must not be assigned to respondents as validated profiles.

### 13.3 G3 inactivity pathway and future engagement result

G3 used four complete original categorical answers: inactivity reason, previous work experience, desire for future work, and desire for future education/training. The selected two-profile consensus passed all ten screening checks: Gower silhouette 0.413, ensemble bootstrap mean ARI 1.000, K-medoids/spectral agreement 0.928/1.000, minimum profile size 21 and permutation p=0.011.

| Profile | Records | Percent | Main pattern |
|---|---:|---:|---|
| Work-and-education engaged, mostly prior work experience | 35 | 62.5% | 97.1% wanted future work, 85.7% wanted further education and 82.9% had worked before. |
| Low/uncertain engagement, mostly no prior work experience | 21 | 37.5% | 71.4% did not want future work, 61.9% were unsure about further education and 76.2% had never worked. |

The result is retained with a narrower interpretation. Removing the 13-category inactivity-reason question reproduced the partition exactly (ARI 1.000), so it did not define the separation. These are **future-engagement/prior-work-experience profiles**, while current inactivity reason remains a programme-needs descriptor inside each group. No single item alone reproduced the clusters; the maximum single-item ARI was 0.554.

### 13.4 G2 educational and inherited cultural capital result

G2 used ordered father/mother education, nominal education status and binary work-while-studying experience. Unknown/refused parental education was unavailable pairwise, and no cultural-capital score was constructed. Diagnostic k=2 groups of 38 and 18 appeared extremely stable (silhouette 0.474; K-medoids and spectral ARI 1.000), but they exactly reproduced `worked_while_studying`. Removing that one item changed agreement to ARI 0.004, whereas removing either parental-education variable or education status left the split unchanged. Both groups had the same median parental-education position, and the searched permutation p-value was 0.230.

G2 is therefore **rejected as a clustering dimension**. The apparent profiles are simply “did not work while studying” and “worked while studying”, not educational/cultural-capital groups.

All proposed Branch G dimensions are now tested or explicitly skipped:

| Dimension | Decision |
|---|---|
| G1 household economic resources/dependency | Retained narrowly as economic role/dependency profiles |
| G2 educational/inherited cultural capital | Rejected; work-while-studying split |
| G3 inactivity pathway/future engagement | Retained narrowly as future-engagement/prior-work-experience profiles |
| G4 psychological readiness/support | Rejected |
| G5 labour-market social connection | Skipped under the no-overlap decision |

---

## 14. Branch E — Unemployed/searching: variable and dimension audit

Branch E contains 34 strict final-path respondents. Its implementation questions are stored in survey Section D, but the analytical research branch is E. The audit found 75 collectively answerable active-path variables and did not use entry branch as the inclusion rule.

| Variable role | Count |
|---|---:|
| Active candidate clustering inputs | 24 |
| Social-capital inputs skipped under no-overlap decision | 3 |
| Profile/programme-mapping descriptors | 26 |
| Conditional descriptors | 16 |
| Routing/audit variables | 6 |

Seven theory-led dimensions were documented, of which six remain active candidates:

| Code | Candidate dimension | Inputs | Main caution/status |
|---|---|---:|---|
| E1 | Job-search psychological readiness and support | 4 | One item per construct; do not claim a validated SDT/readiness scale. |
| E2 | Search intensity and accumulated exposure | 4 | Application/interview count outliers require raw-versus-log sensitivity. |
| E3 | Economic urgency and job-acceptance constraints | 3 | Urgency or the binary minimum-wage item may dominate. |
| E4 | Education-to-work preparedness and learning orientation | 3 | Related observed indicators, not one validated latent construct. |
| E5 | Household economic resources and dependency | 6 | Income-source dominance and resource-versus-role interpretation. |
| E6 | Educational and inherited cultural capital | 4 | Prior branches produced work-while-studying-led results. |
| E7 | Job-search social capital | 3 | Skipped under the existing no-overlapping-social-connectedness decision. |

Direct intervention fields—main obstacle, desired training, employment-service help and job type sought—remain programme-mapping descriptors rather than cluster-forming inputs. Conditional search method, non-search reason, refusal reason and minimum-wage band are not supplied to an all-Branch-E distance.

The central limitation is sample size: with n=34 and a minimum profile size of 15, only k=2 can be eligible; three profiles would require at least 45 respondents. The complete 75-variable table is in `branch_e_variable_dimension_selection_report.md`.

### 14.1 All Branch E dimensions tested

E1–E6 were tested with equal-weight Gower distance, K-medoids/spectral consensus, 100 ensemble bootstraps, single-feature and leave-one-feature-out checks, and 100 shuffled-variable repetitions. E2 also compared raw and log-transformed count encodings. E7 remained skipped.

| Code | Profiles | Key validation result | Decision |
|---|---:|---|---|
| E1 | 17 / 17 | Spectral ARI 0.403; source minimum 11; p=0.050 | Rejected |
| E2 | 26 / 8 | Exactly reproduced active search; p=0.500 | Rejected |
| E3 | 28 / 6 | Exactly reproduced minimum-wage answer | Rejected |
| E4 | 18 / 16 | Silhouette 0.567; ensemble ARI 0.953; K-medoids/spectral ARI 0.882/1.000; p=0.040 | **Retained cautiously—feature dependent** |
| E5 | 22 / 12 | Source ARI 0.484; ambiguous 38.2%; p=0.583 | Rejected |
| E6 | 24 / 10 | Exactly reproduced work while studying | Rejected |
| E7 | — | No-overlap decision | Skipped |

The retained E4 profiles are:

| Profile | Records | Pattern |
|---|---:|---|
| High perceived education utility and strong learning ambition | 18 | 83.3% rated past education very useful, 94.4% planned further education and 66.7% expected postgraduate education. |
| Moderate perceived utility and mixed learning ambition | 16 | 93.8% rated education somewhat useful; 62.5% planned further education, with the remainder unsure or not planning it. |

E4 passed all ten mandatory checks, but removing `past_edu_usefulness` changed the partition almost completely (ARI 0.039). It must therefore be interpreted narrowly as **education-usefulness and further-learning orientation**, not as a validated human-capital or general learning-readiness scale. The complete evidence and rejection reasons are in `branch_e_clustering_results_report.md`.

---

## 15. Automated Branch F candidate-dimension discovery

Because Branch F has many variables, a new script tested whether defensible combinations inside the theory pools could produce additional stable dimensions. It did **not** search all 105 variables freely and then invent meanings for the best result.

### 15.1 Procedure

1. Restricted the cohort to the 81 valid Branch F respondents.
2. Restricted variables to the 34 audited clustering candidates.
3. Calculated mixed-type variable associations: absolute Spearman for ordered/numeric pairs, bias-corrected Cramér's V for nominal pairs and correlation ratio for nominal/numeric pairs.
4. Bootstrapped descriptive variable grouping 60 times for group counts 2–10.
5. Tested respondent-clustering subsets of 2–4 variables only inside D1–D9 theory pools; D7 was visible in variable grouping but skipped from respondent clustering under the overlap decision.
6. Tested k=2, 3 and 4 with K-medoids and spectral clustering.
7. Evaluated silhouette, cross-algorithm ARI, minimum size and single-variable dominance.
8. Shortlisted at most three candidates per theory pool.
9. Ran 30 train/test prediction-strength splits.
10. Compared the best observed result in each pool with the best result from independently permuted variables.

The script evaluated **414 candidate subset/k solutions** and shortlisted 15.

### 15.2 Preliminary pool-wise null results

| Theory pool | Best observed K-medoids silhouette | Preliminary empirical p-value | Interpretation |
|---|---:|---:|---|
| D1 Household resources | 0.767 | 0.129 | Not better than pool-wise shuffled search at 0.05. |
| D2 Educational/cultural capital | 0.814 | 0.161 | Not better than pool-wise shuffled search. |
| D3 Security/formality | 0.562 | 0.484 | No additional discovery evidence. |
| D4 Earnings/time | 0.689 | 0.258 | No additional discovery evidence. |
| D5 Satisfaction/mobility | 0.837 | 0.129 | Attractive raw result, but not beyond searched-null evidence. |
| D6 Qualification/skills | 0.833 | 0.194 | Top candidates were entirely dominated by `received_training`. |
| D8 Motivation/needs | 0.767 | 0.581 | No additional discovery evidence. |
| D9 Search pathway | 0.801 | 0.290 | No additional discovery evidence. |

The descriptive variable grouping selected eight groups by the highest median bootstrap ARI, but its median stability was only about 0.497 and agreement with the theory pools was very low (ARI about 0.04). These data-driven groups must not be named as new constructs.

**Current discovery conclusion:** no extra Branch F dimension was automatically confirmed. This is a useful result: it prevents selecting a high silhouette that arose because many combinations were searched or because one categorical question created an easy split.

The current run used 30 null repetitions as a runtime-feasible screen. At least 200 repetitions should be used before reporting final empirical p-values. Even a significant result would still require theoretical review and preferably confirmation in additional respondents.

---

## 16. What clustering can and cannot do for NYSC programmes

### 16.1 What the profile means

The purpose of dimension-specific clustering is to identify the response profile to which an individual is most similar **within a particular dimension**. A person can simultaneously belong to:

- one economic-resource profile;
- one education/cultural-capital profile;
- one motivation profile; and
- one employment-security or working-time profile, depending on branch.

These are current conditions, not permanent identities.

### 16.2 How existing courses could be recommended

Clustering alone does not know which course is best. It first identifies needs and constraints. A separate, transparent programme-matching layer must then compare those profiles and descriptors with a structured NYSC catalogue containing:

- occupational category and skills taught;
- entry prerequisites and appropriate NVQ level;
- full-time/part-time/weekend format;
- duration;
- location and accessibility;
- cost, stipend or financial-support options;
- employer placement, internship or certification support; and
- support services such as counselling, job-search help or childcare referrals.

A safe recommendation sequence is:

1. **Profile need:** what barrier, resource, motivation or employment condition is indicated?
2. **Individual preference:** ideal sector/work type, location, willingness to relocate and further-study plan.
3. **Eligibility:** education, existing qualification and course prerequisites.
4. **Feasibility:** income urgency, household responsibility, time availability and delivery format.
5. **Expert-reviewed match:** score eligible courses using published programme attributes and NYSC expert rules.
6. **Uncertainty:** show alternatives and flag uncertain cluster membership instead of forcing one recommendation.

For example, an employed respondent with insecure informal work and a preference for current hours may need certification/formalisation support delivered part-time; an employed respondent wanting more hours/income may need an upgrading pathway with stronger placement prospects. The actual course recommendation must also use sector preference, qualifications, prerequisites and catalogue availability.

### 16.3 How programme gaps can be identified

A programme gap exists when a sizeable, stable and meaningful profile has a documented need but the catalogue has no feasible response. Examples include:

- suitable skills course exists, but only full-time delivery is offered to primary earners;
- technical course exists, but no bridging module meets the profile's entry qualification;
- training exists, but no placement/network component addresses weak employment contacts;
- course exists, but a profile first needs counselling, confidence-building or job-search support;
- employed youth need recognition/upgrading of existing skills rather than beginner training.

Gap claims should combine cluster size, confidence, descriptor distributions, catalogue evidence and NYSC expert review. Clusters suggest where to look; they do not by themselves prove that a new programme is necessary.

---

## 17. Answers to recurring methodological questions

### Does more data make clusters more stable?

Usually, more representative data allow more reliable estimation and make genuine structures easier to reproduce. There is no guarantee. More records can reveal that an apparent cluster was sample noise, expose previously absent subgroups or remain unstable if the population behaves as a continuum.

### Do fewer variables make clusters more stable?

Not automatically. Removing irrelevant, duplicated or noisy variables can improve stability. Removing essential variables can produce a stable but shallow split controlled by one question. D5 and D6 showed exactly this danger.

### Is selecting variables part of feature selection?

Yes. The present process is theory-guided feature selection followed by coverage, variation, redundancy, dominance and stability checks.

### Can stability prove the theory?

No. Stability means a specified computational pattern is reproducible. Construct validity requires theoretical coherence, appropriate measurement, expert review and ideally replication or external validation.

### Why not use one very large clustering model?

Twenty to thirty raw variables can give dimensions with more questions disproportionate influence, mix unrelated mechanisms and make a cluster impossible to explain. Dimension-specific profiles are clearer, and any later integrated model should represent each approved dimension once.

### What exactly is the current clustering algorithm?

For retained dimension analyses: equal-weight Gower distance on original answers, K-medoids plus spectral clustering across matched respondent subsamples, followed by K-medoids on the consensus dissimilarity matrix. K-medoids alone was first tested for motivation; the consensus ensemble was adopted only after comparison showed it improved agreement and reproducibility.

---

## 18. Current overall decision register

| Scope | Dimension/result | Status |
|---|---|---|
| Data | Canonical reconstruction and cleaning | Complete |
| Data | Final active-branch reconstruction, including mid-branch switches | Complete and audited |
| Data | New-structure strict cohorts | D=191, E=34, F=81, G=56 |
| Branch D | All-variable PCA/K-means typology | Rejected |
| Branch D | Researcher-constructed five scores and integrated k=3 | Withdrawn/provisional; not current method |
| Branch D | Motivation/study experience | Retained for cautious exploratory use |
| Branch D | Economic resources/household pressure | Retained with caution |
| Branch D | Educational trajectory/cultural capital | Retained |
| Branch D | Transition planning/direction | Rejected |
| Branch D | Social connectedness | Statistically stable but excluded for overlap |
| Global | Household economic resources across 363 records | Rejected |
| Branch F | Broad employment-quality clustering | Rejected |
| Branch F | Household economic resources/responsibility | Rejected; primarily an income-source split and searched-null p=0.059 |
| Branch F | Educational/inherited cultural capital | Rejected; no cross-algorithm size-eligible solution and permutation p=0.683 |
| Branch F | Employment security/formality | Retained with caution |
| Branch F | Earnings/working-time preference | Statistically stable but excluded from final set; descriptive diagnostic only |
| Branch F | Satisfaction/mobility | Rejected; descriptive only |
| Branch F | Qualification/skill development | Rejected; training-item dominated |
| Branch F | Professional social capital | Skipped/excluded under overlap decision |
| Branch F | Work motivation/needs | Rejected; method and encoding sensitive |
| Branch F | Search pathway/barriers | Rejected; insufficient stability |
| Branch F | Automated extra-dimension discovery | Screening complete; no dimension automatically confirmed |
| Branch G | Complete variable/dimension audit | Complete; five candidates proposed |
| Branch G | G1 household economic resources/dependency | Retained cautiously as two household economic role/dependency profiles; not a resource-level classification |
| Branch G | G4 psychological readiness/support | Rejected; no size-eligible candidate, diagnostic smaller group n=11 and leave-one-feature-out instability |
| Branch G | G3 future engagement/prior work experience | Retained with narrowed interpretation; two profiles of 35 and 21, all 10 checks passed |
| Branch G | G2 educational/inherited cultural capital | Rejected; exactly reproduced work while studying and permutation p=0.230 |
| Branch E | Complete variable/dimension audit | Complete; 75 variables classified, six active candidates plus one skipped social-capital dimension |
| Branch E | E1 psychological search readiness/support | Rejected; spectral ARI 0.403 and permutation p=0.050 |
| Branch E | E2 search intensity/exposure | Rejected; direct active-search split, 26/8 |
| Branch E | E3 urgency/acceptance constraints | Rejected; direct minimum-wage split, 28/6 |
| Branch E | E4 education usefulness/further-learning orientation | Retained cautiously; 18/16 profiles, all mandatory checks passed, strong dependence on past-education usefulness |
| Branch E | E5 household economic resources/dependency | Rejected; unstable 22/12 result and p=0.583 |
| Branch E | E6 educational/inherited cultural capital | Rejected; direct work-while-studying split, 24/10 |
| Branch E | E7 job-search social capital | Skipped under no-overlap decision |

---

## 19. Limitations that must accompany the results

1. Branch F has only 81 valid respondents; Branch E has 34 and Branch G has 56. Small profiles can be unstable and are difficult to validate.
2. More observations may improve precision but cannot guarantee stable clusters.
3. Several theoretical constructs are represented by single survey items rather than validated multi-item scales.
4. Gower's equal spacing of ordinal categories is a transparent modelling assumption, not a psychometric fact.
5. Consensus stability does not prove natural, causal or permanent youth types.
6. Conditional questions cannot be treated as ordinary missing values or universal clustering inputs.
7. Parental education is a proxy for family cultural capital; parental occupation has not yet been transformed through a defensible class scheme.
8. The current profile names are descriptive summaries and must not stigmatise or restrict individuals.
9. Programme recommendations require a structured course catalogue, eligibility rules and NYSC expert validation.
10. The Branch F permutation screen currently uses 30 repetitions; final inference needs at least 200 and preferably replication in additional data.

---

## 20. Work remaining and recommended next sequence

1. Review the retained Branch D and Branch F dimensions with the supervisor/NYSC experts and confirm that the variable groupings and profile names are substantively defensible.
2. Increase the Branch F permutation-null run from 30 to at least 200 repetitions before thesis reporting.
3. Decide whether Branch F D1/D2 should be analysed separately despite the weak automated discovery evidence; do not force them merely for symmetry with Branch D.
4. Collect more data, particularly for Branch E and G, before expecting reliable multi-profile clustering. Branch E at n=34 is especially constrained.
5. Review the single cautiously retained Branch E result (E4) and the five rejected diagnostics; replicate E4 in additional Branch E respondents before treating it as established.
6. Obtain and structure the 95-course catalogue with prerequisites, level, category, duration, mode, location, cost/support and placement attributes.
7. Build an expert-reviewed profile-to-programme mapping matrix only from retained profiles and relevant descriptors.
8. Identify catalogue gaps by comparing stable profile needs with available programme features.
9. Validate retained clusters through additional samples, holdout/prediction strength and an NYSC expert workshop.
10. Create an individual assignment procedure that preserves uncertainty and never uses cluster membership as an exclusionary decision by itself.

---

## 21. Reproducible files produced

### Core data preparation

- `nysc_survey_cleaning_and_transformation.ipynb`
- `outputs/nysc_survey_cleaned_values.csv`
- `outputs/nysc_survey_cleaned_labels.csv`
- `outputs/nysc_survey_quality_audit.csv`
- `outputs/nysc_survey_branch_path_corrections.csv`
- `outputs/nysc_survey_branch_integrity_issues.csv`
- `outputs/nysc_survey_feature_manifest.csv`
- `outputs/nysc_survey_preprocessing_summary.json`

### Branch D analysis

- `02_branch_d_clustering_experiments.ipynb`
- `03_branch_d_dimension_engineering.ipynb`
- `04_branch_d_integrated_transition_profiles.ipynb`
- `05_branch_d_motivation_clustering.ipynb`
- `06_branch_d_motivation_algorithm_comparison.ipynb`
- `07_branch_d_motivation_consensus_clustering.ipynb`
- `08_branch_d_economic_resources_clustering.ipynb`
- `09_branch_d_educational_cultural_capital_clustering.ipynb`
- `10_branch_d_transition_planning_clustering.ipynb`
- `11_branch_d_social_connectedness_clustering.ipynb`

### Global and Branch F analysis

- `14_global_household_economic_clustering.ipynb`
- `12_branch_f_employment_security_formality_clustering.ipynb`
- `13_branch_f_variable_dimension_audit.py`
- `15_branch_f_earnings_working_time_clustering.ipynb`
- `16_branch_f_job_satisfaction_mobility_clustering.ipynb`
- `17_branch_f_qualification_skill_development_clustering.ipynb`
- `18_branch_f_work_motivation_sdt_clustering.ipynb`
- `19_branch_f_search_pathway_barriers_clustering.ipynb`
- `20_branch_f_candidate_dimension_discovery.py`
- `branch_f_variable_dimension_selection_report.md`
- `branch_clustering_progress.md`

### Branch G audit and G1 clustering

- `23_branch_g_variable_dimension_audit.py`
- `23_branch_g_variable_dimension_audit.ipynb`
- `24_branch_g_household_economic_resources_clustering.py`
- `24_branch_g_household_economic_resources_clustering.ipynb`
- `25_branch_g_psychological_readiness_support_clustering.py`
- `25_branch_g_psychological_readiness_support_clustering.ipynb`
- `26_branch_g_inactivity_pathway_future_engagement_clustering.py`
- `26_branch_g_inactivity_pathway_future_engagement_clustering.ipynb`
- `27_branch_g_educational_cultural_capital_clustering.py`
- `27_branch_g_educational_cultural_capital_clustering.ipynb`
- `branch_g_variable_dimension_selection_report.md`
- `outputs/branch_g_variable_dimension_audit/branch_g_all_62_variables.csv`
- `outputs/branch_g_variable_dimension_audit/branch_g_proposed_dimensions.csv`
- `outputs/branch_g_variable_dimension_audit/branch_g_variable_role_summary.csv`
- `outputs/branch_g_household_economic_resources_clusters/household_economic_clustering_summary.json`
- `outputs/branch_g_household_economic_resources_clusters/household_economic_profile_scatterplot.png`
- `outputs/branch_g_psychological_readiness_support_clusters/readiness_support_clustering_summary.json`
- `outputs/branch_g_psychological_readiness_support_clusters/readiness_support_profile_scatterplot.png`
- `outputs/branch_g_inactivity_pathway_future_engagement_clusters/pathway_engagement_clustering_summary.json`
- `outputs/branch_g_inactivity_pathway_future_engagement_clusters/pathway_engagement_profile_scatterplot.png`
- `outputs/branch_g_educational_cultural_capital_clusters/educational_cultural_clustering_summary.json`
- `outputs/branch_g_educational_cultural_capital_clusters/educational_cultural_profile_scatterplot.png`

### Branch E audit

- `28_branch_e_variable_dimension_audit.py`
- `28_branch_e_variable_dimension_audit.ipynb`
- `branch_e_variable_dimension_selection_report.md`
- `outputs/branch_e_variable_dimension_audit/branch_e_all_75_variables.csv`
- `outputs/branch_e_variable_dimension_audit/branch_e_proposed_dimensions.csv`
- `outputs/branch_e_variable_dimension_audit/branch_e_variable_role_summary.csv`
- `29_branch_e_all_dimensions_clustering.py`
- `29_branch_e_all_dimensions_clustering.ipynb`
- `branch_e_clustering_results_report.md`
- `outputs/branch_e_all_dimensions_clusters/branch_e_all_dimension_screening_summary.csv`
- `outputs/branch_e_all_dimensions_clusters/e4/profile_scatterplot.png`

Each analysis has a corresponding output directory containing assignments, profile summaries, validation tables, sensitivity tests and graphs. Rejected diagnostic assignments must not be reused as validated youth classifications.

---

## 22. References and methodological sources

1. Bourdieu, P. (1986). “The Forms of Capital.” In J. Richardson (Ed.), *Handbook of Theory and Research for the Sociology of Education*.
2. Deci, E. L., & Ryan, R. M. (2000). “The ‘What’ and ‘Why’ of Goal Pursuits: Human Needs and the Self-Determination of Behavior.” *Psychological Inquiry*, 11(4), 227–268.
3. International Labour Organization. School-to-Work Transition Survey methodology and youth-transition framework.
4. Chavent, M., Kuentz-Simonet, V., Liquet, B., & Saracco, J. (2012). “ClustOfVar: An R Package for the Clustering of Variables.”
5. Tibshirani, R., & Walther, G. (2005). “Cluster Validation by Prediction Strength.” *Journal of Computational and Graphical Statistics*, 14(3), 511–528.
6. Witten, D. M., & Tibshirani, R. (2010). “A Framework for Feature Selection in Clustering.” *Journal of the American Statistical Association*, 105(490), 713–726.
7. Raftery, A. E., & Dean, N. (2006). “Variable Selection for Model-Based Clustering.” *Journal of the American Statistical Association*, 101(473), 168–178.
8. Local project source: `nysc_supervisor_prep.docx`, treated as the research plan and framework specification.
9. Local project source: `Data Analysis Report.docx`, treated as the reporting template rather than an instruction to predetermine results.

---

## 23. Short viva summary

> I first cleaned 481 raw survey submissions and reconstructed the active survey path across several export formats. After quality rules and deduplication, 392 records remained in the cleaned master dataset. The new survey structure provided 363 final-path records; one employed routing-integrity record was excluded, giving 362 strict records. I used the final active branch, not merely the entry branch, and corrected 11 mid-survey branch switches. The adopted method selects variables using theory, clusters original mixed responses with Gower distance, compares K-medoids and spectral clustering, and uses consensus, stability, dominance, sensitivity and permutation checks. In Branch D, three dimensions are retained cautiously. In Branch F, only employment security/formality is retained. In Branch G, G1 and G3 are retained narrowly. All six active Branch E dimensions were tested with k=2 because n=34; only E4 passed every mandatory check, producing 18/16 education-usefulness/further-learning profiles. E4 is strongly dependent on perceived past-education usefulness and therefore remains exploratory. The other Branch E dimensions are rejected, while social capital remains skipped under the no-overlap decision.
