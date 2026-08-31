# Branch E Group Programme Relevance

## Scope and frozen-input verification

This analysis uses each youth's own answers and then aggregates results within the two frozen Branch E profiles. The frozen cohort was verified as **E-P1 n=18** and **E-P2 n=16** (total **34**). Each youth was compared with all **87** V2 courses, producing **2,958 respondent-course rows**. No clustering, assignment, profile, medoid, survey, course, or Branch F output was changed.

This is descriptive group programme relevance, not individual eligibility prediction. A group-level Top 10 course is not suitable for every member merely because it ranks highly.

## Survey-to-course decisions

All four survey variables are whole-Branch-E questions with **34/34 valid responses**. Their actual categories are preserved in `profile_matching_summary.csv`; unmatchable categories are not silently converted into zeros.

| Survey variable | Exact meaning | Defensible V2 correspondence | What is not forced |
|---|---|---|---|
| `ideal_sector` | Preferred sector/industry | `skill_area`; explicit sector/occupation text for finance and teaching | Unsupported sectors receive no component. Manufacturing is explicitly broad. |
| `training_type_would_help` | Training believed most helpful for finding work | ICT `skill_area`; positive-only `nvq_level`/`qualification_type`; credible entrepreneurship content | University degree, apprenticeship, secondary/A-Level and “other” are unscored because V2 lacks an equivalent. |
| `job_type_sought` | Main type of job sought | Controlled skill-area/occupation-family or explicit occupation text | “Professional” and “any available” are unscored; professional status is not inferred from a course title. |
| `ideal_work_type` | Preferred work/employer arrangement | Only “Start my own business,” against credible explicit entrepreneurship content | Private/public/NGO/family employer types and uncertainty are unscored because V2 has no employer-type field. |

The full auditable crosswalk is in `matching_variable_course_field_map.csv`.

## Fixed baseline score

For youth *i* and course *c*:

> relevance(i,c) = 100 × mean of the available binary component matches

Each of the four survey variables can contribute at most one equally weighted component. The weights were not optimized. A component is omitted when the survey answer has no defensible V2 correspondence or when a sparse catalogue field is blank. A blank field is never a zero. The **70/100** threshold is descriptive, not validated eligibility.

Qualification/NVQ/certification and entrepreneurship evidence are **positive-only** because their V2 fields are sparse. Only **1 course** has credible explicit entrepreneurship/self-employment wording after generic management text is rejected: NYSC-C018 Freelancer of Web Design & Development.

Strict Top 3/5 uses score, positive-component count, available-component count, then course ID for reproducibility. Since course ID is arbitrary, the substantive summaries use **tie-adjusted Top 3/5 equivalents**, which split boundary slots fractionally across exact score ties.

## Profile-level response distributions

| Profile | Variable | Actual answer | n/full profile | % |
|---|---|---|---:|---:|
| E-P1 | `ideal_sector` | Information technology and communications | 12/18 | 66.7% |
| E-P1 | `ideal_sector` | Manufacturing or production | 2/18 | 11.1% |
| E-P1 | `ideal_sector` | Personal services (beauty, fitness, wellness) | 1/18 | 5.6% |
| E-P1 | `ideal_sector` | Agriculture, forestry, and fishing | 1/18 | 5.6% |
| E-P1 | `ideal_sector` | Public administration, government, and defence | 1/18 | 5.6% |
| E-P1 | `ideal_sector` | Health, social work, and wellbeing | 1/18 | 5.6% |
| E-P1 | `training_type_would_help` | University degree | 7/18 | 38.9% |
| E-P1 | `training_type_would_help` | Computer and IT training | 4/18 | 22.2% |
| E-P1 | `training_type_would_help` | Completion of vocational/NVQ training | 2/18 | 11.1% |
| E-P1 | `training_type_would_help` | Entrepreneurship training to start own business | 2/18 | 11.1% |
| E-P1 | `training_type_would_help` | Apprenticeship with an employer | 2/18 | 11.1% |
| E-P1 | `training_type_would_help` | Professional/technical certification | 1/18 | 5.6% |
| E-P1 | `job_type_sought` | Professional work (law, medicine, engineering, etc.) | 8/18 | 44.4% |
| E-P1 | `job_type_sought` | Technical work | 5/18 | 27.8% |
| E-P1 | `job_type_sought` | Any available job | 2/18 | 11.1% |
| E-P1 | `job_type_sought` | Self-employment or starting a business | 1/18 | 5.6% |
| E-P1 | `job_type_sought` | Creative or media work | 1/18 | 5.6% |
| E-P1 | `job_type_sought` | Managerial work | 1/18 | 5.6% |
| E-P1 | `ideal_work_type` | Start my own business | 9/18 | 50.0% |
| E-P1 | `ideal_work_type` | Work for a multinational or large private company | 5/18 | 27.8% |
| E-P1 | `ideal_work_type` | Not sure yet | 2/18 | 11.1% |
| E-P1 | `ideal_work_type` | Work for a local private Sri Lankan company | 1/18 | 5.6% |
| E-P1 | `ideal_work_type` | Work for the government or public sector | 1/18 | 5.6% |
| E-P2 | `ideal_sector` | Information technology and communications | 5/16 | 31.2% |
| E-P2 | `ideal_sector` | Manufacturing or production | 4/16 | 25.0% |
| E-P2 | `ideal_sector` | Education and teaching | 2/16 | 12.5% |
| E-P2 | `ideal_sector` | Hotels, restaurants, and hospitality | 1/16 | 6.2% |
| E-P2 | `ideal_sector` | Not sure | 1/16 | 6.2% |
| E-P2 | `ideal_sector` | Finance, banking, and insurance | 1/16 | 6.2% |
| E-P2 | `ideal_sector` | Wholesale, retail, or repair | 1/16 | 6.2% |
| E-P2 | `ideal_sector` | Personal services (beauty, fitness, wellness) | 1/16 | 6.2% |
| E-P2 | `training_type_would_help` | Professional/technical certification | 3/16 | 18.8% |
| E-P2 | `training_type_would_help` | Completion of secondary/A-Level education | 3/16 | 18.8% |
| E-P2 | `training_type_would_help` | University degree | 3/16 | 18.8% |
| E-P2 | `training_type_would_help` | Other type of training | 2/16 | 12.5% |
| E-P2 | `training_type_would_help` | Apprenticeship with an employer | 2/16 | 12.5% |
| E-P2 | `training_type_would_help` | Computer and IT training | 2/16 | 12.5% |
| E-P2 | `training_type_would_help` | Completion of vocational/NVQ training | 1/16 | 6.2% |
| E-P2 | `job_type_sought` | Technical work | 4/16 | 25.0% |
| E-P2 | `job_type_sought` | Any available job | 3/16 | 18.8% |
| E-P2 | `job_type_sought` | Professional work (law, medicine, engineering, etc.) | 3/16 | 18.8% |
| E-P2 | `job_type_sought` | Creative or media work | 2/16 | 12.5% |
| E-P2 | `job_type_sought` | Manual or trade work | 1/16 | 6.2% |
| E-P2 | `job_type_sought` | Self-employment or starting a business | 1/16 | 6.2% |
| E-P2 | `job_type_sought` | Clerical or administrative work | 1/16 | 6.2% |
| E-P2 | `job_type_sought` | Managerial work | 1/16 | 6.2% |
| E-P2 | `ideal_work_type` | Work for a local private Sri Lankan company | 5/16 | 31.2% |
| E-P2 | `ideal_work_type` | Work for a multinational or large private company | 5/16 | 31.2% |
| E-P2 | `ideal_work_type` | Start my own business | 2/16 | 12.5% |
| E-P2 | `ideal_work_type` | Work for the government or public sector | 1/16 | 6.2% |
| E-P2 | `ideal_work_type` | Work for a non-profit or NGO | 1/16 | 6.2% |
| E-P2 | `ideal_work_type` | Not sure yet | 1/16 | 6.2% |
| E-P2 | `ideal_work_type` | Work in a family business (non-farming) | 1/16 | 6.2% |

## E-P1 Top 10

| Rank | Course ID | Course | ≥70/full n (%) | ≥70/sufficient n (%) | Course valid n | Mean | Median | Tie-adj Top 3 eq. n | Tie-adj Top 5 eq. n | Matching variables responsible |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | NYSC-C018 | Freelancer of Web Design & Development | 12/18 (66.7%) | 12/18 (66.7%) | 17 | 86.8 | 100.0 | 3.14 | 4.57 | ideal_sector (n=12); ideal_work_type (n=9); training_type_would_help (n=6); job_type_sought (n=6) |
| 2 | NYSC-C001 | National Diploma in Information & Communication Technology | 12/18 (66.7%) | 12/18 (66.7%) | 18 | 79.6 | 100.0 | 2.33 | 3.91 | ideal_sector (n=12); training_type_would_help (n=7); job_type_sought (n=5) |
| 2 | NYSC-C002 | Information & Communication Technology Technician | 12/18 (66.7%) | 12/18 (66.7%) | 18 | 79.6 | 100.0 | 2.33 | 3.91 | ideal_sector (n=12); training_type_would_help (n=7); job_type_sought (n=5) |
| 2 | NYSC-C003 | Computer Hardware Technician (Full Time) | 12/18 (66.7%) | 12/18 (66.7%) | 18 | 79.6 | 100.0 | 2.33 | 3.91 | ideal_sector (n=12); training_type_would_help (n=7); job_type_sought (n=5) |
| 2 | NYSC-C004 | Computer Network Technician | 12/18 (66.7%) | 12/18 (66.7%) | 18 | 79.6 | 100.0 | 2.33 | 3.91 | ideal_sector (n=12); training_type_would_help (n=7); job_type_sought (n=5) |
| 6 | NYSC-C005 | Computer Hardware Technician (Part Time) | 11/18 (61.1%) | 11/18 (61.1%) | 17 | 75.5 | 100.0 | 2.23 | 3.75 | ideal_sector (n=12); job_type_sought (n=5); training_type_would_help (n=4) |
| 6 | NYSC-C006 | Computer Hardware And Network Technician | 11/18 (61.1%) | 11/18 (61.1%) | 17 | 75.5 | 100.0 | 2.23 | 3.75 | ideal_sector (n=12); job_type_sought (n=5); training_type_would_help (n=4) |
| 6 | NYSC-C007 | Computer Certificate | 11/18 (61.1%) | 11/18 (61.1%) | 17 | 75.5 | 100.0 | 2.23 | 3.75 | ideal_sector (n=12); job_type_sought (n=5); training_type_would_help (n=5) |
| 6 | NYSC-C008 | Computer Applications Assistant | 11/18 (61.1%) | 11/18 (61.1%) | 17 | 75.5 | 100.0 | 2.23 | 3.75 | ideal_sector (n=12); job_type_sought (n=5); training_type_would_help (n=4) |
| 6 | NYSC-C009 | Computer Based Accounting | 11/18 (61.1%) | 11/18 (61.1%) | 17 | 75.5 | 100.0 | 2.23 | 3.75 | ideal_sector (n=12); job_type_sought (n=5); training_type_would_help (n=4) |

## E-P2 Top 10

| Rank | Course ID | Course | ≥70/full n (%) | ≥70/sufficient n (%) | Course valid n | Mean | Median | Tie-adj Top 3 eq. n | Tie-adj Top 5 eq. n | Matching variables responsible |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | NYSC-C001 | National Diploma in Information & Communication Technology | 6/16 (37.5%) | 6/16 (37.5%) | 16 | 45.8 | 41.7 | 1.07 | 1.84 | training_type_would_help (n=6); ideal_sector (n=5); job_type_sought (n=4) |
| 1 | NYSC-C002 | Information & Communication Technology Technician | 6/16 (37.5%) | 6/16 (37.5%) | 16 | 45.8 | 41.7 | 1.07 | 1.84 | training_type_would_help (n=6); ideal_sector (n=5); job_type_sought (n=4) |
| 1 | NYSC-C003 | Computer Hardware Technician (Full Time) | 6/16 (37.5%) | 6/16 (37.5%) | 16 | 45.8 | 41.7 | 1.07 | 1.84 | training_type_would_help (n=6); ideal_sector (n=5); job_type_sought (n=4) |
| 1 | NYSC-C004 | Computer Network Technician | 6/16 (37.5%) | 6/16 (37.5%) | 16 | 45.8 | 41.7 | 1.07 | 1.84 | training_type_would_help (n=6); ideal_sector (n=5); job_type_sought (n=4) |
| 5 | NYSC-C007 | Computer Certificate | 6/16 (37.5%) | 6/16 (37.5%) | 16 | 42.7 | 16.7 | 1.07 | 1.84 | ideal_sector (n=5); training_type_would_help (n=5); job_type_sought (n=4) |
| 5 | NYSC-C010 | Cisco Certified Network Associate | 6/16 (37.5%) | 6/16 (37.5%) | 16 | 42.7 | 16.7 | 1.07 | 1.84 | ideal_sector (n=5); training_type_would_help (n=5); job_type_sought (n=4) |
| 7 | NYSC-C009 | Computer Based Accounting | 5/16 (31.2%) | 5/16 (31.2%) | 15 | 42.2 | 33.3 | 1.73 | 2.69 | ideal_sector (n=6); job_type_sought (n=4); training_type_would_help (n=2) |
| 8 | NYSC-C018 | Freelancer of Web Design & Development | 5/16 (31.2%) | 5/16 (31.2%) | 15 | 42.2 | 33.3 | 1.97 | 2.66 | ideal_sector (n=5); job_type_sought (n=5); ideal_work_type (n=2); training_type_would_help (n=2) |
| 9 | NYSC-C005 | Computer Hardware Technician (Part Time) | 5/16 (31.2%) | 5/16 (31.2%) | 15 | 38.9 | 0.0 | 0.98 | 1.70 | ideal_sector (n=5); job_type_sought (n=4); training_type_would_help (n=2) |
| 9 | NYSC-C006 | Computer Hardware And Network Technician | 5/16 (31.2%) | 5/16 (31.2%) | 15 | 38.9 | 0.0 | 0.98 | 1.70 | ideal_sector (n=5); job_type_sought (n=4); training_type_would_help (n=2) |

## Result quality compared with Branch F

| Diagnostic | Branch E | Branch F | Meaning |
|---|---:|---:|---|
| Scored rows driven only by `ideal_sector` | 1025/2851 (36.0%) | 6053/6092 (99.4%) | Lower means more non-sector information entered the score. |
| Scored rows with 2+ available survey-variable signals | 1585/2851 (55.6%) | 37/6092 (0.6%) | Availability, not necessarily positive agreement. |
| Positive rows with 2+ positive signals | 298/1061 (28.1%) | 25/1115 (2.2%) | Multiple actual answers support the same course; conceptual overlap remains possible. |
| Respondents with an exact top-score tie | 31/34 (91.2%) | 69/72 (95.8%) | A tie means the survey cannot strictly order those courses. |
| Top-score tie size, mean / median / max | 18.3 / 18.0 / 63 | 15.3 / 18.0 / 23 | Smaller indicates greater course discrimination. |
| Within-sector differentiation | 1/28 (3.6%) | Not stored in F outputs | E respondents whose sector-matched courses receive more than one score because another usable answer discriminates them. |

`training_type_would_help` and `job_type_sought` are separate individual answers, but they do not automatically imply fine course specificity. Computer training, creative work and technical work are still broad category signals. Sparse positive-only NVQ/certificate evidence can support a course but cannot safely penalize an undocumented course. The tie diagnostics therefore remain essential.

## Limitations

- The sample is small: 18 and 16 respondents.
- The matching crosswalk is transparent and conservative but has not yet been validated by NYSC subject experts.
- V2 lacks reliable location, fees, current intake, entry requirements, employer/apprenticeship links and individual availability/preferences for schedule, duration and language. No eligibility claim is made.
- Some signals overlap conceptually: ICT sector plus computer training, or self-employment job type plus own-business preference. They are retained as separate actual answers but should not be described as wholly independent constructs.
- Course records sharing only a broad skill area can still tie. Strict course-ID ordering is computational only; tie-adjusted equivalents are the substantive measure.
- The 70 threshold and equal weighting are transparent baseline conventions, not optimized or externally validated parameters.

## Final judgment

**B. mainly broad sector-level relevance is supported**

This judgment follows the fixed diagnostics: sector-only scoring, multi-signal coverage, exact ties, and observed within-sector score differentiation. It does not mean the analysis can determine individual eligibility or guarantee course suitability.
