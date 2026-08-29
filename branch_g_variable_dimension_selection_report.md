# Branch G variable and dimension selection report

## Cohort and scope

This report covers the 56 strict new-survey-structure respondents whose corrected final analytical branch is G — inactive/not currently seeking work. The live application calls the inactive section `F`; the research document calls it Branch `G`. The final translated path, not the entry branch, controls inclusion.

The active paths contain 62 collectively answerable variables. Most core universal and inactive-branch questions have 100% canonical coverage. Questions from implementation Sections D or E were gateway questions answered before some respondents were re-routed to final Branch G; they remain routing evidence and do not enter all-Branch-G clustering.

## Recommended candidate Level-1 dimensions

| dimension | framework | variables | number_of_inputs | minimum_coverage_percent | why_grouped | caution | clustering_status |
|---|---|---|---|---|---|---|---|
| G1 — Household economic resources and dependency | Bourdieu economic capital + ILO SWTS household structure | household_income, household_size, household_workers, household_unemployed, primary_earner_status, primary_income_source | 6 | 100.0 | Captures the household resources available to inactive youth, the number of working/job-seeking household members, and dependence or responsibility for current income. | These are raw indicators, not a validated economic-capital scale. Household counts require consistency checks, and primary income source may create a direct family-supported versus own-income split. | retained as exploratory household economic role/dependency profiles; do not interpret as resource level alone |
| G2 — Educational and inherited cultural capital | Bourdieu cultural capital + ILO SWTS education history | father_edu, mother_edu, edu_status, worked_while_studying | 4 | 100.0 | Represents family educational background, current/recent education position, and exposure to work while studying. | Parental education is a proxy, not a measure of ability or merit. Highest completed education is conditional and is therefore a descriptor rather than an all-Branch-G input. | excluded; diagnostic exactly reproduced work-while-studying |
| G3 — Inactivity pathway and future engagement intention | ILO School-to-Work Transition Survey | reason_not_in_labour_force, ever_worked, wants_to_work_future, wants_further_edu | 4 | 100.0 | Distinguishes current reasons for inactivity, previous labour-market experience, and stated intentions to enter work or education. | The inactivity reason is a direct nominal structural category and may dominate a partition. The intention questions are observed choices, not a latent readiness scale. Leave-one-feature-out and single-item dominance tests are mandatory. | retained as future-engagement/prior-work-experience profiles; inactivity reason is descriptive |
| G4 — Psychological readiness and support for engagement | Self-Determination Theory extension recorded in the survey | future_orientation_g, employment_self_efficacy, support_for_engagement | 3 | 100.0 | Combines direction/planning, perceived capability to find work or training, and anticipated support for re-engagement. | The survey contains one item for each component. Cluster original ordered answers; do not construct or claim a validated SDT scale. | excluded from clustering; use descriptive cross-tabulation |
| G5 — Labour-market social connection | Bourdieu social capital | employment_network_quality, labour_market_connection | 2 | 100.0 | Measures access to people who could help and the flow of information about employment or training opportunities. | Only two closely related indicators are available. They may be better reported as a cross-tabulation unless clustering is cross-method stable and adds more than a direct response-pattern table. | candidate — requires approval and empirical validation |

No dimension is automatically approved by this audit. No total score or formula is proposed. If a dimension is approved, respondents should be compared on their original mixed responses using equal-weight, missing-aware Gower distance, followed by K-medoids/spectral comparison, resampling, dominance and permutation checks.

## Variables deliberately kept outside clustering distances

- `time_use_decision_maker` is substantively important but is one nominal constraint/autonomy question. It should describe inactivity profiles rather than create a standalone capital or autonomy dimension.
- `expected_highest_edu_g` is applicable only to respondents wanting further education and has 57.1% coverage; it is a programme-mapping descriptor.
- Parental occupations remain descriptors until a defensible occupational-class crosswalk is adopted.
- Demographics are used to describe profiles and assess equity, not to create need profiles.
- Conditional education/spell histories are not supplied to an all-Branch-G distance.
- Pre-rerouting unemployment/temporary-absence gateway questions are routing/audit fields.

## Complete variable-role summary

| proposed_role | proposed_dimension | variable_count | minimum_coverage_percent | variables |
|---|---|---|---|---|
| conditional descriptor | Not used in all-Branch-G distance | 13 | 7.1 | age_first_married, spouse_activity, num_children, reason_left_edu, highest_edu_completed, edu_end_year, spell1_activity, spell2_activity, spell1_is_current, spell2_is_current, spell1_contract, spell1_satisfaction, spell1_end_reason |
| profile/programme-mapping descriptor | Not a clustering dimension | 21 | 26.8 | age_group, gender, district, area_type, moved_from_origin, move_reason, marital_status, has_children, father_occ, mother_occ, work_while_study_type, work_while_study_paid, work_while_study_hours, work_while_study_motivation, edu_min_for_decent_job, most_important_life_goal, most_useful_quality_for_job, ideal_work_type, ideal_sector, time_use_decision_maker, expected_highest_edu_g |
| proposed clustering input | G1 — Household economic resources and dependency | 6 | 100.0 | household_size, household_income, household_workers, household_unemployed, primary_earner_status, primary_income_source |
| proposed clustering input | G2 — Educational and inherited cultural capital | 4 | 100.0 | father_edu, mother_edu, edu_status, worked_while_studying |
| proposed clustering input | G3 — Inactivity pathway and future engagement intention | 4 | 100.0 | reason_not_in_labour_force, ever_worked, wants_to_work_future, wants_further_edu |
| proposed clustering input | G4 — Psychological readiness and support for engagement | 3 | 100.0 | future_orientation_g, employment_self_efficacy, support_for_engagement |
| proposed clustering input | G5 — Labour-market social connection | 2 | 100.0 | employment_network_quality, labour_market_connection |
| routing/audit only | Not a clustering dimension | 9 | 8.9 | current_activity_status, desire_for_work, active_search_4weeks, search_method_primary, wanted_to_work, reason_not_seeking, available_to_start, has_job_to_return, looking_while_absent |

## Complete 62-variable audit

| question_id | survey_section | variable | framework_recorded_in_survey | observed_records | coverage_percent | proposed_role | proposed_dimension | question_text |
|---|---|---|---|---|---|---|---|---|
| A1 | A | age_group | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your age? |
| A2 | A | gender | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your gender? |
| A3 | A | district | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Which district do you currently live in? |
| A4 | A | area_type | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | How would you describe your current place of residence? |
| A5 | A | moved_from_origin | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Do you live in the same area where you grew up? |
| A6 | A | move_reason | SWTS | 15 | 26.8 | profile/programme-mapping descriptor | Not a clustering dimension | What was the main reason you moved to your current area? |
| A7 | A | marital_status | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your current marital status? |
| A8 | A | age_first_married | SWTS | 13 | 23.2 | conditional descriptor | Not used in all-Branch-G distance | At what age were you first married? |
| A9 | A | spouse_activity | SWTS | 13 | 23.2 | conditional descriptor | Not used in all-Branch-G distance | What does your spouse or partner currently do? |
| A10 | A | has_children | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Do you have any children? |
| A11 | A | num_children | SWTS | 10 | 17.9 | conditional descriptor | Not used in all-Branch-G distance | How many children do you have? |
| A12 | A | father_edu | SWTS | 56 | 100.0 | proposed clustering input | G2 — Educational and inherited cultural capital | What is the highest level of education your father completed? |
| A13 | A | mother_edu | SWTS | 56 | 100.0 | proposed clustering input | G2 — Educational and inherited cultural capital | What is the highest level of education your mother completed? |
| A14 | A | father_occ | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is or was your father's main occupation? |
| A15 | A | mother_occ | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is or was your mother's main occupation? |
| A16 | A | household_size | SWTS | 56 | 100.0 | proposed clustering input | G1 — Household economic resources and dependency | How many people live in your household in total? |
| A17 | A | household_income | SWTS | 56 | 100.0 | proposed clustering input | G1 — Household economic resources and dependency | What is the approximate total monthly income of your household from all sources? |
| A18 | A | household_workers | SWTS | 56 | 100.0 | proposed clustering input | G1 — Household economic resources and dependency | How many people in your household are currently working for a salary or wage? |
| A19 | A | household_unemployed | SWTS | 56 | 100.0 | proposed clustering input | G1 — Household economic resources and dependency | How many people in your household are currently without work and actively looking for a job? |
| A20 | A | primary_earner_status | Bourdieu | 56 | 100.0 | proposed clustering input | G1 — Household economic resources and dependency | Are you the primary income earner in your household? |
| A21 | A | employment_network_quality | Bourdieu | 56 | 100.0 | proposed clustering input | G5 — Labour-market social connection | Do you personally know people who could help you find employment or training opportunities? |
| B1 | B | edu_status | SWTS | 56 | 100.0 | proposed clustering input | G2 — Educational and inherited cultural capital | Which best describes your most recent education? |
| B2 | B | reason_left_edu | SWTS | 7 | 12.5 | conditional descriptor | Not used in all-Branch-G distance | What was the main reason you left education before completing it? |
| B3 | B | highest_edu_completed | SWTS | 15 | 26.8 | conditional descriptor | Not used in all-Branch-G distance | What is the highest level of education you have completed? |
| B4 | B | edu_end_year | SWTS | 15 | 26.8 | conditional descriptor | Not used in all-Branch-G distance | Approximately what year did you finish or leave your most recent education? |
| B5a_1 | B | spell1_activity | SWTS | 15 | 26.8 | conditional descriptor | Not used in all-Branch-G distance | Immediately after leaving or finishing education, what was your main activity? |
| B5a_2 | B | spell2_activity | SWTS | 4 | 7.1 | conditional descriptor | Not used in all-Branch-G distance | After that first spell, what did you move on to next? |
| B5b_1 | B | spell1_is_current | SWTS | 15 | 26.8 | conditional descriptor | Not used in all-Branch-G distance | Is that still your current situation, or did it end and you moved on to something else? |
| B5b_2 | B | spell2_is_current | SWTS | 4 | 7.1 | conditional descriptor | Not used in all-Branch-G distance | Is that second activity still your current situation? |
| B6_1 | B | spell1_contract | SWTS | 4 | 7.1 | conditional descriptor | Not used in all-Branch-G distance | In that first job after education, what kind of employment contract did you have? |
| B7_1 | B | spell1_satisfaction | SWTS | 4 | 7.1 | conditional descriptor | Not used in all-Branch-G distance | How satisfied were you with that first job overall? |
| B8_1 | B | spell1_end_reason | SWTS | 4 | 7.1 | conditional descriptor | Not used in all-Branch-G distance | Why did that first activity end? |
| B9 | B | worked_while_studying | SWTS | 56 | 100.0 | proposed clustering input | G2 — Educational and inherited cultural capital | Did you work (or do you currently work) while studying? |
| B10 | B | work_while_study_type | SWTS | 18 | 32.1 | profile/programme-mapping descriptor | Not a clustering dimension | How would you describe that work experience while studying? |
| B11 | B | work_while_study_paid | SWTS | 18 | 32.1 | profile/programme-mapping descriptor | Not a clustering dimension | Was that work paid or unpaid? |
| B12 | B | work_while_study_hours | SWTS | 18 | 32.1 | profile/programme-mapping descriptor | Not a clustering dimension | How many hours per week did you work while studying? |
| B13 | B | work_while_study_motivation | SWTS | 18 | 32.1 | profile/programme-mapping descriptor | Not a clustering dimension | What was your main motivation for working while studying? |
| B14 | B | edu_min_for_decent_job | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | In your opinion, what is the minimum level of education a person needs to get a decent job today? |
| B15 | B | most_important_life_goal | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is the most important goal in your life right now? |
| B16 | B | most_useful_quality_for_job | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Which quality do you think is most useful for finding a good job? |
| B17 | B | ideal_work_type | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Ideally, what type of work would you prefer? |
| B18 | B | ideal_sector | SWTS | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Ideally, in which sector or industry do you want to work? |
| B19 | B | primary_income_source | SWTS | 56 | 100.0 | proposed clustering input | G1 — Household economic resources and dependency | Currently, where does most of your money come from? |
| B20 | B | current_activity_status | SWTS | 56 | 100.0 | routing/audit only | Not a clustering dimension | In the past week, what was your main activity? |
| D1 | D | desire_for_work | SWTS | 20 | 35.7 | routing/audit only | Not a clustering dimension | Are you currently looking for work or trying to set up your own business? |
| D2 | D | active_search_4weeks | SWTS | 11 | 19.6 | routing/audit only | Not a clustering dimension | In the past four weeks, have you taken any active steps to find work or set up a business? |
| D3 | D | search_method_primary | SWTS | 5 | 8.9 | routing/audit only | Not a clustering dimension | What was the most active method you used to look for work in the past four weeks? |
| D4 | D | wanted_to_work | SWTS | 6 | 10.7 | routing/audit only | Not a clustering dimension | Even though you did not actively search, did you want to work last week? |
| D5 | D | reason_not_seeking | SWTS | 6 | 10.7 | routing/audit only | Not a clustering dimension | What is the main reason you did not actively seek work in the past four weeks? |
| D6 | D | available_to_start | SWTS | 11 | 19.6 | routing/audit only | Not a clustering dimension | If a job opportunity had arisen last week, would you have been able to start work? |
| E1 | E | has_job_to_return | SWTS | 6 | 10.7 | routing/audit only | Not a clustering dimension | Even though you were not working last week, do you have a job or business to return to? |
| E2 | E | looking_while_absent | SWTS | 6 | 10.7 | routing/audit only | Not a clustering dimension | Are you looking for work or trying to set up a business? |
| BF1 | F | time_use_decision_maker | Bourdieu | 56 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Who mainly determines how you spend your time on a day-to-day basis? |
| F1 | F | reason_not_in_labour_force | SWTS | 56 | 100.0 | proposed clustering input | G3 — Inactivity pathway and future engagement intention | What is your main reason for not currently working or actively looking for work? |
| SF1 | F | future_orientation_g | SDT | 56 | 100.0 | proposed clustering input | G4 — Psychological readiness and support for engagement | How would you describe your sense of direction about your future? |
| BF2 | F | labour_market_connection | Bourdieu | 56 | 100.0 | proposed clustering input | G5 — Labour-market social connection | How connected do you feel to information and opportunities about employment and training? |
| F2 | F | ever_worked | SWTS | 56 | 100.0 | proposed clustering input | G3 — Inactivity pathway and future engagement intention | Have you ever worked for pay or profit at any point in your life? |
| SF2 | F | employment_self_efficacy | SDT | 56 | 100.0 | proposed clustering input | G4 — Psychological readiness and support for engagement | If you decided to actively look for work or training right now, how confident are you that you could be successful? |
| F3 | F | wants_to_work_future | SWTS | 56 | 100.0 | proposed clustering input | G3 — Inactivity pathway and future engagement intention | Do you want to work in the future? |
| SF3 | F | support_for_engagement | SDT | 56 | 100.0 | proposed clustering input | G4 — Psychological readiness and support for engagement | If you were to start working or studying, how much support could you expect from the people around you? |
| F4 | F | wants_further_edu | SWTS | 56 | 100.0 | proposed clustering input | G3 — Inactivity pathway and future engagement intention | Do you want to continue or start education or training in the future? |
| F5 | F | expected_highest_edu_g | SWTS | 32 | 57.1 | profile/programme-mapping descriptor | Not a clustering dimension | What is the highest level of education or training you would like to eventually achieve? |

## Initial data-quality findings

- Strict valid final-Branch-G records: 56.
- Collectively answerable active-path variables: 62.
- Household count conflicts requiring pairwise unavailability rather than correction: 5.
- Household-income refusals: 3.
- `reason_not_in_labour_force` has 13 observed categories; it must remain nominal and may dominate G3.
- The three G4 psychological-readiness items and the two G5 social-connection items have full coverage and all four ordered response levels represented.

## Theory sources

- ILO School-to-Work Transition Survey: inactivity reason, previous employment, and future work/education engagement.
- Bourdieu (1986), *The Forms of Capital*: household economic resources, family educational background, and employment-network resources.
- Deci and Ryan (2000) and the local survey extension: perceived direction, competence/self-efficacy, and relatedness/support for engagement.
- Local `nysc_supervisor_prep.docx`: Branch G was intended to distinguish temporarily constrained, discouraged, and voluntarily inactive youth while retaining motivational and capital context.

## Recommended modelling order

1. G4 psychological readiness and support — three coherent full-coverage branch-specific indicators.
2. G3 inactivity pathway and future engagement — highly actionable, but requires a strong dominance test for inactivity reason.
3. G5 labour-market social connection — theoretically clear but only two indicators; use a cross-tab if clustering adds no value.
4. G1 household economic resources/dependency — test carefully for income-source dominance and count consistency.
5. G2 educational/inherited cultural capital — test last because prior branches showed weak or work-exposure-led solutions.

G1, G4, G3 and G2 have now been run. Under the earlier no-overlapping-social-connectedness decision, G5 remains skipped. All proposed Branch G dimensions are therefore tested or explicitly skipped.

## G1 clustering result

The six original variables were represented by five equal-weight Gower components: ordered household-income position, household worker share, household unemployed share, primary-earner responsibility and nominal primary income source. Household size was used only as the denominator for the two shares, preventing it from receiving a second independent weight. Three income refusals were treated as unavailable pairwise, and five internally inconsistent household-count records made only the two affected share components unavailable; no values were invented.

The selected consensus solution has two profiles:

| Profile | Records | Percent | Defining response pattern |
|---|---:|---:|---|
| Predominantly family/partner-supported non-provider | 41 | 73.2% | 90.2% said someone else was the main provider; 75.6% reported parents/family and 14.6% a partner/spouse as their main personal income source. |
| Predominantly self-income provider/contributor | 15 | 26.8% | 46.7% were the primary earner and 40.0% shared that role; 66.7% reported a regular job/business as their main personal income source. |

The solution passed all nine prespecified screening checks: Gower silhouette 0.372, consensus-ensemble bootstrap mean ARI 1.000, agreement with full K-medoids 0.854 and spectral clustering 0.718, minimum profile size 15, ambiguous membership 3.6%, low original-space confidence 10.7%, and an independently shuffled-variable permutation result of p=0.012 (100 repetitions). No single item exactly recreated the final partition; the strongest was primary income source at ARI 0.640.

The interpretation must nevertheless be narrow. Removing primary income source reduced agreement to ARI 0.356, removing primary-earner status reduced it to 0.480, and the three structural resource indicators alone produced ARI -0.016 against the final profiles. Consequently, this is retained as an exploratory **household economic role/dependency** segmentation. It is not evidence for two low-versus-high economic-capital classes. Confirmation in a larger independent sample is still required.

## G4 clustering result

G4 used the three original four-level ordered answers—`future_orientation_g`, `employment_self_efficacy`, and `support_for_engagement`—with equal-weight Gower distance. All 56 respondents answered all three questions. No combined readiness or SDT score was constructed.

No k=2–4 candidate kept at least 15 respondents in every cluster under both K-medoids and spectral clustering. The best diagnostic k=2 consensus contained 45 respondents with generally greater direction, confidence and support and 11 respondents who were predominantly lost, not confident and lacking support. This diagnostic had Gower silhouette 0.539, ensemble bootstrap mean ARI 0.984, permutation p=0.010 and spectral agreement ARI 1.000, but K-medoids agreement was only ARI 0.590. More importantly, the smaller profile had only 11 respondents, and removing self-efficacy changed the clustering almost completely (ARI -0.017); removing future orientation also produced low agreement (ARI 0.174).

Therefore G4 is **excluded as a clustering dimension**. Its three variables remain theoretically meaningful and programme-relevant, but should be reported through response distributions or a three-way descriptive table until a larger sample can support a stable constrained subgroup. The diagnostic assignments must not be used as validated youth classifications.

## G3 clustering result

G3 used four original categorical answers: current reason for inactivity, whether the respondent had ever worked, desire to work in future, and desire for future education/training. All variables had complete coverage. Inactivity reason and the three-level education intention were kept nominal; no arbitrary ranking or readiness score was introduced.

The selected k=2 consensus produced two profiles:

| Profile | Records | Percent | Defining pattern |
|---|---:|---:|---|
| Work-and-education engaged, mostly prior work experience | 35 | 62.5% | 97.1% wanted future work, 85.7% wanted further education, and 82.9% had worked before. |
| Low/uncertain engagement, mostly no prior work experience | 21 | 37.5% | 71.4% did not want future work, 61.9% were unsure about further education, and 76.2% had never worked. |

All ten screening checks passed: Gower silhouette 0.413, ensemble bootstrap mean ARI 1.000, full K-medoids agreement 0.928, spectral agreement 1.000, minimum profile size 21, ambiguous consensus membership 1.8%, low original-space confidence 12.5%, and permutation p=0.011. No single question reproduced the grouping: the strongest single-item ARI was 0.554 for further-education intention.

The original G3 label must be narrowed. Removing `reason_not_in_labour_force` reproduced the final partition exactly (ARI 1.000), whereas removing future-work intention reduced agreement to ARI 0.357. Thus the result is retained as **future-engagement and prior-work-experience profiles**. The 13-category inactivity reason should describe needs inside each profile, not be claimed as the reason the profiles separate. Intentions are stated responses, not guaranteed future behaviour, and replication beyond this sample of 56 remains necessary.

## G2 clustering result

G2 used ordered parental education, nominal current/recent education status, and binary work-while-studying experience. Questionnaire codes 0–7 supplied the parental-education order; five father and four mother unknown/refusal answers were treated as pairwise unavailable rather than ranked. No cultural-capital score was constructed.

The diagnostic k=2 result produced groups of 38 and 18 and appeared highly stable, with silhouette 0.474 and agreement of ARI 1.000 with both K-medoids and spectral clustering. This apparent stability is not a valid multidimensional result: the groups exactly reproduced `worked_while_studying` (single-item ARI 1.000), and removing that question changed the partition to ARI 0.004. Removing either parental-education variable or education status left the grouping unchanged at ARI 1.000. Both groups also had the same median father- and mother-education position (3/7, corresponding to A/L in the ordered coding). The searched independent-column permutation result was non-significant at p=0.230.

Therefore G2 is **excluded from clustering**. Parental education, education status and work exposure remain meaningful descriptive variables, but the diagnostic no-versus-yes work-while-studying split must not be called cultural-capital profiles.

## Final Branch G dimension decisions

| Dimension | Final decision |
|---|---|
| G1 household economic resources/dependency | Retained narrowly as household economic role/dependency profiles. |
| G2 educational/inherited cultural capital | Rejected; exactly reproduced work while studying. |
| G3 inactivity pathway/future engagement | Retained narrowly as future-engagement/prior-work-experience profiles. |
| G4 psychological readiness/support | Rejected; no size-eligible, cross-method-stable solution. |
| G5 labour-market social connection | Skipped under the earlier no-overlapping-social-connectedness decision. |
