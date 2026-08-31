# Human-Readable Review — 30-Person Validation Batch

Built entirely from already-saved files: `outputs/rag_recommendation_validation_30/api_recommendations_30.jsonl`, `grounding_audit_30.csv`, `evidence_category_audit_30.csv`, `validation_sample_30_selection_rationale.csv`, and `outputs/rag_respondent_evidence/respondent_evidence.jsonl`. **No new API calls were made and no recommendation was regenerated to produce this document.**

**Legend:** every claim below is labelled by evidence type — **[ACTUAL SURVEY ANSWER]** (what the respondent themself said, taken from `respondent_evidence.jsonl`), **[PROFILE / GROUP CONTEXT]** (a group-level research finding from the respondent's frozen profile, never an individual fact), **[COURSE FACT]** (text taken from the retrieved NYSC course document), and **[LLM INFERENCE]** (a reasoning connection the model made, always expected to be hedged). The "ACTUAL SURVEY ANSWERS available to the recommendation system" block for each respondent lists every answered field in every usable evidence category, whether or not the LLM ended up citing it — nothing is omitted or summarised away.

---

## Contents

1. [nysc-0cba8a68-ebf6-47cb-bd45-e2a1d78ad74b (D)](#1-nysc-0cba8a68-ebf6-47cb-bd45-e2a1d78ad74b)
2. [nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88 (D)](#2-nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88)
3. [nysc-4eae9a51-70b3-48ae-ae06-6fe372ac0230 (D)](#3-nysc-4eae9a51-70b3-48ae-ae06-6fe372ac0230)
4. [nysc-4e38db03-e477-420e-9afd-d3f92b53995d (D)](#4-nysc-4e38db03-e477-420e-9afd-d3f92b53995d)
5. [nysc-8ae4a1d8-97c7-4bc4-9dc9-cb7eea0c897f (D)](#5-nysc-8ae4a1d8-97c7-4bc4-9dc9-cb7eea0c897f)
6. [nysc-4401e631-9304-4f41-9ba4-6f84d659f7c8 (D)](#6-nysc-4401e631-9304-4f41-9ba4-6f84d659f7c8)
7. [nysc-515dbda4-d209-46f1-b1cd-a9f996f9cebd (D)](#7-nysc-515dbda4-d209-46f1-b1cd-a9f996f9cebd)
8. [nysc-b556590a-0e0d-4d6f-8b9e-f148e18ca930 (D)](#8-nysc-b556590a-0e0d-4d6f-8b9e-f148e18ca930)
9. [nysc-25c345ec-5f45-4616-adb8-c96e31f3511c (D)](#9-nysc-25c345ec-5f45-4616-adb8-c96e31f3511c)
10. [nysc-0566257f-e441-4134-9a0f-ebedde047f88 (D)](#10-nysc-0566257f-e441-4134-9a0f-ebedde047f88)
11. [nysc-15a74ec0-011b-4f61-804e-72de37c73705 (D)](#11-nysc-15a74ec0-011b-4f61-804e-72de37c73705)
12. [nysc-0a4832c0-3e8a-47e9-ac41-22252b0ceb06 (E)](#12-nysc-0a4832c0-3e8a-47e9-ac41-22252b0ceb06)
13. [nysc-136c3ecd-09d4-4238-8a63-64c8636724df (E)](#13-nysc-136c3ecd-09d4-4238-8a63-64c8636724df)
14. [nysc-2e8a4c77-f611-4fff-9da8-9161a3f0f368 (E)](#14-nysc-2e8a4c77-f611-4fff-9da8-9161a3f0f368)
15. [nysc-3258dc18-84da-4092-82af-cfb84352536e (E)](#15-nysc-3258dc18-84da-4092-82af-cfb84352536e)
16. [nysc-cab6cf5f-13dc-4f50-9d5a-b24f266dc279 (E)](#16-nysc-cab6cf5f-13dc-4f50-9d5a-b24f266dc279)
17. [nysc-04134b0d-f3fe-4a25-916c-ee106362e150 (F)](#17-nysc-04134b0d-f3fe-4a25-916c-ee106362e150)
18. [nysc-4646cb19-0ac0-49ca-a00b-e2d8cb16b65e (F)](#18-nysc-4646cb19-0ac0-49ca-a00b-e2d8cb16b65e)
19. [nysc-03b655c2-0162-44b7-a418-e4d9ac99ccbb (F)](#19-nysc-03b655c2-0162-44b7-a418-e4d9ac99ccbb)
20. [nysc-1a42a4ad-7444-4e03-8b9c-7ce184f7850c (F)](#20-nysc-1a42a4ad-7444-4e03-8b9c-7ce184f7850c)
21. [nysc-0a92b28f-94dc-44ce-9e9e-2d25b35c0b04 (F)](#21-nysc-0a92b28f-94dc-44ce-9e9e-2d25b35c0b04)
22. [nysc-14ffa0bd-0d24-4a0e-b75d-516771a7fbbb (F)](#22-nysc-14ffa0bd-0d24-4a0e-b75d-516771a7fbbb)
23. [nysc-079cc6c0-68dd-4ae3-b5e3-9ffd99d463f3 (F)](#23-nysc-079cc6c0-68dd-4ae3-b5e3-9ffd99d463f3)
24. [nysc-34933c14-655f-4189-800f-2419775963fe (F)](#24-nysc-34933c14-655f-4189-800f-2419775963fe)
25. [nysc-27b17da2-64b7-4031-b4ac-3205b9b2a735 (G)](#25-nysc-27b17da2-64b7-4031-b4ac-3205b9b2a735)
26. [nysc-31cab333-afc9-48c5-baec-8ba48e14defb (G)](#26-nysc-31cab333-afc9-48c5-baec-8ba48e14defb)
27. [nysc-0717027e-65cc-4b29-9b44-17593f66aaf5 (G)](#27-nysc-0717027e-65cc-4b29-9b44-17593f66aaf5)
28. [nysc-27c2ff48-e39c-4db3-aa11-a149d76be479 (G)](#28-nysc-27c2ff48-e39c-4db3-aa11-a149d76be479)
29. [nysc-49b62c9a-e647-4f21-9742-305d52c6b5a9 (G)](#29-nysc-49b62c9a-e647-4f21-9742-305d52c6b5a9)
30. [nysc-5242257e-4708-442a-a41f-1081109194a9 (G)](#30-nysc-5242257e-4708-442a-a41f-1081109194a9)

---

## 1. `nysc-0cba8a68-ebf6-47cb-bd45-e2a1d78ad74b` (Branch D) {#1-nysc-0cba8a68-ebf6-47cb-bd45-e2a1d78ad74b}

**Selection rationale (why this respondent was chosen for the batch):** Education and teaching; distinct D profile combo

### Frozen profile membership(s)

- `D_motivation` — Profile 1: "Consensus motivation profile 1: externally or uncertainly motivated, with moderate study support" (dimension: Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 4: "Work-experienced students, mainly in private institutions" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Post-graduate degree
  - `ideal_sector` = Education and teaching
  - `ideal_work_type` = Not sure yet
  - `plans_after_education` = Immediately go on to further education or training
  - `study_field_preference` = Science or mathematics

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Small town
  - `district` = Puttalam
  - `edu_funding_source` = Paid for by my family
  - `has_children` = No
  - `household_income` = LKR 120,000 – 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 0.0
  - `household_workers` = 2.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = No — not yet
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Private school or private degree-awarding institute
  - `re_entered_education` = No
  - `work_while_study_hours` = 5 to 10 hours
  - `work_while_study_motivation` = To gain work experience and build my CV
  - `work_while_study_paid` = Paid
  - `work_while_study_type` = Internship or apprenticeship in a private company
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 26 – 29 years
  - `autonomy_in_study` = Some — there is flexibility within a mostly fixed curriculum
  - `competence_in_study_field` = Fairly capable — mostly confident with some gaps
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `most_important_life_goal` = Building self-confidence and personal fulfilment
  - `most_useful_quality_for_job` = Communication and interpersonal skills
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `relatedness_at_institution` = Somewhat — I have some connections but am not deeply involved
  - `social_capital_in_edu_access` = Family members advised me or guided the choice
  - `study_motivation_type` = I am not sure why — I am following the path I ended up on

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-072 (Japanese Language); COURSE-067 (French Language); COURSE-074 (Korean Language); COURSE-086 (Tamil Language); COURSE-031 (National Diploma In Television Program Production); COURSE-075 (Mass Communication); COURSE-009 (Information And Communication Technolory Technician); COURSE-003 (Certificate In English Communication Essentials.); COURSE-024 (Draughtperson); COURSE-016 (Graphics Designer); COURSE-020 (Landscape Development Assistant); COURSE-022 (Computer Network Technician); COURSE-035 (Secretary (Secretarial Practices)); COURSE-004 (Professional English)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Education and teaching; study_field_preference=Science or mathematics; expected_highest_edu_d=Post-graduate degree; plans_after_education=Immediately go on to further education or training; current_activity_status=Attending school, university, or a training programme; work_while_study_type=Internship or apprenticeship in a private company; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: communication, english, french, japanese, korean, sinhala, tamil]

#### Rank 1: `COURSE-003` — Certificate In English Communication Essentials.

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course description notes relevance for job aspirants and for those seeking promo...' has low word-overlap (35%) with the retrieved COURSE-003 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Education and teaching — *relevance stated by the model:* "Respondent explicitly named Education and teaching as their ideal sector; English communication courses are commonly relevant to roles in education and teaching (e.g., language teaching, classroom communication)."
  - `plans_after_education` = Immediately go on to further education or training — *relevance stated by the model:* "Respondent intends to continue studying; a short certificate in English communication may support further academic study and teaching-related pathways."
  - `study_field_preference` = Science or mathematics — *relevance stated by the model:* "While the respondent prefers science/mathematics, strong English communication skills can support future postgraduate study and teaching roles in those fields (e.g., explaining concepts, academic writing), so this course may be useful."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p4`, role=supporting_context_only: "Work while studying was prominent, with many respondents in private institutions (profile describes group tendencies only)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "The course is a three-month Certificate in English Communication Essentials combining theoretical knowledge with practical application; delivered online (zoom) and targeted to job aspirants and those pursuing further study." — source: COURSE-003
  - "Course description notes relevance for job aspirants and for those seeking promotions or overseas employment; practical activities and small classes are mentioned." — source: COURSE-003

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to work in Education and teaching and plans further study, a short course improving English communication may help with future teaching roles or postgraduate study (may strengthen teaching-related communication and academic skills)." (hedged; based on: DIRECT respondent facts: ideal_sector = Education and teaching; plans_after_education = Immediately go on to further education or training, Course fact: COURSE-003 is an English communication certificate designed for job aspirants and further study)

**LLM's recommendation explanation (`why_recommended`):** "Direct overlap: respondent wants Education/teaching and to continue education; this course explicitly teaches English communication and is framed for job aspirants and further study, so it plausibly supports teaching-related and academic goals."

**Uncertainties disclosed by the LLM:**
  - The course document contains some [UNCLEAR] text fragments; delivery modality appears to include online (zoom) but full schedule and fees are not fully documented in the excerpt.
  - It is not specified whether the course leads to qualification specifically recognised for formal teacher training or postgraduate entry; that information is not available in the course text.

**Limitations disclosed by the LLM:**
  - No explicit statement in the course text that this certificate qualifies the holder to work as a school teacher or is accepted by teacher-training programmes.
  - Exact start dates, fee amount (beyond a materials fee note elsewhere in the catalogue), and eligibility criteria are not provided in the course document.

#### Rank 2: `COURSE-004` — Professional English

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Education and teaching — *relevance stated by the model:* "Education and teaching is the respondent's stated target sector; professional English training aligns with preparing for teaching or education-related communication roles."
  - `plans_after_education` = Immediately go on to further education or training — *relevance stated by the model:* "Short professional English programmes can help with academic progression and postgraduate study readiness."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - *(none cited — empty for this recommendation)*

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course listed as 'Professional English', full-time, 6 months duration (catalogue card indicates structured professional English offering)." — source: COURSE-004

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent plans to continue into further education and values communication skills, a Professional English course may support academic readiness and teaching-related communication (may improve language proficiency for postgraduate study or classroom use)." (hedged; based on: DIRECT respondent facts: plans_after_education = Immediately go on to further education or training; most_useful_quality_for_job = Communication and interpersonal skills, Course fact: COURSE-004 is a Professional English offering (6-month full-time card shown))

**LLM's recommendation explanation (`why_recommended`):** "The course directly teaches advanced/professional English, which is relevant to someone targeting education/teaching and planning further study; it may strengthen academic and classroom communication skills."

**Uncertainties disclosed by the LLM:**
  - COURSE-004 catalogue card is brief; detailed syllabus, delivery format (beyond 'Full Time' on the card), fees, and accreditation specifics are not included in the visible text.
  - Full compatibility with formal teacher-certification pathways is not stated in the course document.

**Limitations disclosed by the LLM:**
  - The course appears to be full time (catalogue card), which could affect feasibility if the respondent requires part-time study; the respondent did not state a scheduling constraint, so feasibility is uncertain.
  - Entry requirements and specific outcomes for teacher training or postgraduate admission are not documented in the course text.

#### Rank 3: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `plans_after_education` = Immediately go on to further education or training — *relevance stated by the model:* "Respondent plans further study; a diploma can be a pathway into higher-level technical study or specialised postgraduate entry in related fields."
  - `study_field_preference` = Science or mathematics — *relevance stated by the model:* "ICT involves technical, logical and computational subjects that may appeal to someone with an interest in science or mathematics."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p2`, role=supporting_context_only: "Within this economic profile group, many respondents reported ICT or computing as a preferred field of study (group-level tendency only)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course syllabus includes System Analysis & Design, Software Programming, Database Systems, Software Testing, Web Programming and Local Area Network; described as a full-time course held on weekdays leading to Competency Level 5." — source: COURSE-006
  - "Course explicitly described as providing theoretical knowledge and job-oriented practical skills necessary for employment and higher education." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent expressed a preference for Science or mathematics and plans further education, an ICT diploma may be compatible with those interests and could serve as a technical foundation for STEM teaching or further technical study (may support STEM-related career or teaching pathways)." (hedged; based on: DIRECT respondent facts: study_field_preference = Science or mathematics; plans_after_education = Immediately go on to further education or training, Course fact: COURSE-006 covers technical topics (programming, databases, systems) and is positioned as both employment- and higher-education-relevant)

**LLM's recommendation explanation (`why_recommended`):** "The course covers technical topics that overlap with scientific and mathematical reasoning and is framed as a pathway to employment and higher education; this could be relevant if the respondent sees a technical/STEM route within education or postgraduate study."

**Uncertainties disclosed by the LLM:**
  - The course is explicitly full time on weekdays; the respondent did not state explicit schedule constraints, but feasibility (full-time attendance) is unknown.
  - No explicit statement that the diploma leads to teacher training or is accepted by postgraduate education programmes; such articulation is not in the course text.

**Limitations disclosed by the LLM:**
  - Course is full time; if the respondent prefers part-time or weekend study, this may be less feasible — the course document does not offer a part-time option.
  - Entry requirements, fees, exact location, and recognition for teacher-training pathways are not specified in the course document.


---

## 2. `nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88` (Branch D) {#2-nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88}

**Selection rationale (why this respondent was chosen for the batch):** Manufacturing or production

### Frozen profile membership(s)

- `D_motivation` — Profile 2: "Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support" (dimension: Motivation and study experience)
- `D_economic` — Profile 1: "Economic profile 1: relatively lower household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 4: "Work-experienced students, mainly in private institutions" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Post-graduate degree
  - `ideal_sector` = Manufacturing or production
  - `ideal_work_type` = Work for a multinational or large private company
  - `plans_after_education` = Look for a job
  - `study_field_preference` = Science or mathematics

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Metropolitan suburb
  - `district` = Badulla
  - `edu_funding_source` = Government-funded or free of charge
  - `has_children` = No
  - `household_income` = LKR 30,000 – 60,000
  - `household_size` = 4.0
  - `household_unemployed` = 1.0
  - `household_workers` = 1.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = Yes — I am already searching
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Government school or state university
  - `job_search_method_d` = Online job ads (internet, social media)
  - `re_entered_education` = No
  - `work_while_study_hours` = Less than 5 hours
  - `work_while_study_motivation` = To earn money
  - `work_while_study_paid` = Paid
  - `work_while_study_type` = Informal or casual work
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `autonomy_in_study` = Some — there is flexibility within a mostly fixed curriculum
  - `competence_in_study_field` = Very capable — confident and effective in my field
  - `edu_min_for_decent_job` = A/L level
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `most_important_life_goal` = Having financial security or earning a lot
  - `most_useful_quality_for_job` = Scientific or technical qualifications
  - `move_reason` = For education or training
  - `moved_from_origin` = No — I moved from somewhere else
  - `relatedness_at_institution` = Somewhat — I have some connections but am not deeply involved
  - `social_capital_in_edu_access` = I researched and applied entirely on my own initiative
  - `study_motivation_type` = Because I am genuinely passionate about this subject

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-012 (Refrigeration & Air Conditioning Technician); COURSE-034 (Refrigeration & Air Conditioning Technician); COURSE-031 (National Diploma In Television Program Production); COURSE-028 (Lapiderist (Gem Cutting)); COURSE-029 (Mobile Phone Repair Technician); COURSE-030 (Motorcycle Mechanic); COURSE-077 (Mobile Phone Repair Technician); COURSE-040 (Automobile Mechanic); COURSE-005 (Automobile Mechanic); COURSE-078 (Motorcycle Mechanic); COURSE-042 (Automobile Electrician); COURSE-081 (Radio, TV & Allied Equipment Repairer); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-021 (Automobile Electrician); COURSE-038 (Three Wheeler Mechanic)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Manufacturing or production; study_field_preference=Science or mathematics; ideal_work_type=Work for a multinational or large private company; expected_highest_edu_d=Post-graduate degree; plans_after_education=Look for a job; current_activity_status=Attending school, university, or a training programme; work_while_study_type=Informal or casual work; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: air conditioning, automobile, electrical, electronics, english, gem cutting, mechanic, mobile phone, motorcycle, programming, refrigeration, sinhala]

#### Rank 1: `COURSE-034` — Refrigeration & Air Conditioning Technician

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Course is a hands-on technical trade used in manufacturing/production and building services, matching the respondent's stated sector preference."
  - `study_field_preference` = Science or mathematics — *relevance stated by the model:* "Respondent's preference for scientific/technical studies aligns with a technical vocational course teaching engineering-related practical skills."
  - `ideal_work_type` = Work for a multinational or large private company — *relevance stated by the model:* "Large private companies and multinationals often employ technicians for HVAC, refrigeration and facilities roles; the course provides practical technician skills relevant to those roles."
  - `plans_after_education` = Look for a job — *relevance stated by the model:* "The course explicitly aims to provide job-oriented practical skills that could support immediate job seeking."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p4`, role=supporting_context_only: "Work-experienced students, mainly in private institutions (profile-level tendency)"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course overview lists: Repair refrigerators, deep freezers, display units, beetle coolers, water coolers; repair window and split type A/C; operate and maintain central A/C system." — source: COURSE-034
  - "Described as providing theoretical knowledge and job-oriented practical skills; gives competency Level 4 under NVQ standards (document states Level 4)." — source: COURSE-034
  - "Course is described as full time on weekdays (COURSE-034)." — source: COURSE-034

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent named manufacturing/production and scientific study as direct interests, this technical HVAC/refrigeration course appears to overlap with those interests and may support their goal of finding a job in a production or facilities role." (hedged; based on: ideal_sector: Manufacturing or production, study_field_preference: Science or mathematics)
  - "Because the respondent hopes to work for a multinational or large private company, the practical technician skills taught may be useful for roles those employers hire (e.g., facility or maintenance technician), but this is an inference rather than a documented employer connection." (hedged; based on: ideal_work_type: Work for a multinational or large private company, COURSE-034 course content: maintenance and operation of A/C and refrigeration systems)

**LLM's recommendation explanation (`why_recommended`):** "The course teaches practical refrigeration and air-conditioning maintenance skills that plausibly match the respondent's stated interest in manufacturing/production and preference for scientific/technical study, while explicitly aiming to provide job-oriented competencies."

**Uncertainties disclosed by the LLM:**
  - Course document lists this COURSE-034 version as full time on weekdays; another retrieved course (COURSE-012) shows a part-time / weekend variant for a similarly-named course. The respondent's time-availability preference is unknown.
  - No explicit location, fee, exact schedule (dates/times), or entry requirements are stated in the course document.

**Limitations disclosed by the LLM:**
  - The course document does not state fees, exact location or entry requirements — these attributes are not available in Section 3 and must be checked with NYSC before application.
  - Employer connections or guaranteed placement outcomes are not stated in the course document.

#### Rank 2: `COURSE-005` — Automobile Mechanic

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Automobile mechanic skills are firmly technical/trade skills in the broader manufacturing/maintenance sector and align with the respondent's sector preference."
  - `study_field_preference` = Science or mathematics — *relevance stated by the model:* "Respondent's scientific/technical study preference aligns with vehicle engineering and mechanical systems taught in this course."
  - `plans_after_education` = Look for a job — *relevance stated by the model:* "Course explicitly aims to provide job-oriented practical skills and an NVQ Level 4 outcome, which may support immediate job search."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p4`, role=supporting_context_only: "Work-experienced students and a tendency to already be searching for work (profile-level tendency)"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course overview lists engine, transmission, steering, braking and electrical system modules and describes the course as providing theoretical and job-oriented practical skills." — source: COURSE-005
  - "Course described in Section 3 as full time on weekdays and states an NVQ Level 4 competency outcome." — source: COURSE-005

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent plans to look for a job and has a technical study preference, a full-time vocational course in automobile mechanics may provide concrete, employable mechanical skills useful for manufacturing or large private companies with vehicle fleets or production roles." (hedged; based on: plans_after_education: Look for a job, study_field_preference: Science or mathematics, COURSE-005 course content: mechanical systems and NVQ Level 4)

**LLM's recommendation explanation (`why_recommended`):** "Automobile Mechanic teaches mechanical and diagnostic skills closely aligned with technical/scientific study preference and a manufacturing/technical sector orientation; it explicitly aims to produce job-ready competencies (NVQ Level 4)."

**Uncertainties disclosed by the LLM:**
  - The course is shown as full time weekday delivery in COURSE-005; respondent's schedule flexibility is not fully known.
  - No explicit entry requirements, fees, or location details are provided in the course document.

**Limitations disclosed by the LLM:**
  - Missing administrative details (fees, exact location, entry requirements) in the course text — these should be confirmed with NYSC.
  - This recommendation assumes the respondent is willing/able to attend a full-time weekday programme; if they require part-time/weekend training their ability to attend should be checked.

#### Rank 3: `COURSE-021` — Automobile Electrician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = Science or mathematics — *relevance stated by the model:* "Automobile electrician training involves electrical principles and systems consistent with a scientific/technical study preference."
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Vehicle electrical systems and diagnostics are technical skills used in production, maintenance and industrial settings."
  - `plans_after_education` = Look for a job — *relevance stated by the model:* "Course aims to provide job-oriented practical skills which could support job search."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p1`, role=supporting_context_only: "This economic profile describes relatively lower household economic position (profile-level tendency)"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course overview: Auto Electrical course will give theoretical knowledge and job-oriented practical skills necessary for employment and higher education; states full time on weekdays." — source: COURSE-021
  - "By completing this course you can achieve competency Level 4 under NVQ standards (COURSE-021)." — source: COURSE-021

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent values scientific/technical qualifications and plans to seek work, a course teaching auto-electrical systems may provide relevant technical competencies for maintenance or production-related roles." (hedged; based on: study_field_preference: Science or mathematics, plans_after_education: Look for a job, COURSE-021 course content: auto electrical practical/theory and NVQ Level 4)

**LLM's recommendation explanation (`why_recommended`):** "Automobile Electrician delivers electrical and diagnostic skills for vehicles that align with the respondent's scientific/technical study preference and manufacturing/production sector interest, and it explicitly targets job-oriented competence."

**Uncertainties disclosed by the LLM:**
  - COURSE-021 is documented as full time on weekdays; the respondent is currently in higher education and may need to confirm schedule compatibility.
  - No fee, exact venue, or entry requirement information is present in the course document.

**Limitations disclosed by the LLM:**
  - Missing administrative details (fees, exact location, entry requirements) in the course text.
  - No explicit employer partnerships or placement guarantees are mentioned in the document.


---

## 3. `nysc-4eae9a51-70b3-48ae-ae06-6fe372ac0230` (Branch D) {#3-nysc-4eae9a51-70b3-48ae-ae06-6fe372ac0230}

**Selection rationale (why this respondent was chosen for the batch):** Finance, banking, and insurance

### Frozen profile membership(s)

- `D_motivation` — Profile 2: "Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support" (dimension: Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 1: "Re-entered students, often with degree-educated parents" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Post-graduate degree
  - `ideal_sector` = Finance, banking, and insurance
  - `ideal_work_type` = Work for a multinational or large private company
  - `plans_after_education` = Look for a job
  - `study_field_preference` = Commerce, business, or management

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Metropolitan suburb
  - `district` = Colombo
  - `edu_funding_source` = Paid for by my family
  - `has_children` = No
  - `household_income` = Above LKR 200,000
  - `household_size` = 3.0
  - `household_unemployed` = 1.0
  - `household_workers` = 1.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = Other source

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = No — not yet
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Private school or private degree-awarding institute
  - `re_entered_education` = Yes
  - `reason_re_entered` = Needed different qualifications for a different career
  - `work_while_study_hours` = More than 20 hours
  - `work_while_study_motivation` = To gain work experience and build my CV
  - `work_while_study_paid` = Paid
  - `work_while_study_type` = Internship or apprenticeship in a private company
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 18 – 21 years
  - `autonomy_in_study` = Some — there is flexibility within a mostly fixed curriculum
  - `competence_in_study_field` = Somewhat capable — I struggle in some areas
  - `edu_min_for_decent_job` = A/L level
  - `employment_network_quality` = Yes — I know one or two people who might help
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = Command of languages (English, etc.)
  - `move_reason` = Other reason
  - `moved_from_origin` = No — I moved from somewhere else
  - `relatedness_at_institution` = Somewhat — I have some connections but am not deeply involved
  - `social_capital_in_edu_access` = I researched and applied entirely on my own initiative
  - `study_motivation_type` = It aligns with my own goals and will lead to what I want

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-035 (Secretary (Secretarial Practices)); COURSE-071 (Human Recources Management); COURSE-049 (Business Managemant); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-053 (Computer Applications Assistant); COURSE-001 (Freelancer Of Web Design & Development); COURSE-031 (National Diploma In Television Program Production); COURSE-082 (Secretary (Secretarial Practices)); COURSE-055 (Computer Hardware Technician); COURSE-075 (Mass Communication); COURSE-011 (Baker); COURSE-009 (Information And Communication Technolory Technician); COURSE-003 (Certificate In English Communication Essentials.); COURSE-008 (Computer Hardware Technician); COURSE-058 (Computer Based Accounting)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Finance, banking, and insurance; study_field_preference=Commerce, business, or management; ideal_work_type=Work for a multinational or large private company; expected_highest_edu_d=Post-graduate degree; plans_after_education=Look for a job; current_activity_status=Attending school, university, or a training programme; work_while_study_type=Internship or apprenticeship in a private company; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: business, communication, computer, human resources, internet, management, office, secretarial]

#### Rank 1: `COURSE-058` — Computer Based Accounting

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Finance, banking, and insurance — *relevance stated by the model:* "The respondent explicitly stated a preference for the finance sector; a computerised accounting course directly teaches accounting tools used in finance and bookkeeping."
  - `study_field_preference` = Commerce, business, or management — *relevance stated by the model:* "Respondent chose commerce/business as preferred study field; accounting is a core commerce skill."
  - `ideal_work_type` = Work for a multinational or large private company — *relevance stated by the model:* "Working in finance roles at larger firms commonly requires computerised accounting familiarity; this supports practical relevance for the respondent's career goal."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p2`, role=supporting_context_only: "This profile shows relatively higher household economic position and more respondents in private institutions; used only as supporting context for likely capacity to attend courses offered in English and on weekends."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course Overview lists: Peachtree Accounting Package; Sage, MYOB, ACC Package; Quick Books Accounting Package; Final Project with a Presentation" — source: COURSE-058
  - "This is a part time course which will be held on weekends." — source: COURSE-058

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent aims for finance/banking and named commerce/business as their field, a course teaching popular computerised accounting packages may support immediate job-readiness for finance roles (may be useful to build practical skills employers expect)." (hedged; based on: ideal_sector = Finance, banking, and insurance, study_field_preference = Commerce, business, or management, course overview listing accounting software packages (Peachtree, Sage, MYOB, QuickBooks))
  - "The course is described as part-time on weekends, which could make it easier to combine with the respondent's ongoing higher-education attendance (may be easier to attend alongside university)." (hedged; based on: edu_status = Currently in higher education (degree or diploma), course fact: part time on weekends)

**LLM's recommendation explanation (`why_recommended`):** "Computer Based Accounting directly matches the respondent's stated sector (finance) and study-field preference (commerce/business) by teaching widely-used accounting software and practical accounting skills that are relevant for finance roles in larger companies."

**Uncertainties disclosed by the LLM:**
  - The course document does not state explicit entry requirements or any formal prerequisites.
  - Fee, exact schedule times, course duration, and placement/employer links are not documented in the provided course text.

**Limitations disclosed by the LLM:**
  - No explicit information about course duration or certification level beyond the listed modules is provided in the document.
  - The document does not confirm progression pathways or guaranteed employer links; outcomes are not specified.

#### Rank 2: `COURSE-049` — Business Managemant

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = Commerce, business, or management — *relevance stated by the model:* "Respondent explicitly prefers business/commerce; a Business Management course directly covers core topics in this field."
  - `plans_after_education` = Look for a job — *relevance stated by the model:* "The respondent intends to look for a job after education; business-management content can support employability in corporate roles."
  - `ideal_work_type` = Work for a multinational or large private company — *relevance stated by the model:* "Management knowledge is commonly relevant for roles in large private or multinational companies."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_motivation_p2`, role=supporting_context_only: "Profile shows goal-aligned motivation with mixed study confidence; used as supporting context that respondent may be motivated to pursue goal-relevant training."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Business Management course will give theoretical knowledge as well as job oriented practical skills; it is a part time course held on weekends." — source: COURSE-049
  - "Course presented as aimed at developing skills necessary for employment and higher education." — source: COURSE-049

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants commerce/business study and plans to seek employment, a part-time weekend Business Management course could help build employer-relevant management knowledge while they finish higher education (may support employability and transition into corporate roles)." (hedged; based on: study_field_preference = Commerce, business, or management, plans_after_education = Look for a job, course fact: part time, weekends)

**LLM's recommendation explanation (`why_recommended`):** "Business Management aligns with the respondent's stated study-field preference (commerce/business) and with their aim to seek employment — the course claims to teach theoretical and practical job-oriented business skills."

**Uncertainties disclosed by the LLM:**
  - The course document does not specify modules/topics in detail, exact duration, or any entry requirements.
  - No direct statement of connections to multinational employers or placement services is provided.

**Limitations disclosed by the LLM:**
  - Course-level outcomes, assessment method, and certification details are not documented in the excerpt.
  - No fee or exact timetable details are available in the course text.

#### Rank 3: `COURSE-071` — Human Recources Management

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Work for a multinational or large private company — *relevance stated by the model:* "The respondent prefers working in larger private or multinational firms where HR practices and management knowledge are commonly relevant."
  - `study_field_preference` = Commerce, business, or management — *relevance stated by the model:* "HRM is a management/commerce-adjacent field; business/management preference supports relevance of HR training."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p2`, role=supporting_context_only: "This profile more often reports private-institute attendance and online job-searching methods; used only as background context suggesting the respondent is in an environment where HR/business skills may be valued."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course Overview lists: Introduction to Management and HRM; Job descriptions, recruitment, selection, hiring, induction; Discipline Management, Performance Evaluation System, Training and Development; Labour relations, employee welfare, labour law." — source: COURSE-071
  - "This is a part time course which will be held on weekends." — source: COURSE-071

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent aims to work for a multinational or large private company, HRM content (recruitment, discipline management, labour law) may be relevant for corporate entry-level HR or administrative roles in such organisations (may support entry into HR-related positions)." (hedged; based on: ideal_work_type = Work for a multinational or large private company, course fact: HRM modules including recruitment, induction, labour law)
  - "The course is described as part-time on weekends, which may be easier to attend alongside current university studies (may be practical for someone still in higher education)." (hedged; based on: edu_status = Currently in higher education (degree or diploma), course fact: part time, weekends)

**LLM's recommendation explanation (`why_recommended`):** "Human Resources Management covers management and HR topics that are relevant to business/management career interests and to working in larger private or multinational firms; the modules listed map to common corporate HR functions."

**Uncertainties disclosed by the LLM:**
  - Course text contains some [UNCLEAR] markers and the document is validated with limitations; details may be incomplete or partially unclear.
  - No explicit entry requirements, certification level, or employer linkage are stated in the document.

**Limitations disclosed by the LLM:**
  - Some course text contains unclear fragments; exact module depth and assessment are not described.
  - No information on fees, duration, or placement support is provided in the excerpt.


---

## 4. `nysc-4e38db03-e477-420e-9afd-d3f92b53995d` (Branch D) {#4-nysc-4e38db03-e477-420e-9afd-d3f92b53995d}

**Selection rationale (why this respondent was chosen for the batch):** Health, social work, and wellbeing

### Frozen profile membership(s)

- `D_motivation` — Profile 2: "Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support" (dimension: Motivation and study experience)
- `D_economic` — Profile 1: "Economic profile 1: relatively lower household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 2: "State-institution students without work exposure" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Bachelor's degree
  - `ideal_sector` = Health, social work, and wellbeing
  - `ideal_work_type` = Work for the government or public sector
  - `plans_after_education` = Look for a job
  - `study_field_preference` = Science or mathematics

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Small town
  - `district` = Puttalam
  - `edu_funding_source` = Government-funded or free of charge
  - `has_children` = No
  - `household_income` = LKR 120,000 – 200,000
  - `household_size` = 6.0
  - `household_unemployed` = 3.0
  - `household_workers` = 2.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = Yes — I am already searching
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Government school or state university
  - `job_search_method_d` = Through education or training institution
  - `re_entered_education` = No
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `autonomy_in_study` = Some — there is flexibility within a mostly fixed curriculum
  - `competence_in_study_field` = Fairly capable — mostly confident with some gaps
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Yes — I know one or two people who might help
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = Command of languages (English, etc.)
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `relatedness_at_institution` = Strongly — genuinely connected and part of the community
  - `social_capital_in_edu_access` = I researched and applied entirely on my own initiative
  - `study_motivation_type` = Because it aligns with my own goals and will lead to what I want

### Recommendation status: **NO_DEFENSIBLE_RECOMMENDATION**

**Retrieved course candidates (2):** COURSE-031 (National Diploma In Television Program Production); COURSE-006 (National Diploma In Information & Communication Technology)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Health, social work, and wellbeing; study_field_preference=Science or mathematics; ideal_work_type=Work for the government or public sector; expected_highest_edu_d=Bachelor's degree; plans_after_education=Look for a job; current_activity_status=Attending school, university, or a training programme; edu_status=Currently in higher education (degree or diploma)

**[LLM's saved reason for declining]:**

> The respondent explicitly stated direct-preference interests in the health / social work / wellbeing sector and a study-field preference for science or mathematics (Section 1). Neither of the retrieved NYSC course documents (National Diploma in Television Program Production; National Diploma in Information & Communication Technology) teaches health, social work, wellbeing content, or explicitly teaches science/mathematics as the respondent stated. Under the decision rules, direct-preference answers are required to justify a programme's content/field match, so no retrieved course can be defensibly recommended for this respondent based on the available evidence.

**Standard grounding audit on this decline:** PASS

**Evidence-category-discipline audit on this decline:** PASS


---

## 5. `nysc-8ae4a1d8-97c7-4bc4-9dc9-cb7eea0c897f` (Branch D) {#5-nysc-8ae4a1d8-97c7-4bc4-9dc9-cb7eea0c897f}

**Selection rationale (why this respondent was chosen for the batch):** Creative, media, and arts

### Frozen profile membership(s)

- `D_motivation` — Profile 2: "Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support" (dimension: Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 4: "Work-experienced students, mainly in private institutions" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Bachelor's degree
  - `ideal_sector` = Creative, media, and arts
  - `ideal_work_type` = Start my own business
  - `plans_after_education` = Do not know yet
  - `study_field_preference` = Literature, arts, or social sciences

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Metropolitan suburb
  - `district` = Colombo
  - `edu_funding_source` = Paid for by my family
  - `has_children` = No
  - `household_income` = Above LKR 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 1.0
  - `household_workers` = 3.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My regular job or business

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = Yes — I am already searching
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_end_year` = 2026.0
  - `edu_status` = I have completed my education and am not currently studying
  - `highest_edu_completed` = Bachelor's degree
  - `institution_type` = Private school or private degree-awarding institute
  - `job_search_method_d` = Online job ads (internet, social media)
  - `re_entered_education` = No
  - `spell1_activity` = Working for a salary or wage (employed)
  - `spell1_is_current` = Yes — this is still my current situation
  - `work_while_study_hours` = 5 to 10 hours
  - `work_while_study_motivation` = To gain work experience and build my CV
  - `work_while_study_paid` = Paid
  - `work_while_study_type` = Internship or apprenticeship in a private company
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `autonomy_in_study` = Some — there is flexibility within a mostly fixed curriculum
  - `competence_in_study_field` = Somewhat capable — I struggle in some areas
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Yes — I know one or two people who might help
  - `most_important_life_goal` = Making a meaningful contribution to society
  - `most_useful_quality_for_job` = Business and economic knowledge
  - `move_reason` = For education or training
  - `moved_from_origin` = No — I moved from somewhere else
  - `relatedness_at_institution` = Weakly — I feel fairly isolated or disconnected
  - `social_capital_in_edu_access` = Family members advised me or guided the choice
  - `study_motivation_type` = To avoid disappointing my family or feeling guilty about not studying

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (10):** COURSE-062 (Desktop Publisher); COURSE-031 (National Diploma In Television Program Production); COURSE-041 (Preschool Teacher (Early Childhood Development)); COURSE-049 (Business Managemant); COURSE-068 (Graphics Designer); COURSE-009 (Information And Communication Technolory Technician); COURSE-016 (Graphics Designer); COURSE-001 (Freelancer Of Web Design & Development); COURSE-003 (Certificate In English Communication Essentials.); COURSE-006 (National Diploma In Information & Communication Technology)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Creative, media, and arts; study_field_preference=Literature, arts, or social sciences; ideal_work_type=Start my own business; expected_highest_edu_d=Bachelor's degree; plans_after_education=Do not know yet; current_activity_status=Attending school, university, or a training programme; work_while_study_type=Internship or apprenticeship in a private company; highest_edu_completed=Bachelor's degree; edu_status=I have completed my education and am not currently studying; [sector-vocabulary expansion terms: adobe illustrator, adobe indesign, adobe photoshop, child psychology, graphics, television]

#### Rank 1: `COURSE-068` — Graphics Designer

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Creative, media, and arts — *relevance stated by the model:* "Directly names the creative/media/arts sector that Graphics Designer course serves."
  - `study_field_preference` = Literature, arts, or social sciences — *relevance stated by the model:* "Respondent expressed an arts/literature preference, which aligns with graphic design as an arts-related skill area."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "The course's part-time, weekend format and entrepreneurial framing may support someone wanting to start a creative business."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p2`, role=supporting_context_only: "This economic profile had relatively higher household economic position and many private-institution students; may indicate capacity to pursue part-time, fee-paying training if desired"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Graphics Designing courses give theoretical knowledge and job oriented practical skills; this is a part time course which will be held on weekends." — source: COURSE-068
  - "Course overview emphasises entrepreneurial abilities and directing youth to desired occupations." — source: COURSE-068

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business and the course description emphasises entrepreneurial abilities and is part-time on weekends, this Graphics Designer course may be practical for developing creative skills while allowing time to pursue business setup activities." (hedged; based on: ideal_work_type = Start my own business, COURSE-068: part time course which will be held on weekends; emphasises entrepreneurial abilities)

**LLM's recommendation explanation (`why_recommended`):** "Strong content match: respondent named creative/media/arts and arts as preferred field, and this course teaches graphic design (creative skills) in a part-time, weekend format with an entrepreneurial framing that aligns with the respondent's goal to start a business."

**Uncertainties disclosed by the LLM:**
  - Course fee, exact schedule dates, and entry requirements are not stated in the course document.
  - The respondent's current schedule and employer commitments are not fully specified; compatibility with the course timetable is assumed plausible but not confirmed.

**Limitations disclosed by the LLM:**
  - The course document does not list explicit entry requirements or fees.
  - Information about placement, accreditation level, or specific modules beyond the general description is limited.

#### Rank 2: `COURSE-062` — Desktop Publisher

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Creative, media, and arts — *relevance stated by the model:* "Desktop publishing/graphic tools are core to creative/media work the respondent named."
  - `study_field_preference` = Literature, arts, or social sciences — *relevance stated by the model:* "Arts/literature preference aligns with desktop publishing and design skills useful for creative outputs."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p4`, role=supporting_context_only: "Profile shows many work-experienced students and private-institution background; may support practical, job-oriented skills training as next step"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Desktop Publishing & Graphic Designing course covers Adobe PageMaker, Photoshop, InDesign, Illustrator and other desktop-publishing/corel tools; it is a part time course held on weekends." — source: COURSE-062

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent expressed interest in arts/creative sectors and the course teaches industry-standard design software, the Desktop Publisher course could build technical skills useful for creative freelancing or running a small design business." (hedged; based on: study_field_preference = Literature, arts, or social sciences, ideal_sector = Creative, media, and arts, COURSE-062: teaches Photoshop, InDesign, Illustrator and is part-time on weekends)

**LLM's recommendation explanation (`why_recommended`):** "The course teaches concrete desktop-publishing and graphic software skills that map to the respondent's stated creative/art interests and could support entrepreneurship in media/creative production."

**Uncertainties disclosed by the LLM:**
  - Some tool names in the course text have uncertainty markers ([UNCLEAR]) and the document lacks explicit fees and entry requirements.
  - Level or certification detail beyond the software list is limited in the extracted text.

**Limitations disclosed by the LLM:**
  - The course text contains some unclear/extracted items marked [UNCLEAR].
  - No explicit entry requirements or fee information are provided in the document.

#### Rank 3: `COURSE-049` — Business Managemant

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent explicitly wants to start a business; Business Management directly teaches entrepreneurship-related content."
  - `most_useful_quality_for_job` = Business and economic knowledge — *relevance stated by the model:* "Respondent named business/economic knowledge as a useful quality, matching this course's topic."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p2`, role=supporting_context_only: "Profile-level tendency toward private-institution attendance and online job-search methods suggests orientation toward formal business-skills training, as supporting background context only."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Business Management course will give theoretical knowledge as well as job oriented practical that is necessary for employment and higher education. This is a part time course which will be held on weekends." — source: COURSE-049

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start a business and values business/economic knowledge, a Business Management course offered part-time on weekends may help develop business planning and management skills relevant to entrepreneurship." (hedged; based on: ideal_work_type = Start my own business, most_useful_quality_for_job = Business and economic knowledge, COURSE-049: Business Management is part time and held on weekends)

**LLM's recommendation explanation (`why_recommended`):** "Direct skills match for the respondent's stated intention to start a business and stated valuation of business/economic knowledge; part-time weekend delivery may be feasible alongside other activities."

**Uncertainties disclosed by the LLM:**
  - Course syllabus detail, specific entrepreneurship modules, fees, and entry requirements are not provided in the course document.
  - No explicit statement that the course includes startup support, so applicability to a specific business plan is uncertain.

**Limitations disclosed by the LLM:**
  - Absence of explicit module breakdown or fee/entry information in the course text.
  - The course description is generic; it is not clear which business topics (e.g., accounting, marketing, legal) are covered in depth.

#### Rank 4: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course description emphasises developing a skill to earn locally and internation...' has low word-overlap (20%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported); course_fact 'Course duration and fee details visible in the document (e.g., 3 months, fee 20,...' has low word-overlap (21%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Course explicitly aims to teach skills for earning income independently (freelancing / building own business)."
  - `ideal_sector` = Creative, media, and arts — *relevance stated by the model:* "Web design/development can serve creative/media outputs and digital portfolios relevant to the respondent's sector preference."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p4`, role=supporting_context_only: "Profile contains many work-experienced students who search for work and undertake internships; this supports interest in practical, income-generating skill training as context only."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course description emphasises developing a skill to earn locally and internationally, creating a website via hosting/domain management, and guidance on freelancing platforms (Fiverr) and ways to earn money." — source: COURSE-001
  - "Course duration and fee details visible in the document (e.g., 3 months, fee 20,000/=) and teacher experience noted." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business, a course that explicitly trains freelancing/web-business skills and describes methods for earning may directly support their entrepreneurial aim." (hedged; based on: ideal_work_type = Start my own business, COURSE-001: emphasises freelancing, hosting/domain management, and earning methods)

**LLM's recommendation explanation (`why_recommended`):** "This course is directly framed around freelancing and building an income-generating web skills business, which aligns with the respondent's goal to start their own business and their creative/online sector overlap."

**Uncertainties disclosed by the LLM:**
  - While the course lists a fee and start date, other details (exact schedule, accreditation level) are not fully documented in the extracted text.
  - Language mix and scheduling compatibility with the respondent's commitments are not certain.

**Limitations disclosed by the LLM:**
  - Course appears to have explicit fee information in the text, but other formal accreditation or entry requirements are not shown.
  - The document mixes Sinhala/English content; exact language of instruction for each cohort is not fully specified.


---

## 6. `nysc-4401e631-9304-4f41-9ba4-6f84d659f7c8` (Branch D) {#6-nysc-4401e631-9304-4f41-9ba4-6f84d659f7c8}

**Selection rationale (why this respondent was chosen for the batch):** Agriculture, forestry, and fishing

### Frozen profile membership(s)

- `D_motivation` — Profile 3: "Consensus motivation profile 3: highly self-directed, capable and connected" (dimension: Motivation and study experience)
- `D_economic` — Profile 1: "Economic profile 1: relatively lower household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 2: "State-institution students without work exposure" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Post-graduate degree
  - `ideal_sector` = Agriculture, forestry, and fishing
  - `ideal_work_type` = Start my own business
  - `plans_after_education` = Look for a job
  - `study_field_preference` = Health sciences or nursing

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Small town
  - `district` = Kurunegala
  - `edu_funding_source` = Government-funded or free of charge
  - `has_children` = No
  - `household_income` = LKR 60,000 – 120,000
  - `household_size` = 4.0
  - `household_unemployed` = 0.0
  - `household_workers` = 0.0
  - `primary_earner_status` = Shared — several people contribute roughly equally
  - `primary_income_source` = My parents or family

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = No — not yet
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Government school or state university
  - `re_entered_education` = No
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `autonomy_in_study` = A great deal — I have real freedom to shape my learning
  - `competence_in_study_field` = Very capable — confident and effective in my field
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `most_important_life_goal` = Having a good family life
  - `most_useful_quality_for_job` = Business and economic knowledge
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `relatedness_at_institution` = Strongly — genuinely connected and part of the community
  - `social_capital_in_edu_access` = A friend, teacher, or contact recommended it
  - `study_motivation_type` = To avoid disappointing my family or feeling guilty about not studying

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (6):** COURSE-049 (Business Managemant); COURSE-032 (Plant Nursery Development Assistant); COURSE-031 (National Diploma In Television Program Production); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-020 (Landscape Development Assistant); COURSE-001 (Freelancer Of Web Design & Development)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Agriculture, forestry, and fishing; study_field_preference=Health sciences or nursing; ideal_work_type=Start my own business; expected_highest_edu_d=Post-graduate degree; plans_after_education=Look for a job; current_activity_status=Attending school, university, or a training programme; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: landscaping, nursery]

#### Rank 1: `COURSE-032` — Plant Nursery Development Assistant

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "The respondent wants to start their own business; the course description mentions developing entrepreneurial abilities and employment-oriented practical skills useful for starting an enterprise."
  - `ideal_sector` = Agriculture, forestry, and fishing — *relevance stated by the model:* "The course is explicitly about plant nursery development, which falls within agriculture/horticulture and directly matches the respondent's stated sector preference."
  - `study_field_preference` = Health sciences or nursing — *relevance stated by the model:* "Recorded to be transparent: this preference does not match the course content but was considered when assessing overall fit."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p2`, role=supporting_context_only: "Main education funding source: more often reported ‘Government-funded or free of charge’"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course is 'Plant Nursery Development Assistant' and 'will give you theoretical knowledge as well as job oriented practical that is necessary for employment and higher education.'" — source: COURSE-032
  - "This is a full time course which will be held on weekdays." — source: COURSE-032
  - "By completing this course, you can achieve competency Level 4 under the National Vocational Qualifications Competency Standards." — source: COURSE-032

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent stated they want to 'Start my own business' and this course description emphasises entrepreneurial abilities and job-oriented practical skills, the course may support their intention to develop skills useful for starting an agricultural/plant-nursery business." (hedged; based on: DIRECT: ideal_work_type = Start my own business, COURSE: course text mentions developing entrepreneurial abilities and job-oriented practical)
  - "Because the respondent named agriculture, forestry, and fishing as their ideal sector and the course is plant-nursery focused, the subject matter appears directly relevant to that stated sector preference." (hedged; based on: DIRECT: ideal_sector = Agriculture, forestry, and fishing, COURSE: course title and overview 'Plant Nursery Development Assistant')

**LLM's recommendation explanation (`why_recommended`):** "Direct sector match: the respondent explicitly named 'Agriculture, forestry, and fishing' and this course trains plant-nursery skills and offers entrepreneurial/practical training useful for starting an agriculture-related business."

**Uncertainties disclosed by the LLM:**
  - The course document does not state fees or exact location — affordability and travel/venue details are not available in the course text.
  - The course is full-time on weekdays; the respondent is currently in higher education, so schedule compatibility is uncertain and would need confirmation from the respondent or programme.

**Limitations disclosed by the LLM:**
  - No explicit information about entry requirements or eligibility is provided in the course document.
  - No fee, exact schedule dates, or venue location are documented in the retrieved course text.

#### Rank 2: `COURSE-049` — Business Managemant

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "The respondent's desire to start a business directly aligns with a Business Management course that aims to develop entrepreneurial abilities and job-oriented practical knowledge."
  - `study_field_preference` = Health sciences or nursing — *relevance stated by the model:* "Included as background: this stated study preference does not match this course's content (business), but the respondent's entrepreneurship goal makes business skills relevant."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p2`, role=supporting_context_only: "Main education funding source: more often reported ‘Government-funded or free of charge’"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course name 'Business Managemant' aims to develop entrepreneurial abilities and provide theoretical and job-oriented practical knowledge." — source: COURSE-049
  - "This is a part time course which will be held on weekends." — source: COURSE-049
  - "Objective includes directing youth to desired occupations while developing entrepreneurial abilities." — source: COURSE-049

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business and the course explicitly focuses on entrepreneurial abilities, the part-time Business Management course may be useful for building the business knowledge the respondent seeks." (hedged; based on: DIRECT: ideal_work_type = Start my own business, COURSE: course description emphasises developing entrepreneurial abilities)
  - "Because the course is part-time and held on weekends, it may be easier to combine with the respondent's ongoing higher-education studies than a weekday full-time course would be." (hedged; based on: DIRECT: respondent is 'Currently in higher education (degree or diploma)', COURSE: course is part time and held on weekends)

**LLM's recommendation explanation (`why_recommended`):** "The respondent explicitly wants to start a business; this Business Management course explicitly aims to develop entrepreneurial abilities and is offered part-time on weekends, which may fit a student schedule."

**Uncertainties disclosed by the LLM:**
  - The course document does not state fees, exact location, entry requirements, or dates — these logistical details are unknown from the retrieved text.
  - The respondent's stated study field preference (health sciences/nursing) is not matched by this course; relevance stems from their entrepreneurship goal rather than a subject-matter preference.

**Limitations disclosed by the LLM:**
  - No explicit entry requirements or placement/employment outcomes are provided in the course text.
  - No documented information about whether the course content covers agriculture-specific business practices; if the respondent intends an agricultural business specifically, additional detail would be needed.

#### Rank 3: `COURSE-020` — Landscape Development Assistant

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Agriculture, forestry, and fishing — *relevance stated by the model:* "The respondent's stated sector preference includes agricultural/land-based activities; Landscape Development (horticulture/landscaping) is related to plant cultivation and land use."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "The course description notes developing entrepreneurial abilities, which could be relevant to starting a landscaping or land-management enterprise."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p1`, role=supporting_context_only: "Ideal sector: less often reported ‘Information technology and communications’"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course title 'Landscape Development Assistant' and overview stating it gives theoretical knowledge as well as job oriented practical skills necessary for employment and higher education." — source: COURSE-020
  - "This is a full time course which will be held on weekdays and leads to competency Level 4 under NVQ standards." — source: COURSE-020

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent selected an agricultural/land-based sector, the Landscape Development course may be relevant as it covers landscaping/land management skills that overlap with horticulture and could support small-business activity in that space." (hedged; based on: DIRECT: ideal_sector = Agriculture, forestry, and fishing, COURSE: title and overview 'Landscape Development Assistant' with practical skills)
  - "Because the course is full-time on weekdays while the respondent is currently studying at higher education, schedule compatibility may be uncertain and would need confirmation." (hedged; based on: DIRECT: respondent is 'Currently in higher education (degree or diploma)', COURSE: course is full time on weekdays)

**LLM's recommendation explanation (`why_recommended`):** "The course trains practical land/landscape skills that plausibly overlap with the respondent's stated interest in agriculture/forestry and could support entrepreneurial activity (e.g., a landscaping or horticultural business)."

**Uncertainties disclosed by the LLM:**
  - The course document does not provide fees, exact location, or entry requirements.
  - The course is full-time on weekdays which may conflict with the respondent's current higher-education timetable; compatibility is unknown.

**Limitations disclosed by the LLM:**
  - No specific description of whether the course covers commercial/enterprise planning or business modules beyond practical/horticultural skills.
  - No documented information about placement, employer links, or agricultural-farming-specific content beyond landscaping.


---

## 7. `nysc-515dbda4-d209-46f1-b1cd-a9f996f9cebd` (Branch D) {#7-nysc-515dbda4-d209-46f1-b1cd-a9f996f9cebd}

**Selection rationale (why this respondent was chosen for the batch):** Hotels, restaurants, and hospitality

### Frozen profile membership(s)

- `D_motivation` — Profile 3: "Consensus motivation profile 3: highly self-directed, capable and connected" (dimension: Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 4: "Work-experienced students, mainly in private institutions" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Post-graduate degree
  - `ideal_sector` = Hotels, restaurants, and hospitality
  - `ideal_work_type` = Work for a multinational or large private company
  - `plans_after_education` = Look for a job
  - `study_field_preference` = ICT or computing

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Small town
  - `district` = Gampaha
  - `edu_funding_source` = Paid for by my family
  - `has_children` = No
  - `household_income` = LKR 120,000 – 200,000
  - `household_size` = 6.0
  - `household_unemployed` = 2.0
  - `household_workers` = 1.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My partner or spouse

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = Yes — I am already searching
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Private school or private degree-awarding institute
  - `job_search_method_d` = Checking at worksites / factory gates
  - `re_entered_education` = No
  - `work_while_study_hours` = More than 20 hours
  - `work_while_study_motivation` = To gain work experience and build my CV
  - `work_while_study_paid` = Paid
  - `work_while_study_type` = Internship or apprenticeship in a private company
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `autonomy_in_study` = A great deal — I have real freedom to shape my learning
  - `competence_in_study_field` = Fairly capable — mostly confident with some gaps
  - `edu_min_for_decent_job` = Vocational training or NVQ
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = Business and economic knowledge
  - `move_reason` = Other reason
  - `moved_from_origin` = No — I moved from somewhere else
  - `relatedness_at_institution` = Strongly — genuinely connected and part of the community
  - `social_capital_in_edu_access` = I researched and applied entirely on my own initiative
  - `study_motivation_type` = I am genuinely passionate about this subject

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (12):** COURSE-011 (Baker); COURSE-007 (Professional Cookery); COURSE-050 (Cake & Cake Structure); COURSE-047 (Baker); COURSE-031 (National Diploma In Television Program Production); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-071 (Human Recources Management); COURSE-053 (Computer Applications Assistant); COURSE-001 (Freelancer Of Web Design & Development); COURSE-049 (Business Managemant); COURSE-084 (Store Management); COURSE-051 (Cake Decorator)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Hotels, restaurants, and hospitality; study_field_preference=ICT or computing; ideal_work_type=Work for a multinational or large private company; expected_highest_edu_d=Post-graduate degree; plans_after_education=Look for a job; current_activity_status=Attending school, university, or a training programme; work_while_study_type=Internship or apprenticeship in a private company; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: cake, cookery, management]

#### Rank 1: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = ICT or computing — *relevance stated by the model:* "This directly names ICT/computing as the respondent's preferred study field, so it is the primary basis for selecting ICT courses."
  - `ideal_work_type` = Work for a multinational or large private company — *relevance stated by the model:* "Prefers employment in larger organisations where formal ICT qualifications (a diploma) are commonly relevant."
  - `plans_after_education` = Look for a job — *relevance stated by the model:* "Intends to seek employment after study; a diploma-level course emphasising workplace ICT skills aligns with that plan."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p2`, role=supporting_context_only: "This profile often reports ICT or computing as preferred field of study (group-level tendency)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers System Analysis & Design, Software Programming, Database System, Web Programming, Local Area Network and other workplace ICT topics." — source: COURSE-006
  - "This is a full time course which will be held on weekdays." — source: COURSE-006
  - "Course language: English; by completing this course one can achieve Competency Level 5 under NVQ standards." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent explicitly prefers ICT/computing (study_field_preference) and the course teaches core ICT subjects (system design, programming, databases, web programming), this course appears to match the respondent's stated field interest." (hedged; based on: study_field_preference = ICT or computing, Course covers System Analysis & Design, Software Programming, Database System, Web Programming (COURSE-006))
  - "Because the respondent plans to look for a job after education and the course lists workplace-related modules and NVQ Level 5 competency, it could support their stated job-seeking plans." (hedged; based on: plans_after_education = Look for a job, Course mentions workplace information/communication and NVQ competency (COURSE-006))
  - "Because the course is full-time on weekdays while the respondent works >20 hours during study (work_while_study_hours), attending this full-time weekday programme may be more difficult to combine with existing paid work hours; this is a feasibility concern rather than a content mismatch." (hedged; based on: work_while_study_hours = More than 20 hours, Course is full time on weekdays (COURSE-006))

**LLM's recommendation explanation (`why_recommended`):** "The respondent explicitly named ICT/computing as their preferred study field; this National Diploma covers core ICT subjects (programming, databases, web, networking) and awards NVQ-level competency that is plausibly useful for job-seeking in ICT or large private/multinational employers."

**Uncertainties disclosed by the LLM:**
  - The course document does not state exact fees or the enrolment dates for this listing (fee and start-date information not available in the course text).
  - While the course lists full-time weekday delivery, no flexibility or part-time alternative is documented for this specific offering.

**Limitations disclosed by the LLM:**
  - No explicit entry requirements (e.g. prior qualifications) are stated in the course document; eligibility is not documented here.
  - Location or campus for this specific course offering is not provided in the retrieved text.

#### Rank 2: `COURSE-053` — Computer Applications Assistant

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = ICT or computing — *relevance stated by the model:* "Directly indicates a preference for ICT-related training; basic computer applications fit under ICT."
  - `plans_after_education` = Look for a job — *relevance stated by the model:* "Respondent intends to seek employment; a practical computer applications course could support immediate job-readiness."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_motivation_p3`, role=supporting_context_only: "Profile members report competence and autonomous study orientation (group-level tendency)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers ICT introduction, MS-Office, Using Internet & E-mail." — source: COURSE-053
  - "This is a part time course which will be held on weekends." — source: COURSE-053
  - "Course language: English; practical, job-oriented focus." — source: COURSE-053

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent prefers ICT and is already searching for work, a part-time, weekend computer applications course may be useful to build immediate workplace ICT skills that support job-searching." (hedged; based on: study_field_preference = ICT or computing, already_job_searching = Yes — I am already searching, Course covers MS-Office, Internet & E-mail and is part-time on weekends (COURSE-053))
  - "Because the respondent previously worked while studying and values gaining work experience, a short practical ICT skills course may be easier to combine with ongoing commitments than a full-time diploma." (hedged; based on: worked_while_studying = Yes, work_while_study_hours = More than 20 hours, Course is part time on weekends (COURSE-053))

**LLM's recommendation explanation (`why_recommended`):** "The course teaches foundational ICT skills (MS Office, internet/email) that directly align with an ICT/computing preference and with immediate job-seeking; it is part-time on weekends which may better fit someone combining study and work."

**Uncertainties disclosed by the LLM:**
  - Course duration, exact schedule, fees and location are not stated in the extracted text.
  - Level of certification or formal NVQ level is not provided in this listing.

**Limitations disclosed by the LLM:**
  - No explicit entry requirements or placement/employment guarantees are documented.
  - The course appears aimed at basic applications rather than advanced programming, so it may not satisfy ambitions for higher-level ICT roles without further training.

#### Rank 3: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course is delivered in English and Sinhala; listed course fee appears in the ext...' has low word-overlap (24%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported); course_fact 'Course advertisement emphasises earning income locally and internationally and b...' has low word-overlap (30%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = ICT or computing — *relevance stated by the model:* "Respondent's ICT preference supports web development as a relevant ICT sub-field."
  - `plans_after_education` = Look for a job — *relevance stated by the model:* "Respondent intends to seek income after study; a web development/freelancing course may support self-employment or job applications in ICT."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p4`, role=supporting_context_only: "Profile contains many work-experienced students who seek employment (group-level tendency)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers web site development, hosting and domain management, and setting up freelancer platforms (e.g. Fiverr) to earn income." — source: COURSE-001
  - "Course is delivered in English and Sinhala; listed course fee appears in the extract (20,000/=) and duration mentioned as 3 months for one intake." — source: COURSE-001
  - "Course advertisement emphasises earning income locally and internationally and building a business/development of skills." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent named ICT as preferred and wants to look for a job, a course that teaches web development and freelancing tools could support alternative employment paths (freelancing or web roles) consistent with that preference." (hedged; based on: study_field_preference = ICT or computing, plans_after_education = Look for a job, Course covers web development, hosting, and freelancer platform setup (COURSE-001))
  - "Because this course explicitly mentions earning income and contains a short (3-month) duration, it may be attractive if the respondent prefers quicker, income-focused skills training; however the respondent also expects a postgraduate degree eventually, so this could be viewed as short-term, practical skill development." (hedged; based on: expected_highest_edu_d = Post-graduate degree, Course duration ~ 3 months and income-focus (COURSE-001))

**LLM's recommendation explanation (`why_recommended`):** "The course is a practical, short-format web design/development and freelancing programme directly aligned with ICT/computing interests and with job/income-seeking intentions; it also documents a fee and duration which may help planning."

**Uncertainties disclosed by the LLM:**
  - While a fee and duration are visible in the extracted text, other details such as exact schedule, accreditation level and location are not fully documented.
  - Quality or depth of the technical curriculum (e.g. programming languages, frameworks) is not specified beyond hosting, domain and freelancing guidance.

**Limitations disclosed by the LLM:**
  - The course may be oriented toward freelancing and small-business income rather than formal employment in multinational companies the respondent prefers; it may still be useful for building practical web skills but may not directly guarantee placement in large firms.
  - No formal NVQ level is documented for this listing.

#### Rank 4: `COURSE-007` — Professional Cookery

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Hotels, restaurants, and hospitality — *relevance stated by the model:* "The respondent explicitly named hospitality (hotels/restaurants) as their ideal sector; cookery courses are directly relevant to hospitality sector job roles."
  - `plans_after_education` = Look for a job — *relevance stated by the model:* "Respondent intends to seek employment; professional cookery prepares learners for hospitality jobs."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - *(none cited — empty for this recommendation)*

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers Western and Eastern menus, fish and meat items, beverages, stocks, sauces, soups, salads, sweets and desserts — broadly aligned with professional cookery in hospitality." — source: COURSE-007
  - "This is a full time course which will be held on weekdays." — source: COURSE-007
  - "Course language: Sinhala; max students 20; job-oriented practical training is emphasised." — source: COURSE-007

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent explicitly prefers the hotels/restaurants/hospitality sector, a professional cookery course appears to match that sectoral interest directly and could prepare them for kitchen roles in hospitality establishments." (hedged; based on: ideal_sector = Hotels, restaurants, and hospitality, Course covers menus, fish/meat items, beverages and desserts relevant to professional cookery (COURSE-007))
  - "Because the course is full-time on weekdays and the respondent reports working more than 20 hours while studying, the full-time schedule may be harder to combine with current paid-work commitments; this is a feasibility consideration rather than a content mismatch." (hedged; based on: work_while_study_hours = More than 20 hours, Course is full time on weekdays (COURSE-007))

**LLM's recommendation explanation (`why_recommended`):** "The respondent named hospitality as their ideal sector; Professional Cookery teaches core culinary skills directly relevant to hotels and restaurants and emphasises job-oriented practical training."

**Uncertainties disclosed by the LLM:**
  - Course listing does not state accreditation level (NVQ), exact duration, location or fee in the extracted text.
  - No explicit entry requirements or language support details beyond 'Sinhala' are provided.

**Limitations disclosed by the LLM:**
  - Course delivery is full-time on weekdays which may conflict with the respondent's current work hours; schedule flexibility is not documented in the listing.
  - If the respondent's aim is specifically employment in multinational hotels (preferred work type), the course description does not state employer links or placement pathways.


---

## 8. `nysc-b556590a-0e0d-4d6f-8b9e-f148e18ca930` (Branch D) {#8-nysc-b556590a-0e0d-4d6f-8b9e-f148e18ca930}

**Selection rationale (why this respondent was chosen for the batch):** Weak/unsure sector AND field — NO_DEFENSIBLE stress test

### Frozen profile membership(s)

- `D_motivation` — Profile 1: "Consensus motivation profile 1: externally or uncertainly motivated, with moderate study support" (dimension: Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 3: "Private-institution students without work exposure" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Bachelor's degree
  - `ideal_sector` = Not sure
  - `ideal_work_type` = Not sure yet
  - `plans_after_education` = Do not know yet
  - `study_field_preference` = Other field

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Large city
  - `district` = Galle
  - `edu_funding_source` = Paid for by my family
  - `has_children` = No
  - `household_income` = Above LKR 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 1.0
  - `household_workers` = 2.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = No — not yet
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Private school or private degree-awarding institute
  - `re_entered_education` = No
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 18 – 21 years
  - `autonomy_in_study` = Some — there is flexibility within a mostly fixed curriculum
  - `competence_in_study_field` = Not very capable — I frequently feel out of my depth
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `most_important_life_goal` = Finding purpose and meaning in life
  - `most_useful_quality_for_job` = A good general education
  - `move_reason` = For education or training
  - `moved_from_origin` = No — I moved from somewhere else
  - `relatedness_at_institution` = Weakly — I feel fairly isolated or disconnected
  - `social_capital_in_edu_access` = I researched and applied entirely on my own initiative
  - `study_motivation_type` = I am not sure why — I am following the path I ended up on

### Recommendation status: **NO_DEFENSIBLE_RECOMMENDATION**

**Retrieved course candidates (4):** COURSE-031 (National Diploma In Television Program Production); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-026 (Field Assistant (agricultural)); COURSE-036 (Survey Field Assistant)

**Retrieval query summary (used to search, not shown to the model as such):** study_field_preference=Other field; expected_highest_edu_d=Bachelor's degree; plans_after_education=Do not know yet; current_activity_status=Attending school, university, or a training programme; edu_status=Currently in higher education (degree or diploma)

**[LLM's saved reason for declining]:**

> The respondent did not provide any usable direct preference or intent that names a study field, sector, or training area (study_field_preference = 'Other field'; ideal_sector = 'Not sure'; plans_after_education = 'Do not know yet'). Under the decision rules, only DIRECT PREFERENCE/INTENT answers may independently justify choosing a course's content area. Because no specific field or sector was stated, it is not defensible to select any of the retrieved NYSC courses on the respondent's behalf.

**Standard grounding audit on this decline:** PASS

**Evidence-category-discipline audit on this decline:** PASS


---

## 9. `nysc-25c345ec-5f45-4616-adb8-c96e31f3511c` (Branch D) {#9-nysc-25c345ec-5f45-4616-adb8-c96e31f3511c}

**Selection rationale (why this respondent was chosen for the batch):** has_children=Yes, never studied, conflicting intent signals

### Frozen profile membership(s)

- `D_motivation` — Profile 3: "Consensus motivation profile 3: highly self-directed, capable and connected" (dimension: Motivation and study experience)
- `D_economic` — Profile 1: "Economic profile 1: relatively lower household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 1: "Re-entered students, often with degree-educated parents" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = O/L level
  - `ideal_sector` = Manufacturing or production
  - `ideal_work_type` = Work for the government or public sector
  - `plans_after_education` = Stay at home

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Rural area
  - `district` = Jaffna
  - `edu_funding_source` = Scholarship or grant
  - `has_children` = Yes
  - `household_income` = Below LKR 30,000
  - `household_size` = 4.0
  - `household_unemployed` = 4.0
  - `household_workers` = 3.0
  - `num_children` = 2.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My regular job or business

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = Yes — I am already searching
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = I have never studied
  - `institution_type` = Private school or private degree-awarding institute
  - `job_search_method_d` = Public employment office registration
  - `re_entered_education` = Yes
  - `reason_re_entered` = Was not sure what I wanted to do

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 18 – 21 years
  - `autonomy_in_study` = A great deal — I have real freedom to shape my learning
  - `competence_in_study_field` = Very capable — confident and effective in my field
  - `edu_min_for_decent_job` = Vocational training or NVQ
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = IT and digital skills
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `relatedness_at_institution` = Strongly — genuinely connected and part of the community
  - `social_capital_in_edu_access` = I was assigned or directed by a government programme
  - `study_motivation_type` = I am genuinely passionate about this subject

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-012 (Refrigeration & Air Conditioning Technician); COURSE-034 (Refrigeration & Air Conditioning Technician); COURSE-028 (Lapiderist (Gem Cutting)); COURSE-029 (Mobile Phone Repair Technician); COURSE-030 (Motorcycle Mechanic); COURSE-077 (Mobile Phone Repair Technician); COURSE-040 (Automobile Mechanic); COURSE-005 (Automobile Mechanic); COURSE-031 (National Diploma In Television Program Production); COURSE-078 (Motorcycle Mechanic); COURSE-042 (Automobile Electrician); COURSE-064 (Electrician); COURSE-081 (Radio, TV & Allied Equipment Repairer); COURSE-025 (Electrician); COURSE-021 (Automobile Electrician)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Manufacturing or production; ideal_work_type=Work for the government or public sector; expected_highest_edu_d=O/L level; plans_after_education=Stay at home; current_activity_status=Attending school, university, or a training programme; edu_status=I have never studied; [sector-vocabulary expansion terms: air conditioning, automobile, electrical, electronics, english, gem cutting, mechanic, mobile phone, motorcycle, programming, refrigeration, sinhala]

#### Rank 1: `COURSE-030` — Motorcycle Mechanic

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "The respondent explicitly prefers the manufacturing/production sector; motorcycle/mechanic trades are squarely within production/repair occupations aligned to that sector."
  - `expected_highest_edu_d` = O/L level — *relevance stated by the model:* "The course is a vocational trade (practical, competency-level outcomes) which aligns with the respondent's stated expected education level favoring vocational training."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p1`, role=supporting_context_only: "This economic profile indicates relatively lower household economic position (group-level)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Motorcycle Mechanic course will give theoretical knowledge as well as job oriented practical skills necessary for employment and higher education." — source: COURSE-030
  - "This is a full time course which will be held on weekdays." — source: COURSE-030
  - "By completing this course , can achieve Competency Level 3,4 under the National Vocational Qualifications Competency Standards." — source: COURSE-030

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent named manufacturing/production as their ideal sector and this course is a hands-on mechanical trade, it appears compatible with their stated sector preference." (hedged; based on: ideal_sector = Manufacturing or production, COURSE-030: Motorcycle Mechanic teaches practical mechanical skills for employment)
  - "Because the respondent expects an O/L-level highest education and the course leads to NVQ competency levels, this course may suit their expected education pathway." (hedged; based on: expected_highest_edu_d = O/L level, COURSE-030: competency Level 3,4 outcome)
  - "Because the respondent has children and lives in a low-income household, a part-time or weekend format may be easier to combine with responsibilities; however COURSE-030 is documented as full-time weekday delivery (limitation)." (hedged; based on: has_children = Yes, household_income = Below LKR 30,000, COURSE-030: full time course on weekdays)

**LLM's recommendation explanation (`why_recommended`):** "Practical mechanical trade directly matches the respondent's stated interest in manufacturing/production and provides vocational NVQ outcomes appropriate for an O/L-level pathway."

**Uncertainties disclosed by the LLM:**
  - Course-030 is shown as full-time weekdays; respondent's caregiving and household circumstances may make weekday full-time attendance harder — schedule suitability is uncertain.
  - Course fee, exact location in Jaffna, and explicit entry requirements are not documented in the course text provided.

**Limitations disclosed by the LLM:**
  - The course document lists weekday full-time delivery; alternate part-time/weekend offerings are not documented for this specific course in the provided extract.
  - No explicit entry requirements or fee information available in the course document.

#### Rank 2: `COURSE-005` — Automobile Mechanic

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Automobile mechanic/technician is a mechanical trade aligned with production/repair occupations within the manufacturing/production sector."
  - `expected_highest_edu_d` = O/L level — *relevance stated by the model:* "The course awards competency Level 4 under NVQ standards, which fits a vocational pathway appropriate for an O/L-level expectation."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p1`, role=supporting_context_only: "This economic profile indicates relatively lower household economic position (group-level)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Automobile Mechanic/Automobile Technician will give theoretical knowledge as well as job oriented practical skills necessary for employment and higher education." — source: COURSE-005
  - "This is a full time course which will be held on weekdays." — source: COURSE-005
  - "By completing this course , You can achieve competency Level 4 under the National Vocational Qualifications Competency Standards." — source: COURSE-005

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent prefers manufacturing/production and the course trains vehicle mechanical systems (engine, transmission, braking etc.), it appears aligned with their sector preference." (hedged; based on: ideal_sector = Manufacturing or production, COURSE-005: course content includes engine, transmission, steering, braking systems)
  - "Given the respondent's expected O/L-level education and the NVQ Level 4 outcome listed, the course may be suitable as a vocational qualification pathway." (hedged; based on: expected_highest_edu_d = O/L level, COURSE-005: competency Level 4 outcome)

**LLM's recommendation explanation (`why_recommended`):** "Automobile Mechanic is a well-aligned vocational programme teaching the hands-on mechanical skills typical of manufacturing/production occupations and provides NVQ outcomes suitable for the respondent's education expectation."

**Uncertainties disclosed by the LLM:**
  - Documented delivery is full-time on weekdays; the respondent's caregiving responsibilities and household circumstances may affect schedule feasibility.
  - No fee, exact Jaffna location, or entry-requirement details are present in the course extract.

**Limitations disclosed by the LLM:**
  - Schedule (full-time, weekdays) may conflict with respondent's childcare/responsibility constraints — course document does not list part-time options for this specific record.
  - No explicit fee, venue, or entry requirement information available in the provided course text.

#### Rank 3: `COURSE-064` — Electrician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Electrical installation and industrial electrical skills are used in manufacturing, production, and maintenance environments matching the respondent's sector preference."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p1`, role=supporting_context_only: "This economic profile indicates relatively lower household economic position (group-level)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Electrician courses include Domestic Electrical Installation, Repair and Service Motor Generator, Industrial Electrical Installation (Motor Controlling System), P.L.C., Security Solutions." — source: COURSE-064
  - "This is a part time course which will be held on weekends." — source: COURSE-064

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent prioritised manufacturing/production and this course covers industrial electrical installations and motor control systems, it appears relevant to jobs in production or factory maintenance." (hedged; based on: ideal_sector = Manufacturing or production, COURSE-064: includes Industrial Electrical Installation and Motor Controlling System)
  - "Because this COURSE-064 is documented as part-time weekend delivery, it may be easier to combine with the respondent's childcare and household commitments than full-time weekday courses." (hedged; based on: has_children = Yes, COURSE-064: part time weekend delivery)

**LLM's recommendation explanation (`why_recommended`):** "Electrician training teaches electrical and industrial skills relevant to manufacturing/production roles and is offered in a part-time weekend format in the provided document, which may better fit the respondent's household responsibilities."

**Uncertainties disclosed by the LLM:**
  - Course-064's exact location, fee, and entry requirements are not stated in the provided extract.
  - While course content aligns with manufacturing/production tasks, no guarantee it leads to public-sector employment (respondent preferred government/public sector).

**Limitations disclosed by the LLM:**
  - The course document shows part-time weekend delivery for this record; local scheduling and precise timing in Jaffna are not documented and should be confirmed.
  - No fee, venue address, or explicit entry criteria are provided in the course text.

#### Rank 4: `COURSE-034` — Refrigeration & Air Conditioning Technician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS WITH CAUTION
  - caution: inference marked uncertainty_language_used=True but no hedging word found in the text: 'There are two retrieved refrigeration/A/C documents (COURSE-012 indicates a week...'
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Refrigeration & A/C repair and maintenance are technician trades used in manufacturing, cold-chain production facilities, and equipment maintenance — a reasonable match to manufacturing/production preference."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - *(none cited — empty for this recommendation)*

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course teaches repair of refrigerators, deep freezers, display units, water coolers; repair of window and split A/C; operate and maintain central A/C systems." — source: COURSE-034
  - "Document lists this specific COURSE-034 record as a full time course held on weekdays and states NVQ competency Level 4 outcome." — source: COURSE-034

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent named manufacturing/production as their ideal sector and the course trains equipment maintenance used in production and commercial settings, it appears relevant to their sector interest." (hedged; based on: ideal_sector = Manufacturing or production, COURSE-034: refrigeration and A/C repair and maintenance content)
  - "There are two retrieved refrigeration/A/C documents (COURSE-012 indicates a weekend/part-time delivery while COURSE-034 indicates full-time weekdays); schedule suitability for the respondent is therefore uncertain and should be verified." (hedged; based on: COURSE-012: part time weekend delivery, COURSE-034: full time weekday delivery)

**LLM's recommendation explanation (`why_recommended`):** "The course provides hands-on technician skills relevant to repair and maintenance roles common in production and commercial settings, aligning with the respondent's manufacturing/production preference and offering NVQ-level outcomes."

**Uncertainties disclosed by the LLM:**
  - Conflicting delivery format between retrieved documents (part-time weekends vs full-time weekdays) — exact schedule for this course instance is unclear.
  - No explicit entry requirements, fee, or exact location in Jaffna are provided in the extracted documents.

**Limitations disclosed by the LLM:**
  - Schedule ambiguity between COURSE-012 and COURSE-034 requires clarification before enrolment.
  - Course documents do not state fees, venue addresses, or entry criteria; these must be confirmed with NYSC.


---

## 10. `nysc-0566257f-e441-4134-9a0f-ebedde047f88` (Branch D) {#10-nysc-0566257f-e441-4134-9a0f-ebedde047f88}

**Selection rationale (why this respondent was chosen for the batch):** ICT + worked_while_studying — experience-building test

### Frozen profile membership(s)

- `D_motivation` — Profile 3: "Consensus motivation profile 3: highly self-directed, capable and connected" (dimension: Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 4: "Work-experienced students, mainly in private institutions" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Bachelor's degree
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Start my own business
  - `plans_after_education` = Look for a job
  - `study_field_preference` = ICT or computing

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Metropolitan suburb
  - `district` = Colombo
  - `edu_funding_source` = Paid for by my family
  - `has_children` = No
  - `household_income` = Above LKR 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 0.0
  - `household_workers` = 2.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My regular job or business

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = Yes — I am already searching
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Private school or private degree-awarding institute
  - `job_search_method_d` = Online job ads (internet, social media)
  - `re_entered_education` = No
  - `work_while_study_hours` = More than 20 hours
  - `work_while_study_motivation` = To build connections that could lead to future employment
  - `work_while_study_paid` = Paid
  - `work_while_study_type` = Internship or apprenticeship in a private company
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `autonomy_in_study` = A great deal — I have real freedom to shape my learning
  - `competence_in_study_field` = Very capable — confident and effective in my field
  - `edu_min_for_decent_job` = A/L level
  - `employment_network_quality` = Yes — I know one or two people who might help
  - `most_important_life_goal` = Building self-confidence and personal fulfilment
  - `most_useful_quality_for_job` = A good general education
  - `move_reason` = Other reason
  - `moved_from_origin` = No — I moved from somewhere else
  - `relatedness_at_institution` = Strongly — genuinely connected and part of the community
  - `social_capital_in_edu_access` = Family members advised me or guided the choice
  - `study_motivation_type` = Because it aligns with my own goals and will lead to what I want

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-001 (Freelancer Of Web Design & Development); COURSE-053 (Computer Applications Assistant); COURSE-009 (Information And Communication Technolory Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-035 (Secretary (Secretarial Practices)); COURSE-052 (Cisco Certified Network Associate); COURSE-049 (Business Managemant); COURSE-058 (Computer Based Accounting); COURSE-002 (PYTHON); COURSE-057 (Multimedia & Web Design); COURSE-008 (Computer Hardware Technician)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; study_field_preference=ICT or computing; ideal_work_type=Start my own business; expected_highest_edu_d=Bachelor's degree; plans_after_education=Look for a job; current_activity_status=Attending school, university, or a training programme; work_while_study_type=Internship or apprenticeship in a private company; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** STRONG
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course teaches web development, domain & hosting management, setting up Fiverr a...' has low word-overlap (35%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported); course_fact 'Course duration and fee are described (3 months, fee LKR 20,000 in the course te...' has low word-overlap (33%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent explicitly wants to start their own business; this course description explicitly targets freelancing and building one’s own income/business."
  - `study_field_preference` = ICT or computing — *relevance stated by the model:* "Respondent prefers ICT/computing; the course teaches web development which is an ICT field."
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent named IT/communications as ideal sector; web design & development falls squarely within that sector."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_motivation_p3`, role=supporting_context_only: "This profile often reports ICT as a useful skill and shows high study autonomy/competence (group-level pattern)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course teaches web development, domain & hosting management, setting up Fiverr and other freelancer accounts; explicitly frames helping learners earn locally and internationally and develop their own business." — source: COURSE-001
  - "Course duration and fee are described (3 months, fee LKR 20,000 in the course text)." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business and explicitly prefers ICT/ computing, this freelancing-focused web development course may directly support that stated goal." (hedged; based on: ideal_work_type = Start my own business, study_field_preference = ICT or computing, course teaches web development and freelancing tools (COURSE-001))
  - "Because the respondent already searches for work online and has experience working while studying, the practical/industry-focused nature of this course may be a useful, job-oriented complement to their existing activities." (hedged; based on: already_job_searching = Yes — I am already searching, worked_while_studying = Yes, course describes practical, job-oriented training (COURSE-001))

**LLM's recommendation explanation (`why_recommended`):** "Direct match to the respondent's stated desire to start their own business in ICT: the course explicitly teaches web development, domain/hosting management and freelancing marketplaces — skills directly relevant to starting a freelance web business."

**Uncertainties disclosed by the LLM:**
  - Course location and exact schedule are not stated in a way tied to the respondent's district (Colombo) in the course text; availability in Colombo is not confirmed in the document.
  - The fee is stated in the course text but how this aligns with the respondent's funding plan (family-paid) is not tested here.

**Limitations disclosed by the LLM:**
  - The course document shows a fee (LKR 20,000) but does not state entry requirements or exact class times beyond a start date; the respondent's ability to attend alongside current studies depends on schedule and timing which are not fully documented here.
  - This is a short (3-month) course focused on freelancing/web development; it may not substitute for a longer formal ICT diploma if the respondent expects a degree-level credential.

#### Rank 2: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = ICT or computing — *relevance stated by the model:* "Respondent prefers ICT/computing; this diploma is explicitly in Information & Communication Technology."
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent named IT as ideal sector; the diploma covers core ICT subjects relevant to that sector."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p4`, role=supporting_context_only: "Profile contains work-experienced students in private institutions who often combine study and internships."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course curriculum lists system analysis & design, software programming, database systems, web programming, LAN, software testing and workplace communication; described as a full-time weekday course." — source: COURSE-006
  - "Course is full time and held on weekdays; aims to develop entrepreneurial abilities and job-oriented practical skills; achieves NVQ Competency Level 5." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent is studying a higher education programme and has work experience (internship) while studying, a structured diploma covering programming, databases and networking may build on their background and support both job search and future entrepreneurship." (hedged; based on: edu_status = Currently in higher education (degree or diploma), worked_while_studying = Yes — internship/apprenticeship, course curriculum includes software programming, databases, web programming (COURSE-006))
  - "Because the course is full-time on weekdays, this format may be more time-intensive than the respondent's current study/work combination and could be harder to combine with paid work; this is a feasibility concern rather than disqualifying content fit." (hedged; based on: work_while_study_hours = More than 20 hours, course is full time on weekdays (COURSE-006))

**LLM's recommendation explanation (`why_recommended`):** "The diploma covers a broad suite of ICT skills (programming, databases, web, networks) that directly map to the respondent's stated ICT/computing preference and IT sector interest; it also mentions entrepreneurial skills which align with the respondent's wish to start a business."

**Uncertainties disclosed by the LLM:**
  - The course is full-time on weekdays; the respondent currently combines paid internship/work with studies and works more than 20 hours — whether they can attend full-time is uncertain and would need confirmation from the respondent or provider.
  - No explicit entry requirements or exact location details (e.g. Colombo campus) are provided in the course text.

**Limitations disclosed by the LLM:**
  - The absence of explicit location and entry-requirement details in the course document means eligibility and travel/attendance feasibility cannot be confirmed here.
  - Full-time weekday scheduling may conflict with the respondent's current commitments; this is a practical limitation to investigate, not a content mismatch.

#### Rank 3: `COURSE-073` — Java Programming With Software Applications Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = ICT or computing — *relevance stated by the model:* "Respondent prefers ICT/computing; this course teaches Java programming and software application development, a core ICT skill."
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Java/software development is clearly within IT/communications sector the respondent selected."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_motivation_p3`, role=supporting_context_only: "Profile shows higher perceived competence and self-directed motivation in study (group-level pattern)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course provides theoretical and job-oriented practical skills in Java and software application development; it is a part-time weekend course." — source: COURSE-073

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent is already combining study and paid work and values autonomy in study, a part-time weekend programming course may be practical to undertake alongside existing commitments." (hedged; based on: work_while_study_hours = More than 20 hours, autonomy_in_study = A great deal, course is part time, held on weekends (COURSE-073))
  - "Because the respondent is already searching for work and confident in their competence, adding formal programming skills in Java may support their job-search and technical employability in IT." (hedged; based on: already_job_searching = Yes — I am already searching, competence_in_study_field = Very capable, course teaches Java programming (COURSE-073))

**LLM's recommendation explanation (`why_recommended`):** "Direct technical match to the respondent's ICT/computing preference; a part-time weekend format increases practical feasibility for someone working or studying concurrently."

**Uncertainties disclosed by the LLM:**
  - The course document does not state exact class times, location, or entry requirements beyond being part-time; availability in Colombo is not confirmed.
  - It is not specified whether the course provides certification aligned with a national qualification level.

**Limitations disclosed by the LLM:**
  - Missing explicit information about prerequisites or certification level in the course document limits ability to judge whether it meets the respondent's degree-level expectations.
  - While weekends are indicated, exact scheduling and potential clashes with the respondent's current commitments must be confirmed.

#### Rank 4: `COURSE-002` — PYTHON

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = ICT or computing — *relevance stated by the model:* "Respondent prefers ICT/computing; Python is a widely used programming language in ICT."
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Python programming skills are relevant to roles in the IT sector the respondent selected."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p2`, role=supporting_context_only: "Profile members often use online job ads and digital channels when job-searching (group-level pattern)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course card indicates a part-time Python course, 20 students capacity, duration 03 months; labelled 'Part Time' though some catalogue lines are unclear." — source: COURSE-002

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is part-time and short (3 months), it may be practical for the respondent to complete alongside ongoing higher-education commitments and job search." (hedged; based on: edu_status = Currently in higher education (degree or diploma), work_while_study_hours = More than 20 hours, course labelled Part Time and 03 Month duration (COURSE-002))

**LLM's recommendation explanation (`why_recommended`):** "Python is a core ICT skill that aligns with the respondent's stated ICT/computing preference and IT sector interest; the short, part-time format appears compatible with their study/work pattern."

**Uncertainties disclosed by the LLM:**
  - The course document contains unreadable/corrupted lines and explicitly notes remaining uncertainty markers; some details (exact schedule, full syllabus, entry requirements, location) are not fully legible.
  - Certification level and depth of content are unclear from the catalogue card alone.

**Limitations disclosed by the LLM:**
  - Because the source contains some unreadable text, several operational details (precise schedule, prerequisites, full syllabus) could not be confirmed and must be checked with the provider.
  - The catalogue card alone gives limited information about learning outcomes or credential recognition.

#### Rank 5: `COURSE-057` — Multimedia & Web Design

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = ICT or computing — *relevance stated by the model:* "Web design and multimedia fall under ICT/computing interests the respondent reported."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "The course teaches multimedia/web design skills that could be applied in freelance or small business contexts the respondent aspires to."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_motivation_p3`, role=supporting_context_only: "Profile shows a tendency to value IT/digital skills and autonomous study (group-level pattern)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course described as Computer Multimedia Designing, part-time on weekends, job-oriented practical skills." — source: COURSE-057

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start a business and the course focuses on multimedia and web design, it could help them develop marketable skills for a freelance or small ICT business." (hedged; based on: ideal_work_type = Start my own business, course focuses on multimedia & web design (COURSE-057))
  - "Because the course is part-time on weekends, it may be easier to combine with the respondent's ongoing studies and paid work compared with full-time weekday courses." (hedged; based on: work_while_study_hours = More than 20 hours, course is part time, held on weekends (COURSE-057))

**LLM's recommendation explanation (`why_recommended`):** "Practical multimedia and web design skills align with the respondent's ICT preference and entrepreneurial aim; weekend, part-time format increases feasibility for someone juggling studies and work."

**Uncertainties disclosed by the LLM:**
  - The course document does not specify exact schedule times, location, or entry requirements.
  - Depth, certification level and whether the course explicitly covers freelancing/marketplace strategies (as opposed to purely design skills) are not detailed.

**Limitations disclosed by the LLM:**
  - Missing operational details (location, prerequisites, certification level) mean further confirmation is required before enrolment decisions.
  - The course emphasises multimedia and design — if the respondent prefers deeper programming/backend development, this course may be less aligned than programming-focused options.


---

## 11. `nysc-15a74ec0-011b-4f61-804e-72de37c73705` (Branch D) {#11-nysc-15a74ec0-011b-4f61-804e-72de37c73705}

**Selection rationale (why this respondent was chosen for the batch):** Public administration/government sector, new combo

### Frozen profile membership(s)

- `D_motivation` — Profile 1: "Consensus motivation profile 1: externally or uncertainly motivated, with moderate study support" (dimension: Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (dimension: Economic resources and household pressure)
- `D_educational_cultural` — Profile 2: "State-institution students without work exposure" (dimension: Educational trajectory and cultural capital)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_d` = Post-graduate degree
  - `ideal_sector` = Public administration, government, and defence
  - `ideal_work_type` = Work for the government or public sector
  - `plans_after_education` = Immediately go on to further education or training
  - `study_field_preference` = Industrial or technical studies

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Metropolitan suburb
  - `district` = Ratnapura
  - `edu_funding_source` = Paid for by my family
  - `has_children` = No
  - `household_income` = LKR 30,000 – 60,000
  - `household_size` = 4.0
  - `household_unemployed` = 1.0
  - `household_workers` = 1.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `already_job_searching` = No — not yet
  - `current_activity_status` = Attending school, university, or a training programme
  - `edu_status` = Currently in higher education (degree or diploma)
  - `institution_type` = Government school or state university
  - `re_entered_education` = No
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 26 – 29 years
  - `autonomy_in_study` = Some — there is flexibility within a mostly fixed curriculum
  - `competence_in_study_field` = Fairly capable — mostly confident with some gaps
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `most_important_life_goal` = Having a good family life
  - `most_useful_quality_for_job` = Communication and interpersonal skills
  - `move_reason` = For education or training
  - `moved_from_origin` = No — I moved from somewhere else
  - `relatedness_at_institution` = Weakly — I feel fairly isolated or disconnected
  - `social_capital_in_edu_access` = I researched and applied entirely on my own initiative
  - `study_motivation_type` = I am not sure why — I am following the path I ended up on

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (4):** COURSE-031 (National Diploma In Television Program Production); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-064 (Electrician); COURSE-025 (Electrician)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Public administration, government, and defence; study_field_preference=Industrial or technical studies; ideal_work_type=Work for the government or public sector; expected_highest_edu_d=Post-graduate degree; plans_after_education=Immediately go on to further education or training; current_activity_status=Attending school, university, or a training programme; edu_status=Currently in higher education (degree or diploma)

#### Rank 1: `COURSE-025` — Electrician

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = Industrial or technical studies — *relevance stated by the model:* "The respondent explicitly prefers industrial/technical studies, which directly matches Electrician training content."
  - `plans_after_education` = Immediately go on to further education or training — *relevance stated by the model:* "The respondent plans further education; the course text states it provides theoretical knowledge and pathways useful for employment and higher education."
  - `ideal_work_type` = Work for the government or public sector — *relevance stated by the model:* "Working for the public sector is the respondent's goal; technical trades such as electrician are commonly employed in public infrastructure roles, making such a technical qualification plausibly relevant to that aim."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_educational_cultural_p2`, role=supporting_context_only: "Main education funding source: more often reported ‘Government-funded or free of charge’ (24/53, 45.3%)"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course Overview lists practical technical modules (Repair and Service Motor Generator; Industrial Electrical Installation; P.L.C.; Domestic Electrical Installation; Security Solutions)." — source: COURSE-025
  - "Described as a full time weekday course and gives theoretical knowledge as well as job-oriented practical skills; competency levels under National Vocational Qualifications are stated." — source: COURSE-025

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent stated a preference for industrial/technical studies, this electrician course appears directly aligned with their stated field interest." (hedged; based on: study_field_preference = Industrial or technical studies, COURSE-025: Electrician course overview listing industrial electrical topics)
  - "Because the respondent plans to continue with further education, the course's statement that it provides theoretical knowledge and pathways toward higher education may be useful for that plan." (hedged; based on: plans_after_education = Immediately go on to further education or training, COURSE-025: course overview mentioning higher education and NVQ competency levels)

**LLM's recommendation explanation (`why_recommended`):** "The respondent explicitly prefers industrial/technical studies and the Electrician course teaches core industrial electrical skills (industrial/domestic installation, motor repair, PLC) with practical and theoretical components and NVQ alignment — a direct content match to the stated study preference and to the respondent's intent to pursue further training."

**Uncertainties disclosed by the LLM:**
  - The course document does not state exact location or whether it is offered in Ratnapura; local accessibility is not documented here.
  - COURSE-025 is full-time on weekdays; the respondent's personal schedule constraints were not reported, so suitability of the schedule is uncertain.
  - No explicit entry requirements, fees, or duration are provided in the course text.

**Limitations disclosed by the LLM:**
  - Recommendation is based on the respondent's stated field preference and course descriptions only; it does not confirm eligibility or personal fit beyond content alignment.
  - Location, fee, exact schedule details and entry requirements are not present in the course document and should be checked with NYSC before application.

#### Rank 2: `COURSE-064` — Electrician

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = Industrial or technical studies — *relevance stated by the model:* "The respondent explicitly prefers industrial/technical studies, which directly matches Electrician training content."
  - `plans_after_education` = Immediately go on to further education or training — *relevance stated by the model:* "The respondent plans further education; the course text indicates it gives theoretical knowledge as well as practical skills useful for employment and further study."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_motivation_p1`, role=supporting_context_only: "Within this profile, a larger share reported having few useful employment/training contacts."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course Overview lists practical technical topics (Domestic Electrical Installation; Repair and Service Motor Generator; Industrial Electrical Installation; P.L.C.; Security Solutions)." — source: COURSE-064
  - "This document describes the course as a part time weekend programme." — source: COURSE-064

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent prefers industrial/technical studies, this electrician course appears aligned with their stated field interest." (hedged; based on: study_field_preference = Industrial or technical studies, COURSE-064: Electrician course overview listing technical topics)
  - "Because COURSE-064 is described as a part-time weekend course, it may be more practical for someone balancing other commitments than a weekday full-time option, although the respondent did not report specific scheduling constraints." (hedged; based on: COURSE-064: part time weekend course statement, respondent: no direct statement about schedule constraints)

**LLM's recommendation explanation (`why_recommended`):** "Like COURSE-025, this Electrician course teaches core industrial electrical skills that directly match the respondent's stated preference for industrial/technical studies. Its part-time weekend format (documented) may offer a different feasibility option compared with full-time courses."

**Uncertainties disclosed by the LLM:**
  - Exact location, fees, duration, and entry requirements are not provided in the course document.
  - The respondent did not state they require part-time/weekend learning; the part-time format is a possible advantage only if their schedule makes it necessary.

**Limitations disclosed by the LLM:**
  - Recommendation rests on content alignment with the respondent's stated field preference; it does not guarantee eligibility or fit with the respondent's timetable or other personal constraints.
  - The course document does not confirm placement outcomes or employer links; those claims must not be assumed.

#### Rank 3: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `study_field_preference` = Industrial or technical studies — *relevance stated by the model:* "The respondent expressed a preference for technical studies; ICT is a technical field, so it is a plausible but not exact match to 'industrial' studies."
  - `plans_after_education` = Immediately go on to further education or training — *relevance stated by the model:* "The course document states it provides theoretical and practical knowledge useful for employment and higher education, which aligns with the respondent's plan for further training."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `D_economic_p2`, role=supporting_context_only: "Within this economic profile, many respondents reported ICT or computing as their preferred field of study."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course modules include System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network, Software Testing and related workplace communication/management topics." — source: COURSE-006
  - "Described as a full time weekday course giving theoretical and job-oriented practical knowledge and alignment with NVQ competency standards." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent indicated interest in technical studies broadly, ICT training may still be useful even if not their specifically named subfield; it could expand technical skill options for further education or public-sector roles." (hedged; based on: study_field_preference = Industrial or technical studies, COURSE-006: ICT course modules covering multiple technical skills)

**LLM's recommendation explanation (`why_recommended`):** "ICT is a technical field and the course covers a wide set of technical skills and NVQ alignment. If the respondent is open to technical study beyond strictly 'industrial' trades, this ICT diploma could support further education and broaden employability options."

**Uncertainties disclosed by the LLM:**
  - The respondent did not explicitly name ICT as a preferred field, so this is a plausible but not direct content match.
  - No information on location, fees, entry requirements or exact duration is present in the course text.

**Limitations disclosed by the LLM:**
  - This recommendation is more tentative than the electrician options because the respondent specifically named 'industrial or technical studies' rather than ICT/computing.
  - Check eligibility, schedule fit and local availability with NYSC; the course document does not provide those operational details.


---

## 12. `nysc-0a4832c0-3e8a-47e9-ac41-22252b0ceb06` (Branch E) {#12-nysc-0a4832c0-3e8a-47e9-ac41-22252b0ceb06}

**Selection rationale (why this respondent was chosen for the batch):** E profile 1, ICT, entrepreneurship-training interest

### Frozen profile membership(s)

- `E_learning_orientation` — Profile 1: "High perceived education utility and strong learning ambition" (dimension: Education usefulness and further-learning orientation)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `desire_for_work` = Yes
  - `expected_highest_edu_e` = Post-graduate degree
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Start my own business
  - `job_acceptance_conditions` = Only a job that is stable, well paid, AND matches my qualifications
  - `job_type_sought` = Technical work
  - `plans_further_edu` = Yes
  - `training_type_would_help` = Entrepreneurship training to start own business

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Large city
  - `available_to_start` = Yes — I was available and could have started
  - `district` = Colombo
  - `has_children` = No
  - `has_minimum_wage` = Yes — there is a minimum I would not go below
  - `household_income` = Above LKR 200,000
  - `household_size` = 8.0
  - `household_unemployed` = 3.0
  - `household_workers` = 5.0
  - `income_urgency` = Not urgently — I can take time to find the right opportunity
  - `main_obstacle_finding_work` = Working conditions in available jobs are poor
  - `minimum_wage_band` = Above LKR 120,000
  - `primary_earner_status` = Shared — several people contribute roughly equally
  - `primary_income_source` = An education grant, scholarship, or training allowance
  - `willing_to_relocate` = Yes — to another country

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `active_search_4weeks` = Yes — I took active steps in the past four weeks
  - `activity_while_searching` = Planning to start my own business
  - `current_activity_status` = Not working — looking for work or trying to set up a business
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help` = No — none at all
  - `ever_refused_job` = Yes
  - `job_search_duration` = Less than 1 week
  - `num_applications` = 10.0
  - `num_interviews` = 5.0
  - `past_edu_usefulness` = Very useful — directly relevant, employers value it
  - `reason_refused_job` = No possibility for career advancement
  - `search_method_primary` = Looking for resources to start own business
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `edu_min_for_decent_job` = Post-graduate qualification
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `future_planning_orientation` = I have a very clear, specific plan and I am actively working toward it
  - `job_search_autonomy_orientation` = I am looking specifically for work I genuinely want to do
  - `job_search_self_efficacy` = Very confident — I believe I will find suitable work
  - `knows_people_in_target_sector` = Yes — I know several people working in that field
  - `most_important_life_goal` = Finding purpose and meaning in life
  - `most_useful_quality_for_job` = Communication and interpersonal skills
  - `move_reason` = For education or training
  - `moved_from_origin` = No — I moved from somewhere else
  - `network_helpfulness` = Very helpful — I have received real leads and referrals
  - `social_support_job_search` = Very supported — people actively encourage and assist me

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-001 (Freelancer Of Web Design & Development); COURSE-009 (Information And Communication Technolory Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-052 (Cisco Certified Network Associate); COURSE-035 (Secretary (Secretarial Practices)); COURSE-049 (Business Managemant); COURSE-058 (Computer Based Accounting); COURSE-031 (National Diploma In Television Program Production); COURSE-057 (Multimedia & Web Design); COURSE-053 (Computer Applications Assistant); COURSE-002 (PYTHON)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; job_type_sought=Technical work; ideal_work_type=Start my own business; training_type_would_help=Entrepreneurship training to start own business; expected_highest_edu_e=Post-graduate degree; job_acceptance_conditions=Only a job that is stable, well paid, AND matches my qualifications; main_obstacle_finding_work=Working conditions in available jobs are poor; current_activity_status=Not working — looking for work or trying to set up a business; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** STRONG
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course description emphasises freelancing, developing your own skill to earn loc...' has low word-overlap (26%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported); course_fact 'Course length and fee details shown on card (3 months; fee LKR 20,000) in the ca...' has low word-overlap (25%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent explicitly wants to start their own business; this course explicitly teaches freelancing and building an income-generating web development skillset useful for self-employment."
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent named IT as their desired sector; this is a web development course in the IT sector."
  - `training_type_would_help` = Entrepreneurship training to start own business — *relevance stated by the model:* "Respondent asked for entrepreneurship training; the course description explicitly emphasises creating a personal skill to earn domestically and internationally and starting/developing a business."
  - `job_type_sought` = Technical work — *relevance stated by the model:* "Course teaches technical web development skills that align with the respondent's technical job interest."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p1`, role=supporting_context_only: "Within this profile, many respondents report IT as ideal sector and desire to start own businesses; this supports that IT+entrepreneurship training is a commonly aligned combination in the group."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course description emphasises freelancing, developing your own skill to earn locally and internationally, hosting, domain management, creating Fiverr and other accounts and methods to earn money." — source: COURSE-001
  - "Course covers hosting, domain management, web site development, and business-development content; explicit mention of building one’s own business and income methods." — source: COURSE-001
  - "Course length and fee details shown on card (3 months; fee LKR 20,000) in the catalogue card." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business and the course explicitly teaches freelancing, platform setup (Fiverr), hosting and business methods, this course appears directly relevant to the respondent's entrepreneurship intention and IT sector preference." (hedged; based on: ideal_work_type = Start my own business, training_type_would_help = Entrepreneurship training to start own business, COURSE-001 course facts about freelancing, Fiverr, hosting)

**LLM's recommendation explanation (`why_recommended`):** "The course explicitly targets freelancing/web entrepreneurship (hosting, domain management, Fiverr and income methods) which aligns closely with the respondent's stated desire to start a business in IT and their preference for technical work."

**Uncertainties disclosed by the LLM:**
  - The course card shows a fee (LKR 20,000) and other logistical details, but full formal entry requirements and exact schedule/venue details are not provided in the retrieved document.

**Limitations disclosed by the LLM:**
  - Although fee and duration appear on the catalogue card, the course document does not provide a formal entry-requirement section; eligibility cannot be confirmed from the document.
  - The respondent is currently in higher education and expects postgraduate study; timing/compatibility with their studies is unknown and must be checked with the provider.

#### Rank 2: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent selected IT as their preferred sector; this is a broad ICT diploma covering systems analysis, programming, databases, web programming and networks."
  - `job_type_sought` = Technical work — *relevance stated by the model:* "Course contains technical modules (software programming, database systems, LAN, web programming) matching technical job interests."
  - `training_type_would_help` = Entrepreneurship training to start own business — *relevance stated by the model:* "Course description states it aims to develop entrepreneurial abilities alongside technical skills."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p1`, role=supporting_context_only: "Profile shows high perceived usefulness of education and strong further-learning orientation, consistent with pursuing a diploma-level IT qualification."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course includes System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network and includes an explicit objective to develop entrepreneurial abilities." — source: COURSE-006
  - "This is described as a full time course held on weekdays and maps to National Vocational Qualification Level 5." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course combines technical IT modules with stated objectives to develop entrepreneurial abilities, it may help the respondent build both the technical foundation and some entrepreneurial orientation needed to start an IT business." (hedged; based on: ideal_sector = Information technology and communications, training_type_would_help = Entrepreneurship training to start own business, COURSE-006 modules and entrepreneurship objective)
  - "Because the course is full-time on weekdays and the respondent is currently in higher education, the full-time schedule may require the respondent to reconcile study commitments; this is a feasibility consideration rather than a content mismatch." (hedged; based on: edu_status = Currently in higher education (degree or diploma), COURSE-006 course fact that it is full time held on weekdays)

**LLM's recommendation explanation (`why_recommended`):** "The diploma covers multiple core IT technical topics the respondent signalled interest in (programming, databases, web, networks) and explicitly aims to develop entrepreneurial abilities, matching both the sector and the entrepreneurship training preference."

**Uncertainties disclosed by the LLM:**
  - The document states the course is full-time on weekdays; whether the respondent can pause or combine it with their current higher-education commitments is unknown.
  - No explicit entry requirements, fees, or exact venue details are provided in the course document.

**Limitations disclosed by the LLM:**
  - Because the course is full-time, timing may conflict with the respondent's ongoing higher education; this needs checking with the provider.
  - Entry/eligibility criteria are not given in the retrieved text, so eligibility cannot be confirmed from the document.

#### Rank 3: `COURSE-002` — PYTHON

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent expressed an IT sector preference; a Python programming course is directly within IT technical skills."
  - `job_type_sought` = Technical work — *relevance stated by the model:* "Python is a technical programming skill useful for technical roles the respondent seeks."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p1`, role=supporting_context_only: "Profile members often plan further education and view past education as useful, consistent with short technical upskilling courses such as a short Python programme."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course name is PYTHON; catalogue card recovers 'Python මුල සිට ඉගෙන ගන්න' (learn Python from scratch). It is part-time, 20 students capacity, 03 Month duration." — source: COURSE-002

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent seeks technical IT work and the Python course is a short, part-time technical programming course, it may be a practical way to gain programming skills quickly that support technical job prospects or business development in IT." (hedged; based on: job_type_sought = Technical work, ideal_sector = Information technology and communications, COURSE-002 facts: Python course, part time, 3 month duration)

**LLM's recommendation explanation (`why_recommended`):** "A focused Python course offers direct technical skill-building in programming, aligning with the respondent's IT sector preference and technical job interest; the short, part-time format may be practical alongside other commitments."

**Uncertainties disclosed by the LLM:**
  - Two remaining unreadable lines on the catalogue card mean some details are unclear (e.g., precise schedule, fees or prerequisites); the retrieved document has limited visibility.
  - No explicit entry requirements or guaranteed outcomes are stated.

**Limitations disclosed by the LLM:**
  - The catalogue card has some corrupted/unreadable text; full logistical details (exact schedule, fees, instructor background) are not fully documented in the retrieved text.
  - Course-level outcomes (e.g., entrepreneurship content) are not explicitly stated, so additional entrepreneurship training may still be needed for starting a business.

#### Rank 4: `COURSE-049` — Business Managemant

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `training_type_would_help` = Entrepreneurship training to start own business — *relevance stated by the model:* "Respondent explicitly wants entrepreneurship training; a Business Management course addresses business skills relevant to starting and running a business."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent's stated intent to start a business maps to business management content."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p1`, role=supporting_context_only: "The profile shows strong orientation to further learning and many expect higher education; business management training is consistent with that orientation."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course titled 'Business Managemant' and described as giving theoretical knowledge and job-oriented practical skills; offered part time on weekends." — source: COURSE-049

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants entrepreneurship training to start a business, a Business Management course may provide useful business knowledge and practical skills that support their entrepreneurial plans." (hedged; based on: training_type_would_help = Entrepreneurship training to start own business, ideal_work_type = Start my own business, COURSE-049 course fact that it teaches business management and practical skills)

**LLM's recommendation explanation (`why_recommended`):** "Business Management provides core business knowledge and practical skills relevant to starting or managing a business, aligning with the respondent's explicit entrepreneurship training preference."

**Uncertainties disclosed by the LLM:**
  - Course description is general; it does not list specific modules (e.g., accounting, marketing, business planning) in the retrieved text.
  - No explicit fee, entry requirements or schedule details beyond 'part time, weekends' are provided.

**Limitations disclosed by the LLM:**
  - The course document lacks detailed module-level information and specific entrepreneurship-focused modules are not explicitly enumerated; it may be necessary to confirm whether the course includes entrepreneurship or start-up practicals.
  - Entry/eligibility and fee information are not provided in the retrieved text.


---

## 13. `nysc-136c3ecd-09d4-4238-8a63-64c8636724df` (Branch E) {#13-nysc-136c3ecd-09d4-4238-8a63-64c8636724df}

**Selection rationale (why this respondent was chosen for the batch):** E profile 2, ICT, self-employment intent

### Frozen profile membership(s)

- `E_learning_orientation` — Profile 2: "Moderate perceived utility and mixed learning ambition" (dimension: Education usefulness and further-learning orientation)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `desire_for_work` = Yes
  - `expected_highest_edu_e` = Bachelor's degree
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Start my own business
  - `job_acceptance_conditions` = Any job, provided it matches my level of qualification
  - `job_type_sought` = Self-employment or starting a business
  - `plans_further_edu` = Yes
  - `training_type_would_help` = University degree

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Large city
  - `available_to_start` = Yes — I was available and could have started
  - `district` = Colombo
  - `has_children` = No
  - `has_minimum_wage` = No — I would accept whatever is offered
  - `household_income` = Above LKR 200,000
  - `household_size` = 5.0
  - `household_unemployed` = 1.0
  - `household_workers` = 3.0
  - `income_urgency` = Immediately — I need income as soon as possible
  - `main_obstacle_finding_work` = No work experience
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family
  - `willing_to_relocate` = Yes — to another province in Sri Lanka

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `active_search_4weeks` = Yes — I took active steps in the past four weeks
  - `activity_while_searching` = Taking additional education or training courses
  - `current_activity_status` = Recently finished education — have work already arranged
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help` = Advice on how to search for jobs
  - `ever_refused_job` = Yes
  - `has_job_to_return` = No — I do not currently have a job to return to
  - `job_search_duration` = 6 months to 1 year
  - `looking_while_absent` = Yes
  - `num_applications` = 15.0
  - `num_interviews` = 0.0
  - `past_edu_usefulness` = Somewhat useful — helps to some extent
  - `reason_refused_job` = No possibility for career advancement
  - `search_method_primary` = Online job ads (internet, social media)
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 18 – 21 years
  - `edu_min_for_decent_job` = A/L level
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `future_planning_orientation` = I have a very clear, specific plan and I am actively working toward it
  - `job_search_autonomy_orientation` = I have preferences but am flexible and will take good opportunities
  - `job_search_self_efficacy` = Very confident — I believe I will find suitable work
  - `knows_people_in_target_sector` = Yes — I know several people working in that field
  - `most_important_life_goal` = Having financial security or earning a lot
  - `most_useful_quality_for_job` = IT and digital skills
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `network_helpfulness` = Very helpful — I have received real leads and referrals
  - `social_support_job_search` = Very supported — people actively encourage and assist me

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-001 (Freelancer Of Web Design & Development); COURSE-009 (Information And Communication Technolory Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-035 (Secretary (Secretarial Practices)); COURSE-052 (Cisco Certified Network Associate); COURSE-049 (Business Managemant); COURSE-058 (Computer Based Accounting); COURSE-002 (PYTHON); COURSE-057 (Multimedia & Web Design); COURSE-008 (Computer Hardware Technician); COURSE-053 (Computer Applications Assistant)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; job_type_sought=Self-employment or starting a business; ideal_work_type=Start my own business; training_type_would_help=University degree; expected_highest_edu_e=Bachelor's degree; job_acceptance_conditions=Any job, provided it matches my level of qualification; main_obstacle_finding_work=No work experience; current_activity_status=Recently finished education — have work already arranged; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "This course teaches web development — directly within the respondent's stated target sector."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Course explicitly teaches freelancing, how to set up accounts (Fiverr) and how to develop a business — matching the respondent's desire to start their own business."
  - `job_type_sought` = Self-employment or starting a business — *relevance stated by the model:* "The course content (freelancing, earning domestically and internationally) aligns with self-employment goals."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Within this profile some respondents reported IT and digital skills as useful and some planned further education (descriptive group tendency)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Teaching web development, domain & hosting management, creating Fiverr and other accounts, and methods to earn locally and abroad." — source: COURSE-001
  - "Course duration and fee information present in the course text (3 months, fee LKR 20,000)." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business and seeks self-employment, this course's explicit focus on freelancing and setting up online earning channels may be directly useful for their stated goals." (hedged; based on: ideal_work_type = Start my own business, job_type_sought = Self-employment or starting a business, course fact = course teaches freelancing, Fiverr account setup and business development (COURSE-001))

**LLM's recommendation explanation (`why_recommended`):** "The course explicitly teaches web development plus practical freelancing/business setup (Fiverr, hosting, domain management), which directly overlaps the respondent's stated IT sector interest and desire to start their own business/self-employ."

**Uncertainties disclosed by the LLM:**
  - The course page lists a fee (20,000 LKR) and start date details; availability of specific intake dates or seats for this respondent is not confirmed here.
  - No explicit entry requirements or placement/earnings guarantees are stated in the course document.

**Limitations disclosed by the LLM:**
  - Course is promotional text from the catalogue; while it explicitly targets freelancing and business setup, outcomes (earnings, placement) are not guaranteed by the document.
  - Practical schedule (weekdays/weekends) and exact location are not detailed in the extracted text beyond promotional lines.

#### Rank 2: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "The diploma covers broad ICT topics (programming, databases, web programming, networks) that match the respondent's stated sector interest."
  - `training_type_would_help` = University degree — *relevance stated by the model:* "Respondent expressed interest in higher-level study; a National Diploma is a recognised formal ICT qualification and may align with further-education orientation."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Profile shows a tendency toward perceiving education as somewhat useful and mixed further-learning ambition (descriptive)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course includes System Analysis & Design, Software Programming, Database Systems, Web Programming, LAN, and workplace communication — it's a full-time weekday National Diploma." — source: COURSE-006
  - "Course aims to develop entrepreneurial abilities in addition to technical skills and maps to NVQ Competency Level 5." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent is currently in higher education and expects a bachelor's degree, a formal National Diploma with competency recognition may support their further-education orientation and provide technical depth in IT that could help their career/entrepreneurial plans." (hedged; based on: edu_status = Currently in higher education (degree or diploma), plans_further_edu = Yes, course fact = National Diploma provides Level 5 NVQ, covers core IT topics (COURSE-006))

**LLM's recommendation explanation (`why_recommended`):** "The diploma covers a wide set of ICT subjects the respondent named as their target sector. It also mentions developing entrepreneurial abilities, which complements their goal to start a business."

**Uncertainties disclosed by the LLM:**
  - Course is full-time on weekdays; respondent's current study/availability constraints and ability to commit full-time are not fully documented here (the course doc does not provide flexible scheduling info).
  - Entry requirements, exact timetable, fees and location are not detailed in the extracted text.

**Limitations disclosed by the LLM:**
  - The course is full-time; the respondent's current higher-education commitments may conflict depending on schedule — this is not resolved by the course document.
  - No explicit admission criteria or fee details provided in the course extract, so eligibility and cost are unknown.

#### Rank 3: `COURSE-073` — Java Programming With Software Applications Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "The course teaches programming — directly relevant to an IT sector interest."
  - `job_type_sought` = Self-employment or starting a business — *relevance stated by the model:* "Programming skills can support building software products or freelance development services for a self-employed path."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Profile contains respondents who view IT/digital skills as useful (descriptive)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Java programming course gives theoretical knowledge and job-oriented practical skills; it is a part-time weekend course." — source: COURSE-073

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is part-time on weekends, it may be easier to combine with the respondent's ongoing higher education or other commitments compared with full-time weekday courses." (hedged; based on: edu_status = Currently in higher education (degree or diploma), course fact = COURSE-073 is a part-time weekend course)
  - "Acquiring Java programming skills could support the respondent's plan to offer development services or build software for a business they might start." (hedged; based on: job_type_sought = Self-employment or starting a business, course fact = Java programming and applications development (COURSE-073))

**LLM's recommendation explanation (`why_recommended`):** "Provides practical programming skills in a part-time format that aligns with the respondent's IT interest and may be compatible with their studies while supporting self-employment ambitions."

**Uncertainties disclosed by the LLM:**
  - Specific syllabus depth, certification, and post-course support or placement are not described in detail in the course extract.
  - Exact schedule/times for weekend sessions and any entry requirements are not provided.

**Limitations disclosed by the LLM:**
  - While programming is relevant to IT and entrepreneurship, the course document does not promise business-startup training or freelancing-specific modules.
  - No explicit mention of fees or accreditation level beyond course description.

#### Rank 4: `COURSE-002` — PYTHON

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Python programming is a core IT skill relevant to the respondent's stated sector interest."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Profile shows some orientation toward acquiring further education and valuing IT/digital skills (descriptive)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Catalogue card indicates a part-time Python course, 3 months duration, 20 students capacity; text: 'Python මුල සිට ඉගෙන ගන්න' (learn Python from scratch)." — source: COURSE-002

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent is active in online job search and values IT skills, a short part-time Python course may quickly build marketable technical skills useful for freelance or entry-level IT roles." (hedged; based on: search_method_primary = Online job ads (internet, social media), most_useful_quality_for_job = IT and digital skills, course fact = COURSE-002 is a short (3-month) part-time Python course)

**LLM's recommendation explanation (`why_recommended`):** "Short, part-time Python training teaches a core programming skill directly relevant to IT sector interests and to common freelance/entry-level roles."

**Uncertainties disclosed by the LLM:**
  - Some parts of the catalogue card text were unclear in the extract; full syllabus, fee, and schedule details are not fully readable in the provided document.
  - No explicit statement about entrepreneurship or freelancing content is included in the visible text.

**Limitations disclosed by the LLM:**
  - Catalogue card has remaining unreadable lines; this creates uncertainty about exact content and logistics.
  - No explicit entry requirements, accreditation level or post-course support are provided in the extracted text.

#### Rank 5: `COURSE-057` — Multimedia & Web Design

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Web and multimedia design are part of the IT/communications sector the respondent named."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Multimedia/web design skills can support freelancing or running a small digital services business."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Profile shows some respondents value IT/digital skills and further training (descriptive)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course described as 'Computer Multimedia Designing', part-time on weekends, practical job-oriented content." — source: COURSE-057

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is part-time on weekends, it may be practical to attend alongside the respondent's ongoing studies." (hedged; based on: edu_status = Currently in higher education (degree or diploma), course fact = COURSE-057 is part-time and held on weekends)
  - "Multimedia and web design skills could be useful for the respondent if they pursue freelance work or start a small digital services business, given their self-employment interest." (hedged; based on: ideal_work_type = Start my own business, course fact = COURSE-057 teaches multimedia & web design)

**LLM's recommendation explanation (`why_recommended`):** "Provides practical web/multimedia design skills in a part-time format that map to the respondent's IT sector interest and potential freelancing/entrepreneurial objectives."

**Uncertainties disclosed by the LLM:**
  - No detailed syllabus, fees, location or accreditation specifics are given in the extract.
  - Course outcome claims (income, placement) are not specified.

**Limitations disclosed by the LLM:**
  - Course description is high-level and does not explicitly include business-startup modules or freelancing platform guidance.
  - Schedule and entry criteria are not detailed beyond 'part time, weekends'.


---

## 14. `nysc-2e8a4c77-f611-4fff-9da8-9161a3f0f368` (Branch E) {#14-nysc-2e8a4c77-f611-4fff-9da8-9161a3f0f368}

**Selection rationale (why this respondent was chosen for the batch):** E profile 1, Personal services/beauty sector

### Frozen profile membership(s)

- `E_learning_orientation` — Profile 1: "High perceived education utility and strong learning ambition" (dimension: Education usefulness and further-learning orientation)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `desire_for_work` = Yes
  - `expected_highest_edu_e` = Post-graduate degree
  - `ideal_sector` = Personal services (beauty, fitness, wellness)
  - `ideal_work_type` = Start my own business
  - `job_acceptance_conditions` = Any job, provided it pays well enough
  - `job_type_sought` = Professional work (law, medicine, engineering, etc.)
  - `plans_further_edu` = Yes
  - `training_type_would_help` = Entrepreneurship training to start own business

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Small town
  - `available_to_start` = Yes — I was available and could have started
  - `district` = Kurunegala
  - `has_children` = No
  - `has_minimum_wage` = Yes — there is a minimum I would not go below
  - `household_income` = LKR 60,000 – 120,000
  - `household_size` = 5.0
  - `household_unemployed` = 0.0
  - `household_workers` = 3.0
  - `income_urgency` = Immediately — I need income as soon as possible
  - `main_obstacle_finding_work` = Not enough jobs available in this area
  - `minimum_wage_band` = LKR 50,000 – 75,000
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family
  - `willing_to_relocate` = No — I would not move

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `active_search_4weeks` = Yes — I took active steps in the past four weeks
  - `activity_while_searching` = Planning to start my own business
  - `current_activity_status` = Recently finished education — plan to start looking for work
  - `edu_status` = Currently in secondary education (O/L or A/L)
  - `employment_service_help` = No — none at all
  - `ever_refused_job` = No
  - `job_search_duration` = More than 1 year
  - `num_applications` = 7.0
  - `num_interviews` = 7.0
  - `past_edu_usefulness` = Very useful — directly relevant, employers value it
  - `search_method_primary` = Looking for resources to start own business
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 18 – 21 years
  - `edu_min_for_decent_job` = Education level doesn't matter much
  - `employment_network_quality` = No — I have no one I could call on
  - `future_planning_orientation` = I have a general direction but no specific steps yet
  - `job_search_autonomy_orientation` = I have preferences but am flexible and will take good opportunities
  - `job_search_self_efficacy` = Not confident at all — I feel quite hopeless about it
  - `knows_people_in_target_sector` = Yes — I know several people working in that field
  - `most_important_life_goal` = Finding purpose and meaning in life
  - `most_useful_quality_for_job` = IT and digital skills
  - `move_reason` = For education or training
  - `moved_from_origin` = No — I moved from somewhere else
  - `network_helpfulness` = Not helpful at all — I cannot use my connections for this
  - `social_support_job_search` = Not supported at all — I face this largely alone

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-065 (Engineering Draughtsmanship); COURSE-014 (Hair Dresser); COURSE-049 (Business Managemant); COURSE-069 (Hair Dresser); COURSE-007 (Professional Cookery); COURSE-048 (Bridal Dresser); COURSE-004 (Professional English); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-010 (Beautician); COURSE-046 (Beautician); COURSE-066 (Professional English); COURSE-082 (Secretary (Secretarial Practices)); COURSE-064 (Electrician); COURSE-071 (Human Recources Management); COURSE-025 (Electrician)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Personal services (beauty, fitness, wellness); job_type_sought=Professional work (law, medicine, engineering, etc.); ideal_work_type=Start my own business; training_type_would_help=Entrepreneurship training to start own business; expected_highest_edu_e=Post-graduate degree; job_acceptance_conditions=Any job, provided it pays well enough; main_obstacle_finding_work=Not enough jobs available in this area; current_activity_status=Recently finished education — plan to start looking for work; edu_status=Currently in secondary education (O/L or A/L); [sector-vocabulary expansion terms: bridal, hair]

#### Rank 1: `COURSE-049` — Business Managemant

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS WITH CAUTION
  - `activity_while_searching` (EDUCATION_AND_EXPERIENCE_CONTEXT, position 3): PASS WITH CAUTION — experience/background variable given preference-like framing as a secondary citation

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `training_type_would_help` = Entrepreneurship training to start own business — *relevance stated by the model:* "Respondent explicitly asked for entrepreneurship training to start their own business; this course teaches business/management content that plausibly supports that aim."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent stated they want to start their own business; business management content aligns with that stated goal."
  - `activity_while_searching` = Planning to start my own business — *relevance stated by the model:* "Respondent is already planning to start a business, so a business-management course may be directly relevant to that plan."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p1`, role=supporting_context_only: "Profile shows high perceived education utility and strong learning ambition (label: High perceived education utility and strong learning ambition)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course name: Business Managemant; Course will give theoretical knowledge as well as job oriented practical skills; part time course held on weekends." — source: COURSE-049

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent stated they want to start their own business and explicitly requested entrepreneurship training, this Business Management course may support their stated intention to develop managerial and entrepreneurial skills." (hedged; based on: training_type_would_help = Entrepreneurship training to start own business, ideal_work_type = Start my own business, COURSE-049 text describing Business Management content and entrepreneurial objective)
  - "Because the course is described as part-time and held on weekends, it may be easier to attend while managing other short-term commitments or job-search activities." (hedged; based on: COURSE-049: part time course held on weekends, Feasibility context: respondent indicated available_to_start = Yes and income_urgency = Immediately)

**LLM's recommendation explanation (`why_recommended`):** "The respondent explicitly requested entrepreneurship training and wants to start their own business; this Business Management course explicitly teaches business/management topics and is framed to develop entrepreneurial abilities, so it directly aligns with the respondent's stated content need."

**Uncertainties disclosed by the LLM:**
  - The course document does not specify exact location or fees; the respondent is unwilling to relocate, so local availability matters but is not documented here.
  - The course description is general (no detailed syllabus or assessed learning outcomes beyond a high-level statement).

**Limitations disclosed by the LLM:**
  - Location and fee information are not provided in the course document.
  - No explicit entry requirements or certification outcomes beyond a general statement are listed for this specific Business Management card.

#### Rank 2: `COURSE-046` — Beautician (part-time, weekends)

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Personal services (beauty, fitness, wellness) — *relevance stated by the model:* "Respondent explicitly named personal services (beauty, fitness, wellness) as their ideal sector; Beautician course content directly matches that sector."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent wants to start their own business; beautician skills are commonly used to open salons or offer independent personal-services businesses."
  - `activity_while_searching` = Planning to start my own business — *relevance stated by the model:* "Respondent is planning business activity in this area, so vocational beauty training may be practical for that plan."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p1`, role=supporting_context_only: "Profile shows strong learning ambition and plans for further education."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Beautician: course overview includes facial, manicure, pedicure, makeup, flower bouquets & bridal dressing; described as part time course held on weekends." — source: COURSE-046

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent named the personal services sector (beauty) as their ideal sector, the Beautician course content may directly provide the technical skills they want to offer in their own business." (hedged; based on: ideal_sector = Personal services (beauty, fitness, wellness), COURSE-046 course overview listing core beautician skills)
  - "Because this version of the Beautician course is part-time on weekends, it may be easier for the respondent to combine training with other short-term income-earning efforts or continuing schooling." (hedged; based on: COURSE-046: part time, weekends, Feasibility context: respondent currently in secondary education and available_to_start = Yes)

**LLM's recommendation explanation (`why_recommended`):** "The respondent explicitly selected personal services (beauty) and wants to start a business; the Beautician course teaches directly relevant salon/beauty skills and is framed to develop entrepreneurial abilities."

**Uncertainties disclosed by the LLM:**
  - Exact course location, fees, and certification details beyond the brief description are not provided in the document.
  - The respondent indicated they are currently in secondary education; the document does not state whether the course has age or prior-education entry requirements.

**Limitations disclosed by the LLM:**
  - Location and fee information are not included in the course text.
  - Certification level is stated for some beautician records but may vary by instance; verify which exact offering applies locally.

#### Rank 3: `COURSE-069` — Hair Dresser (part-time, weekends)

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Personal services (beauty, fitness, wellness) — *relevance stated by the model:* "Hairdressing is a core activity within the respondent's named ideal sector (personal services/beauty)."
  - `training_type_would_help` = Entrepreneurship training to start own business — *relevance stated by the model:* "Respondent asked for entrepreneurship training; vocational hairdressing skills can be combined with entrepreneurship to run a salon or freelance service."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p1`, role=supporting_context_only: "Profile tends to plan further education and values education usefulness."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Hair Dresser: course provides theoretical knowledge and job-oriented practical skills; described as a part time course held on weekends." — source: COURSE-069

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent selected personal services and wants to start a business, a hairdressing course may supply practical, revenue-generating skills useful for launching a salon or freelance hair-styling service." (hedged; based on: ideal_sector = Personal services (beauty, fitness, wellness), COURSE-069 description of hairdressing practical skills)

**LLM's recommendation explanation (`why_recommended`):** "Hairdressing is squarely within the respondent's stated sector interest and is a commonly entrepreneurial skill for starting a personal-services business; the course is explicitly practical and framed toward employment/entrepreneurial ability."

**Uncertainties disclosed by the LLM:**
  - The course document does not state location, fee, or exact certification level for this offering.
  - The respondent is unwilling to relocate; local availability is unknown from the course text.

**Limitations disclosed by the LLM:**
  - No explicit entry requirements are listed in the course text.
  - Local scheduling beyond 'weekends' is not detailed; check with the provider on local delivery in Kurunegala.

#### Rank 4: `COURSE-048` — Bridal Dresser (part-time, weekends)

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Personal services (beauty, fitness, wellness) — *relevance stated by the model:* "Bridal dressing is a specialized skill within the beauty/personal services sector the respondent named."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Bridal dressing skills can be packaged as a niche entrepreneurial service (e.g., bridal makeup/dressing business)."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p1`, role=supporting_context_only: "Profile members show strong orientation to further learning and view education as useful."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Bridal Dresser: will give theoretical knowledge as well as job oriented practical skills; part time course held on weekends; framed to develop entrepreneurial abilities." — source: COURSE-048

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent aims to start a business in personal services, bridal-dressing training may provide a marketable niche skillset supportive of that entrepreneurial plan." (hedged; based on: ideal_work_type = Start my own business, ideal_sector = Personal services (beauty, fitness, wellness), COURSE-048 description of bridal-dressing practical skills)

**LLM's recommendation explanation (`why_recommended`):** "The respondent's stated sector interest (beauty/personal services) and entrepreneurial aim align with the Bridal Dresser course content, which teaches specialized beauty services that can be commercialized."

**Uncertainties disclosed by the LLM:**
  - Course location, fees, and certification details are not provided in the document.
  - No explicit statement in the course text about market linkage or job placement; entrepreneurial outcomes are implied but not guaranteed.

**Limitations disclosed by the LLM:**
  - Local availability in Kurunegala is not documented; respondent is unwilling to relocate so local delivery matters.
  - Entry requirements are not specified in the course document.


---

## 15. `nysc-3258dc18-84da-4092-82af-cfb84352536e` (Branch E) {#15-nysc-3258dc18-84da-4092-82af-cfb84352536e}

**Selection rationale (why this respondent was chosen for the batch):** E profile 2, Manufacturing, wage barrier

### Frozen profile membership(s)

- `E_learning_orientation` — Profile 2: "Moderate perceived utility and mixed learning ambition" (dimension: Education usefulness and further-learning orientation)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `desire_for_work` = Yes
  - `expected_highest_edu_e` = Diploma
  - `ideal_sector` = Manufacturing or production
  - `ideal_work_type` = Work for a local private Sri Lankan company
  - `job_acceptance_conditions` = Any job, provided it pays well enough
  - `job_type_sought` = Manual or trade work
  - `plans_further_edu` = Do not know yet
  - `training_type_would_help` = Other type of training

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Large city
  - `available_to_start` = Yes — I was available and could have started
  - `district` = Hambantota
  - `has_children` = No
  - `has_minimum_wage` = Yes — there is a minimum I would not go below
  - `household_income` = LKR 60,000 – 120,000
  - `household_size` = 4.0
  - `household_unemployed` = 1.0
  - `household_workers` = 1.0
  - `income_urgency` = Immediately — I need income as soon as possible
  - `main_obstacle_finding_work` = Wages in available jobs are too low
  - `minimum_wage_band` = LKR 75,000 – 120,000
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family
  - `willing_to_relocate` = No — I would not move

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `active_search_4weeks` = Yes — I took active steps in the past four weeks
  - `activity_while_searching` = Staying at home and focusing on the job search
  - `current_activity_status` = Not working — looking for work or trying to set up a business
  - `edu_end_year` = 2023.0
  - `edu_status` = I have completed my education and am not currently studying
  - `employment_service_help` = Advice on how to search for jobs
  - `ever_refused_job` = No
  - `highest_edu_completed` = A/L level (Grade 12–13)
  - `job_search_duration` = More than 1 year
  - `num_applications` = 5.0
  - `num_interviews` = 1.0
  - `past_edu_usefulness` = Somewhat useful — helps to some extent
  - `search_method_primary` = Attending job fairs
  - `spell1_activity` = Looking for work / unemployed
  - `spell1_is_current` = Yes — this is still my current situation
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 26 – 29 years
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `future_planning_orientation` = I have a general direction but no specific steps yet
  - `job_search_autonomy_orientation` = I am mainly looking for any job that will provide income
  - `job_search_self_efficacy` = Fairly confident — I think I will, though it may take time
  - `knows_people_in_target_sector` = Not really — only very distant or indirect connections
  - `most_important_life_goal` = Having financial security or earning a lot
  - `most_useful_quality_for_job` = Ambition and drive
  - `move_reason` = To accompany family
  - `moved_from_origin` = No — I moved from somewhere else
  - `network_helpfulness` = Not very helpful — my network has not opened many doors
  - `social_support_job_search` = Minimally supported — most people are indifferent

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-012 (Refrigeration & Air Conditioning Technician); COURSE-034 (Refrigeration & Air Conditioning Technician); COURSE-031 (National Diploma In Television Program Production); COURSE-028 (Lapiderist (Gem Cutting)); COURSE-005 (Automobile Mechanic); COURSE-029 (Mobile Phone Repair Technician); COURSE-030 (Motorcycle Mechanic); COURSE-077 (Mobile Phone Repair Technician); COURSE-040 (Automobile Mechanic); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-049 (Business Managemant); COURSE-078 (Motorcycle Mechanic); COURSE-042 (Automobile Electrician); COURSE-064 (Electrician); COURSE-081 (Radio, TV & Allied Equipment Repairer)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Manufacturing or production; job_type_sought=Manual or trade work; ideal_work_type=Work for a local private Sri Lankan company; training_type_would_help=Other type of training; expected_highest_edu_e=Diploma; job_acceptance_conditions=Any job, provided it pays well enough; main_obstacle_finding_work=Wages in available jobs are too low; current_activity_status=Not working — looking for work or trying to set up a business; highest_edu_completed=A/L level (Grade 12–13); edu_status=I have completed my education and am not currently studying; [sector-vocabulary expansion terms: air conditioning, automobile, electrical, electronics, english, gem cutting, mechanic, mobile phone, motorcycle, programming, refrigeration, sinhala]

#### Rank 1: `COURSE-005` — Automobile Mechanic

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Automobile mechanic skills are typically classed as trade/technical skills relevant to manufacturing, repair, and production sectors."
  - `job_type_sought` = Manual or trade work — *relevance stated by the model:* "Automobile Mechanic is a manual/trade vocation matching the respondent's stated job-type preference."
  - `ideal_work_type` = Work for a local private Sri Lankan company — *relevance stated by the model:* "Automobile mechanics commonly find employment with local private garages or companies, aligning with the respondent's preferred employer type."
  - `available_to_start` = Yes — I was available and could have started — *relevance stated by the model:* "Indicates readiness to undertake training (course is full-time weekdays as documented)."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Within this profile, attending job fairs and preference for vocational/technical work appear among some members; this is cited only as supporting context, not a fact about the individual."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course will give theoretical knowledge and job-oriented practical skills necessary for employment and higher education." — source: COURSE-005
  - "This is a full time course which will be held on weekdays." — source: COURSE-005
  - "Topics include engine, transmission, steering, braking, electrical systems (petrol and diesel engines etc.)." — source: COURSE-005
  - "Completing this course can achieve Competency Level 4 under NVQ standards." — source: COURSE-005

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent seeks manual/trade work and named manufacturing/production as an ideal sector, this automobile mechanic course may directly support those stated employment intentions." (hedged; based on: job_type_sought = Manual or trade work, ideal_sector = Manufacturing or production, course_fact: Automobile Mechanic teaches trade/technical mechanical skills (COURSE-005))
  - "The respondent's readiness to start (available_to_start = Yes) may make a full-time weekday course feasible, but this is only a possibility — personal schedule details beyond availability are not provided." (hedged; based on: available_to_start = Yes — I was available and could have started, course_fact: full time weekday delivery (COURSE-005))

**LLM's recommendation explanation (`why_recommended`):** "Direct match: respondent explicitly seeks manual/trade work in manufacturing/production and this course teaches practical mechanical trade skills (engine, transmission, electrical systems) commonly used in local private garages or manufacturing-related maintenance roles."

**Uncertainties disclosed by the LLM:**
  - Course location and whether it is offered in Hambantota (respondent's district) are not stated in the course document.
  - Exact entry requirements, fees, course duration specifics beyond 'full time' and NVQ level are not fully detailed in the extracted text.

**Limitations disclosed by the LLM:**
  - The course document states full-time weekday delivery; respondent's broader scheduling constraints beyond 'available_to_start' are unknown.
  - No explicit information about placements, local employer links, or guaranteed job outcomes is provided in the course text.

#### Rank 2: `COURSE-030` — Motorcycle Mechanic

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `job_type_sought` = Manual or trade work — *relevance stated by the model:* "Motorcycle Mechanic is a hands-on trade occupation matching the respondent's stated job-type preference."
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Repair and vehicle maintenance skills are relevant to production/repair sectors and local private employers."
  - `ideal_work_type` = Work for a local private Sri Lankan company — *relevance stated by the model:* "Motorcycle mechanics often work in local private workshops, consistent with the respondent's employer preference."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Profile shows some members preferring technical/vocational work; cited only as background supporting relevance of trade courses."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Motorcycle Mechanic course provides theoretical and job-oriented practical skills necessary for employment and higher education." — source: COURSE-030
  - "This is a full time course which will be held on weekdays." — source: COURSE-030
  - "Completing this course, participants can achieve Competency Level 3 or 4 under NVQ standards." — source: COURSE-030

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent is seeking manual/trade work and wants to work for a local private company, motorcycle mechanic training may be a practical route to local workshop employment or small private-sector repair roles." (hedged; based on: job_type_sought = Manual or trade work, ideal_work_type = Work for a local private Sri Lankan company, course_fact: Motorcycle Mechanic teaches practical repair skills (COURSE-030))

**LLM's recommendation explanation (`why_recommended`):** "Strong content fit: the course delivers hands-on mechanical repair skills that align with the respondent's stated desire for manual/trade employment in a local private setting."

**Uncertainties disclosed by the LLM:**
  - Course location relative to the respondent (Hambantota) is not specified in the course document.
  - Course schedule is full-time weekdays per the document; how that aligns with the respondent's specific daily obligations beyond availability is unknown.

**Limitations disclosed by the LLM:**
  - No explicit fee, exact duration, or entry requirement details are present in the course text.
  - Local employer connections or placement support are not documented in the course excerpt.

#### Rank 3: `COURSE-064` — Electrician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `job_type_sought` = Manual or trade work — *relevance stated by the model:* "Electrician is a recognized manual/trade occupation matching the respondent's stated job-type preference."
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Industrial and domestic electrical installation and maintenance skills are relevant to manufacturing, production, and repair sectors."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Profile-level tendency toward vocational/technical options is present among some members; this is only contextual background."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Electrician course covers domestic and industrial electrical installation, repair and service of motors/generators, PLC, and security solutions." — source: COURSE-064
  - "This is a part time course which will be held on weekends (document states part-time weekends)." — source: COURSE-064

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent seeks manual/trade work in manufacturing/production, electrician training may equip them with skills useful for industrial installation and maintenance roles." (hedged; based on: job_type_sought = Manual or trade work, ideal_sector = Manufacturing or production, course_fact: Electrician includes industrial electrical installation and motor control (COURSE-064))
  - "The course's part-time weekend format may better suit respondents who need to balance other commitments or prefer non-weekday training, though this respondent's specific weekly constraints beyond availability are not detailed." (hedged; based on: course_fact: part time weekends (COURSE-064), available_to_start = Yes — I was available and could have started)

**LLM's recommendation explanation (`why_recommended`):** "Good content fit: electrician skills (domestic and industrial installations, motor control, PLC) match the respondent's expressed interest in manual/trade work and relevance to production/manufacturing settings; weekend delivery may improve feasibility."

**Uncertainties disclosed by the LLM:**
  - No explicit course location or whether it runs near Hambantota is provided.
  - Exact entry requirements, fees, and course length are not shown in the extracted text.

**Limitations disclosed by the LLM:**
  - While part-time weekends are documented, practical details (hours per weekend, total duration) are missing from the course extract.
  - No employer placement or local hiring links are documented in the course text.

#### Rank 4: `COURSE-012` — Refrigeration & Air Conditioning Technician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course is described as part time and held on weekends (COURSE-012 explicitly sta...' has low word-overlap (39%) with the retrieved COURSE-012 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `job_type_sought` = Manual or trade work — *relevance stated by the model:* "Refrigeration & A/C technician is a hands-on trade role aligned with manual/trade work preferences."
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Refrigeration and A/C skills are relevant to manufacturing (cold chain, plant maintenance) and repair/service sectors."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Profile includes members who view vocational training as useful; used only as supporting context."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers repair of refrigerators, deep freezers, display units, coolers; repair of window and split type A/C; operate and maintain central A/C systems; prepare estimates." — source: COURSE-012
  - "Course is described as part time and held on weekends (COURSE-012 explicitly states part time weekends in one variant and full time weekdays in another retrieved variant — validated documents include both COURSE-012 and COURSE-034 which differ on part/full-time)." — source: COURSE-012

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent seeks manual/trade employment in production-related sectors, refrigeration/A/C technician skills may be applicable to maintenance and service roles in local private companies or manufacturing facilities." (hedged; based on: job_type_sought = Manual or trade work, ideal_sector = Manufacturing or production, course_fact: refrigeration & A/C practical repair and maintenance skills (COURSE-012))

**LLM's recommendation explanation (`why_recommended`):** "Relevant trade skills: the course teaches practical refrigeration and A/C repair and maintenance skills that align with the respondent's stated preference for manual/trade work and potential roles in manufacturing/production or local private service businesses."

**Uncertainties disclosed by the LLM:**
  - There is a discrepancy across retrieved documents about whether this specific course is part-time (weekends) or full-time (weekdays) — the two retrieved documents (COURSE-012 and COURSE-034) present different schedules.
  - No course location or fee information is provided.

**Limitations disclosed by the LLM:**
  - Because of conflicting schedule information across retrieved course documents, the respondent should verify the actual delivery format and timing before applying.
  - No explicit statement about training placements, nearby site availability, or employer links is present.

#### Rank 5: `COURSE-029` — Mobile Phone Repair Technician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `job_type_sought` = Manual or trade work — *relevance stated by the model:* "Mobile phone repair is a practical trade skill consistent with the respondent's stated job-type preference."
  - `ideal_work_type` = Work for a local private Sri Lankan company — *relevance stated by the model:* "Mobile phone repair technicians commonly find work in local private repair shops or small businesses."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Some members of this profile show interest in hands-on vocational training; used only as background context."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Mobile Phone Repairing Craftsman course gives theoretical knowledge and job-oriented practical skills necessary for employment and higher education." — source: COURSE-029
  - "This is a full time course which will be held on weekdays (COURSE-029)." — source: COURSE-029
  - "Completing this course can achieve Competency Level 4 under NVQ standards." — source: COURSE-029

**[LLM INFERENCE] Contextual inferences made:**
  - "Given the respondent's preference for manual/trade work and local private employment, mobile phone repair training may offer a route to small-business or workshop employment or self-employment locally." (hedged; based on: job_type_sought = Manual or trade work, ideal_work_type = Work for a local private Sri Lankan company, course_fact: Mobile Phone Repair Technician teaches practical repair skills (COURSE-029))

**LLM's recommendation explanation (`why_recommended`):** "Direct content fit: course offers practical repair skills for a hands-on trade that can be used in local private repair businesses or small enterprises, aligning with the respondent's stated preferences."

**Uncertainties disclosed by the LLM:**
  - No explicit course location or fee information is included in the course document.
  - Full-time weekday delivery may affect feasibility depending on the respondent's unreported daily constraints beyond availability.

**Limitations disclosed by the LLM:**
  - The course text does not specify whether training or job opportunities exist specifically in Hambantota.
  - No explicit placement or employer-network information is provided.


---

## 16. `nysc-cab6cf5f-13dc-4f50-9d5a-b24f266dc279` (Branch E) {#16-nysc-cab6cf5f-13dc-4f50-9d5a-b24f266dc279}

**Selection rationale (why this respondent was chosen for the batch):** E profile 2, sector unsure but job_type/training signals present — partial-weak test

### Frozen profile membership(s)

- `E_learning_orientation` — Profile 2: "Moderate perceived utility and mixed learning ambition" (dimension: Education usefulness and further-learning orientation)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `desire_for_work` = Yes
  - `expected_highest_edu_e` = Post-graduate degree
  - `ideal_sector` = Not sure
  - `ideal_work_type` = Work for a multinational or large private company
  - `job_acceptance_conditions` = Only a job that is stable, well paid, AND matches my qualifications
  - `job_type_sought` = Professional work (law, medicine, engineering, etc.)
  - `plans_further_edu` = Yes
  - `training_type_would_help` = Professional/technical certification

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Small town
  - `available_to_start` = Yes — I was available and could have started
  - `district` = Kalutara
  - `has_children` = No
  - `has_minimum_wage` = Yes — there is a minimum I would not go below
  - `household_income` = Above LKR 200,000
  - `household_size` = 5.0
  - `household_unemployed` = 1.0
  - `household_workers` = 3.0
  - `income_urgency` = Immediately — I need income as soon as possible
  - `main_obstacle_finding_work` = Working conditions in available jobs are poor
  - `minimum_wage_band` = LKR 75,000 – 120,000
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family
  - `willing_to_relocate` = Yes — to another country

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `active_search_4weeks` = Yes — I took active steps in the past four weeks
  - `activity_while_searching` = Taking additional education or training courses
  - `current_activity_status` = Recently finished education — plan to start looking for work
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help` = Advice on how to search for jobs
  - `ever_refused_job` = Yes
  - `job_search_duration` = Less than 1 week
  - `num_applications` = 80.0
  - `num_interviews` = 2.0
  - `past_edu_usefulness` = Somewhat useful — helps to some extent
  - `reason_refused_job` = No possibility for career advancement
  - `search_method_primary` = Online job ads (internet, social media)
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `edu_min_for_decent_job` = Vocational training or NVQ
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `future_planning_orientation` = I know I want something different but do not know how to get there
  - `job_search_autonomy_orientation` = I am looking specifically for work I genuinely want to do
  - `job_search_self_efficacy` = Fairly confident — I think I will, though it may take time
  - `knows_people_in_target_sector` = Not really — only very distant or indirect connections
  - `most_important_life_goal` = Building self-confidence and personal fulfilment
  - `most_useful_quality_for_job` = Communication and interpersonal skills
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `network_helpfulness` = Not very helpful — my network has not opened many doors
  - `social_support_job_search` = Very supported — people actively encourage and assist me

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-065 (Engineering Draughtsmanship); COURSE-031 (National Diploma In Television Program Production); COURSE-007 (Professional Cookery); COURSE-004 (Professional English); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-066 (Professional English); COURSE-082 (Secretary (Secretarial Practices)); COURSE-071 (Human Recources Management); COURSE-010 (Beautician); COURSE-011 (Baker); COURSE-033 (Plumber); COURSE-020 (Landscape Development Assistant); COURSE-021 (Automobile Electrician); COURSE-030 (Motorcycle Mechanic); COURSE-037 (Tailor)

**Retrieval query summary (used to search, not shown to the model as such):** job_type_sought=Professional work (law, medicine, engineering, etc.); ideal_work_type=Work for a multinational or large private company; training_type_would_help=Professional/technical certification; expected_highest_edu_e=Post-graduate degree; job_acceptance_conditions=Only a job that is stable, well paid, AND matches my qualifications; main_obstacle_finding_work=Working conditions in available jobs are poor; current_activity_status=Recently finished education — plan to start looking for work; edu_status=Currently in higher education (degree or diploma)

#### Rank 1: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `job_type_sought` = Professional work (law, medicine, engineering, etc.) — *relevance stated by the model:* "Respondent seeks professional work; ICT is a recognised professional/technical field that commonly leads to roles in companies the respondent aims for."
  - `training_type_would_help` = Professional/technical certification — *relevance stated by the model:* "Course is a National Diploma (technical certification) which directly matches the respondent's stated preferred type of training."
  - `ideal_work_type` = Work for a multinational or large private company — *relevance stated by the model:* "ICT skills are frequently required by multinational or large private companies, aligning with the respondent's workplace preference."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Within this profile many respondents view IT and digital skills as useful and some seek technical work"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course includes modules such as System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network, Software Testing" — source: COURSE-006
  - "This is a full time course held on weekdays and awards Competency Level 5 under NVQ standards" — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent asked for professional/technical certification and wants to work in multinational or large private companies, this ICT diploma may directly support that stated ambition." (hedged; based on: training_type_would_help = Professional/technical certification, ideal_work_type = Work for a multinational or large private company)
  - "Because the course lists programming, databases and networking modules, it may be useful across a range of professional ICT roles the respondent might target." (hedged; based on: course modules listed in COURSE-006)

**LLM's recommendation explanation (`why_recommended`):** "The National Diploma in ICT is a technical/professional certification whose content (programming, databases, networking) plausibly prepares a candidate for professional roles in companies like the respondent described. The respondent explicitly asked for professional/technical certification and expressed interest in professional work and multinational employers."

**Uncertainties disclosed by the LLM:**
  - The course document does not state explicit entry requirements for applicants.
  - The course is full-time on weekdays; respondent availability or preference for part-time/weekend study is not specified beyond general availability to start.

**Limitations disclosed by the LLM:**
  - No fee, exact schedule details beyond 'full time/weekdays', or location of delivery are provided in the course document.
  - Completion outcomes (placement, guaranteed progression to specific employers) are not documented in the course text.

#### Rank 2: `COURSE-065` — Engineering Draughtsmanship

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `job_type_sought` = Professional work (law, medicine, engineering, etc.) — *relevance stated by the model:* "Respondent explicitly included 'engineering' in the list of professional work types sought; draughtsmanship is an engineering-related technical skill."
  - `training_type_would_help` = Professional/technical certification — *relevance stated by the model:* "Course is described as providing theoretical knowledge and job-oriented practical skills consistent with professional/technical certification."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Within this profile a portion of respondents selected engineering or technical work as a desired type of job"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Engineering Draughtsmanship gives theoretical knowledge and job-oriented practical skills and is a part time course held on weekends." — source: COURSE-065

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent named engineering as an example of professional work they seek, this engineering draughtsmanship course may be relevant for building technical skills aligned with that stated interest." (hedged; based on: job_type_sought = Professional work (law, medicine, engineering, etc.), course description in COURSE-065 referencing engineering draughtsmanship)
  - "Because the course is part-time on weekends, it may be easier to combine with the respondent's current higher-education status or other commitments compared with a full-time weekday programme." (hedged; based on: edu_status = Currently in higher education (degree or diploma), COURSE-065 stating 'part time course... held on weekends')

**LLM's recommendation explanation (`why_recommended`):** "Engineering Draughtsmanship aligns with the respondent's explicit inclusion of engineering among the professional job types they seek and matches their stated preference for professional/technical certification. It is also offered part-time on weekends, which could be practical while the respondent finishes higher education."

**Uncertainties disclosed by the LLM:**
  - The course document does not state specific entry requirements or qualification level (NVQ level) for this course.
  - No fee, exact location, or duration is provided beyond 'part time' and 'weekends'.

**Limitations disclosed by the LLM:**
  - Course description is brief and does not list exact competencies, software, or progression pathways to engineering degrees or employers.
  - It is not documented whether this course confers an NVQ or other nationally recognised certification.

#### Rank 3: `COURSE-066` — Professional English

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Work for a multinational or large private company — *relevance stated by the model:* "Working in multinational or large private companies often values strong English communication; improving professional English may support that stated workplace preference."
  - `most_useful_quality_for_job` = Communication and interpersonal skills — *relevance stated by the model:* "Respondent values communication skills; a Professional English course directly addresses language and communication ability."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "Within this profile communication and IT skills are among commonly cited useful qualities for jobs"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Professional English is an English language course giving theoretical knowledge and job-oriented practical skills; it is a part time course held on weekends (25 students)." — source: COURSE-066

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent prioritises communication skills and aims to work in multinational/large companies, improving professional English may support those ambitions by strengthening a skill the respondent values." (hedged; based on: most_useful_quality_for_job = Communication and interpersonal skills, ideal_work_type = Work for a multinational or large private company, COURSE-066 description)

**LLM's recommendation explanation (`why_recommended`):** "Professional English addresses the respondent's stated emphasis on communication skills and their aim to work in multinational or large private firms where professional English can be advantageous. The course is part-time on weekends, which may fit alongside finishing studies."

**Uncertainties disclosed by the LLM:**
  - The course document does not state specific proficiency outcomes, entry requirements, fees, or exact schedule beyond 'part time' and 'weekends'.
  - It is not clear whether the course awards a recognised certification that the respondent would count as a 'professional/technical certification'.

**Limitations disclosed by the LLM:**
  - Professional English alone is unlikely to fully qualify someone for a technical professional role; it is best seen as complementary to a technical qualification (e.g., ICT or engineering).
  - No placement or employer-connection information is given.

#### Rank 4: `COURSE-071` — Human Recources Management

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Work for a multinational or large private company — *relevance stated by the model:* "HR skills are relevant to professional roles in larger organisations the respondent wants to join."
  - `training_type_would_help` = Professional/technical certification — *relevance stated by the model:* "Course is presented as a part-time programme teaching HRM topics (recruitment, discipline management, labour law) which can be a professional certification area."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `E_learning_orientation_p2`, role=supporting_context_only: "This profile sometimes seeks professional or managerial type work and values training that is job-relevant"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers Introduction to Management and HRM, Recruitment/Selection, Discipline Management, Labour law and employee welfare; it is a part time weekend course." — source: COURSE-071

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants professional work in larger companies, HRM training could be relevant if they are considering business/people-management career tracks." (hedged; based on: ideal_work_type = Work for a multinational or large private company, COURSE-071 topics listed)
  - "Because the course is part-time on weekends, it may be practical to undertake while completing higher education or searching for work." (hedged; based on: edu_status = Currently in higher education (degree or diploma), COURSE-071 stated 'part time... weekends')

**LLM's recommendation explanation (`why_recommended`):** "Human Resources Management teaches professional topics used in large organisations and is offered part-time; it could be appropriate if the respondent is open to HR/management career paths within multinational or large private firms."

**Uncertainties disclosed by the LLM:**
  - Respondent did not state an explicit interest in HR as a field; recommendation relies on alignment with the broader goal of entering professional roles in large organisations.
  - Course document contains some unclear text and does not state certification level, fees, or exact duration.

**Limitations disclosed by the LLM:**
  - Because the respondent listed several professional fields (including engineering) and 'ideal_sector' was 'Not sure', HRM may be a less direct content match compared with ICT or engineering draughtsmanship.
  - No explicit NVQ or accredited certification level is documented in the course text; entry requirements and placement outcomes are not provided.


---

## 17. `nysc-04134b0d-f3fe-4a25-916c-ee106362e150` (Branch F) {#17-nysc-04134b0d-f3fe-4a25-916c-ee106362e150}

**Selection rationale (why this respondent was chosen for the batch):** F profile 1 (insecure), weak/unsure sector, professional occupational_class

### Frozen profile membership(s)

- `F_employment_security` — Profile 1: "Temporary/no-contract employment with uncertain security" (dimension: Employment security and formality)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `acceptance_conditions_search` = Only a job that was stable, well paid, AND matched my qualifications
  - `expected_highest_edu_f` = Post-graduate degree
  - `hopes_to_change_job` = Not sure
  - `ideal_sector` = Not sure
  - `ideal_work_type` = Not sure yet
  - `income_hours_preference` = Keep things the same as they are now
  - `plans_further_edu_f` = Yes

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `actual_hours_last_week` = 50.0
  - `area_type` = Large city
  - `district` = Colombo
  - `had_min_wage_during_search` = Yes
  - `has_children` = No
  - `household_income` = *[respondent selected "Prefer not to say"]*
  - `household_size` = 5.0
  - `household_unemployed` = 1.0
  - `household_workers` = 2.0
  - `monthly_income_band` = Below LKR 20,000
  - `obstacle_finding_this_job` = No major obstacles — the process was straightforward
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family
  - `usual_hours_per_week` = 40.0
  - `who_paid_training` = Myself or my family
  - `willing_to_relocate_f` = I have no strong preference

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `contract_satisfaction` = Satisfied — for another reason
  - `contract_type` = Written contract — temporary (under 12 months)
  - `current_activity_status` = Working for pay, profit, or family gain for at least one hour
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help_f` = No — none at all
  - `employment_status` = For an employer — for a salary or wage
  - `enterprise_location_type` = A fixed location — office, shop, factory, or site
  - `enterprise_registered` = Yes — it is registered
  - `enterprise_size` = 50 workers or more
  - `ever_refused_job_f` = Yes
  - `has_second_job` = No
  - `hours_below_normal` = No — I worked my normal hours or more
  - `interviews_before_hire` = 4.0
  - `job_recruitment_method` = Through a job advertisement (newspaper, internet, social media)
  - `job_security_12months` = Not likely — I doubt I will still have this job
  - `jobs_applied_before_hire` = 9.0
  - `occupational_class` = Professional work (doctor, lawyer, engineer, accountant, teacher, etc.)
  - `paid_taxes` = Yes
  - `past_edu_useful_for_job` = Somewhat useful — helps in some areas
  - `qualification_job_match` = Very well — my qualifications are central to this job
  - `reason_not_union` = I have never been approached to join
  - `reason_refused_job_f` = Waiting for a better offer
  - `received_training` = Yes
  - `registered_as_jobseeker` = No
  - `search_duration_before_hire` = 1 to 2 months
  - `sector_formality` = Fully formal — registered employer, written contract, statutory benefits
  - `training_duration` = 6 months to 1 year
  - `training_provider` = Other
  - `training_type_received` = Training in new technologies
  - `union_member` = No
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `competence_growth_at_work` = Yes — I am constantly learning and growing in this role
  - `edu_min_for_decent_job` = A/L level
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `gender_equality_at_work` = Equal opportunities for women and men
  - `insecurity_bothers` = Yes — it worries or stresses me
  - `job_satisfaction` = Somewhat unsatisfied
  - `most_important_life_goal` = Having leisure, freedom, and personal time
  - `most_useful_quality_for_job` = A good general education
  - `move_reason` = Other reason
  - `moved_from_origin` = No — I moved from somewhere else
  - `professional_network_growth` = Yes — significantly, I have built valuable professional relationships
  - `relatedness_at_work` = Very connected — genuinely part of the team and valued
  - `work_autonomy` = A great deal — real freedom in how I approach my work
  - `work_motivation_type` = I find the work genuinely interesting and meaningful in itself

### Recommendation status: **NO_DEFENSIBLE_RECOMMENDATION**

**Retrieved course candidates (15):** COURSE-031 (National Diploma In Television Program Production); COURSE-007 (Professional Cookery); COURSE-041 (Preschool Teacher (Early Childhood Development)); COURSE-004 (Professional English); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-066 (Professional English); COURSE-082 (Secretary (Secretarial Practices)); COURSE-034 (Refrigeration & Air Conditioning Technician); COURSE-012 (Refrigeration & Air Conditioning Technician); COURSE-010 (Beautician); COURSE-011 (Baker); COURSE-033 (Plumber); COURSE-020 (Landscape Development Assistant); COURSE-021 (Automobile Electrician); COURSE-030 (Motorcycle Mechanic)

**Retrieval query summary (used to search, not shown to the model as such):** expected_highest_edu_f=Post-graduate degree; obstacle_finding_this_job=No major obstacles — the process was straightforward; current_activity_status=Working for pay, profit, or family gain for at least one hour; employment_status=For an employer — for a salary or wage; occupational_class=Professional work (doctor, lawyer, engineer, accountant, teacher, etc.); qualification_job_match=Very well — my qualifications are central to this job; training_type_received=Training in new technologies; edu_status=Currently in higher education (degree or diploma)

**[LLM's saved reason for declining]:**

> The respondent did not state any direct preference for a study field, sector, or training topic (ideal_sector = Not sure; ideal_work_type = Not sure; no study_field_preference provided). Under the task's decision rules, direct-preference/intent answers are required to justify a programme's content/field match. Other information (education background, prior training in new technologies, or feasibility details) can support or refine a match but may not by themselves select programme content. Because no usable direct preference naming a field or sector is present, none of the retrieved NYSC course documents can be defensibly recommended as a content match for this respondent.

**Standard grounding audit on this decline:** PASS

**Evidence-category-discipline audit on this decline:** PASS WITH CAUTION
  - `training_type_received` (EDUCATION_AND_EXPERIENCE_CONTEXT): PASS WITH CAUTION — decline reason contains both a content/field-relevance judgement and the respondent's answer to 'training_type_received' (EDUCATION_AND_EXPERIENCE_CONTEXT); flagged for human review of whether that context-only fact improperly shaped the content judgement — co-occurrence is not proof of misuse


---

## 18. `nysc-4646cb19-0ac0-49ca-a00b-e2d8cb16b65e` (Branch F) {#18-nysc-4646cb19-0ac0-49ca-a00b-e2d8cb16b65e}

**Selection rationale (why this respondent was chosen for the batch):** F profile 2 (secure), weak/unsure sector

### Frozen profile membership(s)

- `F_employment_security` — Profile 2: "Predominantly permanent employment with stronger security" (dimension: Employment security and formality)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `acceptance_conditions_search` = Only a job that was stable, well paid, AND matched my qualifications
  - `expected_highest_edu_f` = Post-graduate degree
  - `hopes_to_change_job` = Not sure
  - `ideal_sector` = Not sure
  - `ideal_work_type` = Not sure yet
  - `income_hours_preference` = Keep things the same as they are now
  - `plans_further_edu_f` = Yes

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `actual_hours_last_week` = 40.0
  - `area_type` = Small town
  - `district` = Galle
  - `had_min_wage_during_search` = No — I would have accepted any wage
  - `has_children` = No
  - `household_income` = *[respondent selected "Prefer not to say"]*
  - `household_size` = 4.0
  - `household_unemployed` = 0.0
  - `household_workers` = 2.0
  - `monthly_income_band` = LKR 120,000 – 200,000
  - `obstacle_finding_this_job` = No work experience
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My regular job or business
  - `usual_hours_per_week` = 45.0
  - `willing_to_relocate_f` = I have no strong preference

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `contract_satisfaction` = Satisfied — it gives me the job security I need
  - `contract_type` = Written contract — permanent/unlimited
  - `current_activity_status` = Working for pay, profit, or family gain for at least one hour
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help_f` = No — none at all
  - `employment_status` = For an employer — for a salary or wage
  - `enterprise_location_type` = A fixed location — office, shop, factory, or site
  - `enterprise_registered` = Yes — it is registered
  - `enterprise_size` = Do not know
  - `ever_refused_job_f` = Yes
  - `has_second_job` = No
  - `hours_below_normal` = Yes — I worked fewer hours than normal
  - `interviews_before_hire` = 1.0
  - `job_recruitment_method` = Through a job advertisement (newspaper, internet, social media)
  - `job_security_12months` = Very likely — my job is secure
  - `jobs_applied_before_hire` = 1.0
  - `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.)
  - `paid_taxes` = Yes
  - `past_edu_useful_for_job` = Somewhat useful — helps in some areas
  - `qualification_job_match` = Very well — my qualifications are central to this job
  - `reason_below_normal_hours` = Other
  - `reason_not_union` = I have never thought about it
  - `reason_refused_job_f` = Waiting for a better offer
  - `received_training` = No
  - `registered_as_jobseeker` = No
  - `search_duration_before_hire` = 3 to 6 months
  - `sector_formality` = Fully formal — registered employer, written contract, statutory benefits
  - `union_member` = No
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `competence_growth_at_work` = Yes — I am constantly learning and growing in this role
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `gender_equality_at_work` = Equal opportunities for women and men
  - `job_satisfaction` = Somewhat satisfied
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = A good general education
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `professional_network_growth` = Yes — significantly, I have built valuable professional relationships
  - `relatedness_at_work` = Very connected — genuinely part of the team and valued
  - `work_autonomy` = A great deal — real freedom in how I approach my work
  - `work_motivation_type` = I find the work genuinely interesting and meaningful in itself

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-082 (Secretary (Secretarial Practices)); COURSE-035 (Secretary (Secretarial Practices)); COURSE-031 (National Diploma In Television Program Production); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-053 (Computer Applications Assistant); COURSE-034 (Refrigeration & Air Conditioning Technician); COURSE-012 (Refrigeration & Air Conditioning Technician); COURSE-010 (Beautician); COURSE-011 (Baker); COURSE-033 (Plumber); COURSE-020 (Landscape Development Assistant); COURSE-021 (Automobile Electrician); COURSE-030 (Motorcycle Mechanic); COURSE-037 (Tailor); COURSE-008 (Computer Hardware Technician)

**Retrieval query summary (used to search, not shown to the model as such):** expected_highest_edu_f=Post-graduate degree; obstacle_finding_this_job=No work experience; current_activity_status=Working for pay, profit, or family gain for at least one hour; employment_status=For an employer — for a salary or wage; occupational_class=Clerical or office work (data entry, receptionist, secretary, etc.); qualification_job_match=Very well — my qualifications are central to this job; edu_status=Currently in higher education (degree or diploma)

#### Rank 1: `COURSE-082` — Secretary (Secretarial Practices)

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Covers secretarial duties: meetings, mailing, correspondence, travel arrangement...' has low word-overlap (33%) with the retrieved COURSE-082 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.) — *relevance stated by the model:* "The respondent currently works in a clerical/office role; secretarial training maps directly to that occupational area."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent stated intention to pursue further education, supporting a recommendation for a skills/upgrading course."
  - `edu_status` = Currently in higher education (degree or diploma) — *relevance stated by the model:* "The respondent is already in higher education and aims for further study; an applied vocational course could fit those plans."
  - `income_hours_preference` = Keep things the same as they are now — *relevance stated by the model:* "Respondent prefers not to change income/hours, so part-time or weekend scheduling is relevant to feasibility."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Within this profile, 'Plans further education/training' was commonly answered Yes (92.3%) and many have formal, secure jobs."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "This is a part time course which will be held on weekends." — source: COURSE-082
  - "Covers secretarial duties: meetings, mailing, correspondence, travel arrangements; develops communication and office skills." — source: COURSE-082
  - "Course language: English; max students 30." — source: COURSE-082

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent currently works in a clerical/office role and prefers to 'keep things the same' in hours, a part-time weekend secretarial course may be easier to combine with their existing work commitments." (hedged; based on: occupational_class = Clerical or office work (data entry, receptionist, secretary, etc.), income_hours_preference = Keep things the same as they are now, COURSE-082: part time course on weekends)

**LLM's recommendation explanation (`why_recommended`):** "The Secretary (Secretarial Practices) course directly teaches skills used in clerical/office roles (secretarial duties, communication, handling correspondence). The respondent currently works in a clerical occupation and is pursuing further education, so this course content aligns with their background and likely career path. The course is offered part-time on weekends, which may fit the respondent's preference to maintain current work hours."

**Uncertainties disclosed by the LLM:**
  - The course document does not state entry requirements or fees; eligibility and cost are unknown from the provided text.
  - We do not know whether the course is offered in Galle or at a location convenient to the respondent; location details are not in the document.

**Limitations disclosed by the LLM:**
  - Recommendation uses the respondent's current occupational class as the primary content-match signal (allowed by the decision standard) rather than an explicit stated sector preference (the respondent answered 'Not sure' for ideal_sector).
  - No explicit placement/employment guarantee is stated in the course document.

#### Rank 2: `COURSE-053` — Computer Applications Assistant

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.) — *relevance stated by the model:* "Clerical roles commonly require MS Office, email and basic ICT skills taught by this course."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent's intent to continue education supports recommending a skills course to build workplace competencies."
  - `income_hours_preference` = Keep things the same as they are now — *relevance stated by the model:* "Part-time/weekend scheduling is relevant to combining study with current work."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Within this profile, many respondents reported employer-sponsored or on-the-job training (employer-paid training was common among those receiving training)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "This is a part time course which will be held on weekends." — source: COURSE-053
  - "Covers ICT introduction, MS-Office, Using Internet & E-mail." — source: COURSE-053
  - "Language: English; max students 20." — source: COURSE-053

**[LLM INFERENCE] Contextual inferences made:**
  - "Because clerical work often uses MS Office and email, the Computer Applications Assistant course may directly build skills the respondent uses at work or could use to strengthen their qualifications." (hedged; based on: occupational_class = Clerical or office work (data entry, receptionist, secretary, etc.), COURSE-053: course content includes MS-Office, Internet & E-mail)
  - "Because the course is offered on weekends, it may be more practical for the respondent to attend without changing their weekday work schedule." (hedged; based on: income_hours_preference = Keep things the same as they are now, COURSE-053: part time course on weekends)

**LLM's recommendation explanation (`why_recommended`):** "The Computer Applications Assistant course teaches basic ICT and MS Office skills directly relevant to clerical/office work. It is offered part-time on weekends, which could be compatible with the respondent's desire to maintain their current working hours while pursuing further education."

**Uncertainties disclosed by the LLM:**
  - No information in the course document about fees, exact location, or formal entry requirements.
  - We do not know whether the course language (English) matches the respondent's language preference or comfort.

**Limitations disclosed by the LLM:**
  - Recommendation assumes the respondent would prefer practical ICT skills for clerical advancement even though they did not explicitly name a field preference (their ideal_sector is 'Not sure'). This uses allowed evidence (occupational_class) for content selection.
  - No guarantee of employer support or recognition beyond the course description is documented.

#### Rank 3: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent intends to continue education; a diploma-level ICT programme could serve that plan."
  - `edu_status` = Currently in higher education (degree or diploma) — *relevance stated by the model:* "Respondent's ongoing higher education suggests they may be equipped to undertake a diploma-level programme."
  - `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.) — *relevance stated by the model:* "Some ICT diploma modules (database, workplace information, communication) could be relevant to advanced clerical or office roles."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Within this profile, technical and permanent employment was present for many; the profile also showed high rates of continuing education."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Full-time course held on weekdays covering System Analysis & Design, Software Programming, Database Systems, Web Programming, LAN, and workplace communication." — source: COURSE-006
  - "By completing this course, one can achieve Competency Level 5 under NVQ standards." — source: COURSE-006
  - "Language: English; max students 20." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the diploma covers database, workplace information, and communication topics that can be useful in more advanced office/technical roles, it may support the respondent's aim to progress in their career or education." (hedged; based on: plans_further_edu_f = Yes, COURSE-006: modules include Database System, Manage Workplace Information, Manage Workplace Communication)
  - "Because the course is full-time on weekdays and the respondent currently works around 40–45 hours per week, the full-time schedule may be less easy to combine with current employment (it may require schedule changes or leave)." (hedged; based on: usual_hours_per_week = 45.0, actual_hours_last_week = 40.0, COURSE-006: This is a full time course which will be held on weekdays.)

**LLM's recommendation explanation (`why_recommended`):** "The National Diploma in ICT offers substantive technical modules (databases, programming, web, networks) that could broaden the respondent's qualifications beyond clerical tasks and support further education goals. It awards an NVQ Level 5 competency which aligns with the respondent's intention to pursue higher-level education."

**Uncertainties disclosed by the LLM:**
  - The course is full-time on weekdays; it is not documented whether flexible study modes or part-time options exist.
  - No explicit entry requirements, fees, or local delivery location are provided in the document.

**Limitations disclosed by the LLM:**
  - This recommendation is cautious because the respondent did not explicitly state an interest in ICT as a sector (ideal_sector = 'Not sure'); the match is based on potential career upskilling rather than a direct stated sector preference.
  - Attending a full-time weekday programme could be impractical without changes to the respondent's current employment arrangements; this is noted as an inference, not a claim of impossibility.


---

## 19. `nysc-03b655c2-0162-44b7-a418-e4d9ac99ccbb` (Branch F) {#19-nysc-03b655c2-0162-44b7-a418-e4d9ac99ccbb}

**Selection rationale (why this respondent was chosen for the batch):** F profile 1, Retail/repair, job-change-for-pay intent

### Frozen profile membership(s)

- `F_employment_security` — Profile 1: "Temporary/no-contract employment with uncertain security" (dimension: Employment security and formality)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `acceptance_conditions_search` = Any job, provided it paid well enough
  - `hopes_to_change_job` = Yes — I want to change
  - `ideal_sector` = Wholesale, retail, or repair
  - `ideal_work_type` = Start my own business
  - `income_hours_preference` = Keep things the same as they are now
  - `plans_further_edu_f` = Not sure yet
  - `reason_wants_to_change` = To get higher pay

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `actual_hours_last_week` = 0.0
  - `area_type` = Metropolitan suburb
  - `district` = Puttalam
  - `had_min_wage_during_search` = Yes
  - `has_children` = No
  - `household_income` = Above LKR 200,000
  - `household_size` = 7.0
  - `household_unemployed` = 0.0
  - `household_workers` = 1.0
  - `monthly_income_band` = LKR 70,000 – 120,000
  - `obstacle_finding_this_job` = No major obstacles — the process was straightforward
  - `primary_earner_status` = Shared — several people contribute roughly equally
  - `primary_income_source` = My regular job or business
  - `usual_hours_per_week` = 7.0
  - `willing_to_relocate_f` = Yes — to another country

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `contract_satisfaction` = Satisfied — the wage is high enough that I accept the terms
  - `contract_type` = No contract at all
  - `current_activity_status` = Working for pay, profit, or family gain for at least one hour
  - `edu_end_year` = 2014.0
  - `edu_status` = I have completed my education and am not currently studying
  - `employment_service_help_f` = No — none at all
  - `employment_status` = In a family business or farm for the family's benefit
  - `enterprise_location_type` = In my own home or someone else's home
  - `enterprise_registered` = Yes — it is registered
  - `enterprise_size` = Less than 5 workers
  - `ever_refused_job_f` = No
  - `has_second_job` = No
  - `highest_edu_completed` = A/L level (Grade 12–13)
  - `hours_below_normal` = Yes — I worked fewer hours than normal
  - `interviews_before_hire` = 0.0
  - `job_recruitment_method` = Through friends or relatives
  - `job_security_12months` = Likely but not certain — I have some concern
  - `jobs_applied_before_hire` = 0.0
  - `occupational_class` = Service or sales work (retail, beauty, hospitality, security, etc.)
  - `paid_taxes` = Yes
  - `past_edu_useful_for_job` = Very useful — directly relevant and applied daily
  - `qualification_job_match` = Very well — my qualifications are central to this job
  - `reason_below_normal_hours` = Business reduction or lack of orders or clients
  - `reason_not_union` = I have a negative view of trade unions
  - `received_training` = No
  - `registered_as_jobseeker` = No
  - `search_duration_before_hire` = 6 months to 1 year
  - `sector_formality` = Fully formal — registered employer, written contract, statutory benefits
  - `spell1_activity` = Self-employed / running own business
  - `spell1_is_current` = Yes — this is still my current situation
  - `union_member` = No
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_first_married` = 30.0
  - `age_group` = 30 – 35 years
  - `competence_growth_at_work` = Somewhat — there is some growth but it has slowed
  - `edu_min_for_decent_job` = Post-graduate qualification
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `gender_equality_at_work` = Equal opportunities for women and men
  - `insecurity_bothers` = Yes — it worries or stresses me
  - `job_satisfaction` = Somewhat satisfied
  - `most_important_life_goal` = Having financial security or earning a lot
  - `most_useful_quality_for_job` = Communication and interpersonal skills
  - `move_reason` = To accompany family
  - `moved_from_origin` = No — I moved from somewhere else
  - `professional_network_growth` = Yes — significantly, I have built valuable professional relationships
  - `relatedness_at_work` = Very connected — genuinely part of the team and valued
  - `spouse_activity` = Working for a salary or wage
  - `work_autonomy` = A great deal — real freedom in how I approach my work
  - `work_motivation_type` = Primarily for the income — I need the money

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-035 (Secretary (Secretarial Practices)); COURSE-071 (Human Recources Management); COURSE-049 (Business Managemant); COURSE-082 (Secretary (Secretarial Practices)); COURSE-053 (Computer Applications Assistant); COURSE-025 (Electrician); COURSE-064 (Electrician); COURSE-055 (Computer Hardware Technician); COURSE-034 (Refrigeration & Air Conditioning Technician); COURSE-001 (Freelancer Of Web Design & Development); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-003 (Certificate In English Communication Essentials.); COURSE-012 (Refrigeration & Air Conditioning Technician); COURSE-022 (Computer Network Technician); COURSE-008 (Computer Hardware Technician)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Wholesale, retail, or repair; ideal_work_type=Start my own business; reason_wants_to_change=To get higher pay; obstacle_finding_this_job=No major obstacles — the process was straightforward; current_activity_status=Working for pay, profit, or family gain for at least one hour; employment_status=In a family business or farm for the family's benefit; occupational_class=Service or sales work (retail, beauty, hospitality, security, etc.); qualification_job_match=Very well — my qualifications are central to this job; highest_edu_completed=A/L level (Grade 12–13); edu_status=I have completed my education and am not currently studying; [sector-vocabulary expansion terms: business, communication, computer, human resources, internet, management, office, secretarial]

#### Rank 1: `COURSE-049` — Business Managemant

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "The respondent explicitly wants to start their own business; a Business Management course directly teaches skills for running a business."
  - `ideal_sector` = Wholesale, retail, or repair — *relevance stated by the model:* "The respondent's preferred sector is commerce/retail; business management content is applicable to starting or improving a retail/wholesale enterprise."
  - `spell1_activity` = Self-employed / running own business — *relevance stated by the model:* "The respondent is already self-employed, so business-management training may build on their current activity and support business growth."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Within this profile many respondents reported wanting to start their own business and a proportion reported having self-employment; profile evidence supports that management/formalisation training can be relevant for similar respondents."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Business Managemant course will give you theoretical knowledge as well as job oriented practical ... part time course which will be held on weekends." — source: COURSE-049
  - "Objective includes developing entrepreneurial abilities by obtaining the necessary knowledge, skills and gentle attitudes within a disciplined environment." — source: COURSE-049

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent stated they want to start their own business and is already self-employed, the Business Management course may help them formalise and grow their enterprise." (hedged; based on: ideal_work_type = Start my own business, spell1_activity = Self-employed / running own business, COURSE-049: course objective developing entrepreneurial abilities)
  - "Because the course is offered on weekends (part-time), it may be easier to combine with the respondent's existing work responsibilities than a full‑time weekday course." (hedged; based on: COURSE-049: part time, held on weekends, spell1_activity = Self-employed / running own business)

**LLM's recommendation explanation (`why_recommended`):** "Direct match: respondent wants to start their own business and the course explicitly teaches business/entrepreneurial skills and practical knowledge. It is part-time on weekends, which may be compatible with someone already running a business."

**Uncertainties disclosed by the LLM:**
  - The course description does not list detailed syllabus items (e.g. finance, marketing, bookkeeping) nor fee, exact schedule, or entry requirements in the retrieved document.
  - It is not documented whether the course includes retail-specific modules (stock, wholesale processes) tailored to this respondent's wholesale/retail interest.

**Limitations disclosed by the LLM:**
  - No specific fee information or precise schedule (dates/times) is documented in the course extract.
  - No explicit entry requirements or certification prerequisites are listed in the provided course text.

#### Rank 2: `COURSE-053` — Computer Applications Assistant

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Starting or running a small business commonly requires office/computer skills (documentation, email, MS Office) which this course teaches."
  - `spell1_activity` = Self-employed / running own business — *relevance stated by the model:* "The respondent runs a small registered enterprise; computer/office skills may support record-keeping, invoicing, or online sales."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Many in this profile reported limited prior formal training for current jobs; short practical ICT courses are consistent with the profile's observed training needs."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course Overview: ICT introduction; MS-Office; Using Internet & E-mail. This is a part time course which will be held on weekends." — source: COURSE-053

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent is self-employed and wants to grow/payraise their business, basic ICT and MS-Office skills may be useful for business administration, marketing or invoicing." (hedged; based on: spell1_activity = Self-employed / running own business, ideal_work_type = Start my own business, COURSE-053: ICT introduction; MS-Office; Internet & E-mail)
  - "Because the course is part time on weekends, it may be feasible to attend while continuing to run a small business." (hedged; based on: COURSE-053: part time, held on weekends, spell1_activity = Self-employed / running own business)

**LLM's recommendation explanation (`why_recommended`):** "The course teaches MS-Office, internet and email skills which plausibly support small-business administration and could help the respondent professionalise record-keeping, customer communications, or online presence."

**Uncertainties disclosed by the LLM:**
  - The retrieved description does not state fee, precise duration, or whether training includes specific retail/wholesale e-commerce modules.
  - We cannot confirm mode (in-person vs hybrid) or certification level beyond the short course description.

**Limitations disclosed by the LLM:**
  - No explicit statement that the course covers retail-specific business systems (POS, inventory) is present in the document.
  - No entry requirements, placement support, or fee details are given in the course text.

#### Rank 3: `COURSE-055` — Computer Hardware Technician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Wholesale, retail, or repair — *relevance stated by the model:* "The respondent named 'repair' as part of their ideal sector; a Computer Hardware Technician course explicitly teaches repair and maintenance of PCs and related devices."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Repair skills can be the basis for a small repair business (service shop or add-on to retail business)."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Profile members more often reported not having received training for their current job; a vocational repair course could address this training gap."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course Overview: PC assembling; Maintenance Repair PCs; Install and Configure Internal, External Devices; Software Installation; Network and Internet. Part time course held on weekends." — source: COURSE-055

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent's ideal sector includes repair, the Computer Hardware Technician course may directly build repair skills that could be offered as a service or combined with a retail business." (hedged; based on: ideal_sector = Wholesale, retail, or repair, COURSE-055: PC assembling, maintenance and repair, device installation)
  - "Because the course is offered on weekends (part time), it may be more practical to take while running an existing small business." (hedged; based on: COURSE-055: part time, held on weekends, spell1_activity = Self-employed / running own business)

**LLM's recommendation explanation (`why_recommended`):** "Direct content match: respondent listed 'repair' within their ideal sector and the course explicitly teaches repair and maintenance of computer hardware — skills that can be monetised in a small repair or retail-support business."

**Uncertainties disclosed by the LLM:**
  - The course text does not specify fee, exact duration, certification level, or whether tools/materials are provided.
  - It is not documented whether the local/regional offering is available in Puttalam (respondent's district) or whether there are placement/entrepreneurship modules.

**Limitations disclosed by the LLM:**
  - No explicit entry requirements or placement/employment outcomes are documented in the course extract.
  - If the respondent's retail business is not electronics-related, the direct applicability of computer-hardware repair may be limited.


---

## 20. `nysc-1a42a4ad-7444-4e03-8b9c-7ce184f7850c` (Branch F) {#20-nysc-1a42a4ad-7444-4e03-8b9c-7ce184f7850c}

**Selection rationale (why this respondent was chosen for the batch):** F profile 1, Creative arts, no-experience barrier

### Frozen profile membership(s)

- `F_employment_security` — Profile 1: "Temporary/no-contract employment with uncertain security" (dimension: Employment security and formality)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `acceptance_conditions_search` = Only a job that was stable, well paid, AND matched my qualifications
  - `expected_highest_edu_f` = Bachelor's degree
  - `hopes_to_change_job` = Not sure
  - `ideal_sector` = Creative, media, and arts
  - `ideal_work_type` = Not sure yet
  - `income_hours_preference` = Fewer hours and correspondingly less income
  - `plans_further_edu_f` = Yes

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `actual_hours_last_week` = 40.0
  - `area_type` = Metropolitan suburb
  - `district` = Gampaha
  - `had_min_wage_during_search` = No — I would have accepted any wage
  - `has_children` = No
  - `household_income` = Above LKR 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 0.0
  - `household_workers` = 1.0
  - `monthly_income_band` = LKR 40,000 – 70,000
  - `obstacle_finding_this_job` = No work experience
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family
  - `usual_hours_per_week` = 40.0
  - `who_paid_training` = My employer
  - `willing_to_relocate_f` = I have no strong preference

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `contract_satisfaction` = Satisfied — the wage is high enough that I accept the terms
  - `contract_type` = Written contract — temporary (under 12 months)
  - `current_activity_status` = Working for pay, profit, or family gain for at least one hour
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help_f` = Advice on how to search for jobs
  - `employment_status` = For an employer — for a salary or wage
  - `enterprise_location_type` = A fixed location — office, shop, factory, or site
  - `enterprise_registered` = Yes — it is registered
  - `enterprise_size` = 50 workers or more
  - `ever_refused_job_f` = No
  - `has_second_job` = No
  - `hours_below_normal` = No — I worked my normal hours or more
  - `interviews_before_hire` = 2.0
  - `job_recruitment_method` = Through friends or relatives
  - `job_security_12months` = Likely but not certain — I have some concern
  - `jobs_applied_before_hire` = 3.0
  - `occupational_class` = Other
  - `paid_taxes` = No
  - `past_edu_useful_for_job` = Somewhat useful — helps in some areas
  - `qualification_job_match` = Very well — my qualifications are central to this job
  - `reason_not_union` = I have never thought about it
  - `received_training` = Yes
  - `registered_as_jobseeker` = Yes
  - `search_duration_before_hire` = Less than 1 week — I was recruited or it was immediate
  - `sector_formality` = Fully formal — registered employer, written contract, statutory benefits
  - `training_duration` = 1 to 4 weeks
  - `training_provider` = My employer (on-the-job)
  - `training_type_received` = Training in new technologies
  - `union_member` = No
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `competence_growth_at_work` = Somewhat — there is some growth but it has slowed
  - `edu_min_for_decent_job` = Education level doesn't matter much
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `gender_equality_at_work` = Equal opportunities for women and men
  - `insecurity_bothers` = Yes — it worries or stresses me
  - `job_satisfaction` = Somewhat satisfied
  - `most_important_life_goal` = Having leisure, freedom, and personal time
  - `most_useful_quality_for_job` = Communication and interpersonal skills
  - `move_reason` = Other reason
  - `moved_from_origin` = No — I moved from somewhere else
  - `professional_network_growth` = Not really — my network has stayed roughly the same
  - `relatedness_at_work` = Very connected — genuinely part of the team and valued
  - `work_autonomy` = A great deal — real freedom in how I approach my work
  - `work_motivation_type` = It aligns with my personal goals and who I want to become

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-062 (Desktop Publisher); COURSE-031 (National Diploma In Television Program Production); COURSE-041 (Preschool Teacher (Early Childhood Development)); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-068 (Graphics Designer); COURSE-016 (Graphics Designer); COURSE-009 (Information And Communication Technolory Technician); COURSE-034 (Refrigeration & Air Conditioning Technician); COURSE-012 (Refrigeration & Air Conditioning Technician); COURSE-010 (Beautician); COURSE-011 (Baker); COURSE-033 (Plumber); COURSE-020 (Landscape Development Assistant); COURSE-021 (Automobile Electrician); COURSE-030 (Motorcycle Mechanic)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Creative, media, and arts; expected_highest_edu_f=Bachelor's degree; obstacle_finding_this_job=No work experience; current_activity_status=Working for pay, profit, or family gain for at least one hour; employment_status=For an employer — for a salary or wage; occupational_class=Other; qualification_job_match=Very well — my qualifications are central to this job; training_type_received=Training in new technologies; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: adobe illustrator, adobe indesign, adobe photoshop, child psychology, graphics, television]

#### Rank 1: `COURSE-068` — Graphics Designer

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Creative, media, and arts — *relevance stated by the model:* "Directly names the creative sector; graphics design is a core creative/media field."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent intends to pursue further education, supporting suitability of a skills/qualification course."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Within this profile, many respondents were currently in higher education and a high share worked while studying (conditional)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Graphic Designing course will give you theoretical knowledge as well as job oriented practical skills that are necessary for employment and higher education." — source: COURSE-068
  - "This is a part time course which will be held on weekends." — source: COURSE-068
  - "Max students: 20; Language: English; Course length indicated (part-time variant visible in source)." — source: COURSE-068

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent stated a preference for 'fewer hours and correspondingly less income', a part-time weekend graphics course may be easier for them to combine with existing weekday work/study commitments than a full-time weekday programme." (hedged; based on: income_hours_preference: Fewer hours and correspondingly less income, course_fact: This is a part time course which will be held on weekends. (COURSE-068))
  - "Because the respondent named the creative/media sector as their ideal sector, practical graphic-design training may support their stated sector interest and future education plans." (hedged; based on: ideal_sector: Creative, media, and arts, plans_further_edu_f: Yes, course_fact: Graphic Designing course will give you theoretical knowledge as well as job oriented practical skills. (COURSE-068))

**LLM's recommendation explanation (`why_recommended`):** "Course content (graphic design) directly matches the respondent's stated ideal sector (creative, media, and arts). The course is explicitly part-time on weekends, which may align with the respondent's preference for fewer hours and existing weekday commitments."

**Uncertainties disclosed by the LLM:**
  - The course document does not state fees, exact schedule hours, entry requirements, or the precise campus location for this part-time variant.
  - Language is English; respondent's language preference/comfort is not documented here.

**Limitations disclosed by the LLM:**
  - No explicit fee, eligibility or entry-requirement information is available in the course document provided.
  - While the part-time format is documented for COURSE-068, the exact weekly hours and assessment/qualification details are not fully specified in the extract.

#### Rank 2: `COURSE-062` — Desktop Publisher

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Creative, media, and arts — *relevance stated by the model:* "Desktop publishing and software skills are core to creative and media work (layout, visual content), aligning with the respondent's sector preference."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent plans further education; a technical creative course supports that intention."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Profile shows many respondents who were studying while working and who received employer or other training; this is supporting context only."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Desktop Publishing & Graphic Designing course will give you theoretical knowledge as well as job oriented practical that is necessary for employment and higher education." — source: COURSE-062
  - "This is a part time course which will be held on weekends." — source: COURSE-062
  - "Course covers Adobe PageMaker, Corel Draw, Adobe Photoshop CS6, Adobe InDesign CS6, Adobe Illustrator CS6 and related tools." — source: COURSE-062

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course lists practical desktop-publishing and graphic-software training and the respondent prefers the creative sector, this course may support the respondent's stated sector interest by building directly applicable creative/production skills." (hedged; based on: ideal_sector: Creative, media, and arts, course_fact: Course covers Adobe Photoshop, InDesign, Illustrator, Corel Draw, etc. (COURSE-062))
  - "Because the course is described as part-time on weekends, it may be more feasible for a respondent who currently works weekdays (40 hours/week) than a full-time weekday programme would be." (hedged; based on: usual_hours_per_week: 40.0, course_fact: This is a part time course which will be held on weekends. (COURSE-062))

**LLM's recommendation explanation (`why_recommended`):** "The course explicitly teaches desktop-publishing and graphic-software skills that map closely to creative/media sector roles the respondent identified. It is offered part-time on weekends, which may fit the respondent's work schedule and stated desire for fewer hours."

**Uncertainties disclosed by the LLM:**
  - The course document does not include explicit fee, detailed schedule hours, entry requirements, or campus location.
  - Some course text had uncertainty markers in the source (e.g. Corel Draw / Corel Photopaint lines marked [UNCLEAR]), which slightly reduces specificity of the extracted tool list.

**Limitations disclosed by the LLM:**
  - No explicit information on fees, admissions criteria, or qualification level is available in the provided extract.
  - The language is English; the respondent's language comfort is not documented here and could affect fit.

#### Rank 3: `COURSE-031` — National Diploma In Television Program Production

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Creative, media, and arts — *relevance stated by the model:* "Television production is a core creative-media field directly aligned with the respondent's stated sector preference."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent's intention to pursue further education supports recommending a diploma-level programme."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Profile shows many respondents in higher education; this is supporting context only and does not assert it applies to the individual beyond their own reported edu_status."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "National Diploma in TV Programme & Production Technology course will give you theoretical knowledge as well as job oriented practical that is necessary for employment and higher education." — source: COURSE-031
  - "This is a full time course which will be held on weekdays." — source: COURSE-031
  - "Completion can achieve competency Level 5 under the National Vocational Qualifications Competency Standards." — source: COURSE-031

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent named the creative/media sector as their ideal sector and the course is a TV production diploma, the programme may support their sector-aligned education and career aims." (hedged; based on: ideal_sector: Creative, media, and arts, course_fact: National Diploma in TV Programme & Production Technology content and qualification Level 5. (COURSE-031))
  - "Because the course is full-time on weekdays and the respondent reports working ~40 hours/week, attending this programme may be harder to combine with their current job, although the respondent also indicated they are 'Currently in higher education' and 'plans_further_edu_f: Yes', which suggests they have experience combining study and work; the scheduling mismatch is an important practical uncertainty." (hedged; based on: usual_hours_per_week: 40.0, edu_status: Currently in higher education (degree or diploma), course_fact: This is a full time course which will be held on weekdays. (COURSE-031))

**LLM's recommendation explanation (`why_recommended`):** "Content (television programme production) directly matches the respondent's stated creative/media interest and offers a formal diploma (NVQ Level 5) that aligns with the respondent's plan for further education."

**Uncertainties disclosed by the LLM:**
  - The course is full-time on weekdays which may conflict with the respondent's current weekday work schedule (40 hrs/week).
  - The document does not state fees, explicit entry requirements, exact campus location, or whether part-time/alternate delivery options exist.

**Limitations disclosed by the LLM:**
  - No explicit entry requirements, fees, or location details are provided in the course extract.
  - Recommendation assumes the respondent would consider full-time study despite current work; this is an inference and may not reflect their actual availability.


---

## 21. `nysc-0a92b28f-94dc-44ce-9e9e-2d25b35c0b04` (Branch F) {#21-nysc-0a92b28f-94dc-44ce-9e9e-2d25b35c0b04}

**Selection rationale (why this respondent was chosen for the batch):** F profile 2, Manufacturing, satisfied/stable

### Frozen profile membership(s)

- `F_employment_security` — Profile 2: "Predominantly permanent employment with stronger security" (dimension: Employment security and formality)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `acceptance_conditions_search` = Only a job that was stable, well paid, AND matched my qualifications
  - `expected_highest_edu_f` = Bachelor's degree
  - `hopes_to_change_job` = No — I want to stay in this job
  - `ideal_sector` = Manufacturing or production
  - `ideal_work_type` = Start my own business
  - `income_hours_preference` = More hours and correspondingly more income
  - `plans_further_edu_f` = Yes

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `actual_hours_last_week` = 42.0
  - `area_type` = Small town
  - `district` = Colombo
  - `had_min_wage_during_search` = Yes
  - `has_children` = No
  - `household_income` = LKR 120,000 – 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 1.0
  - `household_workers` = 2.0
  - `monthly_income_band` = LKR 70,000 – 120,000
  - `obstacle_finding_this_job` = No major obstacles — the process was straightforward
  - `primary_earner_status` = Shared — several people contribute roughly equally
  - `primary_income_source` = My regular job or business
  - `usual_hours_per_week` = 40.0
  - `who_paid_training` = An international organization or donor
  - `willing_to_relocate_f` = No — I would not move

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `contract_satisfaction` = Satisfied — it gives me the job security I need
  - `contract_type` = Written contract — permanent/unlimited
  - `current_activity_status` = Working for pay, profit, or family gain for at least one hour
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help_f` = No — none at all
  - `employment_status` = For an employer — for a salary or wage
  - `enterprise_location_type` = A fixed location — office, shop, factory, or site
  - `enterprise_registered` = Yes — it is registered
  - `enterprise_size` = 50 workers or more
  - `ever_refused_job_f` = No
  - `has_second_job` = Yes
  - `hours_below_normal` = Yes — I worked fewer hours than normal
  - `interviews_before_hire` = 5.0
  - `job_recruitment_method` = Through a job advertisement (newspaper, internet, social media)
  - `job_security_12months` = Very likely — my job is secure
  - `jobs_applied_before_hire` = 10.0
  - `occupational_class` = Technical work (IT technician, lab technician, etc.)
  - `paid_taxes` = *[respondent selected "Prefer not to say"]*
  - `past_edu_useful_for_job` = Very useful — directly relevant and applied daily
  - `qualification_job_match` = Very well — my qualifications are central to this job
  - `reason_below_normal_hours` = Education leave or training
  - `received_training` = Yes
  - `registered_as_jobseeker` = Yes
  - `search_duration_before_hire` = 1 to 4 weeks
  - `sector_formality` = Fully formal — registered employer, written contract, statutory benefits
  - `training_duration` = Less than one week
  - `training_provider` = A private contractor or trainer
  - `training_type_received` = On-the-job mentoring with a colleague
  - `union_member` = Yes
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `competence_growth_at_work` = Yes — I am constantly learning and growing in this role
  - `edu_min_for_decent_job` = A/L level
  - `employment_network_quality` = Yes — I know one or two people who might help
  - `gender_equality_at_work` = Equal opportunities for women and men
  - `job_satisfaction` = Very satisfied
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = IT and digital skills
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `professional_network_growth` = Yes — significantly, I have built valuable professional relationships
  - `relatedness_at_work` = Very connected — genuinely part of the team and valued
  - `work_autonomy` = A great deal — real freedom in how I approach my work
  - `work_motivation_type` = I find the work genuinely interesting and meaningful in itself

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-012 (Refrigeration & Air Conditioning Technician); COURSE-034 (Refrigeration & Air Conditioning Technician); COURSE-029 (Mobile Phone Repair Technician); COURSE-031 (National Diploma In Television Program Production); COURSE-077 (Mobile Phone Repair Technician); COURSE-028 (Lapiderist (Gem Cutting)); COURSE-005 (Automobile Mechanic); COURSE-030 (Motorcycle Mechanic); COURSE-040 (Automobile Mechanic); COURSE-049 (Business Managemant); COURSE-078 (Motorcycle Mechanic); COURSE-042 (Automobile Electrician); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-081 (Radio, TV & Allied Equipment Repairer); COURSE-021 (Automobile Electrician)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Manufacturing or production; ideal_work_type=Start my own business; expected_highest_edu_f=Bachelor's degree; obstacle_finding_this_job=No major obstacles — the process was straightforward; current_activity_status=Working for pay, profit, or family gain for at least one hour; employment_status=For an employer — for a salary or wage; occupational_class=Technical work (IT technician, lab technician, etc.); qualification_job_match=Very well — my qualifications are central to this job; training_type_received=On-the-job mentoring with a colleague; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: air conditioning, automobile, electrical, electronics, english, gem cutting, mechanic, mobile phone, motorcycle, programming, refrigeration, sinhala]

#### Rank 1: `COURSE-005` — Automobile Mechanic

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS WITH CAUTION
  - `edu_status` (EDUCATION_AND_EXPERIENCE_CONTEXT, position 3): PASS WITH CAUTION — experience/background variable given preference-like framing as a secondary citation

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent explicitly wants to start their own business; technical mechanic training commonly supports starting a repair/maintenance business."
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Respondent named manufacturing/production as their preferred sector; automobile/mechanic skills are within vehicle production/repair/maintenance trades related to that sector."
  - `edu_status` = Currently in higher education (degree or diploma) — *relevance stated by the model:* "Respondent is pursuing higher education and has indicated plans for further education, suggesting they value formal training credentials; the course awards NVQ Level 4 which may align with that preference."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "This profile contained many respondents working in technical occupations and with stable formal employment; this supports that technical vocational training is consistent with the broader profile group."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course provides theoretical and job-oriented practical skills in engine, transmission, steering, braking, electrical systems." — source: COURSE-005
  - "This is a full time course held on weekdays and leads to Competency Level 4 under NVQ standards." — source: COURSE-005

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business and selected a technical sector (manufacturing/production), automobile mechanic training may support setting up a repair or small manufacturing/maintenance enterprise." (hedged; based on: ideal_work_type = Start my own business, ideal_sector = Manufacturing or production, course fact: Automobile Mechanic gives practical skills usable in repair/maintenance businesses)
  - "Because the respondent is currently in higher education and values further education, the NVQ Level 4 outcome may appear useful for formal credentialing or progression." (hedged; based on: edu_status = Currently in higher education (degree or diploma), course fact: Achieve Competency Level 4 under NVQ)

**LLM's recommendation explanation (`why_recommended`):** "Direct preference for manufacturing/production and a stated intention to start a business align well with hands-on mechanical training that teaches vehicle systems and practical repair skills. The course explicitly teaches practical skills and awards an NVQ Level 4 competency."

**Uncertainties disclosed by the LLM:**
  - The course document lists this as full-time weekday delivery; respondent works ~40 hrs/week and is in higher education — compatibility with schedule is uncertain.
  - No fee, exact location, entry requirements, or start dates are stated in the course document.

**Limitations disclosed by the LLM:**
  - Course schedule (full-time weekdays) may conflict with the respondent's working and study commitments; respondent did not state they cannot attend full-time, so this is only a potential constraint.
  - The course document does not specify fees, distance from Colombo small-town location, or explicit entry criteria.

#### Rank 2: `COURSE-034` — Refrigeration & Air Conditioning Technician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent wants to start a business; refrigeration/AC repair is a common small-business trade."
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Refrigeration/AC technician skills are technical/production-adjacent and fit within respondent's sector preference for technical trades."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Profile respondents commonly had technical occupations and received training; technical upskilling fits the profile context."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course teaches repair of refrigerators, deep freezers, display units, water coolers, repair of window and split A/C, operation and maintenance of central A/C systems." — source: COURSE-034
  - "Course is described as full time held on weekdays and leads to Competency Level 4 under NVQ standards." — source: COURSE-034

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent intends to start a business, refrigeration/AC repair training could provide practical skills useful to offering repair, installation, and maintenance services as a small enterprise." (hedged; based on: ideal_work_type = Start my own business, course fact: Refrigeration & AC course teaches repair and operation/maintenance skills)

**LLM's recommendation explanation (`why_recommended`):** "The course offers practical, hands-on technical skills in a trade where small-business opportunities (repair/maintenance services) are common. The course's explicit entrepreneurial framing and NVQ Level 4 outcome align with the respondent's business and further-education intentions."

**Uncertainties disclosed by the LLM:**
  - Course document lists full-time weekday delivery; respondent's working/study schedule may limit availability.
  - Some retrieved variants of this course (other record) described a part-time weekend format, but exact delivery for the available seat(s) in Colombo is unclear from the documents.
  - No fee or explicit entry requirements are documented.

**Limitations disclosed by the LLM:**
  - Delivery schedule (full-time weekdays per COURSE-034) may be difficult to combine with respondent's current job and studies; the course catalogue contains at least one screenshot variant indicating part-time/weekend delivery (COURSE-012) but it is unclear which format applies at which centre.
  - Location and start-date specifics are not stated, and the respondent is unwilling to relocate.

#### Rank 3: `COURSE-030` — Motorcycle Mechanic

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Manufacturing or production — *relevance stated by the model:* "Motorcycle/mechanic skills are technical and align with manufacturing/repair trades within the respondent's preferred sector."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Motorcycle repair is frequently a small-business trade; the respondent's entrepreneurial intention supports relevance."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Profile includes many technical workers and high reported usefulness of prior education for jobs, suggesting vocational technical training is plausible."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Motorcycle Mechanic course gives theoretical knowledge and job-oriented practical skills and can achieve competency Level 3 or 4 under NVQ standards." — source: COURSE-030
  - "Course is described as full time held on weekdays (some part-time weekend variants exist in other records)." — source: COURSE-030

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start a business and selected a technical sector, motorcycle mechanic training may be useful for setting up or expanding a vehicle-repair business." (hedged; based on: ideal_work_type = Start my own business, ideal_sector = Manufacturing or production, course fact: Motorcycle Mechanic teaches practical repair skills)

**LLM's recommendation explanation (`why_recommended`):** "The course teaches practical vehicle repair skills that map to the respondent's sector preference and entrepreneurial intention; NVQ outcomes indicate formal credentialing which the respondent values."

**Uncertainties disclosed by the LLM:**
  - Course delivery is listed as full-time weekdays which may conflict with the respondent's work/study schedule; other retrieved records show weekend/part-time variants but site-specific details are not given.
  - No fee, exact location, or entry requirements are specified in the course text.

**Limitations disclosed by the LLM:**
  - Potential schedule conflict with respondent's current full-time job and ongoing higher education — compatibility is unknown.
  - Respondent is unwilling to relocate; course location within Colombo/small-town network is not specified in the document.

#### Rank 4: `COURSE-049` — Business Managemant

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent explicitly wants to start their own business; business management training directly targets entrepreneurship and business skills."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent plans further education, indicating openness to formal management training."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Profile respondents often reported plans for further education and received training; business-management upskilling fits this profile tendency."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course overview states Business Management will give theoretical knowledge and job-oriented practical skills and is a part-time weekend course." — source: COURSE-049
  - "Course is part-time and held on weekends (document shows English language, 25 max students)." — source: COURSE-049

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start a business, business-management training may provide useful planning, management and entrepreneurial skills to support that goal." (hedged; based on: ideal_work_type = Start my own business, course fact: Business Management course provides theoretical and practical entrepreneurial/business skills)
  - "Because the course is described as part-time on weekends, it may be more compatible with the respondent's ongoing work and study commitments than full-time weekday courses." (hedged; based on: course fact: Business Management is part-time, weekends, respondent fact: works ~40 hours/week and is in higher education)

**LLM's recommendation explanation (`why_recommended`):** "Business Management directly matches the respondent's stated intention to start their own business and is offered part-time on weekends, which could be easier to combine with work and study commitments."

**Uncertainties disclosed by the LLM:**
  - The course document does not list fees, precise curriculum modules, duration, or explicit entry requirements.
  - Language is English; respondent's preferred language(s) are not stated (some technical courses are listed in Sinhala), so language fit is unknown.

**Limitations disclosed by the LLM:**
  - Missing details on fee, exact schedule, and entry requirements — these are not present in the course document.
  - If the respondent prefers instruction in Sinhala rather than English, language mismatch could be a barrier; respondent language preference was not provided.


---

## 22. `nysc-14ffa0bd-0d24-4a0e-b75d-516771a7fbbb` (Branch F) {#22-nysc-14ffa0bd-0d24-4a0e-b75d-516771a7fbbb}

**Selection rationale (why this respondent was chosen for the batch):** F profile 1, ICT, qualification mismatch signal

### Frozen profile membership(s)

- `F_employment_security` — Profile 1: "Temporary/no-contract employment with uncertain security" (dimension: Employment security and formality)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `acceptance_conditions_search` = Only a job that was stable, well paid, AND matched my qualifications
  - `expected_highest_edu_f` = Bachelor's degree
  - `hopes_to_change_job` = Yes — I want to change
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Work for a local private Sri Lankan company
  - `income_hours_preference` = Keep things the same as they are now
  - `plans_further_edu_f` = Yes
  - `reason_wants_to_change` = To get better career prospects and advancement

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `actual_hours_last_week` = 45.0
  - `area_type` = Rural area
  - `district` = Jaffna
  - `had_min_wage_during_search` = Yes
  - `has_children` = No
  - `household_income` = LKR 60,000 – 120,000
  - `household_size` = 5.0
  - `household_unemployed` = 1.0
  - `household_workers` = 2.0
  - `monthly_income_band` = LKR 20,000 – 40,000
  - `obstacle_finding_this_job` = No major obstacles — the process was straightforward
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family
  - `usual_hours_per_week` = 45.0
  - `who_paid_training` = My employer
  - `willing_to_relocate_f` = Yes — within the same province

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `contract_satisfaction` = Satisfied — it gives me the flexibility I need
  - `contract_type` = No contract at all
  - `current_activity_status` = Recently finished education — have work already arranged
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help_f` = No — none at all
  - `employment_status` = For an employer — without direct pay
  - `enterprise_location_type` = A fixed location — office, shop, factory, or site
  - `enterprise_registered` = Yes — it is registered
  - `enterprise_size` = 50 workers or more
  - `ever_refused_job_f` = Yes
  - `has_job_to_return` = Yes — I will return to my job
  - `has_second_job` = No
  - `hours_below_normal` = No — I worked my normal hours or more
  - `interviews_before_hire` = 10.0
  - `job_recruitment_method` = Through a job fair
  - `job_security_12months` = Not likely — I doubt I will still have this job
  - `jobs_applied_before_hire` = 100.0
  - `occupational_class` = Technical work (IT technician, lab technician, etc.)
  - `paid_taxes` = Yes
  - `past_edu_useful_for_job` = Somewhat useful — helps in some areas
  - `qualification_job_match` = Partially — I am somewhat over-qualified or under-qualified
  - `reason_not_union` = I am not sure what a union would do for me
  - `reason_refused_job_f` = Waiting for a better offer
  - `reason_temp_absence` = Education leave or training
  - `received_training` = Yes
  - `registered_as_jobseeker` = No
  - `search_duration_before_hire` = 1 to 2 months
  - `sector_formality` = Mostly formal — some documentation but not fully compliant
  - `training_duration` = 1 to 3 months
  - `training_provider` = A private training institution
  - `training_type_received` = Training in new technologies
  - `union_member` = No
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 26 – 29 years
  - `competence_growth_at_work` = Somewhat — there is some growth but it has slowed
  - `edu_min_for_decent_job` = Education level doesn't matter much
  - `employment_network_quality` = No — I have no one I could call on
  - `gender_equality_at_work` = Equal opportunities for women and men
  - `insecurity_bothers` = No — I accept it or it does not concern me
  - `job_satisfaction` = Very satisfied
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = Communication and interpersonal skills
  - `move_reason` = For work or employment reasons
  - `moved_from_origin` = No — I moved from somewhere else
  - `professional_network_growth` = Somewhat — I have a few useful new connections
  - `relatedness_at_work` = Somewhat connected — reasonable working relationships
  - `work_autonomy` = Very little — most things are prescribed for me
  - `work_motivation_type` = It aligns with my personal goals and who I want to become

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-009 (Information And Communication Technolory Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-035 (Secretary (Secretarial Practices)); COURSE-008 (Computer Hardware Technician); COURSE-052 (Cisco Certified Network Associate); COURSE-022 (Computer Network Technician); COURSE-058 (Computer Based Accounting); COURSE-001 (Freelancer Of Web Design & Development); COURSE-002 (PYTHON); COURSE-057 (Multimedia & Web Design); COURSE-053 (Computer Applications Assistant)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; ideal_work_type=Work for a local private Sri Lankan company; expected_highest_edu_f=Bachelor's degree; reason_wants_to_change=To get better career prospects and advancement; obstacle_finding_this_job=No major obstacles — the process was straightforward; current_activity_status=Recently finished education — have work already arranged; employment_status=For an employer — without direct pay; occupational_class=Technical work (IT technician, lab technician, etc.); qualification_job_match=Partially — I am somewhat over-qualified or under-qualified; training_type_received=Training in new technologies; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Directly names the IT sector as the respondent's preferred field; matches the course's subject area."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent intends further education, consistent with a diploma-level programme."
  - `hopes_to_change_job` = Yes — I want to change — *relevance stated by the model:* "Motivation to change jobs supports taking a course that could enable career advancement."
  - `expected_highest_edu_f` = Bachelor's degree — *relevance stated by the model:* "Aims for higher education; a National Diploma may be compatible with progression toward degree-level goals."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Many in this profile name Information technology and communications as their ideal sector (group-level tendency)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course is a full time National Diploma covering system analysis & design, software programming, database systems, web programming, LAN, workplace communication and planning (semesters 1–2)." — source: COURSE-006
  - "Course aims to provide theoretical knowledge and job-oriented practical skills and offers competency Level 5 under NVQ standards." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent stated a desire to pursue further education and to change jobs, this full-time diploma may support their goal of stronger IT qualifications for career advancement." (hedged; based on: plans_further_edu_f = Yes, hopes_to_change_job = Yes, course fact: National Diploma content and NVQ Level 5)

**LLM's recommendation explanation (`why_recommended`):** "Direct alignment: respondent explicitly chose Information Technology and Communications and intends further education; this diploma is specifically an ICT programme and offers vocationally-oriented, levelled training that could support career advancement."

**Uncertainties disclosed by the LLM:**
  - The course is full-time on weekdays; the respondent's current work/leave situation and ability to attend full-time is not detailed in the course document and may affect feasibility.
  - No explicit entry requirements, dates, or location details for this specific intake are stated in the course text provided.

**Limitations disclosed by the LLM:**
  - Course schedule (full-time weekdays) may be difficult to combine with the respondent's arranged job to return to; the course document does not state flexible or part-time options.
  - The course document does not specify exact location or fees in the provided extract.

#### Rank 2: `COURSE-073` — Java Programming With Software Applications Development

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Directly names the IT sector; Java/software development is squarely within that sector."
  - `hopes_to_change_job` = Yes — I want to change — *relevance stated by the model:* "Respondent seeks job change and career advancement; upskilling in programming supports that goal."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Indicates willingness to undertake further technical training like this part-time course."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Profile members often have technical occupational classifications and express intentions to change jobs."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Java course provides theoretical knowledge and job-oriented practical skills for software applications development; it is a part time course held on weekends." — source: COURSE-073

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is offered part-time on weekends, it may be easier for the respondent to combine study with existing work or a job they will return to." (hedged; based on: course fact: part time, held on weekends (COURSE-073), respondent fact: has_job_to_return = Yes)

**LLM's recommendation explanation (`why_recommended`):** "Strong topical fit: respondent wants IT work and career advancement; a weekend Java programming course offers practical software development skills relevant to IT roles and may be more feasible alongside work."

**Uncertainties disclosed by the LLM:**
  - No explicit location (e.g., whether this course runs in Jaffna or within the respondent's province) or fee information is provided in the course text.
  - Course duration, entry requirements, and accreditation details beyond the description are not specified.

**Limitations disclosed by the LLM:**
  - Course document does not confirm if remote/online attendance is available or whether the schedule aligns exactly with the respondent's weekly commitments.
  - No information about recognized certification level or articulation to degree programmes in the provided extract.

#### Rank 3: `COURSE-056` — Computer Hardware And Network Technician

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent selected IT; course covers hardware and networking, core areas in IT."
  - `occupational_class` = Technical work (IT technician, lab technician, etc.) — *relevance stated by the model:* "Respondent already works in a technical role; a hardware/network course could build on that background."
  - `hopes_to_change_job` = Yes — I want to change — *relevance stated by the model:* "Upskilling in hardware/networking could support a job change within IT."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Profile has a high share of respondents in technical occupations (IT technicians)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers computer hardware with network topics and is a part time course held on weekends." — source: COURSE-056

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent has a technical occupational background, this hardware-and-network course may build on existing practical experience and support a transition to more secure or advanced technical roles." (hedged; based on: occupational_class = Technical work, course fact: Computer Hardware With Network content (COURSE-056))

**LLM's recommendation explanation (`why_recommended`):** "Matches the respondent's expressed IT sector interest and technical occupational background; part-time weekend delivery increases practical feasibility for someone with work commitments."

**Uncertainties disclosed by the LLM:**
  - The course document does not state exact location, fees, duration, or entry requirements.
  - No explicit statement that the course is offered in Jaffna or within the respondent's preferred relocation radius.

**Limitations disclosed by the LLM:**
  - While part-time weekends may be easier to attend, the respondent's actual weekly hours and employer leave arrangements are not confirmed here.
  - Certification level and how employers value this specific NYSC course versus other industry certificates (e.g., vendor certifications) are not described in the extract.

#### Rank 4: `COURSE-052` — Cisco Certified Network Associate

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent's sector preference aligns with network-focused training like CCNA."
  - `hopes_to_change_job` = Yes — I want to change — *relevance stated by the model:* "Network certification could help with job transition and improved prospects in IT."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Profile members commonly have technical occupations where network skills are relevant."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "CISCO Network Associate course provides theoretical knowledge and job-oriented practical skills; it is a part time course held on weekends." — source: COURSE-052

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is part-time and network skills are in-demand in IT, obtaining CCNA-style training could plausibly support the respondent's aim to improve career prospects." (hedged; based on: course fact: part time, held on weekends (COURSE-052), respondent fact: hopes_to_change_job = Yes)

**LLM's recommendation explanation (`why_recommended`):** "Network-focused certification aligns with the respondent's IT sector preference and could concretely strengthen technical qualifications for employers."

**Uncertainties disclosed by the LLM:**
  - The course document does not confirm whether this is an official Cisco-branded certification or how it maps to industry credentials.
  - No location, fee, or entry requirement details are provided in the extract.

**Limitations disclosed by the LLM:**
  - If the respondent aims for a degree path, the articulation between this CCNA course and formal degree credit is not documented here.
  - Availability in Jaffna or nearby centres is not specified.

#### Rank 5: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course covers web development topics (hosting, domain management, creating a web...' has low word-overlap (19%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Web design and development is a core IT skill area, matching the respondent's sector preference."
  - `hopes_to_change_job` = Yes — I want to change — *relevance stated by the model:* "Skills for freelancing or web development could enable new employment pathways or entrepreneurship."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent is open to further study that could include short technical courses for web development."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p1`, role=supporting_context_only: "Within this profile, some respondents express desire to start businesses or pursue self-employed technical work."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers web development topics (hosting, domain management, creating a website) and also teaches how to set up freelance accounts (e.g., Fiverr); duration mentioned as 3 months and a fee is shown in the card." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent values career advancement and the course explicitly targets freelancing and web development, it may support both employment-change aims and entrepreneurial options." (hedged; based on: respondent facts: hopes_to_change_job = Yes; plans_further_edu_f = Yes, course fact: content includes web development, hosting, and freelancing guidance (COURSE-001))

**LLM's recommendation explanation (`why_recommended`):** "Practical, job-oriented web development and freelancing skills align with the respondent's IT sector interest and stated goal of improving career prospects; the course explicitly targets income-generation via web skills."

**Uncertainties disclosed by the LLM:**
  - The course listing includes a fee and schedule details in its card but the full verification of those logistical specifics (exact location, how it runs in Jaffna) is not present in the provided extracts.
  - It is unclear how this short course articulates with the respondent's degree plans or formal accreditation.

**Limitations disclosed by the LLM:**
  - The course card contains promotional content and a stated fee; while present in the extract, the full accreditation or NVQ equivalence is not documented here.
  - No explicit information about entry requirements, exact venue, or remote delivery options is provided.


---

## 23. `nysc-079cc6c0-68dd-4ae3-b5e3-9ffd99d463f3` (Branch F) {#23-nysc-079cc6c0-68dd-4ae3-b5e3-9ffd99d463f3}

**Selection rationale (why this respondent was chosen for the batch):** F profile 2, ICT, wants to change job

### Frozen profile membership(s)

- `F_employment_security` — Profile 2: "Predominantly permanent employment with stronger security" (dimension: Employment security and formality)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `acceptance_conditions_search` = Any job, provided it matched my qualifications
  - `expected_highest_edu_f` = Post-graduate degree
  - `hopes_to_change_job` = Yes — I want to change
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Start my own business
  - `income_hours_preference` = Keep things the same as they are now
  - `plans_further_edu_f` = Yes
  - `reason_wants_to_change` = To get better career prospects and advancement

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `actual_hours_last_week` = 58.0
  - `area_type` = Metropolitan suburb
  - `district` = Puttalam
  - `had_min_wage_during_search` = Yes
  - `has_children` = No
  - `household_income` = Above LKR 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 0.0
  - `household_workers` = 2.0
  - `monthly_income_band` = LKR 120,000 – 200,000
  - `obstacle_finding_this_job` = No major obstacles — the process was straightforward
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My regular job or business
  - `usual_hours_per_week` = 40.0
  - `who_paid_training` = My employer
  - `willing_to_relocate_f` = No — I would not move

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `contract_satisfaction` = Satisfied — it gives me the flexibility I need
  - `contract_type` = Written contract — permanent/unlimited
  - `current_activity_status` = Working for pay, profit, or family gain for at least one hour
  - `edu_end_year` = 2021.0
  - `edu_status` = I have completed my education and am not currently studying
  - `employment_service_help_f` = Information about job vacancies
  - `employment_status` = For an employer — for a salary or wage
  - `enterprise_location_type` = A fixed location — office, shop, factory, or site
  - `enterprise_registered` = Yes — it is registered
  - `enterprise_size` = 10 to 19 workers
  - `ever_refused_job_f` = No
  - `has_second_job` = No
  - `highest_edu_completed` = Post-graduate (Masters, PhD, etc.)
  - `hours_below_normal` = No — I worked my normal hours or more
  - `interviews_before_hire` = 10.0
  - `job_recruitment_method` = Directly recruited by the employer
  - `job_security_12months` = Likely but not certain — I have some concern
  - `jobs_applied_before_hire` = 20.0
  - `occupational_class` = Managerial work (manager, director, department head)
  - `paid_taxes` = Yes
  - `past_edu_useful_for_job` = Very useful — directly relevant and applied daily
  - `qualification_job_match` = Very well — my qualifications are central to this job
  - `reason_not_union` = I have a negative view of trade unions
  - `received_training` = Yes
  - `registered_as_jobseeker` = Yes
  - `search_duration_before_hire` = More than 1 year
  - `sector_formality` = Fully formal — registered employer, written contract, statutory benefits
  - `spell1_activity` = Working for a salary or wage (employed)
  - `spell1_is_current` = Yes — this is still my current situation
  - `training_duration` = 3 to 6 months
  - `training_provider` = A private training institution
  - `training_type_received` = Apprenticeship training
  - `union_member` = No
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 30 – 35 years
  - `competence_growth_at_work` = Yes — I am constantly learning and growing in this role
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Not really — I have very few useful contacts
  - `gender_equality_at_work` = Equal opportunities for women and men
  - `insecurity_bothers` = No — I accept it or it does not concern me
  - `job_satisfaction` = Somewhat satisfied
  - `most_important_life_goal` = Having a good family life
  - `most_useful_quality_for_job` = IT and digital skills
  - `move_reason` = Other reason
  - `moved_from_origin` = No — I moved from somewhere else
  - `professional_network_growth` = Yes — significantly, I have built valuable professional relationships
  - `relatedness_at_work` = Very connected — genuinely part of the team and valued
  - `work_autonomy` = A great deal — real freedom in how I approach my work
  - `work_motivation_type` = It aligns with my personal goals and who I want to become

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-001 (Freelancer Of Web Design & Development); COURSE-009 (Information And Communication Technolory Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-052 (Cisco Certified Network Associate); COURSE-035 (Secretary (Secretarial Practices)); COURSE-049 (Business Managemant); COURSE-058 (Computer Based Accounting); COURSE-057 (Multimedia & Web Design); COURSE-053 (Computer Applications Assistant); COURSE-002 (PYTHON); COURSE-008 (Computer Hardware Technician)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; ideal_work_type=Start my own business; expected_highest_edu_f=Post-graduate degree; reason_wants_to_change=To get better career prospects and advancement; obstacle_finding_this_job=No major obstacles — the process was straightforward; current_activity_status=Working for pay, profit, or family gain for at least one hour; employment_status=For an employer — for a salary or wage; occupational_class=Managerial work (manager, director, department head); qualification_job_match=Very well — my qualifications are central to this job; training_type_received=Apprenticeship training; highest_edu_completed=Post-graduate (Masters, PhD, etc.); edu_status=I have completed my education and am not currently studying; [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** STRONG
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course description emphasises developing own business and earning domestically a...' has low word-overlap (12%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "The course explicitly teaches how to develop a business (freelancing) and manage online accounts/earning — aligns with wanting to start own business."
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Course content (web development, hosting, online freelancing) is within IT/communications sector the respondent named."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent intends further education, consistent with taking a short vocational course to build skills for entrepreneurship."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Within this profile many respondents selected 'Start my own business' and IT was a common ideal sector; this supports that IT/entrepreneurship training is a plausible route for similar respondents."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course teaches web development, domain & hosting management, and creating freelance accounts (Fiverr) for earning" — source: COURSE-001
  - "Course description emphasises developing own business and earning domestically and internationally" — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business and the course explicitly covers freelancing, this course may directly support that stated entrepreneurship goal." (hedged; based on: ideal_work_type = Start my own business, COURSE-001: teaches freelancing, hosting, domain management)

**LLM's recommendation explanation (`why_recommended`):** "The respondent explicitly wants to start their own business in the IT sector; this course teaches web development plus practical freelancing and hosting skills that map directly to that goal."

**Uncertainties disclosed by the LLM:**
  - Course schedule (start dates, weekday/weekend delivery) and exact entry requirements are not documented in the retrieved course text.
  - Course fee is stated in the document (LKR 20,000) for Course-001; practical affordability relative to respondent circumstances was not requested and is not assessed here.

**Limitations disclosed by the LLM:**
  - The document does not state placement, accreditation beyond a certificate, or guaranteed income outcomes.
  - No explicit information on course location relative to respondent's district (Puttalam) — travel feasibility is uncertain.

#### Rank 2: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Course is an ICT diploma covering systems analysis, programming, databases, networking and web programming — directly within the respondent's named sector."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent plans further education; a National Diploma is a formal vocational qualification that could align with that intention."
  - `hopes_to_change_job` = Yes — I want to change — *relevance stated by the model:* "A diploma offering multiple ICT skills may support the respondent's stated wish to change roles for better career prospects and advancement."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Respondents in this profile commonly reported receiving training and having formal employment — suggesting formal upskilling (diplomas) is a plausible option for similar respondents."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course modules: System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network, Software Testing, and workplace communication/management." — source: COURSE-006
  - "This is a full time course held on weekdays and leads to National Vocational Qualifications Competency Level 5." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent is a post-graduate and values further education, a formal diploma that maps to NVQ Level 5 may be attractive for career advancement or credibility in the IT sector." (hedged; based on: expected_highest_edu_f = Post-graduate degree, plans_further_edu_f = Yes, COURSE-006: leads to NVQ Competency Level 5)

**LLM's recommendation explanation (`why_recommended`):** "The course covers a broad set of IT competencies that align with the respondent's stated sector interest and desire to change jobs and pursue further education; it provides a formal NVQ-level credential which may support advancement."

**Uncertainties disclosed by the LLM:**
  - The course is full-time weekday delivery; the respondent currently works ~40–58 hours/week — whether they can attend a full-time weekday course is unclear.
  - The course description does not specify the training location relative to the respondent's district (Puttalam).

**Limitations disclosed by the LLM:**
  - No explicit entry requirements or selection criteria are listed in the course text; eligibility is not asserted.
  - No explicit information about fees or employer sponsorship for this specific course is provided (the respondent previously had employer-paid training, but course-specific sponsorship is not documented).

#### Rank 3: `COURSE-073` — Java Programming With Software Applications Development

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Course is a programming course (Java) which falls squarely within the respondent's named sector."
  - `hopes_to_change_job` = Yes — I want to change — *relevance stated by the model:* "Learning programming could help change role or move into software development, supporting the respondent's aim for better career prospects."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "This profile shows many members worked while studying and had formal employment — part-time programming courses are offered in the catalogue and may fit working respondents in this profile."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course focuses on Java programming and software application development; described as a part-time weekend course." — source: COURSE-073

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is part-time on weekends and the respondent works long hours, the weekend format may be easier to combine with current employment than a full-time weekday course." (hedged; based on: usual_hours_per_week = 40.0 and actual_hours_last_week = 58.0, COURSE-073: part time weekend delivery)

**LLM's recommendation explanation (`why_recommended`):** "Java programming directly matches the respondent's IT sector preference and could enable a job change or upskilling; the weekend part-time format may be more feasible given the respondent's working hours."

**Uncertainties disclosed by the LLM:**
  - Exact schedule (specific weekend hours) and location are not stated in the course text.
  - No explicit entry requirement or prior-experience requirement is listed in the document.

**Limitations disclosed by the LLM:**
  - The course description does not state whether it issues an NVQ or other formal credential.
  - It is not documented whether employer sponsorship would be available for this specific course.

#### Rank 4: `COURSE-002` — PYTHON

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Python is a core programming language used across IT occupations; this matches the respondent's stated sector interest."
  - `hopes_to_change_job` = Yes — I want to change — *relevance stated by the model:* "Learning Python could support transitioning into software roles or data-related roles, consistent with the respondent's reason for changing (career prospects/advancement)."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Members of this profile frequently pursue training and further education; short part-time programming courses are present in the catalogue."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course card indicates 'PYTHON' course, part-time, 20 students, 03 Month duration (some extracted text has unreadable fragments)." — source: COURSE-002

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is short (3 months) and part-time, it may be a practical way for the respondent to gain a concrete programming skill without a long full-time commitment." (hedged; based on: COURSE-002: part time, 03 Month duration, plans_further_edu_f = Yes)

**LLM's recommendation explanation (`why_recommended`):** "Python training is directly relevant to IT sector skills the respondent values and can be a concise route to gainable, applicable technical skills for career change or entrepreneurship."

**Uncertainties disclosed by the LLM:**
  - The retrieved course document contains some unreadable/corrupted lines; specific curriculum details, delivery times, and exact eligibility are not fully visible.
  - Location and precise schedule are not stated in the readable text.

**Limitations disclosed by the LLM:**
  - Because parts of the course card were unreadable, some course details (prerequisites, exact syllabus) could not be verified from the provided text.
  - No information on certification level or recognition beyond the card text is available.

#### Rank 5: `COURSE-057` — Multimedia & Web Design

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Multimedia and web design are subfields of IT/communications and match the respondent's sector preference."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Course content (web/multimedia design) could support creating services/products useful for a freelance or small web-design business."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Part-time weekend IT-oriented courses are common in the catalogue for respondents in this profile, suggesting such formats are typical."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course described as Computer Multimedia Designing and is a part-time weekend course." — source: COURSE-057

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start a business and the course covers multimedia/web design, it could supply practical skills usable to offer services as an entrepreneur or freelancer." (hedged; based on: ideal_work_type = Start my own business, COURSE-057: Multimedia & Web Design, part-time weekends)

**LLM's recommendation explanation (`why_recommended`):** "Multimedia & Web Design provides practical web/multimedia skills relevant to IT entrepreneurship and freelancing, and the weekend part-time delivery may fit the respondent's working schedule."

**Uncertainties disclosed by the LLM:**
  - Course syllabus detail (which specific tools or platforms are taught) is not listed in the extracted text.
  - No explicit location or entry requirement is provided.

**Limitations disclosed by the LLM:**
  - Recommendation is based on general course title and part-time status; lacking detailed syllabus or accreditation information limits certainty about specific skill outcomes.
  - No fee details are provided in the course text.


---

## 24. `nysc-34933c14-655f-4189-800f-2419775963fe` (Branch F) {#24-nysc-34933c14-655f-4189-800f-2419775963fe}

**Selection rationale (why this respondent was chosen for the batch):** F profile 2, ICT self-employed, financing obstacle

### Frozen profile membership(s)

- `F_employment_security` — Profile 2: "Predominantly permanent employment with stronger security" (dimension: Employment security and formality)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `acceptance_conditions_search` = Only a job that was stable, well paid, AND matched my qualifications
  - `expected_highest_edu_f` = Post-graduate degree
  - `hopes_to_change_job` = No — I want to stay in this job
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Start my own business
  - `income_hours_preference` = More hours and correspondingly more income
  - `plans_further_edu_f` = Yes

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `actual_hours_last_week` = 0.0
  - `area_type` = Small town
  - `district` = Gampaha
  - `had_min_wage_during_search` = Yes
  - `has_children` = No
  - `household_income` = LKR 60,000 – 120,000
  - `household_size` = 5.0
  - `household_unemployed` = 1.0
  - `household_workers` = 2.0
  - `main_business_obstacle` = Access to finance or capital
  - `monthly_income_band` = Below LKR 20,000
  - `obstacle_finding_this_job` = No education or qualifications
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My regular job or business
  - `usual_hours_per_week` = 5.0
  - `who_paid_training` = My employer
  - `willing_to_relocate_f` = No — I would not move

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `business_funding_source` = My own savings
  - `business_helpers` = Yes — both paid and unpaid workers
  - `business_profitability` = Breaking even
  - `contract_satisfaction` = Satisfied — for another reason
  - `contract_type` = No contract at all
  - `current_activity_status` = I have a job but was temporarily away from it last week
  - `edu_status` = Currently in higher education (degree or diploma)
  - `employment_service_help_f` = No — none at all
  - `employment_status` = In my own business or self-employed (no employees)
  - `enterprise_location_type` = In my own home or someone else's home
  - `enterprise_registered` = Yes — it is registered
  - `ever_refused_job_f` = Yes
  - `has_job_to_return` = Yes — I will return to my job
  - `has_second_job` = Yes
  - `hours_below_normal` = Yes — I worked fewer hours than normal
  - `interviews_before_hire` = 0.0
  - `job_security_12months` = Very likely — my job is secure
  - `jobs_applied_before_hire` = 0.0
  - `occupational_class` = Technical work (IT technician, lab technician, etc.)
  - `paid_taxes` = Yes
  - `past_edu_useful_for_job` = Very useful — directly relevant and applied daily
  - `qualification_job_match` = Very well — my qualifications are central to this job
  - `reason_below_normal_hours` = Education leave or training
  - `reason_not_union` = I have never thought about it
  - `reason_refused_job_f` = No advancement prospects
  - `reason_self_employed` = Potential for higher income
  - `reason_temp_absence` = Education leave or training
  - `received_training` = Yes
  - `registered_as_jobseeker` = No
  - `search_duration_before_hire` = Less than 1 week — I was recruited or it was immediate
  - `sector_formality` = Fully informal — no documentation, cash only
  - `training_duration` = 3 to 6 months
  - `training_provider` = My employer (on-the-job)
  - `training_type_received` = Training in new technologies
  - `union_member` = No
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `competence_growth_at_work` = Yes — I am constantly learning and growing in this role
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Yes — I know one or two people who might help
  - `job_satisfaction` = Very satisfied
  - `most_important_life_goal` = Having financial security or earning a lot
  - `most_useful_quality_for_job` = Communication and interpersonal skills
  - `move_reason` = For education or training
  - `moved_from_origin` = No — I moved from somewhere else
  - `professional_network_growth` = Yes — significantly, I have built valuable professional relationships
  - `relatedness_at_work` = Somewhat connected — reasonable working relationships
  - `work_autonomy` = Some — flexibility within defined boundaries
  - `work_motivation_type` = It aligns with my personal goals and who I want to become

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-009 (Information And Communication Technolory Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-001 (Freelancer Of Web Design & Development); COURSE-052 (Cisco Certified Network Associate); COURSE-035 (Secretary (Secretarial Practices)); COURSE-008 (Computer Hardware Technician); COURSE-022 (Computer Network Technician); COURSE-049 (Business Managemant); COURSE-058 (Computer Based Accounting); COURSE-031 (National Diploma In Television Program Production); COURSE-057 (Multimedia & Web Design)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; ideal_work_type=Start my own business; expected_highest_edu_f=Post-graduate degree; obstacle_finding_this_job=No education or qualifications; main_business_obstacle=Access to finance or capital; current_activity_status=I have a job but was temporarily away from it last week; employment_status=In my own business or self-employed (no employees); occupational_class=Technical work (IT technician, lab technician, etc.); qualification_job_match=Very well — my qualifications are central to this job; training_type_received=Training in new technologies; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** STRONG
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course explicitly advertises methods to develop one’s own business and earn both...' has low word-overlap (33%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "The course is an IT/web development course; the respondent explicitly prefers IT as their target sector."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "The course explicitly targets freelancing and starting one's own income-generating web business, matching the respondent's desire to start a business."
  - `edu_status` = Currently in higher education (degree or diploma) — *relevance stated by the model:* "The respondent is studying and may value a course that supports further education and credentialing; the course offers a certificate and practical skills."
  - `employment_status` = In my own business or self-employed (no employees) — *relevance stated by the model:* "Respondent already runs a small registered enterprise; a freelancing/web business course may build directly on that entrepreneurial activity."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Within this profile, Information technology and communications is a common ideal sector and many plan to start their own business (group tendency)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course teaches web site development, domain & hosting management, and how to set up freelancer accounts (Fiverr and others) and earn money." — source: COURSE-001
  - "Course explicitly advertises methods to develop one’s own business and earn both locally and internationally." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start their own business and already runs a registered small enterprise, this freelancing/web-development course may directly support those entrepreneurial aims by teaching practical steps (domain/hosting, freelancing platforms)." (hedged; based on: ideal_work_type = Start my own business, employment_status = In my own business or self-employed (no employees), COURSE-001 course facts about freelancing, domain/hosting and business development)

**LLM's recommendation explanation (`why_recommended`):** "This course directly teaches web development and freelancing/business setup (domain/hosting, Fiverr accounts) which aligns closely with the respondent's stated IT sector preference and desire to start their own business."

**Uncertainties disclosed by the LLM:**
  - Course fee (listed elsewhere for COURSE-001 in the course text: 20,000/=) appears in the course snapshot but broader entry/eligibility or scheduling details beyond the snapshot are not fully documented in the dataset.
  - The respondent is currently in higher education; the course duration and exact schedule compatibility with their studies is not fully documented here.

**Limitations disclosed by the LLM:**
  - While the course text lists a fee and some logistics, the retrieved document does not provide a complete schedule or formal entry requirements beyond the advertised snapshot — this dataset cannot confirm eligibility or exact time commitments.
  - Any claim that this course will guarantee business income or employment would be inappropriate; the course only provides skills and guidance as stated in the document.

#### Rank 2: `COURSE-057` — Multimedia & Web Design

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Course is in multimedia/web design within the IT field the respondent selected."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Web and multimedia skills can support freelance or small-business digital services, consistent with the respondent's entrepreneurship aim."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "High within-profile interest in IT and entrepreneurial directions supports that IT-skills training is a relevant area for youths in this group."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course advertised as Computer Multimedia Designing and Multimedia & Web Design; focused on practical, job-oriented skills; part-time weekend delivery." — source: COURSE-057

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is offered part-time on weekends and the respondent is studying and currently has a job/self-business, this weekend format may be easier to combine with existing commitments than a weekday full-time course." (hedged; based on: COURSE-057 fact: part-time, weekends, edu_status = Currently in higher education (degree or diploma), employment_status = In my own business or self-employed (no employees))

**LLM's recommendation explanation (`why_recommended`):** "The course teaches web and multimedia design skills within IT and is offered as a part-time weekend program, which plausibly supports the respondent's IT sector interest and entrepreneurial aim while being easier to combine with study/work commitments."

**Uncertainties disclosed by the LLM:**
  - Exact curriculum topics and depth (e.g., portfolio-building, freelancing business modules) beyond the brief overview are not fully detailed in the retrieved text.
  - Specific schedule dates and any entry requirements are not documented in the course extract.

**Limitations disclosed by the LLM:**
  - The course description does not list full entry requirements or a detailed syllabus in this dataset; further enquiry with NYSC would be needed to confirm fit for the respondent's current skill level.
  - No explicit claim of certification level or linkage to higher education progression is provided in the excerpt.

#### Rank 3: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Course is a comprehensive ICT diploma covering system analysis, programming, databases, networking and workplace skills in the IT sector the respondent selected."
  - `plans_further_edu_f` = Yes — *relevance stated by the model:* "Respondent plans further education; a National Diploma may align with that intention."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Within this profile, many respondents reported IT as their ideal sector and high uptake of training for current jobs, indicating training pathways in IT are common."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers System Analysis & Design, Software Programming, Database Systems, Web Programming, LAN and workplace communication — a broad ICT diploma; full-time weekday delivery; awards competency Level 5 under NVQ standards." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course provides broad ICT competencies and the respondent is in higher education and works in a technical/IT role, the diploma may help formalise and deepen skills and support future education goals." (hedged; based on: COURSE-006 facts about diploma content and NVQ Level 5, edu_status = Currently in higher education (degree or diploma), occupational_class = Technical work (IT technician, lab technician, etc.))

**LLM's recommendation explanation (`why_recommended`):** "A comprehensive ICT diploma aligns with the respondent's stated IT sector preference and further-education intention; it covers both technical and workplace skills that could support higher qualifications and entrepreneurial competence."

**Uncertainties disclosed by the LLM:**
  - The course is full-time on weekdays; the respondent is currently studying and has business activity — compatibility with their schedule is uncertain.
  - The retrieved document does not specify explicit entry prerequisites beyond the diploma description.

**Limitations disclosed by the LLM:**
  - Full-time weekday format may be harder to combine with the respondent's ongoing higher-education studies and business commitments; this is a scheduling concern, not a content mismatch.
  - The dataset does not provide complete details on fees, exact timetable, or formal entry criteria for assessing eligibility.

#### Rank 4: `COURSE-073` — Java Programming With Software Applications Development

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "This course is software-development focused within the IT sector the respondent prefers."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Software application development skills could support creating products/services for an entrepreneurial software business or freelancing."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `F_employment_security_p2`, role=supporting_context_only: "Profile respondents commonly work in technical IT roles and receive on-the-job training; formal programming training is consistent with group training patterns."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course teaches Java and software application development; part-time weekend delivery is noted." — source: COURSE-073

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course focuses on Java and application development and is offered part-time on weekends, it may be practical for the respondent to acquire programming skills while continuing studies/business activity." (hedged; based on: COURSE-073 part-time weekend fact, edu_status = Currently in higher education (degree or diploma), employment_status = In my own business or self-employed (no employees))

**LLM's recommendation explanation (`why_recommended`):** "Java and software-application development are relevant technical skills within the respondent's chosen IT sector and can support software-based entrepreneurship or freelance development work."

**Uncertainties disclosed by the LLM:**
  - The course description in the retrieved text is brief; the exact syllabus depth, prerequisites, and outcomes are not fully specified.
  - Compatibility with the respondent's exact study schedule is not confirmed.

**Limitations disclosed by the LLM:**
  - The course document does not provide detailed prerequisites or certification-level information in this extract; further clarification from NYSC would be helpful.
  - Acquiring Java skills alone may not be sufficient to guarantee successful business creation; business/market skills and experience also matter.


---

## 25. `nysc-27b17da2-64b7-4031-b4ac-3205b9b2a735` (Branch G) {#25-nysc-27b17da2-64b7-4031-b4ac-3205b9b2a735}

**Selection rationale (why this respondent was chosen for the batch):** G economic_role p1 / future_engagement p1, ICT, caregiving time-constraint

### Frozen profile membership(s)

- `G_economic_role` — Profile 1: "Predominantly family/partner-supported non-provider" (dimension: Household economic role and dependency)
- `G_future_engagement` — Profile 1: "Work-and-education engaged, mostly prior work experience" (dimension: Future engagement and prior work experience)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_g` = Post-graduate degree
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Work for the government or public sector
  - `wants_further_edu` = Yes
  - `wants_to_work_future` = Yes — I want to work at some point

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Metropolitan suburb
  - `district` = Colombo
  - `has_children` = No
  - `household_income` = Above LKR 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 2.0
  - `household_workers` = 2.0
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My parents or family
  - `reason_not_in_labour_force` = Other reason
  - `support_for_engagement` = A great deal — people would actively support and encourage me
  - `time_use_decision_maker` = Family obligations — caregiving responsibilities determine my schedule

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `current_activity_status` = Recently finished education — plan to start looking for work
  - `edu_status` = Currently in higher education (degree or diploma)
  - `ever_worked` = Yes — I have worked before
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = No — I have no one I could call on
  - `employment_self_efficacy` = Very confident — I believe I could find something suitable
  - `future_orientation_g` = I have a clear plan and I am working toward specific goals even now
  - `labour_market_connection` = Very connected — I hear about jobs and training opportunities regularly
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = IT and digital skills
  - `moved_from_origin` = Yes — I grew up here and still live here

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-009 (Information And Communication Technolory Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-035 (Secretary (Secretarial Practices)); COURSE-052 (Cisco Certified Network Associate); COURSE-058 (Computer Based Accounting); COURSE-001 (Freelancer Of Web Design & Development); COURSE-002 (PYTHON); COURSE-057 (Multimedia & Web Design); COURSE-008 (Computer Hardware Technician); COURSE-053 (Computer Applications Assistant); COURSE-031 (National Diploma In Television Program Production)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; ideal_work_type=Work for the government or public sector; expected_highest_edu_g=Post-graduate degree; reason_not_in_labour_force=Other reason; current_activity_status=Recently finished education — plan to start looking for work; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "The course is explicitly ICT-focused and therefore directly matches the respondent's stated sector preference."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Respondent wants further education; this is a full-time diploma that builds higher-level vocational qualifications."
  - `wants_to_work_future` = Yes — I want to work at some point — *relevance stated by the model:* "Respondent intends to work in future; ICT vocational training may support that transition."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "Profile shows high rates of wanting further education and prior work experience (work-and-education engaged)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers system analysis & design, software programming, database systems, web programming, LAN and related ICT topics." — source: COURSE-006
  - "Described as a full time course held on weekdays and leads to National Vocational Qualifications Competency Level 5." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent explicitly stated an interest in IT and communications, this full-time diploma appears directly relevant to that stated sector preference." (hedged; based on: ideal_sector = Information technology and communications, COURSE-006 course topics (system analysis, programming, databases, web programming))
  - "Because the respondent wants further education and aims for a high educational level (post-graduate), completing a recognised vocational diploma may support progression to higher study or strengthen an employment application." (hedged; based on: wants_further_edu = Yes, expected_highest_edu_g = Post-graduate degree, COURSE-006 leads to NVQ Competency Level 5)

**LLM's recommendation explanation (`why_recommended`):** "Direct sector match: respondent named IT & communications and the course explicitly teaches core ICT skills and higher-level vocational content (NVQ Level 5). It also supports further education and employment intent."

**Uncertainties disclosed by the LLM:**
  - Course fee, precise schedule dates, and entry requirements are not stated in the course document.
  - Course is full-time on weekdays; the respondent reported family obligations determine schedule, so schedule compatibility is uncertain.

**Limitations disclosed by the LLM:**
  - The course document does not provide fee or entry-requirement information.
  - Full-time weekday format may be harder to combine with caregiving-determined schedules; this is an uncertainty, not a disqualifier.

#### Rank 2: `COURSE-009` — Information And Communication Technolory Technician

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Course content focuses on practical ICT tasks consistent with the respondent's sector preference."
  - `wants_to_work_future` = Yes — I want to work at some point — *relevance stated by the model:* "Practical technician skills could help the respondent enter the IT workforce."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - *(none cited — empty for this recommendation)*

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers word processing, spreadsheets, presentations, databases, internet/email, OS installation, network troubleshooting, web page design and basic software solutions." — source: COURSE-009
  - "Listed as a full time course held on weekdays." — source: COURSE-009

**[LLM INFERENCE] Contextual inferences made:**
  - "These practical ICT skills may be useful for someone seeking entry-level IT roles or further technical training, given the respondent's stated desire to work in IT." (hedged; based on: ideal_sector = Information technology and communications, COURSE-009 course topics (office software, networking, web pages, basic software))

**LLM's recommendation explanation (`why_recommended`):** "The course offers hands-on ICT technician skills that map directly to the respondent's stated sector interest and work intent."

**Uncertainties disclosed by the LLM:**
  - No fee or specific entry requirement information is provided in the course document.
  - Full-time weekday schedule may conflict with the respondent's caregiving-determined schedule; schedule compatibility is unknown.

**Limitations disclosed by the LLM:**
  - The course document lacks explicit entry criteria and fee details.
  - Format is full-time; whether the respondent can attend full-time is unknown and should be confirmed with the provider.

#### Rank 3: `COURSE-073` — Java Programming With Software Applications Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Java programming and software application development are core IT skills matching the respondent's sector preference."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "A technical programming course supports further technical education and employability in IT."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - *(none cited — empty for this recommendation)*

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course provides theoretical knowledge and job-oriented practical skills in Java and software applications development." — source: COURSE-073
  - "This is a part-time course held on weekends." — source: COURSE-073

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent reported family obligations determine their schedule, the course's part-time weekend format may be easier to combine with those responsibilities than a weekday full-time course." (hedged; based on: time_use_decision_maker = Family obligations — caregiving responsibilities determine my schedule, COURSE-073 is part time on weekends)
  - "Programming skills taught in this course may support the respondent's aim to work in IT and could complement higher education goals." (hedged; based on: ideal_sector = Information technology and communications, wants_further_edu = Yes, COURSE-073 course topic = Java programming)

**LLM's recommendation explanation (`why_recommended`):** "Strong topical match: Java and software development directly align with the respondent's IT sector interest; part-time weekend delivery may better fit caregiving-constrained schedules."

**Uncertainties disclosed by the LLM:**
  - No explicit fee or entry requirement is provided in the course document.
  - Although weekend format may be more convenient, actual schedule compatibility with the respondent's caregiving duties is uncertain.

**Limitations disclosed by the LLM:**
  - Course document does not list entry requirements or fees.
  - Being a technical programming course, prior programming experience requirements (if any) are not documented here.

#### Rank 4: `COURSE-052` — Cisco Certified Network Associate

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Networking is a core IT area that aligns with the respondent's stated sector."
  - `wants_to_work_future` = Yes — I want to work at some point — *relevance stated by the model:* "Cisco certification-oriented skills are commonly applied in IT roles and could support employment prospects."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - *(none cited — empty for this recommendation)*

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course presents CISCO Network Associate training with theoretical and job-oriented practical content." — source: COURSE-052
  - "This is a part time course which will be held on weekends." — source: COURSE-052

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is part-time on weekends, it may be easier to combine with caregiving duties than a weekday full-time course, though actual compatibility is unknown." (hedged; based on: time_use_decision_maker = Family obligations — caregiving responsibilities determine my schedule, COURSE-052 is part time on weekends)

**LLM's recommendation explanation (`why_recommended`):** "Networking training matches the respondent's IT sector preference and is targeted technical training that could support entry into IT roles."

**Uncertainties disclosed by the LLM:**
  - Course document does not show fees, entry prerequisites, or exact schedule details beyond 'weekends'.
  - Whether the respondent has any prior networking knowledge required by the course is not recorded here.

**Limitations disclosed by the LLM:**
  - No entry-requirement or fee information in the course text.
  - The course's part-time weekend schedule may or may not fit the respondent's real-world caregiving constraints; this must be confirmed.

#### Rank 5: `COURSE-053` — Computer Applications Assistant

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Course provides core computer application skills relevant to many IT roles and office-based public sector positions."
  - `ideal_work_type` = Work for the government or public sector — *relevance stated by the model:* "Computer applications and MS Office skills are commonly required in government/public-sector administrative roles."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "This profile shows a substantial share believing a university degree is needed for decent jobs and being engaged with further education; practical application skills can complement formal education."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course overview lists ICT introduction, MS-Office, and using internet & e-mail; part-time on weekends." — source: COURSE-053

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to work for the government/public sector and listed IT/digital skills as important, basic computer application training may be practical for public-sector administrative roles." (hedged; based on: ideal_work_type = Work for the government or public sector, most_useful_quality_for_job = IT and digital skills, COURSE-053 topics (MS-Office, internet & e-mail))
  - "Weekend, part-time delivery may be easier to fit around caregiving-influenced schedules than weekday full-time courses." (hedged; based on: time_use_decision_maker = Family obligations — caregiving responsibilities determine my schedule, COURSE-053 is part time on weekends)

**LLM's recommendation explanation (`why_recommended`):** "Offers foundational computer/office skills that map to both IT sector preference and to typical public-sector administrative job requirements; weekend part-time format may aid feasibility."

**Uncertainties disclosed by the LLM:**
  - No fee, duration, or explicit entry requirements are provided in the course document.
  - The exact level of qualification provided and how it maps to government hiring criteria is not stated.

**Limitations disclosed by the LLM:**
  - Course document lacks detailed information about fees and formal entry requirements.
  - This is an introductory/office-skills course; if the respondent seeks advanced technical certification or degree-level progression, additional study would be needed.


---

## 26. `nysc-31cab333-afc9-48c5-baec-8ba48e14defb` (Branch G) {#26-nysc-31cab333-afc9-48c5-baec-8ba48e14defb}

**Selection rationale (why this respondent was chosen for the batch):** G p1/p2, Personal services/beauty, seasonal-worker, low engagement

### Frozen profile membership(s)

- `G_economic_role` — Profile 1: "Predominantly family/partner-supported non-provider" (dimension: Household economic role and dependency)
- `G_future_engagement` — Profile 2: "Low/uncertain engagement, mostly no prior work experience" (dimension: Future engagement and prior work experience)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `ideal_sector` = Personal services (beauty, fitness, wellness)
  - `ideal_work_type` = Work in a family business (non-farming)
  - `wants_further_edu` = Not sure yet
  - `wants_to_work_future` = No — I do not want to work

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Small town
  - `district` = Jaffna
  - `has_children` = No
  - `household_income` = LKR 30,000 – 60,000
  - `household_size` = 23.0
  - `household_unemployed` = 2
  - `household_workers` = 23
  - `primary_earner_status` = No — someone else is the main provider
  - `primary_income_source` = My partner or spouse
  - `reason_not_in_labour_force` = Awaiting the busy season (seasonal worker)
  - `support_for_engagement` = Some — I would have moderate support
  - `time_use_decision_maker` = Family obligations — caregiving responsibilities determine my schedule

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `current_activity_status` = Not working — looking for work or trying to set up a business
  - `edu_end_year` = 2022
  - `edu_status` = I have completed my education and am not currently studying
  - `ever_worked` = No — I have never worked
  - `highest_edu_completed` = Vocational certificate or NVQ
  - `spell1_activity` = Self-employed / running own business
  - `spell1_contract` = Oral contract — temporary (12–36 months)
  - `spell1_end_reason` = Temporary job ended
  - `spell1_is_current` = No — it ended and I moved on to something else
  - `spell1_satisfaction` = Somewhat unsatisfied
  - `spell2_activity` = Home duties — caring for family or household
  - `spell2_is_current` = No — it ended and I moved on again
  - `spell3_activity` = Working for a salary or wage (employed)
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_first_married` = 23
  - `age_group` = 18 – 21 years
  - `edu_min_for_decent_job` = O/L level
  - `employment_network_quality` = Yes — I know one or two people who might help
  - `employment_self_efficacy` = Not very confident — I have significant doubts
  - `future_orientation_g` = I want to change my situation but feel stuck and unsure how to start
  - `labour_market_connection` = Weakly connected — I rarely receive useful information
  - `most_important_life_goal` = Having leisure, freedom, and personal time
  - `most_useful_quality_for_job` = A good general education
  - `move_reason` = For work or employment reasons
  - `moved_from_origin` = No — I moved from somewhere else
  - `spouse_activity` = Working for a salary or wage

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-014 (Hair Dresser); COURSE-049 (Business Managemant); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-054 (Computer Certificate); COURSE-003 (Certificate In English Communication Essentials.); COURSE-069 (Hair Dresser); COURSE-048 (Bridal Dresser); COURSE-010 (Beautician); COURSE-046 (Beautician); COURSE-001 (Freelancer Of Web Design & Development); COURSE-006 (National Diploma In Information & Communication Technology); COURSE-011 (Baker); COURSE-033 (Plumber); COURSE-020 (Landscape Development Assistant); COURSE-021 (Automobile Electrician)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Personal services (beauty, fitness, wellness); ideal_work_type=Work in a family business (non-farming); reason_not_in_labour_force=Awaiting the busy season (seasonal worker); current_activity_status=Not working — looking for work or trying to set up a business; highest_edu_completed=Vocational certificate or NVQ; edu_status=I have completed my education and am not currently studying; [sector-vocabulary expansion terms: bridal, hair]

#### Rank 1: `COURSE-046` — Beautician (part time / weekends)

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Personal services (beauty, fitness, wellness) — *relevance stated by the model:* "The course teaches beautician skills which directly match the respondent's stated preferred sector."
  - `ideal_work_type` = Work in a family business (non-farming) — *relevance stated by the model:* "Beautician skills are commonly usable in small/family-run personal services businesses; this supports relevance to working in a family business."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p2`, role=supporting_context_only: "Profile members often report low/uncertain future engagement and little prior work experience; this may contextualise the respondent's low confidence and need for accessible training."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Beautician course overview includes facial, manicure, pedicure, makeup, flower bouquets & bridal dressing." — source: COURSE-046
  - "This is a part time course which will be held on weekends." — source: COURSE-046

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent reported that 'Family obligations — caregiving responsibilities determine my schedule', a part-time weekend format may be easier to combine with those responsibilities." (hedged; based on: time_use_decision_maker = Family obligations — caregiving responsibilities determine my schedule, COURSE-046: part time / weekends)
  - "Because the respondent wants to work in a family business, learning a widely-used personal services skill like beautician work could be useful for operating or contributing to such a business." (hedged; based on: ideal_work_type = Work in a family business (non-farming), COURSE-046: beautician skills taught (makeup, manicure, bridal dressing))

**LLM's recommendation explanation (`why_recommended`):** "Direct sector match: the respondent explicitly named personal services (beauty, fitness, wellness). The course teaches core beautician skills (facial, manicure, pedicure, makeup, bridal dressing) and is offered part-time on weekends, which may better fit the respondent's caregiving-determined schedule and support participation while managing family obligations."

**Uncertainties disclosed by the LLM:**
  - Course language is Sinhala (documented), which may affect accessibility if respondent prefers another language; respondent language preference was not provided.
  - Exact location of course delivery and any entry requirements are not stated in the course document.
  - No fee information is provided in the course document.

**Limitations disclosed by the LLM:**
  - The respondent indicated 'I do not want to work' in wants_to_work_future; recommendation relies on her stated ideal_sector and ideal_work_type rather than current intent to work.
  - Course detail lists part-time schedule but not specific times/dates; weekend timing may still conflict with the respondent's caregiving schedule.

#### Rank 2: `COURSE-014` — Hair Dresser (full time weekdays)

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Personal services (beauty, fitness, wellness) — *relevance stated by the model:* "Hairdressing is a core personal-services skill area matching the respondent's preferred sector."
  - `ideal_work_type` = Work in a family business (non-farming) — *relevance stated by the model:* "Hairdressing skills can be applied in small or family-run salons, matching the respondent's stated ideal work type."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_economic_role_p1`, role=supporting_context_only: "Profile members are often not main household providers and may rely on family support; this may affect how training could be used (e.g., within a family business)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers straightening, hair coloring, hair stylist and hair setting, hair treatment, perming, hair cutting." — source: COURSE-014
  - "This is a full time course which will be held on weekdays." — source: COURSE-014

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent named working in a family business and personal-services as preferred, hairdressing skills may be applicable if the family business is in personal services or could expand into it." (hedged; based on: ideal_work_type = Work in a family business (non-farming), COURSE-014: hairdressing skills taught (coloring, cutting, styling))

**LLM's recommendation explanation (`why_recommended`):** "Strong content alignment with the respondent's stated interest in personal services: the course teaches multiple hairdressing skills that are directly relevant to beauty/wellness work and to family-run salons or services."

**Uncertainties disclosed by the LLM:**
  - Course is full-time on weekdays which may conflict with the respondent's caregiving-determined schedule (time_use_decision_maker).
  - Course language is Sinhala; respondent language preference is not recorded.
  - No fee information or explicit entry requirements are present in the course document.

**Limitations disclosed by the LLM:**
  - Because the course is full-time weekdays, it may be less feasible for someone whose schedule is determined by family caregiving unless other arrangements exist.
  - The respondent indicated 'wants_to_work_future: No', so motivation to enrol is uncertain; recommendation is based on stated sector and work-type preferences rather than current employment intent.

#### Rank 3: `COURSE-048` — Bridal Dresser (part time / weekends)

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Personal services (beauty, fitness, wellness) — *relevance stated by the model:* "Bridal dressing is a specialised personal-services skill aligned with the respondent's stated sector preference."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p2`, role=supporting_context_only: "Profile members often have little prior paid work experience; a short practical course could help bridge skills gaps."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Bridal Dresser course provides theoretical knowledge and job-oriented practical skills; it is a part time course held on weekends." — source: COURSE-048

**[LLM INFERENCE] Contextual inferences made:**
  - "Given the course is offered on weekends, it may be more compatible with the respondent's stated caregiving-driven schedule than weekday full-time options." (hedged; based on: time_use_decision_maker = Family obligations — caregiving responsibilities determine my schedule, COURSE-048: part time / weekends)

**LLM's recommendation explanation (`why_recommended`):** "The respondent named personal services as their ideal sector; bridal dressing is a targeted skill within beauty services and the part-time/weekend schedule may fit caregiving constraints better than weekday full-time courses."

**Uncertainties disclosed by the LLM:**
  - Exact course timing and location are not provided in the document.
  - Language of delivery is Sinhala; respondent language preference is not documented.
  - No fee or entry-requirement data are present in the course text.

**Limitations disclosed by the LLM:**
  - Bridal dressing is a specialised sub-field; if the respondent prefers more general beauty skills, they might prefer a broader beautician course.
  - The respondent's current stated lack of desire to work means interest in enrolling may be limited; this recommendation uses stated sector preference rather than current intent.

#### Rank 4: `COURSE-049` — Business Managemant (part time / weekends)

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_work_type` = Work in a family business (non-farming) — *relevance stated by the model:* "Business management content can support running or improving a family business, matching the respondent's stated ideal work type."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_economic_role_p1`, role=supporting_context_only: "Profile members are often family-supported and may aim to work within family structures; business skills could support small/family enterprises."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Business Management course gives theoretical knowledge and job-oriented practical that is necessary for employment and higher education; it is a part time course held on weekends." — source: COURSE-049

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent expressed an interest in working in a family business, business management training may help them run or contribute to that business (e.g., bookkeeping, basic management)." (hedged; based on: ideal_work_type = Work in a family business (non-farming), COURSE-049: Business Management content and part-time/weekend format)

**LLM's recommendation explanation (`why_recommended`):** "Although not a direct beauty-sector skill, business management training could be useful if the respondent intends to operate or support a family-run personal-services business (e.g., salon management, entrepreneurship). The weekend part-time format may fit caregiving responsibilities."

**Uncertainties disclosed by the LLM:**
  - Course title and description are generic; the syllabus detail (specific business topics covered) is not provided.
  - No fee, exact schedule, or entry requirements are specified in the document.
  - It is uncertain whether the respondent wants to work now (they said 'I do not want to work'), so motivation to take a business course is unclear.

**Limitations disclosed by the LLM:**
  - Recommendation for a management course rests on inferred entrepreneurial or family-business support needs rather than an explicit respondent statement about wanting business training.
  - If the respondent prefers hands-on beauty skills rather than business topics, this course may be less directly useful.


---

## 27. `nysc-0717027e-65cc-4b29-9b44-17593f66aaf5` (Branch G) {#27-nysc-0717027e-65cc-4b29-9b44-17593f66aaf5}

**Selection rationale (why this respondent was chosen for the batch):** G p2/p1, ICT, 'no suitable work in area' barrier

### Frozen profile membership(s)

- `G_economic_role` — Profile 2: "Predominantly self-income provider/contributor" (dimension: Household economic role and dependency)
- `G_future_engagement` — Profile 1: "Work-and-education engaged, mostly prior work experience" (dimension: Future engagement and prior work experience)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_g` = Post-graduate degree
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Start my own business
  - `wants_further_edu` = Yes
  - `wants_to_work_future` = Yes — I want to work at some point

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Small town
  - `district` = Colombo
  - `has_children` = No
  - `household_income` = LKR 60,000 – 120,000
  - `household_size` = 4.0
  - `household_unemployed` = 1.0
  - `household_workers` = 2.0
  - `primary_earner_status` = Shared — several people contribute roughly equally
  - `primary_income_source` = My regular job or business
  - `reason_not_in_labour_force` = Believe there is no suitable work available in this area
  - `support_for_engagement` = Some — I would have moderate support
  - `time_use_decision_maker` = I decide for myself — I have full autonomy over my time

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `current_activity_status` = Home duties — looking after family or the household
  - `edu_status` = Currently in higher education (degree or diploma)
  - `ever_worked` = Yes — I have worked before
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 26 – 29 years
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `employment_self_efficacy` = Very confident — I believe I could find something suitable
  - `future_orientation_g` = I have a general sense of direction but no concrete plan yet
  - `labour_market_connection` = Very connected — I hear about jobs and training opportunities regularly
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = Ambition and drive
  - `moved_from_origin` = Yes — I grew up here and still live here

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-001 (Freelancer Of Web Design & Development); COURSE-009 (Information And Communication Technolory Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-035 (Secretary (Secretarial Practices)); COURSE-052 (Cisco Certified Network Associate); COURSE-049 (Business Managemant); COURSE-058 (Computer Based Accounting); COURSE-002 (PYTHON); COURSE-057 (Multimedia & Web Design); COURSE-008 (Computer Hardware Technician); COURSE-053 (Computer Applications Assistant)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; ideal_work_type=Start my own business; expected_highest_edu_g=Post-graduate degree; reason_not_in_labour_force=Believe there is no suitable work available in this area; current_activity_status=Home duties — looking after family or the household; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** STRONG
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course teaches web development, domain & hosting management, setting up Fiverr a...' has low word-overlap (29%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported); course_fact 'Course duration shown (3 months) and targets ages 15-45; contains explicit entre...' has low word-overlap (28%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Directly names the IT sector, which is the primary topic taught by this web design & development freelancing course."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Respondent wants to start their own business; this course explicitly teaches freelancing and ways to earn (domestic and international), matching entrepreneurial intent."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Indicates willingness to take additional study, supporting enrollment in short practical courses."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "Work-and-education engaged, high employment self-efficacy and connection to labour-market information"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course teaches web development, domain & hosting management, setting up Fiverr and other accounts and ways to earn money; explicitly targets developing one's own business and earning domestically and abroad." — source: COURSE-001
  - "Course duration shown (3 months) and targets ages 15-45; contains explicit entrepreneurship/freelancing content and practical site hosting/management training." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent said they want to start their own business and this course explicitly focuses on freelancing and building a web-income business, it appears directly aligned with the respondent's stated entrepreneurial intention." (hedged; based on: ideal_work_type = Start my own business, COURSE-001: course description teaching freelancing, domain/hosting, Fiverr)
  - "Because the respondent is currently in higher education and reported willingness to pursue further education, a short (3-month) vocational course may be practical for combining with study, though the respondent's exact schedule constraints are unknown." (hedged; based on: edu_status = Currently in higher education (degree or diploma), COURSE-001: 03 Month duration listed)

**LLM's recommendation explanation (`why_recommended`):** "Strong content overlap: respondent wants IT sector work and to start their own business; this course explicitly teaches web development plus freelancing/marketplace setup and income-generation methods, matching both sector and entrepreneurial intent."

**Uncertainties disclosed by the LLM:**
  - Course fee is documented in the course text (20,000/=) but broader eligibility/entry requirements and exact schedule details beyond start date are not fully documented in the course card.
  - How the course schedule (exact session times) would combine with the respondent's current commitments is not specified.

**Limitations disclosed by the LLM:**
  - The course document lists fee and some logistics but does not state formal entry requirements or accreditation specifics beyond a certificate; the respondent's formal eligibility is not asserted here.
  - The course's language and exact classroom location are not detailed beyond contact numbers; local availability in the respondent's neighbourhood is not confirmed.

#### Rank 2: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Direct sector preference matches the broad ICT content of this diploma."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Respondent indicated desire for further education, consistent with enrolling in a diploma-level programme."
  - `expected_highest_edu_g` = Post-graduate degree — *relevance stated by the model:* "High educational aspiration suggests receptivity to formal diploma-level training that can contribute to further study or professional development."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "Many in this profile report being 'work-and-education engaged' and open to further education."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Covers system analysis & design, software programming, database systems, web programming, LAN, workplace communication and planning — a comprehensive ICT diploma." — source: COURSE-006
  - "Document states this is a full time course held on weekdays and aims to develop entrepreneurial abilities as well as technical skills." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent aspires to the IT sector and to further education (including postgraduate aspirations), a formal diploma that offers Level 5 competency may support both vocational skill-building and longer-term academic/professional objectives." (hedged; based on: ideal_sector = Information technology and communications, wants_further_edu = Yes, COURSE-006: National Diploma content and Level 5 competency claim)
  - "Because the course is full-time on weekdays and the respondent reports autonomy over time, full-time attendance may be feasible for them, though their current study and household duties create unknown scheduling constraints." (hedged; based on: time_use_decision_maker = I decide for myself — I have full autonomy over my time, edu_status = Currently in higher education (degree or diploma), COURSE-006: full time, weekdays)

**LLM's recommendation explanation (`why_recommended`):** "The diploma provides wide-ranging ICT technical skills (programming, databases, web, networking) that match the respondent's stated IT sector interest and desire for further education; the document also emphasises entrepreneurial abilities, aligning with the respondent's business intention."

**Uncertainties disclosed by the LLM:**
  - The course is described as full-time on weekdays; the respondent's exact availability and whether they can accommodate full-time weekday study alongside current commitments is unknown.
  - Specific entry requirements, fees, and exact campus/location details are not provided in the course text.

**Limitations disclosed by the LLM:**
  - Full-time weekday schedule may be harder to combine with other study or responsibilities; this is not a disqualifier but should be checked with the respondent.
  - Course document does not list explicit entry criteria or fee amounts in the extracted text; eligibility and costs need confirmation with NYSC directly.

#### Rank 3: `COURSE-073` — Java Programming With Software Applications Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent's sector preference aligns with programming/software development content taught in this Java course."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Indicates willingness to take technical training that could support career or business development."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "Profile shows higher employment self-efficacy and connection to labour-market information, suggesting receptivity to technical upskilling."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Java course provides theoretical and practical skills in software applications development; described as a part-time weekend course." — source: COURSE-073

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent has an IT sector preference and wants further education, a part-time weekend programming course could help them develop technical skills useful for starting an IT business or freelancing." (hedged; based on: ideal_sector = Information technology and communications, wants_further_edu = Yes, COURSE-073: Java course content and part-time weekends format)

**LLM's recommendation explanation (`why_recommended`):** "Provides focused programming skills (Java/software app development) directly relevant to IT-sector ambitions and potentially useful for building products/services in an entrepreneurial venture; part-time weekend format may be easier to combine with other commitments."

**Uncertainties disclosed by the LLM:**
  - Course document does not list specific prerequisites or detailed syllabus items beyond the general description.
  - Exact weekend schedule (times/dates) and fees are not specified in the extracted text.

**Limitations disclosed by the LLM:**
  - While programming skills are relevant, the course description does not explicitly cover entrepreneurship or freelancing platforms; respondent seeking business-specific training may need supplemental entrepreneurial modules.
  - No explicit entry requirements listed in the course text; eligibility should be checked.

#### Rank 4: `COURSE-002` — PYTHON

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Python programming is a core IT skill that matches the respondent's sector preference."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Respondent's willingness to study further supports enrollment in a short technical course like Python."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "Profile tendency toward wanting further education and being work-engaged supports short technical upskilling."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course titled 'PYTHON' with part-time attendance, 20-student capacity, and 3-month duration; described as learning Python from beginning." — source: COURSE-002

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants IT-sector skills and further education, a short part-time Python course may be useful to develop programming ability that supports freelancing or building an IT business." (hedged; based on: ideal_sector = Information technology and communications, wants_further_edu = Yes, COURSE-002: Part-time, 03 Month Python course)

**LLM's recommendation explanation (`why_recommended`):** "Short, part-time Python training directly develops an in-demand IT skill that can support software freelancing, data-related work, or product development — all relevant to IT-sector entrepreneurial aims."

**Uncertainties disclosed by the LLM:**
  - The course card has some unreadable portions and limited detail about syllabus depth, prerequisites, fees, and schedule.
  - Entry requirements and exact delivery modality beyond 'Part Time' are not fully documented.

**Limitations disclosed by the LLM:**
  - Incomplete document text (catalogue card had uncertainty markers) limits certainty about exact syllabus and outcomes.
  - Course does not explicitly state entrepreneurship/freelancing content; respondent may need additional business/marketplace skills.

#### Rank 5: `COURSE-057` — Multimedia & Web Design

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Course topic (multimedia and web design) falls within IT and communications."
  - `ideal_work_type` = Start my own business — *relevance stated by the model:* "Web/multimedia design skills can be used to offer freelance or business services, aligning with entrepreneurial intent."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_economic_role_p2`, role=supporting_context_only: "Profile shows many members seek entrepreneurial skills and have connections to labour-market information (supporting practical training relevance)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course described as 'Computer Multimedia Designing' with part-time weekend delivery and practical, job-oriented focus." — source: COURSE-057

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants to start a business in the IT sector, multimedia and web design skills may support creating products/services or offering freelance client work." (hedged; based on: ideal_work_type = Start my own business, ideal_sector = Information technology and communications, COURSE-057: Multimedia & Web Design content and weekend part-time format)

**LLM's recommendation explanation (`why_recommended`):** "Practical multimedia and web design skills are relevant to IT-sector entrepreneurship and freelancing; part-time weekend scheduling could help combine training with other commitments."

**Uncertainties disclosed by the LLM:**
  - The course summary does not list a detailed syllabus or explicit entrepreneurship/freelancing modules.
  - Fees, exact schedule, and entry requirements are not provided in the extracted text.

**Limitations disclosed by the LLM:**
  - Course appears focused on design skills; respondent seeking business formation or marketplace monetization training may need supplementary business management content.
  - Location and precise timing are not documented; local availability should be checked.


---

## 28. `nysc-27c2ff48-e39c-4db3-aa11-a149d76be479` (Branch G) {#28-nysc-27c2ff48-e39c-4db3-aa11-a149d76be479}

**Selection rationale (why this respondent was chosen for the batch):** G p2/p1, ICT, caregiving + shared provider

### Frozen profile membership(s)

- `G_economic_role` — Profile 2: "Predominantly self-income provider/contributor" (dimension: Household economic role and dependency)
- `G_future_engagement` — Profile 1: "Work-and-education engaged, mostly prior work experience" (dimension: Future engagement and prior work experience)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_g` = Bachelor's degree
  - `ideal_sector` = Information technology and communications
  - `ideal_work_type` = Work for a local private Sri Lankan company
  - `wants_further_edu` = Yes
  - `wants_to_work_future` = Yes — I want to work at some point

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Large city
  - `district` = Kalutara
  - `has_children` = No
  - `household_income` = LKR 120,000 – 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 1.0
  - `household_workers` = 2.0
  - `primary_earner_status` = Shared — several people contribute roughly equally
  - `primary_income_source` = My regular job or business
  - `reason_not_in_labour_force` = Personal or family responsibilities (caring for children, elderly, etc.)
  - `support_for_engagement` = A great deal — people would actively support and encourage me
  - `time_use_decision_maker` = Family obligations — caregiving responsibilities determine my schedule

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `current_activity_status` = Recently finished education — plan to start looking for work
  - `edu_status` = Currently in higher education (degree or diploma)
  - `ever_worked` = Yes — I have worked before
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_group` = 22 – 25 years
  - `edu_min_for_decent_job` = University degree
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `employment_self_efficacy` = Very confident — I believe I could find something suitable
  - `future_orientation_g` = I want to change my situation but feel stuck and unsure how to start
  - `labour_market_connection` = Very connected — I hear about jobs and training opportunities regularly
  - `most_important_life_goal` = Having leisure, freedom, and personal time
  - `most_useful_quality_for_job` = IT and digital skills
  - `moved_from_origin` = Yes — I grew up here and still live here

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-059 (Non-Liner Video Editing With Digital 3D Animation); COURSE-055 (Computer Hardware Technician); COURSE-073 (Java Programming With Software Applications Development); COURSE-009 (Information And Communication Technolory Technician); COURSE-056 (Computer Hardware And Network Technician); COURSE-035 (Secretary (Secretarial Practices)); COURSE-052 (Cisco Certified Network Associate); COURSE-058 (Computer Based Accounting); COURSE-001 (Freelancer Of Web Design & Development); COURSE-002 (PYTHON); COURSE-057 (Multimedia & Web Design); COURSE-008 (Computer Hardware Technician); COURSE-053 (Computer Applications Assistant); COURSE-031 (National Diploma In Television Program Production)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Information technology and communications; ideal_work_type=Work for a local private Sri Lankan company; expected_highest_edu_g=Bachelor's degree; reason_not_in_labour_force=Personal or family responsibilities (caring for children, elderly, etc.); current_activity_status=Recently finished education — plan to start looking for work; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: accounting, animation, autocad, cisco, communication, computer, database, graphics, hardware, internet, java, management, network, office, programming, python, software, video editing, web design]

#### Rank 1: `COURSE-006` — National Diploma In Information & Communication Technology

**Evidence strength:** STRONG
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Direct match to the course's IT/ICT subject matter; allowed to select programme content based on direct preference."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Respondent stated they want further education, supporting recommendation of a formal diploma course."
  - `wants_to_work_future` = Yes — I want to work at some point — *relevance stated by the model:* "Interest in working aligns with taking vocational training aimed at employment."
  - `ideal_work_type` = Work for a local private Sri Lankan company — *relevance stated by the model:* "Shows preference for local private-sector employment where ICT skills are often relevant."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "Work-and-education engaged, high self-efficacy and strong connection to labour-market information (profile-level tendency)"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network and workplace communication/management modules." — source: COURSE-006
  - "Described as a full time course held on weekdays." — source: COURSE-006
  - "Aims to provide theoretical knowledge and job-oriented practical skills; competency Level 5 under NVQ referenced." — source: COURSE-006

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent explicitly named IT as their ideal sector and wants further education, this full-time ICT diploma appears directly relevant to their stated career interest and education plans." (hedged; based on: Section 1: ideal_sector = Information technology and communications, Section 1: wants_further_edu = Yes, COURSE-006: course overview listing core IT topics)
  - "Because the course is a diploma covering programming, databases and networking, it may support the respondent's stated aim to work in local private IT companies by building relevant technical skills." (hedged; based on: Section 1: ideal_work_type = Work for a local private Sri Lankan company, COURSE-006: includes Software Programming, Database Systems, Web Programming, Local Area Network)

**LLM's recommendation explanation (`why_recommended`):** "Direct content match: respondent named IT as their preferred sector and wants further education; the National Diploma covers core ICT topics (programming, databases, web, LAN) that align with local IT roles."

**Uncertainties disclosed by the LLM:**
  - Course is described as full time on weekdays; respondent reports family-influenced schedule decisions, so weekday full-time timing may be harder to combine with those constraints (the course document does not state flexibility options).
  - No explicit entry requirements or fee information are provided in the course document.

**Limitations disclosed by the LLM:**
  - Course schedule (full time, weekdays) may conflict with the respondent's reported family-determined schedule — this is not an exclusion but a practical constraint to check.
  - The course document does not state fees, exact location, or explicit entry requirements; these attributes are unknown from the provided text.

#### Rank 2: `COURSE-073` — Java Programming With Software Applications Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Respondent's stated IT sector preference directly aligns with a programming-focused course."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Supports taking a part-time programming course to build technical skills."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "Profile-level tendency: many in this profile report being well-connected to labour-market information and having high self-efficacy (supporting engagement in targeted training)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Described as a Java course giving theoretical knowledge and job-oriented practical skills for employment and higher education." — source: COURSE-073
  - "This is a part time course held on weekends." — source: COURSE-073

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course teaches Java programming and is part-time on weekends, it may be a practical way for the respondent to gain programming skills while managing other commitments." (hedged; based on: COURSE-073: Java programming content and part-time weekend schedule, Section 1: time_use_decision_maker = Family obligations — caregiving responsibilities determine my schedule)

**LLM's recommendation explanation (`why_recommended`):** "Programming skills (Java) are directly relevant to IT roles the respondent expressed interest in; the weekend, part-time format may better accommodate family-influenced scheduling than a weekday full-time course."

**Uncertainties disclosed by the LLM:**
  - Course duration, fees, exact timetable and entry requirements are not specified in the document extract.
  - We cannot assume the weekend schedule fully solves the respondent's scheduling constraints; it only appears more compatible.

**Limitations disclosed by the LLM:**
  - The course document lacks explicit location, fee, and entry-requirement details.
  - No explicit linkage to employer placement or certification beyond the course description is provided.

#### Rank 3: `COURSE-001` — Freelancer Of Web Design & Development

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Course duration and fee noted (03 months, fee LKR 20,000) and promises a governm...' has low word-overlap (29%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported); course_fact 'Aimed at developing skills to earn locally and internationally; mentions practic...' has low word-overlap (8%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Web design & development is a sub-area of IT and communications matching the respondent's sector preference."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Respondent's intention to continue education supports taking a vocational web development course."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p1`, role=supporting_context_only: "Many in this profile are connected to labour-market opportunities and have support for engagement, which may align with pursuing practical, employable web development skills."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course covers web development topics including hosting, domain management, building a website, platform (Fiverr) account setup and freelance earning methods." — source: COURSE-001
  - "Course duration and fee noted (03 months, fee LKR 20,000) and promises a government-recognised certificate (per text)." — source: COURSE-001
  - "Aimed at developing skills to earn locally and internationally; mentions practical outcomes and instructor experience." — source: COURSE-001

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent values IT/digital skills and aims to work for local private companies, web development and freelancing skills may expand their employment options (local company roles or freelance work), though freelancing is not the respondent's explicitly stated primary goal." (hedged; based on: Section 1: most_useful_quality_for_job = IT and digital skills, COURSE-001: web development and freelancing content)

**LLM's recommendation explanation (`why_recommended`):** "Web development is an IT skill directly relevant to the respondent's stated sector interest; the short, practical course (3 months) can build portfolio-relevant skills and includes details (fee, duration) that may help planning."

**Uncertainties disclosed by the LLM:**
  - The respondent expressed a preference for working in a local private company rather than freelancing specifically; freelancing content may or may not align with that primary aim.
  - Although the course lists a fee, the document does not specify entry requirements or exact schedule (start dates beyond the single promotional mention).

**Limitations disclosed by the LLM:**
  - This course emphasises freelancing and entrepreneurial income generation; it may be more tailored to self-employment than employment in a company.
  - While some logistical details (fee, duration) are present, other practical details (precise timetable, accreditation specifics) are limited in the document.

#### Rank 4: `COURSE-052` — Cisco Certified Network Associate

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Information technology and communications — *relevance stated by the model:* "Networking skills are core to many IT roles and directly relate to the respondent's stated sector preference."
  - `wants_to_work_future` = Yes — I want to work at some point — *relevance stated by the model:* "Taking a recognized networking course could support employability in IT roles."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_economic_role_p2`, role=supporting_context_only: "Profile-level tendency: respondents often report useful employment/training contacts and connection to labour-market information (supporting networking or certification choices)."

**[COURSE FACT] Course evidence cited by the LLM:**
  - "CISCO Network Associate course provides theoretical knowledge and job-oriented practical skills; described as part time on weekends." — source: COURSE-052

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the course is a recognised networking-focused curriculum and is offered part time on weekends, it may allow the respondent to build specific, employer-valued networking skills while managing other obligations." (hedged; based on: COURSE-052: CISCO Network Associate content and part-time weekend schedule, Section 1: time_use_decision_maker = Family obligations — caregiving responsibilities determine my schedule)

**LLM's recommendation explanation (`why_recommended`):** "Networking certification/skills are highly relevant within IT and can be directly applicable to many local private company IT roles; weekend, part-time delivery appears more feasible given the respondent's scheduling constraints."

**Uncertainties disclosed by the LLM:**
  - The course document does not specify exact certification outcomes (e.g. whether industry Cisco certification exam is included), fees, or precise schedule details.
  - We cannot assume employer recognition or guaranteed certification from the course text alone.

**Limitations disclosed by the LLM:**
  - Missing explicit details about fees, entry requirements, and whether an external Cisco exam is provided or supported.
  - Part-time weekend format is stated, but exact weekly time commitment is not detailed.


---

## 29. `nysc-49b62c9a-e647-4f21-9742-305d52c6b5a9` (Branch G) {#29-nysc-49b62c9a-e647-4f21-9742-305d52c6b5a9}

**Selection rationale (why this respondent was chosen for the batch):** G p2/p2 (rare combo), Education sector, provider+children, conflicting work-intent signals

### Frozen profile membership(s)

- `G_economic_role` — Profile 2: "Predominantly self-income provider/contributor" (dimension: Household economic role and dependency)
- `G_future_engagement` — Profile 2: "Low/uncertain engagement, mostly no prior work experience" (dimension: Future engagement and prior work experience)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `expected_highest_edu_g` = Post-graduate degree
  - `ideal_sector` = Education and teaching
  - `ideal_work_type` = Work for the government or public sector
  - `wants_further_edu` = Yes
  - `wants_to_work_future` = No — I do not want to work

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Metropolitan suburb
  - `district` = Trincomalee
  - `has_children` = Yes
  - `household_income` = LKR 120,000 – 200,000
  - `household_size` = 4.0
  - `household_unemployed` = 2.0
  - `household_workers` = 2.0
  - `num_children` = 2.0
  - `primary_earner_status` = Yes — I provide the main household income
  - `primary_income_source` = My regular job or business
  - `reason_not_in_labour_force` = Currently in education or training
  - `support_for_engagement` = Some — I would have moderate support
  - `time_use_decision_maker` = I decide for myself — I have full autonomy over my time

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `current_activity_status` = Home duties — looking after family or the household
  - `edu_status` = Currently in higher education (degree or diploma)
  - `ever_worked` = No — I have never worked
  - `worked_while_studying` = Yes

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_first_married` = 35.0
  - `age_group` = 30 – 35 years
  - `edu_min_for_decent_job` = Post-graduate qualification
  - `employment_network_quality` = Yes — I know several people with useful connections
  - `employment_self_efficacy` = Fairly confident — I probably could with effort
  - `future_orientation_g` = I have a general sense of direction but no concrete plan yet
  - `labour_market_connection` = Somewhat connected — I occasionally hear of relevant things
  - `most_important_life_goal` = Being successful in work or my career
  - `most_useful_quality_for_job` = A good general education
  - `moved_from_origin` = Yes — I grew up here and still live here
  - `spouse_activity` = Working for a salary or wage

### Recommendation status: **RECOMMENDATIONS_AVAILABLE**

**Retrieved course candidates (15):** COURSE-006 (National Diploma In Information & Communication Technology); COURSE-072 (Japanese Language); COURSE-067 (French Language); COURSE-074 (Korean Language); COURSE-086 (Tamil Language); COURSE-031 (National Diploma In Television Program Production); COURSE-075 (Mass Communication); COURSE-009 (Information And Communication Technolory Technician); COURSE-003 (Certificate In English Communication Essentials.); COURSE-082 (Secretary (Secretarial Practices)); COURSE-024 (Draughtperson); COURSE-016 (Graphics Designer); COURSE-020 (Landscape Development Assistant); COURSE-022 (Computer Network Technician); COURSE-035 (Secretary (Secretarial Practices))

**Retrieval query summary (used to search, not shown to the model as such):** ideal_sector=Education and teaching; ideal_work_type=Work for the government or public sector; expected_highest_edu_g=Post-graduate degree; reason_not_in_labour_force=Currently in education or training; current_activity_status=Home duties — looking after family or the household; edu_status=Currently in higher education (degree or diploma); [sector-vocabulary expansion terms: communication, english, french, japanese, korean, sinhala, tamil]

#### Rank 1: `COURSE-003` — Certificate In English Communication Essentials.

**Evidence strength:** STRONG
**Standard grounding audit:** PASS WITH CAUTION
  - caution: course_fact 'Offered online (zoom) and explicitly targets people seeking employment or higher...' has low word-overlap (12%) with the retrieved COURSE-003 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Education and teaching — *relevance stated by the model:* "The respondent explicitly wants to work in education/teaching; strong need for communication skills is directly relevant to teaching roles and to further study."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "The respondent expressed a desire for further education, so a short course that supports academic and professional communication can help that goal."
  - `expected_highest_edu_g` = Post-graduate degree — *relevance stated by the model:* "The respondent aspires to high-level study; improving English communication may support postgraduate study and teaching."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_economic_role_p2`, role=supporting_context_only: "Profile members often report useful employment/training contacts and reasonable labour-market connection"
  - profile `G_future_engagement_p2`, role=supporting_context_only: "Profile members sometimes report lower work engagement but include people currently in higher education"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course is a 3-month programme combining theoretical knowledge with practical application; described as useful for job aspirants and for those seeking promotions or migrant work." — source: COURSE-003
  - "Offered online (zoom) and explicitly targets people seeking employment or higher study; small classes and practical activities are emphasised." — source: COURSE-003

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent wants further education and aspires to postgraduate study, an English communication certificate may help with academic study and teaching-related communication skills." (hedged; based on: wants_further_edu = Yes, expected_highest_edu_g = Post-graduate degree, COURSE-003: course description emphasises communication skills and preparation for study/employment)
  - "Because the course is offered online (zoom) and the respondent currently has home duties and childcare, the course's online/short format may be easier to combine with those responsibilities." (hedged; based on: current_activity_status = Home duties — looking after family or the household, has_children = Yes, COURSE-003: 'zoom' delivery and 3-month duration)

**LLM's recommendation explanation (`why_recommended`):** "The respondent named Education and teaching as their ideal sector and wants further/higher study. This certified English communication course explicitly targets job-seekers and those pursuing further education, offers practical language improvement, and is short/online — all of which align with the respondent's stated education and teaching aspirations."

**Uncertainties disclosed by the LLM:**
  - The respondent's current English proficiency level is not recorded here, so the course's fit depends on their baseline skills.
  - Exact schedule, fees (beyond general mention of course duration and online delivery), and local availability for this respondent in Trincomalee are not specified in the course document.

**Limitations disclosed by the LLM:**
  - Course document contains some [UNCLEAR] fragments in other places; full administrative details (entry requirements, fees, exact start dates for the respondent's branch) are not available in the extracted text.
  - While the course appears aimed at employment and further study, it is not explicitly a teacher-training qualification — it focuses on communication skills that are transferable to teaching.

#### Rank 2: `COURSE-086` — Tamil Language

**Evidence strength:** MODERATE
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Education and teaching — *relevance stated by the model:* "Language teaching/education roles often require strong local-language skills; language courses can support teaching capability or multilingual classroom work."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "The respondent's desire for further education suggests value in courses that strengthen language skills used in study or teaching."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_future_engagement_p2`, role=supporting_context_only: "Some profile members are currently in higher education; language courses are commonly used to support study progression"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course overview: 'Cover all skills of Tamil Language required to use the language efficiently and professionally'; described as a part-time weekend course." — source: COURSE-086
  - "Course described as providing theoretical knowledge and job-oriented practical skills relevant for employment and higher education." — source: COURSE-086

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent is based in Trincomalee (a district where Tamil is commonly used) and wants to work in education, learning or strengthening Tamil may be useful for teaching in local schools or for supporting students in their area." (hedged; based on: district = Trincomalee, ideal_sector = Education and teaching, COURSE-086: course covers Tamil language skills and is part-time/weekends)
  - "Because the course is part-time and held on weekends, it may be easier to combine with the respondent's household duties than a full-time weekday programme." (hedged; based on: current_activity_status = Home duties — looking after family or the household, COURSE-086: described as part time on weekends)

**LLM's recommendation explanation (`why_recommended`):** "The respondent wants to pursue further education and aims for the education/teaching sector. A Tamil language course could strengthen language skills useful for teaching locally in Trincomalee or supporting multilingual classrooms. The course's part-time weekend format also aligns with the respondent's caregiving responsibilities."

**Uncertainties disclosed by the LLM:**
  - The respondent's native/working language(s) and current Tamil proficiency are not specified here, so the utility of a Tamil course depends on those unknowns.
  - Exact fees, entry requirements, and class location details specific to the respondent are not documented in the course extract.

**Limitations disclosed by the LLM:**
  - The course is a language-focused offering, not an accredited teacher training qualification; additional teacher-specific pedagogy training may be required for formal teaching roles.
  - Course document lacks specific administrative details (exact schedule, fees) for local delivery in Trincomalee.

#### Rank 3: `COURSE-075` — Mass Communication

**Evidence strength:** LIMITED
**Standard grounding audit:** PASS
**Evidence-category-discipline audit:** PASS

**[ACTUAL SURVEY ANSWER] Direct respondent evidence cited by the LLM:**
  - `ideal_sector` = Education and teaching — *relevance stated by the model:* "The respondent's interest in education/teaching can overlap with communication and media skills useful for educational materials, outreach, or school-level media/communication roles."
  - `wants_further_edu` = Yes — *relevance stated by the model:* "Mass communication can support further study ambitions and build transferable skills (presentation, language, media) relevant to education and public-sector roles."

**[PROFILE / GROUP CONTEXT] Profile context cited by the LLM:**
  - profile `G_economic_role_p2`, role=supporting_context_only: "Profile members sometimes report useful employment/training contacts and labour-market connection which may help translate communication skills into opportunities"

**[COURSE FACT] Course evidence cited by the LLM:**
  - "Course overview lists language practice, print communication, radio, poetry/song/drama and is described as part-time on weekends." — source: COURSE-075
  - "Course aims to give theoretical knowledge and job-oriented practical skills necessary for employment and higher education." — source: COURSE-075

**[LLM INFERENCE] Contextual inferences made:**
  - "Because the respondent aspires to education and teaching and values good general education, mass communication skills (public speaking, media, material creation) may support roles like educational outreach, curriculum support, or creating learning materials." (hedged; based on: ideal_sector = Education and teaching, most_useful_quality_for_job = A good general education, COURSE-075: course covers communication and media-related skills)
  - "Because the course is part-time on weekends, it may be more feasible for someone with household duties than a full-time weekday programme." (hedged; based on: current_activity_status = Home duties — looking after family or the household, COURSE-075: described as part time on weekends)

**LLM's recommendation explanation (`why_recommended`):** "Mass Communication teaches practical communication and media skills that are transferable to educational roles (e.g., preparing learning materials, educational outreach). The part-time/weekend format may also be feasible alongside the respondent's family responsibilities."

**Uncertainties disclosed by the LLM:**
  - It is not explicit that this course prepares candidates for formal teaching certification; its direct applicability to classroom teaching is indirect.
  - No fee, entry requirement, or precise local scheduling information for the respondent in Trincomalee is provided in the course text.

**Limitations disclosed by the LLM:**
  - Course is focused on communication/media rather than pedagogy; additional teacher-training would likely be needed for formal teaching positions.
  - The extracted course text is in Sinhala; language-of-instruction compatibility with the respondent is not confirmed.


---

## 30. `nysc-5242257e-4708-442a-a41f-1081109194a9` (Branch G) {#30-nysc-5242257e-4708-442a-a41f-1081109194a9}

**Selection rationale (why this respondent was chosen for the batch):** G p2/p2, weak/unsure sector, does not wish to work — strong NO_DEFENSIBLE test

### Frozen profile membership(s)

- `G_economic_role` — Profile 2: "Predominantly self-income provider/contributor" (dimension: Household economic role and dependency)
- `G_future_engagement` — Profile 2: "Low/uncertain engagement, mostly no prior work experience" (dimension: Future engagement and prior work experience)

### ACTUAL SURVEY ANSWERS available to the recommendation system

**DIRECT PREFERENCE / INTENT:**
  - `ideal_sector` = Not sure
  - `ideal_work_type` = I do not wish to work
  - `wants_further_edu` = Not sure yet
  - `wants_to_work_future` = No — I do not want to work

**FEASIBILITY / CONSTRAINT CONTEXT:**
  - `area_type` = Metropolitan suburb
  - `district` = Kurunegala
  - `has_children` = No
  - `household_income` = *[respondent selected "Prefer not to say"]*
  - `household_size` = 4.0
  - `household_unemployed` = 3.0
  - `household_workers` = 1.0
  - `primary_earner_status` = Shared — several people contribute roughly equally
  - `primary_income_source` = Other source
  - `reason_not_in_labour_force` = Other reason
  - `support_for_engagement` = None or opposition — I would face resistance from those around me
  - `time_use_decision_maker` = Economic necessity — I have no choice but to do what I do

**EDUCATION AND EXPERIENCE CONTEXT:**
  - `current_activity_status` = Recently finished education — have work already arranged
  - `edu_status` = Currently doing post-graduate studies
  - `ever_worked` = No — I have never worked
  - `has_job_to_return` = No — I do not currently have a job to return to
  - `worked_while_studying` = No

**INDIVIDUAL CONTEXT ONLY (explanation only, must not independently drive ranking):**
  - `age_first_married` = 34.0
  - `age_group` = 26 – 29 years
  - `edu_min_for_decent_job` = Education level doesn't matter much
  - `employment_network_quality` = No — I have no one I could call on
  - `employment_self_efficacy` = Not confident at all — I feel it would be very difficult for me
  - `future_orientation_g` = I feel quite lost and uncertain about what the future holds for me
  - `labour_market_connection` = Not connected — I feel cut off from opportunities and information
  - `most_important_life_goal` = Having leisure, freedom, and personal time
  - `most_useful_quality_for_job` = Ambition and drive
  - `move_reason` = Other reason
  - `moved_from_origin` = No — I moved from somewhere else
  - `spouse_activity` = Self-employed / own business

### Recommendation status: **NO_DEFENSIBLE_RECOMMENDATION**

**Retrieved course candidates (1):** COURSE-006 (National Diploma In Information & Communication Technology)

**Retrieval query summary (used to search, not shown to the model as such):** ideal_work_type=I do not wish to work; reason_not_in_labour_force=Other reason; current_activity_status=Recently finished education — have work already arranged; edu_status=Currently doing post-graduate studies

**[LLM's saved reason for declining]:**

> The respondent did not state any direct content/field preference (ideal_sector = 'Not sure'; wants_further_edu = 'Not sure yet') and explicitly indicated they do not wish to work. Per the decision rules, only the respondent's direct preference/intent answers may justify selecting a course's content/field. Because there is no usable direct-preference evidence linking the respondent to the ICT subject matter in COURSE-006, recommending that course as a defensible content fit would require substituting other evidence (education status, group-profile tendencies, or feasibility/context variables), which is not permitted. If the respondent expresses an interest in ICT, computing, or in training generally, COURSE-006 (National Diploma in ICT) could be reconsidered.

**Standard grounding audit on this decline:** PASS

**Evidence-category-discipline audit on this decline:** PASS


---

## Data-completeness assessment

See the accompanying message for the full answer to "do the saved files contain enough information to reconstruct exactly what evidence the LLM saw for all 30 respondents?" Short answer: **yes, but by deterministic reconstruction, not as a literally-saved verbatim prompt transcript** — see the report for the precise reasoning and a recommendation to save the literal constructed prompt text in future runs for stronger auditability.
