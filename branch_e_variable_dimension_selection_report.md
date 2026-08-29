# Branch E variable and dimension selection report

## Cohort and scope

This report covers the 34 strict new-survey-structure respondents whose corrected final analytical branch is E — unemployed/available and seeking or wanting work. The live application records these questions in implementation Section `D`; the research document calls the analytical group Branch `E`. The final translated path, not the entry branch, controls inclusion.

The active paths contain 75 collectively answerable variables. Core common questions and most Branch-E search questions have complete canonical coverage. Conditional questions such as search method, refusal reason and minimum-wage band remain descriptors rather than universal clustering inputs.

## Recommended candidate Level-1 dimensions

| dimension | framework | variables | number_of_inputs | minimum_coverage_percent | why_grouped | caution | clustering_status |
|---|---|---|---|---|---|---|---|
| E1 — Job-search psychological readiness and support | Self-Determination Theory extension recorded in the survey | job_search_self_efficacy, job_search_autonomy_orientation, social_support_job_search, future_planning_orientation | 4 | 100.0 | Captures perceived search capability, autonomous versus pressured search orientation, social support, and future direction while seeking work. | Each construct has one ordered item. Use original responses and do not claim a validated SDT or employability-readiness scale. | candidate — requires approval and empirical validation |
| E2 — Search intensity and accumulated exposure | ILO School-to-Work Transition Survey | active_search_4weeks, job_search_duration, num_applications, num_interviews | 4 | 100.0 | Represents recent search activation, time exposed to unemployment/search, and accumulated applications and interviews. | Application/interview counts are exposure-dependent and contain large values. Raw-range versus robust/log-count sensitivity is mandatory; this is not a job-seeker effort score. | candidate — requires approval and empirical validation |
| E3 — Economic urgency and job-acceptance constraints | Bourdieu field/economic position + ILO SWTS job acceptance | income_urgency, job_acceptance_conditions, has_minimum_wage | 3 | 100.0 | Combines urgency to earn with the conditions and minimum-income boundary affecting which job offers respondents would accept. | These are stated constraints/preferences, not an economic-capital scale. The binary minimum-wage answer or the highly concentrated urgency item may dominate. | candidate — requires approval and empirical validation |
| E4 — Education-to-work preparedness and learning orientation | ILO School-to-Work Transition Survey human-capital transition | past_edu_usefulness, plans_further_edu, expected_highest_edu_e | 3 | 100.0 | Captures perceived usefulness of past education and stated orientation toward additional education or training. | Perceived usefulness and future educational plans are related but not one validated latent construct. Keep nominal responses nominal and require leave-one-item-out validation. | candidate — requires approval and empirical validation |
| E5 — Household economic resources and dependency | Bourdieu economic capital + ILO SWTS household structure | household_income, household_size, household_workers, household_unemployed, primary_earner_status, primary_income_source | 6 | 100.0 | Captures household resource position, worker/job-seeker composition, and the respondent's dependence or responsibility for income. | Household counts require consistency checks and income source may produce a direct dependency split. Interpret economic role separately from resource level. | candidate — requires approval and empirical validation |
| E6 — Educational and inherited cultural capital | Bourdieu cultural capital + ILO SWTS education history | father_edu, mother_edu, edu_status, worked_while_studying | 4 | 100.0 | Represents parental educational background, current/recent education position, and work exposure while studying. | Parental education is a proxy, not merit or ability. Prior branches produced work-while-studying-dominated results, so test last if at all. | candidate — requires approval and empirical validation |
| E7 — Job-search social capital | Bourdieu social capital | employment_network_quality, knows_people_in_target_sector, network_helpfulness | 3 | 100.0 | Measures general employment contacts, sector-specific contacts, and whether those contacts have actually helped the search. | This overlaps the previously excluded social-connectedness dimensions and is marked skipped unless the research scope changes. | skipped under no-overlapping-social-connectedness decision |

No dimension is automatically approved by this audit. No total score or formula is proposed. If a dimension is approved, respondents should be compared on their original mixed responses using equal-weight, missing-aware Gower distance, followed by K-medoids/spectral comparison, resampling, dominance and permutation checks.

## Variables deliberately kept outside clustering distances

- `main_obstacle_finding_work`, `training_type_would_help`, `employment_service_help` and `job_type_sought` are direct programme-mapping descriptors; using them to create clusters would risk merely reproducing the answer categories that should later guide intervention matching.
- Search method, non-search reason, refusal reason and minimum-wage band are conditional and cannot enter an all-Branch-E distance without inventing values for inapplicable respondents.
- Parental occupations remain descriptors until a defensible occupational-class crosswalk is adopted.
- Demographics are used to describe profiles and assess equity, not to create need profiles.
- Conditional education/spell histories are not supplied to an all-Branch-E distance.
- Constant eligibility/routing questions validate Branch E membership rather than recreate it.

## Complete variable-role summary

| proposed_role | proposed_dimension | variable_count | minimum_coverage_percent | variables |
|---|---|---|---|---|
| conditional descriptor | Not used in all-Branch-E distance | 16 | 2.9 | age_first_married, spouse_activity, reason_left_edu, highest_edu_completed, edu_end_year, spell1_activity, spell2_activity, spell1_is_current, spell2_is_current, spell1_contract, spell1_satisfaction, spell1_end_reason, search_method_primary, reason_not_seeking, reason_refused_job, minimum_wage_band |
| profile/programme-mapping descriptor | Not a clustering dimension | 26 | 23.5 | age_group, gender, district, area_type, moved_from_origin, move_reason, marital_status, has_children, father_occ, mother_occ, work_while_study_type, work_while_study_paid, work_while_study_hours, work_while_study_motivation, edu_min_for_decent_job, most_important_life_goal, most_useful_quality_for_job, ideal_work_type, ideal_sector, job_type_sought, ever_refused_job, employment_service_help, activity_while_searching, willing_to_relocate, main_obstacle_finding_work, training_type_would_help |
| proposed clustering input | E1 — Job-search psychological readiness and support | 4 | 100.0 | job_search_self_efficacy, job_search_autonomy_orientation, social_support_job_search, future_planning_orientation |
| proposed clustering input | E2 — Search intensity and accumulated exposure | 4 | 100.0 | active_search_4weeks, job_search_duration, num_applications, num_interviews |
| proposed clustering input | E3 — Economic urgency and job-acceptance constraints | 3 | 100.0 | income_urgency, job_acceptance_conditions, has_minimum_wage |
| proposed clustering input | E4 — Education-to-work preparedness and learning orientation | 3 | 100.0 | past_edu_usefulness, plans_further_edu, expected_highest_edu_e |
| proposed clustering input | E5 — Household economic resources and dependency | 6 | 100.0 | household_size, household_income, household_workers, household_unemployed, primary_earner_status, primary_income_source |
| proposed clustering input | E6 — Educational and inherited cultural capital | 4 | 100.0 | father_edu, mother_edu, edu_status, worked_while_studying |
| routing/audit only | Not a clustering dimension | 6 | 14.7 | current_activity_status, desire_for_work, wanted_to_work, available_to_start, has_job_to_return, looking_while_absent |
| skipped clustering input | E7 — Job-search social capital | 3 | 100.0 | employment_network_quality, knows_people_in_target_sector, network_helpfulness |

## Complete 75-variable audit

| question_id | survey_section | variable | framework_recorded_in_survey | observed_records | coverage_percent | proposed_role | proposed_dimension | question_text |
|---|---|---|---|---|---|---|---|---|
| A1 | A | age_group | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your age? |
| A2 | A | gender | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your gender? |
| A3 | A | district | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Which district do you currently live in? |
| A4 | A | area_type | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | How would you describe your current place of residence? |
| A5 | A | moved_from_origin | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Do you live in the same area where you grew up? |
| A6 | A | move_reason | SWTS | 8 | 23.5 | profile/programme-mapping descriptor | Not a clustering dimension | What was the main reason you moved to your current area? |
| A7 | A | marital_status | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your current marital status? |
| A8 | A | age_first_married | SWTS | 1 | 2.9 | conditional descriptor | Not used in all-Branch-E distance | At what age were you first married? |
| A9 | A | spouse_activity | SWTS | 1 | 2.9 | conditional descriptor | Not used in all-Branch-E distance | What does your spouse or partner currently do? |
| A10 | A | has_children | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Do you have any children? |
| A12 | A | father_edu | SWTS | 34 | 100.0 | proposed clustering input | E6 — Educational and inherited cultural capital | What is the highest level of education your father completed? |
| A13 | A | mother_edu | SWTS | 34 | 100.0 | proposed clustering input | E6 — Educational and inherited cultural capital | What is the highest level of education your mother completed? |
| A14 | A | father_occ | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is or was your father's main occupation? |
| A15 | A | mother_occ | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is or was your mother's main occupation? |
| A16 | A | household_size | SWTS | 34 | 100.0 | proposed clustering input | E5 — Household economic resources and dependency | How many people live in your household in total? |
| A17 | A | household_income | SWTS | 34 | 100.0 | proposed clustering input | E5 — Household economic resources and dependency | What is the approximate total monthly income of your household from all sources? |
| A18 | A | household_workers | SWTS | 34 | 100.0 | proposed clustering input | E5 — Household economic resources and dependency | How many people in your household are currently working for a salary or wage? |
| A19 | A | household_unemployed | SWTS | 34 | 100.0 | proposed clustering input | E5 — Household economic resources and dependency | How many people in your household are currently without work and actively looking for a job? |
| A20 | A | primary_earner_status | Bourdieu | 34 | 100.0 | proposed clustering input | E5 — Household economic resources and dependency | Are you the primary income earner in your household? |
| A21 | A | employment_network_quality | Bourdieu | 34 | 100.0 | skipped clustering input | E7 — Job-search social capital | Do you personally know people who could help you find employment or training opportunities? |
| B1 | B | edu_status | SWTS | 34 | 100.0 | proposed clustering input | E6 — Educational and inherited cultural capital | Which best describes your most recent education? |
| B2 | B | reason_left_edu | SWTS | 1 | 2.9 | conditional descriptor | Not used in all-Branch-E distance | What was the main reason you left education before completing it? |
| B3 | B | highest_edu_completed | SWTS | 5 | 14.7 | conditional descriptor | Not used in all-Branch-E distance | What is the highest level of education you have completed? |
| B4 | B | edu_end_year | SWTS | 5 | 14.7 | conditional descriptor | Not used in all-Branch-E distance | Approximately what year did you finish or leave your most recent education? |
| B5a_1 | B | spell1_activity | SWTS | 5 | 14.7 | conditional descriptor | Not used in all-Branch-E distance | Immediately after leaving or finishing education, what was your main activity? |
| B5a_2 | B | spell2_activity | SWTS | 1 | 2.9 | conditional descriptor | Not used in all-Branch-E distance | After that first spell, what did you move on to next? |
| B5b_1 | B | spell1_is_current | SWTS | 5 | 14.7 | conditional descriptor | Not used in all-Branch-E distance | Is that still your current situation, or did it end and you moved on to something else? |
| B5b_2 | B | spell2_is_current | SWTS | 1 | 2.9 | conditional descriptor | Not used in all-Branch-E distance | Is that second activity still your current situation? |
| B6_1 | B | spell1_contract | SWTS | 1 | 2.9 | conditional descriptor | Not used in all-Branch-E distance | In that first job after education, what kind of employment contract did you have? |
| B7_1 | B | spell1_satisfaction | SWTS | 1 | 2.9 | conditional descriptor | Not used in all-Branch-E distance | How satisfied were you with that first job overall? |
| B8_1 | B | spell1_end_reason | SWTS | 1 | 2.9 | conditional descriptor | Not used in all-Branch-E distance | Why did that first activity end? |
| B9 | B | worked_while_studying | SWTS | 34 | 100.0 | proposed clustering input | E6 — Educational and inherited cultural capital | Did you work (or do you currently work) while studying? |
| B10 | B | work_while_study_type | SWTS | 10 | 29.4 | profile/programme-mapping descriptor | Not a clustering dimension | How would you describe that work experience while studying? |
| B11 | B | work_while_study_paid | SWTS | 10 | 29.4 | profile/programme-mapping descriptor | Not a clustering dimension | Was that work paid or unpaid? |
| B12 | B | work_while_study_hours | SWTS | 10 | 29.4 | profile/programme-mapping descriptor | Not a clustering dimension | How many hours per week did you work while studying? |
| B13 | B | work_while_study_motivation | SWTS | 10 | 29.4 | profile/programme-mapping descriptor | Not a clustering dimension | What was your main motivation for working while studying? |
| B14 | B | edu_min_for_decent_job | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | In your opinion, what is the minimum level of education a person needs to get a decent job today? |
| B15 | B | most_important_life_goal | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is the most important goal in your life right now? |
| B16 | B | most_useful_quality_for_job | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Which quality do you think is most useful for finding a good job? |
| B17 | B | ideal_work_type | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Ideally, what type of work would you prefer? |
| B18 | B | ideal_sector | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Ideally, in which sector or industry do you want to work? |
| B19 | B | primary_income_source | SWTS | 34 | 100.0 | proposed clustering input | E5 — Household economic resources and dependency | Currently, where does most of your money come from? |
| B20 | B | current_activity_status | SWTS | 34 | 100.0 | routing/audit only | Not a clustering dimension | In the past week, what was your main activity? |
| BD1 | D | knows_people_in_target_sector | Bourdieu | 34 | 100.0 | skipped clustering input | E7 — Job-search social capital | Do you personally know anyone working in the sector or occupation you are targeting? |
| D1 | D | desire_for_work | SWTS | 34 | 100.0 | routing/audit only | Not a clustering dimension | Are you currently looking for work or trying to set up your own business? |
| SD1 | D | job_search_self_efficacy | SDT | 34 | 100.0 | proposed clustering input | E1 — Job-search psychological readiness and support | How confident are you that you will eventually find suitable work? |
| BD2 | D | network_helpfulness | Bourdieu | 34 | 100.0 | skipped clustering input | E7 — Job-search social capital | How helpful have your personal contacts actually been in your job search so far? |
| D2 | D | active_search_4weeks | SWTS | 34 | 100.0 | proposed clustering input | E2 — Search intensity and accumulated exposure | In the past four weeks, have you taken any active steps to find work or set up a business? |
| SD2 | D | job_search_autonomy_orientation | SDT | 34 | 100.0 | proposed clustering input | E1 — Job-search psychological readiness and support | When thinking about the work you are searching for, which best describes your approach? |
| BD3 | D | income_urgency | Bourdieu | 34 | 100.0 | proposed clustering input | E3 — Economic urgency and job-acceptance constraints | How urgently do you need to start earning income? |
| D3 | D | search_method_primary | SWTS | 26 | 76.5 | conditional descriptor | Not used in all-Branch-E distance | What was the most active method you used to look for work in the past four weeks? |
| SD3 | D | social_support_job_search | SDT | 34 | 100.0 | proposed clustering input | E1 — Job-search psychological readiness and support | How supported do you feel by the people around you in your efforts to find work? |
| D4 | D | wanted_to_work | SWTS | 8 | 23.5 | routing/audit only | Not a clustering dimension | Even though you did not actively search, did you want to work last week? |
| SD4 | D | future_planning_orientation | SDT | 34 | 100.0 | proposed clustering input | E1 — Job-search psychological readiness and support | How would you describe your sense of direction and planning for the future? |
| D5 | D | reason_not_seeking | SWTS | 8 | 23.5 | conditional descriptor | Not used in all-Branch-E distance | What is the main reason you did not actively seek work in the past four weeks? |
| D6 | D | available_to_start | SWTS | 34 | 100.0 | routing/audit only | Not a clustering dimension | If a job opportunity had arisen last week, would you have been able to start work? |
| D7 | D | job_search_duration | SWTS | 34 | 100.0 | proposed clustering input | E2 — Search intensity and accumulated exposure | For how long have you been available and looking for work? |
| D8 | D | job_type_sought | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What sort of job are you mainly looking for? |
| D9 | D | ever_refused_job | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Have you ever refused a job that was offered to you? |
| D10 | D | reason_refused_job | SWTS | 13 | 38.2 | conditional descriptor | Not used in all-Branch-E distance | What was the main reason you refused that job offer? |
| D11 | D | job_acceptance_conditions | SWTS | 34 | 100.0 | proposed clustering input | E3 — Economic urgency and job-acceptance constraints | If you were offered a job today, which best describes what you would accept? |
| D12 | D | has_minimum_wage | SWTS | 34 | 100.0 | proposed clustering input | E3 — Economic urgency and job-acceptance constraints | Is there a minimum monthly income below which you would not accept a job? |
| D12b | D | minimum_wage_band | SWTS | 28 | 82.4 | conditional descriptor | Not used in all-Branch-E distance | What is the approximate minimum monthly income you would need to accept a job? |
| D13 | D | employment_service_help | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Have you received any assistance from an employment or careers service? |
| D14 | D | activity_while_searching | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What have you mainly been doing while looking for a job? |
| D15 | D | num_applications | SWTS | 34 | 100.0 | proposed clustering input | E2 — Search intensity and accumulated exposure | Since you started looking for work, approximately how many jobs have you applied for? |
| D16 | D | num_interviews | SWTS | 34 | 100.0 | proposed clustering input | E2 — Search intensity and accumulated exposure | Since you started looking for work, how many job interviews have you attended? |
| D17 | D | willing_to_relocate | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Would you consider relocating to find work? |
| D18 | D | main_obstacle_finding_work | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What has been the main obstacle in finding a good job? |
| D19 | D | past_edu_usefulness | SWTS | 34 | 100.0 | proposed clustering input | E4 — Education-to-work preparedness and learning orientation | Do you feel that the education or training you have received is useful for getting a job? |
| D20 | D | training_type_would_help | SWTS | 34 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What kind of training would be most helpful for you to find a job? |
| D21 | D | plans_further_edu | SWTS | 34 | 100.0 | proposed clustering input | E4 — Education-to-work preparedness and learning orientation | Do you plan to continue your education or training in the future? |
| D22 | D | expected_highest_edu_e | SWTS | 34 | 100.0 | proposed clustering input | E4 — Education-to-work preparedness and learning orientation | What is the highest level of education or training you expect to eventually achieve? |
| E1 | E | has_job_to_return | SWTS | 5 | 14.7 | routing/audit only | Not a clustering dimension | Even though you were not working last week, do you have a job or business to return to? |
| E2 | E | looking_while_absent | SWTS | 5 | 14.7 | routing/audit only | Not a clustering dimension | Are you looking for work or trying to set up a business? |

## Initial data-quality findings

- Strict valid final-Branch-E records: 34.
- Collectively answerable active-path variables: 75.
- Household count conflicts requiring pairwise unavailability rather than correction: 0.
- Household-income refusals: 5.
- Maximum reported applications: 80; maximum interviews: 50. Robust/log-count sensitivity is required for E2.
- `desire_for_work` and `available_to_start` are constant eligibility answers; `active_search_4weeks` varies (26 yes, 8 no) and is retained only in the search-process dimension.
- With n=34 and a minimum profile size of 15, only k=2 can be eligible; three profiles would require at least 45 respondents.

## Theory sources

- ILO School-to-Work Transition Survey: search activity, duration, applications/interviews, acceptance conditions, obstacles, services and education-to-work transition.
- Bourdieu (1986), *The Forms of Capital*: household economic position, inherited educational background, search networks and labour-market field constraints.
- Deci and Ryan (2000) and the local survey extension: autonomy, perceived competence, relatedness/support and future direction during job search.
- Local `nysc_supervisor_prep.docx`: Branch E concerns unemployed youth navigating search activity, barriers, motivation, networks and programme-relevant support needs.

## Recommended modelling order

1. E1 job-search psychological readiness/support — the most coherent full-coverage branch-specific set.
2. E2 search intensity/exposure — highly actionable, but requires raw-versus-log count sensitivity.
3. E3 economic urgency/acceptance constraints — test for binary-item and urgency dominance.
4. E4 education-to-work preparedness/learning orientation — keep nominal items nominal and test coherence.
5. E5 household economic resources/dependency — test carefully for income-source dominance and count consistency.
6. E6 educational/inherited cultural capital — test last because previous branches produced work-exposure-led results.
7. E7 job-search social capital — skipped under the earlier no-overlapping-social-connectedness decision.

The recommended first clustering attempt was E1. Because n=34 is small, every result remains exploratory and uses k=2 only under the existing minimum-size rule.

## Post-audit clustering decisions

All six active dimensions were subsequently tested with the common validation pipeline. Full details are in `branch_e_clustering_results_report.md`.

| Dimension | Final decision |
|---|---|
| E1 job-search psychological readiness/support | Rejected: spectral ARI 0.403, smallest source group 11, permutation p=0.050. |
| E2 search intensity/exposure | Rejected: exactly reproduced recent active-search status; groups 26/8. |
| E3 economic urgency/acceptance constraints | Rejected: exactly reproduced the minimum-wage yes/no answer; groups 28/6. |
| E4 education-to-work preparedness/learning orientation | Retained cautiously as education-usefulness/further-learning orientation; groups 18/16, but strongly dependent on `past_edu_usefulness`. |
| E5 household economic resources/dependency | Rejected: groups 22/12, low source agreement and permutation p=0.583. |
| E6 educational/inherited cultural capital | Rejected: exactly reproduced work while studying; groups 24/10. |
| E7 job-search social capital | Skipped under the no-overlap decision. |
