# Branch F variable and dimension selection report

## Cohort and scope

This report covers the corrected new-survey-structure employed branch. There are 82 strict final-Branch-F records; one routing-corrupted record is retained in the cleaned master data but excluded here, leaving 81 valid records.

The raw active survey path contains 105 collectively answerable variables. The earlier 84-variable figure described only the modelling manifest (39 universal + 45 retained Branch-F variables) and omitted conditional follow-ups. This report uses all 105.

The live application calls the employed section `E`, while the research document calls the analytical employed branch `F`. Variables are matched by stable variable name and final path, not by assuming that the section letter is identical.

## Proposed Level-1 clustering dimensions

| dimension | framework | variables | number_of_inputs | minimum_coverage_percent | why_grouped | caution |
|---|---|---|---|---|---|---|
| D1 — Household economic resources and responsibility | Bourdieu economic capital + SWTS household structure | household_income, household_size, household_workers, household_unemployed, primary_earner_status, primary_income_source | 6 | 100.0 | Separates employed youth by resources available to the household and by the respondent's responsibility for providing them. | These are raw indicators, not a published scale. Household counts must be checked for internal consistency before clustering. |
| D2 — Educational and inherited cultural capital | Bourdieu institutionalised/inherited cultural capital + SWTS education history | father_edu, mother_edu, edu_status, worked_while_studying | 4 | 100.0 | Captures family educational background, the respondent's recent educational position, and prior exposure to work while studying. | highest_edu_completed is answered by only 21/81 and must not be interpreted as missing education for the other 60 respondents. |
| D3 — Employment security and formality | ILO SWTS employment quality + Bourdieu field position | contract_type, job_security_12months, sector_formality | 3 | 100.0 | Measures contractual stability, perceived continuity of the job, and formal/informal labour-market position. | enterprise registration and tax payment are descriptors because sector_formality already summarises related information. |
| D4 — Earnings and working-time adequacy | ILO SWTS employment conditions and under/over-employment | monthly_income_band, usual_hours_per_week, income_hours_preference | 3 | 100.0 | Distinguishes low/high earnings and whether respondents want more hours/income, fewer hours/income, or no change. | Actual hours last week can reflect a temporary event, so it is retained as a descriptor rather than double-weighting hours. |
| D5 — Subjective job satisfaction and mobility intention | ILO SWTS satisfactory-employment/transition concept | job_satisfaction, contract_satisfaction, hopes_to_change_job | 3 | 100.0 | Separates respondents who evaluate the job positively and intend to stay from those who are dissatisfied or considering another job. | contract_satisfaction contains reason categories and must be treated as nominal, not as an invented numeric rank. |
| D6 — Qualification use and skill development | Bourdieu cultural-capital utilisation + ILO SWTS education/training relevance | qualification_job_match, past_edu_useful_for_job, received_training | 3 | 100.0 | Captures whether existing qualifications are used, whether prior education is useful, and whether current-job training is occurring. | Training type, provider, duration, and payer are conditional descriptors for the respondents who received training. |
| D7 — Professional social capital | Bourdieu social capital | employment_network_quality, professional_network_growth | 2 | 100.0 | Measures useful employment contacts already available and whether the current job is expanding professional connections. | With only two direct indicators, clustering should proceed only if validation is adequate; otherwise report a cross-tabulation instead. |
| D8 — Work motivation and psychological need experience | Self-Determination Theory (Deci and Ryan, 2000) | work_autonomy, competence_growth_at_work, relatedness_at_work, work_motivation_type | 4 | 100.0 | Directly represents autonomy, competence, relatedness, and autonomous-to-controlled work motivation. | The survey uses one question per construct; cluster raw responses and do not claim a validated SDT scale or invent a total score. |
| D9 — Transition-to-work search pathway and barriers | ILO School-to-Work Transition Survey | registered_as_jobseeker, employment_service_help_f, jobs_applied_before_hire, interviews_before_hire, search_duration_before_hire, obstacle_finding_this_job | 6 | 100.0 | Captures the intensity, duration, institutional support, and main barrier involved in obtaining the current job. | Application/interview counts require outlier checks. Refusal and reservation conditions remain descriptors because they measure selectivity, not search difficulty itself. |

No dimension score or formula is proposed here. Each analysis should compare respondents on the original answers using a mixed-data distance such as Gower distance. Theory determines which variables belong together; it does not justify inventing a total score.

## Complete variable-role summary

| proposed_role | proposed_dimension | variable_count | minimum_coverage_percent | variables |
|---|---|---|---|---|
| conditional descriptor | Not used in all-Branch-F distance | 27 | 1.2 | age_first_married, spouse_activity, num_children, reason_left_edu, highest_edu_completed, edu_end_year, spell1_activity, spell2_activity, spell3_activity, spell1_is_current, spell2_is_current, spell1_contract, spell2_contract, spell1_satisfaction, spell2_satisfaction, spell1_end_reason, spell2_end_reason, reason_temp_absence, reason_below_normal_hours, reason_wants_to_change, insecurity_bothers, reason_not_union, training_type_received, training_provider, training_duration, who_paid_training, reason_refused_job_f |
| profile/programme-mapping descriptor | Not a clustering dimension | 30 | 38.3 | age_group, gender, district, area_type, moved_from_origin, move_reason, marital_status, has_children, father_occ, mother_occ, work_while_study_type, work_while_study_paid, work_while_study_hours, work_while_study_motivation, edu_min_for_decent_job, most_important_life_goal, most_useful_quality_for_job, ideal_work_type, ideal_sector, enterprise_location_type, occupational_class, has_second_job, willing_to_relocate_f, plans_further_edu_f, expected_highest_edu_f, union_member, ever_refused_job_f, acceptance_conditions_search, had_min_wage_during_search, employment_status |
| proposed clustering input | D1 — Household economic resources and responsibility | 6 | 100.0 | household_size, household_income, household_workers, household_unemployed, primary_earner_status, primary_income_source |
| proposed clustering input | D2 — Educational and inherited cultural capital | 4 | 100.0 | father_edu, mother_edu, edu_status, worked_while_studying |
| proposed clustering input | D3 — Employment security and formality | 3 | 100.0 | sector_formality, contract_type, job_security_12months |
| proposed clustering input | D4 — Earnings and working-time adequacy | 3 | 100.0 | usual_hours_per_week, income_hours_preference, monthly_income_band |
| proposed clustering input | D5 — Subjective job satisfaction and mobility intention | 3 | 100.0 | contract_satisfaction, job_satisfaction, hopes_to_change_job |
| proposed clustering input | D6 — Qualification use and skill development | 3 | 100.0 | qualification_job_match, received_training, past_edu_useful_for_job |
| proposed clustering input | D7 — Professional social capital | 2 | 100.0 | employment_network_quality, professional_network_growth |
| proposed clustering input | D8 — Work motivation and psychological need experience | 4 | 100.0 | work_autonomy, competence_growth_at_work, relatedness_at_work, work_motivation_type |
| proposed clustering input | D9 — Transition-to-work search pathway and barriers | 6 | 100.0 | registered_as_jobseeker, employment_service_help_f, jobs_applied_before_hire, interviews_before_hire, search_duration_before_hire, obstacle_finding_this_job |
| routing/audit only | Not a clustering dimension | 2 | 21.0 | current_activity_status, has_job_to_return |
| self-employed subgroup description | Separate n=11 subgroup | 5 | 13.6 | reason_self_employed, business_helpers, business_funding_source, business_profitability, main_business_obstacle |
| validation/profile descriptor | Avoid duplicate or temporary-event weighting | 4 | 100.0 | enterprise_registered, paid_taxes, actual_hours_last_week, hours_below_normal |
| wage-worker subgroup description | Separate n=70 subgroup | 3 | 86.4 | job_recruitment_method, enterprise_size, gender_equality_at_work |

## Complete 105-variable audit

| question_id | survey_section | variable | framework_recorded_in_survey | observed_records | coverage_percent | proposed_role | proposed_dimension | question_text |
|---|---|---|---|---|---|---|---|---|
| A1 | A | age_group | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your age? |
| A2 | A | gender | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your gender? |
| A3 | A | district | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Which district do you currently live in? |
| A4 | A | area_type | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | How would you describe your current place of residence? |
| A5 | A | moved_from_origin | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Do you live in the same area where you grew up? |
| A6 | A | move_reason | SWTS | 31 | 38.3 | profile/programme-mapping descriptor | Not a clustering dimension | What was the main reason you moved to your current area? |
| A7 | A | marital_status | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is your current marital status? |
| A8 | A | age_first_married | SWTS | 6 | 7.4 | conditional descriptor | Not used in all-Branch-F distance | At what age were you first married? |
| A9 | A | spouse_activity | SWTS | 6 | 7.4 | conditional descriptor | Not used in all-Branch-F distance | What does your spouse or partner currently do? |
| A10 | A | has_children | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Do you have any children? |
| A11 | A | num_children | SWTS | 1 | 1.2 | conditional descriptor | Not used in all-Branch-F distance | How many children do you have? |
| A12 | A | father_edu | SWTS | 81 | 100.0 | proposed clustering input | D2 — Educational and inherited cultural capital | What is the highest level of education your father completed? |
| A13 | A | mother_edu | SWTS | 81 | 100.0 | proposed clustering input | D2 — Educational and inherited cultural capital | What is the highest level of education your mother completed? |
| A14 | A | father_occ | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is or was your father's main occupation? |
| A15 | A | mother_occ | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is or was your mother's main occupation? |
| A16 | A | household_size | SWTS | 81 | 100.0 | proposed clustering input | D1 — Household economic resources and responsibility | How many people live in your household in total? |
| A17 | A | household_income | SWTS | 81 | 100.0 | proposed clustering input | D1 — Household economic resources and responsibility | What is the approximate total monthly income of your household from all sources? |
| A18 | A | household_workers | SWTS | 81 | 100.0 | proposed clustering input | D1 — Household economic resources and responsibility | How many people in your household are currently working for a salary or wage? |
| A19 | A | household_unemployed | SWTS | 81 | 100.0 | proposed clustering input | D1 — Household economic resources and responsibility | How many people in your household are currently without work and actively looking for a job? |
| A20 | A | primary_earner_status | Bourdieu | 81 | 100.0 | proposed clustering input | D1 — Household economic resources and responsibility | Are you the primary income earner in your household? |
| A21 | A | employment_network_quality | Bourdieu | 81 | 100.0 | proposed clustering input | D7 — Professional social capital | Do you personally know people who could help you find employment or training opportunities? |
| B1 | B | edu_status | SWTS | 81 | 100.0 | proposed clustering input | D2 — Educational and inherited cultural capital | Which best describes your most recent education? |
| B2 | B | reason_left_edu | SWTS | 1 | 1.2 | conditional descriptor | Not used in all-Branch-F distance | What was the main reason you left education before completing it? |
| B3 | B | highest_edu_completed | SWTS | 21 | 25.9 | conditional descriptor | Not used in all-Branch-F distance | What is the highest level of education you have completed? |
| B4 | B | edu_end_year | SWTS | 21 | 25.9 | conditional descriptor | Not used in all-Branch-F distance | Approximately what year did you finish or leave your most recent education? |
| B5a_1 | B | spell1_activity | SWTS | 21 | 25.9 | conditional descriptor | Not used in all-Branch-F distance | Immediately after leaving or finishing education, what was your main activity? |
| B5a_2 | B | spell2_activity | SWTS | 6 | 7.4 | conditional descriptor | Not used in all-Branch-F distance | After that first spell, what did you move on to next? |
| B5a_3 | B | spell3_activity | SWTS | 4 | 4.9 | conditional descriptor | Not used in all-Branch-F distance | What is your current main activity now? |
| B5b_1 | B | spell1_is_current | SWTS | 21 | 25.9 | conditional descriptor | Not used in all-Branch-F distance | Is that still your current situation, or did it end and you moved on to something else? |
| B5b_2 | B | spell2_is_current | SWTS | 6 | 7.4 | conditional descriptor | Not used in all-Branch-F distance | Is that second activity still your current situation? |
| B6_1 | B | spell1_contract | SWTS | 2 | 2.5 | conditional descriptor | Not used in all-Branch-F distance | In that first job after education, what kind of employment contract did you have? |
| B6_2 | B | spell2_contract | SWTS | 3 | 3.7 | conditional descriptor | Not used in all-Branch-F distance | What kind of employment contract did you have in that second job? |
| B7_1 | B | spell1_satisfaction | SWTS | 2 | 2.5 | conditional descriptor | Not used in all-Branch-F distance | How satisfied were you with that first job overall? |
| B7_2 | B | spell2_satisfaction | SWTS | 3 | 3.7 | conditional descriptor | Not used in all-Branch-F distance | How satisfied were you with that second job? |
| B8_1 | B | spell1_end_reason | SWTS | 2 | 2.5 | conditional descriptor | Not used in all-Branch-F distance | Why did that first activity end? |
| B8_2 | B | spell2_end_reason | SWTS | 3 | 3.7 | conditional descriptor | Not used in all-Branch-F distance | Why did that second activity end? |
| B9 | B | worked_while_studying | SWTS | 81 | 100.0 | proposed clustering input | D2 — Educational and inherited cultural capital | Did you work (or do you currently work) while studying? |
| B10 | B | work_while_study_type | SWTS | 63 | 77.8 | profile/programme-mapping descriptor | Not a clustering dimension | How would you describe that work experience while studying? |
| B11 | B | work_while_study_paid | SWTS | 63 | 77.8 | profile/programme-mapping descriptor | Not a clustering dimension | Was that work paid or unpaid? |
| B12 | B | work_while_study_hours | SWTS | 63 | 77.8 | profile/programme-mapping descriptor | Not a clustering dimension | How many hours per week did you work while studying? |
| B13 | B | work_while_study_motivation | SWTS | 63 | 77.8 | profile/programme-mapping descriptor | Not a clustering dimension | What was your main motivation for working while studying? |
| B14 | B | edu_min_for_decent_job | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | In your opinion, what is the minimum level of education a person needs to get a decent job today? |
| B15 | B | most_important_life_goal | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | What is the most important goal in your life right now? |
| B16 | B | most_useful_quality_for_job | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Which quality do you think is most useful for finding a good job? |
| B17 | B | ideal_work_type | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Ideally, what type of work would you prefer? |
| B18 | B | ideal_sector | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Ideally, in which sector or industry do you want to work? |
| B19 | B | primary_income_source | SWTS | 81 | 100.0 | proposed clustering input | D1 — Household economic resources and responsibility | Currently, where does most of your money come from? |
| B20 | B | current_activity_status | SWTS | 81 | 100.0 | routing/audit only | Not a clustering dimension | In the past week, what was your main activity? |
| BE1 | E | qualification_job_match | Bourdieu | 81 | 100.0 | proposed clustering input | D6 — Qualification use and skill development | How well does your current job use your actual qualifications and training? |
| E1 | E | has_job_to_return | SWTS | 17 | 21.0 | routing/audit only | Not a clustering dimension | Even though you were not working last week, do you have a job or business to return to? |
| SE1 | E | work_autonomy | SDT | 81 | 100.0 | proposed clustering input | D8 — Work motivation and psychological need experience | How much autonomy and choice do you have in how you carry out your work? |
| BE2 | E | sector_formality | Bourdieu | 81 | 100.0 | proposed clustering input | D3 — Employment security and formality | How would you describe the formality of your work situation? |
| SE2 | E | competence_growth_at_work | SDT | 81 | 100.0 | proposed clustering input | D8 — Work motivation and psychological need experience | Does your current work help you grow, develop new skills, and feel more capable? |
| BE3 | E | professional_network_growth | Bourdieu | 81 | 100.0 | proposed clustering input | D7 — Professional social capital | Has this job expanded your professional network and connections in any meaningful way? |
| E3 | E | reason_temp_absence | SWTS | 17 | 21.0 | conditional descriptor | Not used in all-Branch-F distance | Why did you not work last week? |
| SE3 | E | relatedness_at_work | SDT | 81 | 100.0 | proposed clustering input | D8 — Work motivation and psychological need experience | How connected and supported do you feel by the people you work with? |
| E4 | E | enterprise_location_type | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Where is the workplace or business you work at located? |
| SE4 | E | work_motivation_type | SDT | 81 | 100.0 | proposed clustering input | D8 — Work motivation and psychological need experience | What primarily motivates you to do this job? |
| E5 | E | enterprise_registered | SWTS | 81 | 100.0 | validation/profile descriptor | Avoid duplicate or temporary-event weighting | Is the business or enterprise you work for officially registered with government authorities? |
| E6 | E | paid_taxes | SWTS | 81 | 100.0 | validation/profile descriptor | Avoid duplicate or temporary-event weighting | Did you pay taxes last year on your earnings from this work? |
| E7 | E | occupational_class | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Which occupational class best describes your current job? |
| E8 | E | contract_type | SWTS | 81 | 100.0 | proposed clustering input | D3 — Employment security and formality | What kind of employment contract are you currently working under? |
| E9 | E | contract_satisfaction | SWTS | 81 | 100.0 | proposed clustering input | D5 — Subjective job satisfaction and mobility intention | How do you feel about your current contract situation? |
| E10 | E | has_second_job | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | In addition to your main job, do you have a second job? |
| E11 | E | usual_hours_per_week | SWTS | 81 | 100.0 | proposed clustering input | D4 — Earnings and working-time adequacy | How many hours per week do you usually work at your main job? |
| E12 | E | actual_hours_last_week | SWTS | 81 | 100.0 | validation/profile descriptor | Avoid duplicate or temporary-event weighting | Last week, how many hours did you actually work at your main job? |
| E13 | E | income_hours_preference | SWTS | 81 | 100.0 | proposed clustering input | D4 — Earnings and working-time adequacy | If you could choose regarding your work hours and income, which would you prefer? |
| E14 | E | hours_below_normal | SWTS | 81 | 100.0 | validation/profile descriptor | Avoid duplicate or temporary-event weighting | Were your actual hours worked last week less than your normal working hours? |
| E15 | E | reason_below_normal_hours | SWTS | 32 | 39.5 | conditional descriptor | Not used in all-Branch-F distance | What was the main reason you worked fewer hours than normal last week? |
| E16 | E | monthly_income_band | SWTS | 81 | 100.0 | proposed clustering input | D4 — Earnings and working-time adequacy | On average, what is your total income from work per month? |
| E17 | E | job_satisfaction | SWTS | 81 | 100.0 | proposed clustering input | D5 — Subjective job satisfaction and mobility intention | Overall, how satisfied are you with your main job? |
| E18 | E | hopes_to_change_job | SWTS | 81 | 100.0 | proposed clustering input | D5 — Subjective job satisfaction and mobility intention | Do you hope to change your main job in the future? |
| E19 | E | reason_wants_to_change | SWTS | 46 | 56.8 | conditional descriptor | Not used in all-Branch-F distance | What is the most important reason you want to change your job? |
| E20 | E | job_security_12months | SWTS | 81 | 100.0 | proposed clustering input | D3 — Employment security and formality | How likely is it that you will be able to keep your main job over the next 12 months? |
| E21 | E | insecurity_bothers | SWTS | 34 | 42.0 | conditional descriptor | Not used in all-Branch-F distance | Does the uncertainty about your job situation bother you? |
| E22 | E | willing_to_relocate_f | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Would you consider relocating to find different or better work? |
| E23 | E | plans_further_edu_f | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Do you plan to continue your education or training in the future? |
| E24 | E | expected_highest_edu_f | SWTS | 71 | 87.7 | profile/programme-mapping descriptor | Not a clustering dimension | What is the highest level of education or training you expect to eventually achieve? |
| E25 | E | union_member | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Are you a member of a trade union or worker's association? |
| E26 | E | reason_not_union | SWTS | 75 | 92.6 | conditional descriptor | Not used in all-Branch-F distance | Why are you not a member of a trade union? |
| E27 | E | received_training | SWTS | 81 | 100.0 | proposed clustering input | D6 — Qualification use and skill development | Did you receive any training or development specifically for your current job? |
| E28 | E | training_type_received | SWTS | 65 | 80.2 | conditional descriptor | Not used in all-Branch-F distance | What was the main type of training you received for this job? |
| E29 | E | training_provider | SWTS | 65 | 80.2 | conditional descriptor | Not used in all-Branch-F distance | Who provided that training? |
| E30 | E | training_duration | SWTS | 65 | 80.2 | conditional descriptor | Not used in all-Branch-F distance | How long did that training last? |
| E31 | E | who_paid_training | SWTS | 65 | 80.2 | conditional descriptor | Not used in all-Branch-F distance | Who mainly paid for that training? |
| E32 | E | registered_as_jobseeker | SWTS | 81 | 100.0 | proposed clustering input | D9 — Transition-to-work search pathway and barriers | Before getting this job, did you register as a jobseeker with any employment service? |
| E33 | E | employment_service_help_f | SWTS | 81 | 100.0 | proposed clustering input | D9 — Transition-to-work search pathway and barriers | Did you receive any help from an employment service before finding this job? |
| E34 | E | jobs_applied_before_hire | SWTS | 81 | 100.0 | proposed clustering input | D9 — Transition-to-work search pathway and barriers | Approximately how many jobs did you apply for before starting this job? |
| E35 | E | interviews_before_hire | SWTS | 81 | 100.0 | proposed clustering input | D9 — Transition-to-work search pathway and barriers | How many interviews did you attend before starting this job? |
| E36 | E | ever_refused_job_f | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | Before starting this job, did you ever refuse a job that was offered to you? |
| E37 | E | reason_refused_job_f | SWTS | 36 | 44.4 | conditional descriptor | Not used in all-Branch-F distance | What was the main reason you refused that other offer? |
| E38 | E | acceptance_conditions_search | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | When searching for this job, which best describes what you were willing to accept? |
| E39 | E | had_min_wage_during_search | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | When searching for this job, was there a minimum income below which you would not have accepted an offer? |
| E40 | E | search_duration_before_hire | SWTS | 81 | 100.0 | proposed clustering input | D9 — Transition-to-work search pathway and barriers | How long were you actively looking for work before finding this job? |
| E41 | E | obstacle_finding_this_job | SWTS | 81 | 100.0 | proposed clustering input | D9 — Transition-to-work search pathway and barriers | Looking back, what was the main obstacle you faced in finding this job? |
| E42 | E | past_edu_useful_for_job | SWTS | 81 | 100.0 | proposed clustering input | D6 — Qualification use and skill development | Has your past education or training been useful for getting or performing this job? |
| E43 | E | employment_status | SWTS | 81 | 100.0 | profile/programme-mapping descriptor | Not a clustering dimension | In your current job, business, or farm, how do you usually work? |
| E44 | E | job_recruitment_method | SWTS | 70 | 86.4 | wage-worker subgroup description | Separate n=70 subgroup | How did you get your current job? |
| E45 | E | enterprise_size | SWTS | 70 | 86.4 | wage-worker subgroup description | Separate n=70 subgroup | How many workers are employed in the organisation you work for? |
| E46 | E | gender_equality_at_work | SWTS | 70 | 86.4 | wage-worker subgroup description | Separate n=70 subgroup | In your current workplace, do women and men have equal opportunities for advancement? |
| E47 | E | reason_self_employed | SWTS | 11 | 13.6 | self-employed subgroup description | Separate n=11 subgroup | Why did you choose to be self-employed rather than work for an employer? |
| E48 | E | business_helpers | SWTS | 11 | 13.6 | self-employed subgroup description | Separate n=11 subgroup | Does anyone help you in your business or economic activity? |
| E49 | E | business_funding_source | SWTS | 11 | 13.6 | self-employed subgroup description | Separate n=11 subgroup | How did you mainly get the money to start your current business? |
| E50 | E | business_profitability | SWTS | 11 | 13.6 | self-employed subgroup description | Separate n=11 subgroup | Currently, is your business making a profit, a loss, or breaking even? |
| E51 | E | main_business_obstacle | SWTS | 11 | 13.6 | self-employed subgroup description | Separate n=11 subgroup | What is the most important challenge you face in running your business? |

## Theory sources used

- ILO School-to-Work Transition Survey: structural position, employment conditions, stable/satisfactory employment, job-search pathway, and barriers.
- Bourdieu (1986), *The Forms of Capital*: economic, cultural, and social capital and position within a field.
- Deci and Ryan (2000), *The What and Why of Goal Pursuits*: autonomy, competence, relatedness, and regulatory/motivation style.
- The local `nysc_supervisor_prep.docx`: maps the survey variables to the three frameworks and specifies branch-specific clustering.

## Current modelling status

The variable audit now functions as the theory-first candidate plan. All D1–D9
dimensions have been tested or explicitly skipped. D1 household resources was
rejected because its apparent result was primarily an income-source split. D2
educational/inherited cultural capital was rejected because no candidate met
the cross-algorithm minimum-size rule, spectral stability was insufficient, and
the permutation p-value was 0.683. The only retained Branch-F clustering is D3
employment security/formality, with caution. D4 earnings/working-time preference
was statistically stable but is excluded by the final researcher scope decision
because it is mainly a direct preference split rather than a multidimensional
profile. See `branch_clustering_progress.md` for the complete decision register.
