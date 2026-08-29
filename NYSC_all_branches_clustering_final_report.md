# NYSC Youth Transition Survey

## Final all-branches clustering report

**Project:** Youth Labour Market Programme Matching through Unsupervised Clustering of School-to-Work Transition Profiles  
**Researcher:** Fernando W. S. V. — IT22166456 — R26-DS-014  
**Partner:** National Youth Services Council (NYSC), Sri Lanka  
**Report date:** 25 August 2026  
**Analytical status:** Final exploratory clustering results for Branches D, E, F and G

---

## Executive summary

This report consolidates the final clustering work for all four youth-transition branches. It records the analytical sample, adopted method, theory-guided dimensions, every retained and rejected result, the final profile interpretations, limitations and the appropriate next use of the profiles.

The raw export contained 481 submissions. After cleaning, quality rules and deduplication, 392 records remained in the cleaned master dataset. The current clustering analyses use 363 respondents from the new survey structure, classified by their **final active branch**, not merely the branch in which they entered the survey. One Branch F routing-integrity record was excluded because it lacked the core employment-status response. The strict clustering sample is therefore **362 respondents: D=191, E=34, F=81 and G=56**.

The final analysis does **not** claim that all respondents form one universal set of youth types. It uses dimension-specific clustering. A person can have one profile for motivation, another for economic role and another for educational trajectory or employment security.

Seven dimension models are retained for cautious exploratory use:

| Branch | Retained dimension | k | Profile sizes | Final interpretation strength |
|---|---|---:|---|---|
| D — In education | Motivation and study experience | 3 | 47 / 75 / 69 | Retained with ambiguity and measurement cautions |
| D — In education | Economic resources and household pressure | 2 | 44 / 147 | Retained cautiously |
| D — In education | Educational trajectory and cultural capital | 4 | 15 / 53 / 57 / 66 | Retained; strongest Branch D structural result |
| E — Unemployed/searching | Education usefulness and further-learning orientation | 2 | 18 / 16 | Retained cautiously; strongly feature-dependent |
| F — Employed | Employment security and formality | 2 | 29 / 52 | Retained with ambiguity/PAC caution |
| G — Inactive | Household economic role and dependency | 2 | 41 / 15 | Retained narrowly; not a low/high resource classification |
| G — Inactive | Future engagement and prior work experience | 2 | 35 / 21 | Retained with a narrowed interpretation |

All other tested results were rejected, skipped or deliberately excluded. A high silhouette or perfect stability was not accepted when a split merely copied one questionnaire answer, depended on one feature, created an undersized group, disagreed across algorithms or duplicated a variable already used in another retained dimension.

These seven systems are exploratory response profiles, not diagnoses, permanent identities or validated psychometric scales. They may inform programme-needs analysis, but course recommendations require a separate transparent matching layer using eligibility, preferences, feasibility, course attributes and NYSC expert review.

---

## 1. Research and theoretical basis

The clustering plan is grounded in three complementary sources:

| Framework | Role in this analysis |
|---|---|
| ILO School-to-Work Transition Survey (SWTS) | Defines education-to-work status, employment conditions, job-search behaviour, barriers and transition pathways. |
| Bourdieu's forms of capital | Supports attention to economic resources, inherited educational/cultural background, social-network resources and labour-market position. |
| Self-Determination Theory (SDT) | Supports attention to autonomy, competence, relatedness/support and the type of motivation guiding study, work or transition. |

The survey routes respondents to four research branches:

| Branch | Current transition position |
|---|---|
| D | In education |
| E | Unemployed and seeking/transitioning |
| F | Employed, including temporary absence with a job to return to |
| G | Inactive or not currently seeking work |

Theory was used to propose which questions could represent a coherent dimension. It was not used to force a cluster result. Data coverage, variation, cross-method agreement, stability, feature dominance and interpretability determined whether a proposed dimension was retained.

---

## 2. Data preparation and correct analytical cohorts

### 2.1 Cleaning and transformation

The source CSV contained 481 submissions and 2,547 flattened fields created by multiple versions of the survey application. Cleaning reconstructed one canonical row per submission from the newer answer objects, intermediate analysis objects and legacy top-level fields.

Readable labels and internal values came from the survey export itself. Newer records supplied `answers.<question>.label` and `answers.<question>.value`; equivalent label/value fields were recovered from older layouts. No readable category was guessed from its numeric code.

The main cleaning operations were:

1. Standardising blanks and missing tokens.
2. Recovering canonical answers across export formats.
3. Using active-path answers rather than off-path audit copies.
4. Preserving parallel readable-label and internal-value datasets.
5. Separately reconstructing entry branch and final active branch.
6. Removing test/debug records and records outside age 15–35.
7. Requiring a recognised branch and at least ten recovered answers.
8. Deduplicating resubmissions by retaining the latest submission for repeated session IDs.
9. Preserving conditional missingness as not applicable rather than fabricating answers.
10. Auditing outliers and inconsistencies rather than deleting them automatically.

### 2.2 Record accounting

| Stage | Records |
|---|---:|
| Raw submissions | 481 |
| Eligible before deduplication | 443 |
| Duplicate/resubmission records removed | 51 |
| Final cleaned master dataset | 392 |
| New-structure final-path cohort | 363 |
| Strict clustering cohort after one Branch F exclusion | 362 |

Quality flags overlap and must not be summed as independent deletion counts. The cleaned master includes 29 records outside the new-structure clustering cohort: six legacy final-branch records and 23 entry-branch fallback records. They are retained for audit but are not mixed into strict final-path clustering.

### 2.3 Final-branch reconstruction

The entry branch is not always the final analytical branch because respondents can change path after later gateway answers. For new-structure records, the last branch-specific section in `path.active_sections` was treated as authoritative. The application section letters were translated to research branches as follows:

| Application section | Research branch |
|---|---|
| C | D — In education |
| D | E — Unemployed/searching |
| E | F — Employed |
| F | G — Inactive |

This logic preserved 31 cases whose entry and final branches differed and corrected 11 cases in which stale branch metadata disagreed with the final active path. Therefore, respondents who switched branch in the middle of the questionnaire were assigned to the branch containing their final substantive answers.

### 2.4 Final strict cohort

| Branch | New-structure final path | Excluded for integrity | Final clustering n |
|---|---:|---:|---:|
| D — In education | 191 | 0 | 191 |
| E — Unemployed/searching | 34 | 0 | 34 |
| F — Employed | 82 | 1 | 81 |
| G — Inactive | 56 | 0 | 56 |
| **Total** | **363** | **1** | **362** |

The excluded Branch F case had an employed final path but no `employment_status`, a core response required for a valid employed record.

---

## 3. Final clustering method

### 3.1 Theory-guided feature selection

Questions were grouped into a proposed dimension only when they had a defensible common meaning. Demographics, direct programme preferences, routing questions and conditional follow-ups were generally retained as profile descriptors rather than used to create clusters. This prevents clusters from simply reproducing known branches, demographic categories or skip-logic patterns.

The method does not create invented 0–100 scores. Original responses are compared directly.

### 3.2 Gower distance

For each pair of respondents, question-level differences are calculated as follows:

- nominal answers: 0 when the categories match and 1 when they differ;
- ordered answers: rank difference divided by the available rank range;
- numeric answers: absolute difference divided by the permitted or observed range;
- missing/not-applicable answer: that component is omitted for that respondent pair.

The overall pairwise distance is the equal-weight mean of available question-level differences:

\[
d(i,j)=\frac{\sum_p w_{ijp}\,\delta_{ijp}}{\sum_p w_{ijp}}
\]

This equation measures response-pattern dissimilarity. It does not claim that a respondent has a researcher-invented capital, motivation or readiness score.

### 3.3 Consensus ensemble

The retained analyses combine two algorithms using the same Gower relationships:

1. K-medoids, which groups respondents around actual respondents.
2. Spectral clustering, which partitions the Gower-based similarity structure differently.
3. Each method is run on 100 matched 80% respondent subsamples, creating 200 base partitions.
4. For each pair of respondents, co-association is the proportion of eligible runs in which they appear in the same cluster.
5. Final clusters are produced by K-medoids on `1 − co-association`.

The consensus ensemble is not assumed to be better merely because it combines algorithms. It is retained only when its result also passes the substantive and diagnostic checks.

### 3.4 Validation and decision logic

| Check | What it tests |
|---|---|
| Gower silhouette | Separation on the original-response distance used for clustering. |
| Subsample/bootstrap ARI | Whether similar memberships return when respondents are resampled. |
| ARI against full K-medoids and spectral solutions | Dependence on one source algorithm. |
| Minimum profile size | Prevents interpretation of very small groups; most analyses required at least 15. |
| Single-feature ARI | Whether one question alone recreates the cluster assignment. |
| Leave-one-feature-out ARI | Whether removal of one question destroys the result. |
| Encoding sensitivity | Whether reasonable alternative encodings materially change the partition. |
| Ambiguity/PAC | Whether respondent pairs often lie in uncertain middle consensus values. |
| Permutation test | Whether an attractive searched result exceeds patterns obtainable after independently shuffling variables. |
| Profile meaning | Whether differences are coherent, non-stigmatising and useful for programme analysis. |

No universal `PAC ≤ 0.20` rule is claimed. PAC is comparative evidence, not proof. Likewise, a scatterplot is only a two-dimensional display of higher-dimensional distances; its axes are display coordinates, not survey questions or theoretical scores.

---

## 4. Final all-branches decision register

### 4.1 Retained profile systems

| Branch | Dimension | Inputs/components | k and sizes | Main evidence | Final decision |
|---|---|---|---|---|---|
| D | Motivation and study experience | `study_motivation_type`, `autonomy_in_study`, `competence_in_study_field`, `relatedness_at_institution` | k=3; 47/75/69 | Silhouette 0.350; bootstrap ARI 0.981; ARI vs K-medoids 0.968 and spectral 0.712; PAC 0.193; 7/8 checks | Retained for exploratory use, with ambiguity and one-item-per-construct cautions |
| D | Economic resources and household pressure | Income position; household worker/unemployed shares; primary-earner responsibility; income source; education funding source | k=2; 44/147 | Silhouette 0.436; bootstrap ARI 0.986; source ARIs 0.849/0.796; 7/8 checks | Retained cautiously |
| D | Educational trajectory and cultural capital | Parental education, expected education, institution type, work while studying, education re-entry | k=4; 15/53/57/66 | Silhouette 0.427; bootstrap ARI 0.963; source ARIs 0.776/0.934; 8/8 checks | Retained |
| E | Education usefulness and further-learning orientation | `past_edu_usefulness`, `plans_further_edu`, `expected_highest_edu_e` | k=2; 18/16 | Silhouette 0.567; bootstrap ARI 0.953; source ARIs 0.882/1.000; p=0.040; 10/10 checks | Retained cautiously; strongly dependent on past education usefulness |
| F | Employment security and formality | `contract_type`, `job_security_12months`, `sector_formality` | k=2; 29/52 | Silhouette 0.368; bootstrap ARI 0.953; source ARIs 0.854/0.950; 7/8 checks | Retained with PAC/ambiguity caution |
| G | Household economic role and dependency | Income position; worker/unemployed shares; primary-earner status; primary income source | k=2; 41/15 | Silhouette 0.372; bootstrap ARI 1.000; source ARIs 0.854/0.718; p=0.012; 9/9 checks | Retained narrowly; role/dependency, not resource level |
| G | Future engagement and prior work experience | `reason_not_in_labour_force`, `ever_worked`, `wants_to_work_future`, `wants_further_edu` | k=2; 35/21 | Silhouette 0.413; bootstrap ARI 1.000; source ARIs 0.928/1.000; p=0.011; 10/10 checks | Retained with narrowed interpretation |

### 4.2 Rejected, skipped and excluded systems

| Scope | Dimension/attempt | Outcome | Reason not retained |
|---|---|---|---|
| D | All-variable PCA/K-means | 183/8 diagnostic split | Tiny cluster; holdout contained only one cluster; not a usable typology |
| D | Constructed five scores and integrated k=3 | 52/87/52 | Researcher-defined scores were not validated; silhouette 0.186; weak stability/agreement; withdrawn |
| D | Transition planning and direction | 120/71 | Silhouette 0.245; spectral ARI 0.137; PAC 0.751; 5/8 checks |
| D | Social connectedness | 51/83/57 and statistically stable | Deliberately excluded because `relatedness_at_institution` already appears in motivation, causing double-counting |
| Global | Household economic clustering across D/E/F/G | 135/228 | Full K-medoids ARI 0.011; raw-count sensitivity ARI 0.011; PAC 0.609; rejected |
| E1 | Job-search psychological readiness/support | 17/17 | Spectral ARI 0.403; source-method minimum group 11; p=0.050 |
| E2 | Search intensity/exposure | 26/8 | Exactly reproduced active-search answer; undersized profile; p=0.500 |
| E3 | Economic urgency/acceptance constraints | 28/6 | Exactly reproduced the minimum-wage answer; undersized profile |
| E5 | Household economic resources/dependency | 22/12 | Source ARI 0.484; 38.2% ambiguous; p=0.583; undersized profile |
| E6 | Educational/inherited cultural capital | 24/10 | Exactly reproduced work while studying; undersized profile |
| E7 | Job-search social capital | Not run | Skipped under the prior no-overlapping-social-connectedness decision |
| F D1 | Household resources/responsibility | 21/60 | Income-source dominated; leave-source-out ARI −0.036; structural components ARI 0.000; p=0.059 |
| F D2 | Educational/inherited cultural capital | Diagnostic 21/60 | No candidate met size rule in both algorithms; p=0.683; work-while-studying dominated |
| F | Broad employment quality | 29/25/27 | Silhouette 0.263; spectral ARI 0.444; only 6/8 checks |
| F D4 | Earnings/working-time adequacy | 51/30 and statistically stable | Researcher excluded it because preference item controlled the result; descriptive diagnostic only |
| F D5 | Satisfaction/mobility | 34/47 | Removing `hopes_to_change_job` gave ARI −0.007; PAC 0.519; encoding-sensitive |
| F D6 | Qualification/skill development | 65/16 | Exactly reproduced `received_training`; leave-training-out ARI 0.014; reduced retest weak |
| F D7 | Professional social capital | Not run | Skipped under no-overlap decision |
| F D8 | Work motivation/psychological needs | No eligible solution | No k=2–4 result met cross-algorithm size rule; method and encoding sensitivity |
| F D9 | Search pathway/barriers | 48/33 diagnostic | Silhouette 0.165; bootstrap ARI 0.532; spectral ARI 0.038; 35.8% low confidence |
| F | Automated extra-dimension discovery | 414 candidates; 15 shortlisted | No theory-pool result exceeded the searched permutation screen; no extra dimension confirmed |
| G2 | Educational/inherited cultural capital | 38/18 | Exactly reproduced work while studying; leave-item-out ARI 0.004; p=0.230 |
| G4 | Psychological readiness/support | 45/11 diagnostic | No size-eligible solution; K-medoids ARI 0.590; leave-self-efficacy-out ARI −0.017 |
| G5 | Labour-market social connection | Not run | Skipped under no-overlap decision; only two closely related items |

---

## 5. Branch D — In education

### 5.1 Cohort and selected dimensions

Branch D contains 191 strict final-path respondents. Forty-eight variables are available in the broad branch manifest, but only coherent, sufficiently covered inputs enter clustering. Demographics, aspirations, conditional education history and programme preferences remain descriptors unless a specific dimension justifies their use.

| Dimension | Cluster-forming variables | Theory and purpose | Decision |
|---|---|---|---|
| Motivation and study experience | `study_motivation_type`, `autonomy_in_study`, `competence_in_study_field`, `relatedness_at_institution` | SDT motivation, autonomy, competence and relatedness in the study context | Retained cautiously |
| Economic resources and household pressure | `household_income`; worker/unemployed household shares; `primary_earner_status`; `primary_income_source`; `edu_funding_source` | Bourdieu economic capital and SWTS household/education-financing position | Retained cautiously |
| Educational trajectory and cultural capital | `father_edu`, `mother_edu`, `expected_highest_edu_d`, `institution_type`, `worked_while_studying`, `re_entered_education` | Inherited educational background plus current educational trajectory | Retained |
| Transition planning and direction | `plans_after_education`, `ideal_work_type`, `ideal_sector`, `study_field_preference` | SWTS education-to-work plans and aspirations | Rejected empirically |
| Social connectedness and support pathways | `employment_network_quality`, `relatedness_at_institution` | Bourdieu network resources and institutional belonging | Excluded to avoid overlap |

`highest_edu_completed` was observed for only 3 of 191 current students because it was conditionally asked after completing/leaving education. It was excluded from distance. `edu_status` was near-constant and contained six conflicts with final current-attendance routing, so the final branch remained authoritative and this variable was also excluded.

### 5.2 Retained D1: motivation and study experience

| Profile | n | Interpretation |
|---|---:|---|
| Externally or uncertainly motivated, with moderate study support | 47 | Motivation was more external/uncertain and the combined study-support responses were moderate. |
| Goal-aligned motivation with mixed confidence and support | 75 | Study direction was more goal-aligned, while competence and relatedness were mixed. |
| Highly self-directed, capable and connected | 69 | Responses indicated stronger autonomous motivation, perceived competence and institutional relatedness. |

The three labels summarise four questions only. They are not clinical or validated SDT types. About 23.6% of respondents had low Gower membership confidence, so uncertain assignments must remain flagged.

### 5.3 Retained D2: economic resources and household pressure

| Profile | n | Interpretation |
|---|---:|---|
| Relatively lower household economic position | 44 | Lower relative position across the observed income, household-labour, earner-responsibility and education-funding pattern. |
| Relatively higher household economic position | 147 | Higher relative position across the same observed components. |

Twenty-nine respondents declined household income. Five records had workers plus unemployed greater than household size; their derived shares were treated as unavailable rather than silently corrected. Missing-aware Gower used the remaining comparable components.

### 5.4 Retained D3: educational trajectory and cultural capital

| Profile | n | Interpretation |
|---|---:|---|
| Re-entered students, often with degree-educated parents | 15 | Re-entry into education was prominent, often alongside higher parental education. |
| State-institution students without work exposure | 53 | State-institution attendance and no work-while-studying experience. |
| Private-institution students without work exposure | 57 | Private-institution attendance and no work-while-studying experience. |
| Work-experienced students, mainly in private institutions | 66 | Work while studying was prominent, with many respondents in private institutions. |

Parental education is only a proxy for family cultural capital; it is not a measure of intelligence or merit. Sensitivity analysis showed that work experience and institution type are important drivers and must remain explicit in interpretation.

### 5.5 D dimensions not retained

- Transition planning was rejected because K-medoids and spectral clustering did not agree sufficiently and the consensus structure was ambiguous.
- Social connectedness was statistically stable but removed from the final set because it reused institutional relatedness from motivation.
- Parental occupations were not converted to a capital score because no defensible occupational-class crosswalk was available.
- Life goals, plans and belief items remain descriptors because the survey does not provide a validated scale supporting their aggregation.

---

## 6. Branch E — Unemployed/searching

### 6.1 Cohort and candidate dimensions

Branch E contains only 34 strict final-path respondents and 75 collectively answerable variables. With a minimum profile size of 15, only k=2 can be eligible; k=3 would require at least 45 respondents. This sharply limits the number of defensible clusters.

| Code | Dimension | Inputs | Decision |
|---|---|---|---|
| E1 | Job-search psychological readiness/support | `job_search_self_efficacy`, `job_search_autonomy_orientation`, `social_support_job_search`, `future_planning_orientation` | Rejected |
| E2 | Search intensity/exposure | `active_search_4weeks`, `job_search_duration`, `num_applications`, `num_interviews` | Rejected |
| E3 | Economic urgency/acceptance constraints | `income_urgency`, `job_acceptance_conditions`, `has_minimum_wage` | Rejected |
| E4 | Education usefulness/further-learning orientation | `past_edu_usefulness`, `plans_further_edu`, `expected_highest_edu_e` | Retained cautiously |
| E5 | Household resources/dependency | `household_size`, `household_income`, `household_workers`, `household_unemployed`, `primary_earner_status`, `primary_income_source` | Rejected |
| E6 | Educational/inherited cultural capital | `father_edu`, `mother_edu`, `edu_status`, `worked_while_studying` | Rejected |
| E7 | Job-search social capital | `employment_network_quality`, `knows_people_in_target_sector`, `network_helpfulness` | Skipped under no-overlap decision |

Direct programme fields such as main obstacle, desired training, job type sought and employment-service help remain descriptors for later programme matching.

### 6.2 Retained E4: education usefulness and further-learning orientation

| Profile | n | Main pattern |
|---|---:|---|
| High perceived education utility and strong learning ambition | 18 | 83.3% rated past education very useful; 94.4% planned further education; 66.7% expected postgraduate education. |
| Moderate perceived utility and mixed learning ambition | 16 | 93.8% rated education somewhat useful; 62.5% planned further education; the remainder were unsure or did not plan it. |

The model passed all ten mandatory checks, but removing `past_edu_usefulness` changed membership almost completely (ARI 0.039). Therefore, the correct narrow label is **education-usefulness and further-learning orientation**. It must not be presented as a validated human-capital, readiness or ability classification. Replication with more unemployed respondents is particularly important.

### 6.3 Why the other E dimensions were rejected

E2, E3 and E6 created easy but shallow splits that simply reproduced active search, minimum-wage preference and work-while-studying answers. E1 did not agree sufficiently across source methods. E5 was ambiguous, unstable across methods and not significant against shuffled variables. These are useful descriptive questions, but assigning cluster identities from them would add little beyond reading the original response.

---

## 7. Branch F — Employed

### 7.1 Cohort and variable audit

There are 81 valid employed respondents after the one integrity exclusion: 70 wage workers and 11 self-employed respondents. The full active-path audit identified 105 collectively answerable variables. Only 34 theory-proposed variables were eligible as cluster inputs; the remaining variables were retained as programme descriptors, conditional variables, subgroup descriptors, validation fields or routing fields.

| Code | Dimension | Inputs | Decision |
|---|---|---|---|
| D1 | Household resources/responsibility | Household income/size/workers/unemployed, primary-earner status, primary income source | Rejected |
| D2 | Educational/inherited cultural capital | Parental education, education status, work while studying | Rejected |
| D3 | Employment security/formality | `contract_type`, `job_security_12months`, `sector_formality` | Retained cautiously |
| D4 | Earnings/working-time adequacy | `monthly_income_band`, `usual_hours_per_week`, `income_hours_preference` | Excluded; descriptive diagnostic only |
| D5 | Satisfaction/mobility intention | `job_satisfaction`, `contract_satisfaction`, `hopes_to_change_job` | Rejected |
| D6 | Qualification use/skill development | `qualification_job_match`, `past_edu_useful_for_job`, `received_training` | Rejected |
| D7 | Professional social capital | `employment_network_quality`, `professional_network_growth` | Skipped under no-overlap decision |
| D8 | Work motivation/psychological needs | `work_autonomy`, `competence_growth_at_work`, `relatedness_at_work`, `work_motivation_type` | Rejected |
| D9 | Search pathway/barriers | Jobseeker registration, service help, applications, interviews, duration and obstacle | Rejected |

Conditional wage-worker and self-employed questions were not mixed into one all-employed distance because doing so would make distance depend on which subgroup path a respondent received.

### 7.2 Retained D3: employment security and formality

| Profile | n | Interpretation |
|---|---:|---|
| Temporary/no-contract employment with uncertain security | 29 | Temporary or absent contracts combined with weaker 12-month security and formality responses. |
| Predominantly permanent employment with stronger security | 52 | Permanent contracts and stronger expected security/formality were more common. |

This is the only retained Branch F clustering. It describes employment conditions, not respondent worth or employability. It should guide questions about formalisation, certification, protection and feasible upgrading rather than automatically assign a course.

### 7.3 Important excluded diagnostic: D4

D4 formed a stable 51/30 split, but leave-one-feature-out analysis showed that working-time/income preference controlled the grouping. Both groups had a median monthly-income-band code of 4 and median usual working hours of 40. The result must not be called low-income versus high-income clustering.

- 51 respondents mostly preferred their current hours/income.
- 30 respondents mostly preferred more hours/more income.

This preference remains valuable for scheduling and programme-feasibility analysis, but it is not a final multidimensional cluster system.

### 7.4 Automated search for additional F dimensions

The constrained discovery script evaluated 414 variable-subset/k solutions only within theory-approved pools and shortlisted 15. It compared observed results with independently shuffled-variable searches. No additional theory-pool result was automatically confirmed. This prevents selection of a high silhouette obtained merely because many combinations were searched or one category produced an easy partition.

The Branch F discovery screen used 30 permutation repetitions. At least 200 should be run before any final inferential claim, although a lower p-value would still not replace theoretical review or replication.

---

## 8. Branch G — Inactive

### 8.1 Cohort and candidate dimensions

Branch G contains 56 strict final-path respondents and 62 collectively answerable variables.

| Code | Dimension | Inputs | Decision |
|---|---|---|---|
| G1 | Household resources/dependency | Household size/income/workers/unemployed, primary-earner status, primary income source | Retained narrowly as economic role/dependency |
| G2 | Educational/inherited cultural capital | Parental education, education status, work while studying | Rejected |
| G3 | Inactivity pathway/future engagement | Inactivity reason, ever worked, future work intention, future education intention | Retained narrowly |
| G4 | Psychological readiness/support | Future orientation, employment self-efficacy, support for engagement | Rejected |
| G5 | Labour-market social connection | Employment network quality, labour-market connection | Skipped under no-overlap decision |

### 8.2 Retained G1: household economic role and dependency

| Profile | n | Main pattern |
|---|---:|---|
| Predominantly family/partner-supported non-provider | 41 | 90.2% were not the main provider; 75.6% relied mainly on parents/family and 14.6% on a partner/spouse. |
| Predominantly self-income provider/contributor | 15 | 86.7% were main/shared earners; 66.7% reported a regular job/business as their main personal income source. |

The original title implied household resources, but structural resources alone had ARI −0.016 with the final grouping. Primary income source was the strongest item, though no single item exactly reproduced membership. The defensible interpretation is therefore **economic role/dependency**, not lower versus higher household resources.

### 8.3 Retained G3: future engagement and prior work experience

| Profile | n | Main pattern |
|---|---:|---|
| Work-and-education engaged, mostly prior work experience | 35 | 97.1% wanted future work, 85.7% wanted further education and 82.9% had worked before. |
| Low/uncertain engagement, mostly no prior work experience | 21 | 71.4% did not want future work, 61.9% were unsure about further education and 76.2% had never worked. |

Removing the 13-category current inactivity reason reproduced the final membership exactly (ARI 1.000), so that variable did not create the split. It should instead be used to describe the concrete barriers and circumstances inside each profile. No single remaining item alone recreated the cluster; the maximum single-item ARI was 0.554.

### 8.4 Why G2 and G4 were rejected

G2 was a direct work-while-studying split rather than an educational/cultural-capital structure. G4 had attractive separation and stability but created an undersized group of 11 and was destroyed when self-efficacy was removed. These indicators remain useful individually for programme planning but are not assigned as cluster identities.

---

## 9. What the final profiles mean

### 9.1 Dimension-specific, not whole-person labels

A respondent belongs to a profile only within a retained dimension. For example, a Branch D respondent can simultaneously be:

- in the goal-aligned motivation profile;
- in the relatively lower household economic-position profile; and
- in the private-institution/no-work-exposure educational profile.

None of these alone describes the whole person. The current report therefore does not present a Level 2 integrated youth typology. The earlier integrated-score attempt was withdrawn because the scores were not validated and the clusters were weak.

### 9.2 How profiles can support existing-programme recommendations

Clusters identify shared conditions or needs. Course recommendation needs a separate rule-based and expert-reviewed layer:

1. Use the retained dimension profile to identify a need or constraint.
2. Add individual descriptors such as ideal sector, preferred work type, desired training, main obstacle, location and willingness to relocate.
3. Check education and course prerequisites.
4. Check feasibility: income urgency, household responsibility, delivery mode, duration, cost and support.
5. Compare the respondent with structured NYSC course attributes.
6. Present suitable alternatives and preserve uncertainty rather than making the cluster a gatekeeping rule.

Examples of profile-relevant support include:

- insecure employed youth: certification, formalisation, labour-rights information or part-time upgrading;
- unemployed youth with strong learning ambition: sector-aligned training filtered by entry requirements and search barriers;
- inactive youth wanting work/education: re-engagement, recognition of prior experience and barrier-specific support;
- family-supported inactive youth: readiness, exposure and feasible pathways, interpreted alongside inactivity reason;
- current students with lower household position: funding, flexible delivery or placement support, without assuming low motivation.

### 9.3 How programme gaps can be identified

A gap is suggested when a sizeable, reproducible profile has a documented need but the course/support catalogue has no feasible response. A valid gap statement must combine:

- retained cluster size and uncertainty;
- original response distributions and programme descriptors;
- actual course prerequisites, content, delivery mode, duration, location and support;
- NYSC expert review; and
- preferably replication in additional respondents.

Clusters indicate where to investigate. They do not, by themselves, prove that a new programme must be created.

---

## 10. Overall findings and interpretation

1. **Branch D has the richest retained profile structure.** Its larger sample supports three separate dimensions and up to four profiles. Educational trajectory/cultural capital received the strongest complete diagnostic support.
2. **Branch E is severely sample-constrained.** Only one narrow two-profile result is retained and it depends strongly on perceived education usefulness. It requires replication.
3. **Branch F supports only employment security/formality as final clustering.** Many seemingly stable alternatives copied a single answer or failed cross-method checks. The non-retained variables remain highly useful as programme descriptors.
4. **Branch G supports two narrow systems.** One describes economic role/dependency; the other describes future engagement and prior experience. Neither should be broadened beyond its observed drivers.
5. **Rejected results are substantive evidence.** They show that some dimensions behave as continua, contain too few respondents, or are better represented by direct questionnaire responses than by cluster labels.
6. **More data can improve precision but cannot guarantee stability.** New data may reproduce, revise or dissolve the current structures.
7. **No single final all-youth clustering is justified.** The rejected global clustering and withdrawn integrated-score experiment support keeping the current dimension- and branch-specific approach.

---

## 11. Limitations

1. Branch sizes are unequal and E=34 is particularly small.
2. Several constructs use one item per theoretical component rather than validated multi-item scales.
3. Ordinal Gower spacing is a transparent modelling choice, not a psychometric interval claim.
4. Consensus stability shows reproducibility under the specified procedure; it does not prove natural, causal or permanent types.
5. Conditional and subgroup questions cannot fairly be included in every respondent's distance.
6. Parental education is a limited proxy for inherited cultural capital. Parental occupation has not been converted through a defensible occupational-class scheme.
7. Several retained systems still have feature-dependence or ambiguity cautions.
8. Profile names are descriptive and must not stigmatise respondents or be used to deny programme access.
9. Programme recommendation requires a structured NYSC catalogue and expert-validated matching rules.
10. Independent data or a future larger sample is needed for external validation.

---

## 12. Recommended next steps

1. Freeze this seven-model set as the current exploratory clustering result; do not promote rejected diagnostic assignments.
2. Review the retained variable groupings and profile names with the supervisor and NYSC domain experts.
3. Collect additional respondents, especially in Branch E and G, and retest the same prespecified models without changing definitions to chase better scores.
4. Increase the Branch F discovery permutation screen from 30 to at least 200 only if automated discovery will be reported inferentially.
5. Structure the 95-course catalogue by skill area, prerequisites, qualification/NVQ level, delivery mode, duration, location, cost/support and placement links.
6. Join retained profiles with individual programme descriptors and build an explicit profile-to-programme evidence matrix.
7. Identify catalogue gaps only after feasibility and expert review.
8. Develop an assignment function that returns profile membership plus uncertainty and the original answers driving that assignment.

---

## 13. Reproducible outputs

### Core preparation

- `nysc_survey_cleaning_and_transformation.ipynb`
- `outputs/nysc_survey_cleaned_values.csv`
- `outputs/nysc_survey_cleaned_labels.csv`
- `outputs/nysc_survey_quality_audit.csv`
- `outputs/nysc_survey_branch_path_corrections.csv`
- `outputs/nysc_survey_branch_integrity_issues.csv`

### Branch D

- `07_branch_d_motivation_consensus_clustering.ipynb`
- `08_branch_d_economic_resources_clustering.ipynb`
- `09_branch_d_educational_cultural_capital_clustering.ipynb`
- `10_branch_d_transition_planning_clustering.ipynb`
- `11_branch_d_social_connectedness_clustering.ipynb`

### Branch E

- `28_branch_e_variable_dimension_audit.ipynb`
- `29_branch_e_all_dimensions_clustering.ipynb`
- `branch_e_variable_dimension_selection_report.md`
- `branch_e_clustering_results_report.md`
- `outputs/branch_e_all_dimensions_clusters/branch_e_all_dimension_screening_summary.csv`

### Branch F

- `12_branch_f_employment_security_formality_clustering.ipynb`
- `13_branch_f_variable_dimension_audit.py`
- `15_branch_f_earnings_working_time_clustering.ipynb`
- `16_branch_f_job_satisfaction_mobility_clustering.ipynb`
- `17_branch_f_qualification_skill_development_clustering.ipynb`
- `18_branch_f_work_motivation_sdt_clustering.ipynb`
- `19_branch_f_search_pathway_barriers_clustering.ipynb`
- `20_branch_f_candidate_dimension_discovery.py`
- `branch_f_variable_dimension_selection_report.md`

### Branch G

- `23_branch_g_variable_dimension_audit.ipynb`
- `24_branch_g_household_economic_resources_clustering.ipynb`
- `25_branch_g_psychological_readiness_support_clustering.ipynb`
- `26_branch_g_inactivity_pathway_future_engagement_clustering.ipynb`
- `27_branch_g_educational_cultural_capital_clustering.ipynb`
- `branch_g_variable_dimension_selection_report.md`

Rejected diagnostic assignments must not be reused as validated youth classifications.

---

## 14. References

1. Bourdieu, P. (1986). “The Forms of Capital.” In J. Richardson (Ed.), *Handbook of Theory and Research for the Sociology of Education*.
2. Deci, E. L., & Ryan, R. M. (2000). “The ‘What’ and ‘Why’ of Goal Pursuits: Human Needs and the Self-Determination of Behavior.” *Psychological Inquiry*, 11(4), 227–268.
3. International Labour Organization. School-to-Work Transition Survey methodology and youth-transition framework.
4. Tibshirani, R., & Walther, G. (2005). “Cluster Validation by Prediction Strength.” *Journal of Computational and Graphical Statistics*, 14(3), 511–528.
5. Witten, D. M., & Tibshirani, R. (2010). “A Framework for Feature Selection in Clustering.” *Journal of the American Statistical Association*, 105(490), 713–726.
6. Raftery, A. E., & Dean, N. (2006). “Variable Selection for Model-Based Clustering.” *Journal of the American Statistical Association*, 101(473), 168–178.
7. Local research plan: `nysc_supervisor_prep.docx`.
8. Local reporting guide: `Data Analysis Report.docx`.

---

## 15. Viva-ready summary

> I cleaned 481 raw survey submissions and retained 392 master records after quality checks and deduplication. For current clustering, I used 363 new-structure respondents classified by their final active survey path, not their entry branch; one invalid employed-path record was excluded, leaving 362 respondents across D=191, E=34, F=81 and G=56. I used theory-guided feature selection, Gower distance on original mixed responses, repeated K-medoids and spectral clustering, and a consensus partition. I retained a result only when it had adequate profile sizes, separation, resampling stability, cross-algorithm agreement, no unacceptable single-question dominance and a meaningful narrow interpretation. The final output is seven dimension-specific profile systems: three in Branch D, one in E, one in F and two in G. They are exploratory need and condition profiles, not permanent youth types. Course recommendation is the next separate stage and must combine profiles with individual preferences, eligibility, feasibility, structured course attributes and NYSC expert review.
