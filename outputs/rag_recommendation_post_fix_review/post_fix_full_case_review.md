# Final Post-Fix Results — All 10 Respondents, Full Detail

Built entirely from already-saved files in `outputs/rag_recommendation_post_fix_review/` (the final live post-fix run) and `outputs/rag_respondent_evidence/respondent_evidence.jsonl`. **No API calls were made and nothing was rerun to produce this document.**

---

## 1. `nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88` (Branch D)

**Case type:** Strong DIRECT_MATCH control case (Manufacturing/production).

**Frozen profile membership(s):**
- `D_motivation` — Profile 2: "Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support" (Motivation and study experience)
- `D_economic` — Profile 1: "Economic profile 1: relatively lower household economic position" (Economic resources and household pressure)
- `D_educational_cultural` — Profile 4: "Work-experienced students, mainly in private institutions" (Educational trajectory and cultural capital)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `expected_highest_edu_d` (DIRECT_PREFERENCE_OR_INTENT) = Post-graduate degree
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Manufacturing or production
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Work for a multinational or large private company
- `plans_after_education` (DIRECT_PREFERENCE_OR_INTENT) = Look for a job
- `study_field_preference` (DIRECT_PREFERENCE_OR_INTENT) = Science or mathematics

**How profile context was used overall: REINFORCED**
> All four profile citations (work-while-studying, active job-searching, valuing technical qualifications) describe group tendencies consistent with this respondent's own stated manufacturing/production interest and vocational orientation — supporting colour, not a deciding factor, and not contradicted.

**Recommendation status: RECOMMENDATIONS_AVAILABLE**

### Rank 1: `COURSE-005` — Automobile Mechanic
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct match between the respondent's stated Manufacturing/production sector preference and the course's clear mechanical/manufacturing-relevant content (explicit practical skills and vocational competency).)

**Why recommended:** Direct sector alignment: the respondent named Manufacturing/production and this course provides practical mechanical skills and a recognised vocational competency relevant to manufacturing, vehicle maintenance, and related technical roles that can support immediate job search.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — The course teaches core mechanical skills used in vehicle production and servicing, which maps to the respondent's stated Manufacturing/production sector interest.
- `study_field_preference` = Science or mathematics — Mechanical and vehicle-technology training is a technical/engineering-adjacent application of science and mathematics study preference.
- `plans_after_education` = Look for a job — The course is vocational and explicitly framed for employment, matching the respondent's intention to seek work after education.

**Profile context cited for this specific course:**
- `D_educational_cultural_p4`: Many profile members worked while studying and were already searching for work; vocational, work-oriented programmes are common in this profile (supporting-context-only).

**Course facts used:**
- "Course gives theoretical knowledge and job-oriented practical skills; full time course held on weekdays; competency Level 4 under National Vocational Qualifications." (source: COURSE-005)
- "Covers engine, transmission, steering, braking, electrical systems (practical mechanical skills)." (source: COURSE-005)

**LLM inference(s) made:**
- "This vocational mechanical programme may support the respondent's stated preference for Manufacturing/production and their plan to look for a job because it provides job-oriented practical skills aligned with production/maintenance roles." (hedged)
- "Because the respondent is already searching for work and has experience working while studying, a competency-level vocational credential (Level 4) may be immediately useful in applying to technical roles in manufacturing or large private companies." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document does not state fees, exact location, or explicit entry requirements.
- The course is documented as full time on weekdays; the respondent is currently in higher education, so schedule compatibility is uncertain.
- No information on course fees or whether any bursary/scholarship is available in the provided document.
- The course format is full time (weekdays) in the document; if the respondent cannot free weekday time due to studies, schedule may be a constraint (this is unconfirmed).
- Exact location/branch offering this course is not specified in the provided course text.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-040` — Automobile Mechanic
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct sector match with explicit mechanical skills taught and a stated employment orientation; additional feasibility support because a part-time weekend variant is documented.)

**Why recommended:** Technical/mechanical content aligns with the respondent's Manufacturing/production sector preference and employment-focused plan; the documented weekend/part-time format may also improve feasibility while studying.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Course content (engine, transmission, braking, suspension) aligns with manufacturing/production and vehicle-technology technical roles.
- `plans_after_education` = Look for a job — The course is vocational and described as intended to enable employment, matching the respondent's immediate job-seeking plan.

**Profile context cited for this specific course:**
- `D_educational_cultural_p4`: Profile members commonly combined study with work experience and were actively searching for employment (supporting-context-only).

**Course facts used:**
- "Course covers overhead engines, transmission, steering, braking, suspension; described as part time held on weekends in this document." (source: COURSE-040)

**LLM inference(s) made:**
- "Because this particular course instance is described as part-time on weekends, it may be easier for the respondent to combine with ongoing studies or part-time work compared with a weekday full-time course." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Some course listings for 'Automobile Mechanic' in the catalogue show full-time weekday delivery while others show part-time weekend delivery; the specific offering for this respondent is not confirmed.
- No fee, exact branch location, or entry requirements are stated in the document.
- The course text does not provide explicit fee, duration in weeks/months, or entry criteria.
- Variability across catalogue entries (some Automobile Mechanic records show full time, others part time) means format for a given centre is uncertain.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 3: `COURSE-034` — Refrigeration & Air Conditioning Technician
**DIRECT_MATCH** | Evidence strength: **MODERATE** (Direct sector and technical-skill alignment is clear, but catalogue inconsistency about delivery format and lack of specific local-offering details reduce certainty about immediate feasibility.)

**Why recommended:** The course provides technical, industrial maintenance skills that directly map to Manufacturing/production-sector work and the respondent's science/maths interest; it is framed for employment and practical competency.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Refrigeration/AC technician skills are industrial/technical and commonly used in manufacturing, production facilities, and maintenance roles, matching the respondent's sector interest.
- `study_field_preference` = Science or mathematics — The course involves technical, applied physical science skills (systems operation, repair) compatible with a science/maths study preference.

**Profile context cited for this specific course:**
- `D_motivation_p2`: Profile members value scientific or technical qualifications as useful for jobs (supporting-context-only).

**Course facts used:**
- "Course teaches repair of refrigerators, deep freezers, display units, water coolers, repair of window and split A/C, operate and maintain central A/C systems; described as full time on weekdays in one document and part time on weekends in another (catalogue shows both variants)." (source: COURSE-012 / COURSE-034)
- "Course description frames training as job-oriented practical skills and entrepreneurial ability development." (source: COURSE-034)

**LLM inference(s) made:**
- "Training in refrigeration and AC maintenance may support the respondent's objective to work in Production/Manufacturing because many large companies require in-house HVAC and refrigeration maintenance staff, and the course explicitly provides practical job-oriented skills." (hedged)
- "There is some catalogue inconsistency about whether the course is offered weekday full time or weekend part time; if a weekend variant is available it may be easier to combine with the respondent's continuing studies." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Inconsistent catalogue entries about whether this course is offered part-time (weekends) or full-time (weekdays) for a given centre.
- No fee, exact location/branch, duration, or entry requirement information is documented in the provided extracts.
- The course documents do not state fees or entry requirements.
- The candidate's exact ability to attend weekday full-time versus weekend part-time sessions is not known and must be confirmed with the NYSC centre.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 4: `COURSE-030` — Motorcycle Mechanic
**DIRECT_MATCH** | Evidence strength: **MODERATE** (Clear vocational/mechanical alignment with the respondent's stated sector, but narrower occupational focus and missing local/delivery details reduce overall certainty.)

**Why recommended:** Direct technical/mechanical content maps to the respondent's Manufacturing/production sector preference and employment-focused intentions; some course instances are part-time which could suit students working while studying.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Mechanical repair and maintenance skills are relevant to production, small-scale manufacturing supply chains, and technical roles within manufacturing firms.
- `plans_after_education` = Look for a job — The course is vocational and explicitly job-oriented, aligning with the respondent's plan to seek employment.

**Profile context cited for this specific course:**
- `D_educational_cultural_p4`: Profile members often worked while studying and sought employment; short vocational courses are commonly used to enter the labour market (supporting-context-only).

**Course facts used:**
- "MotorCycle Mechanic course provides practical job-oriented skills; documented as a part-time weekend course in one listing and as full time in another (catalogue shows part time weekends for some records)." (source: COURSE-030 / COURSE-078)

**LLM inference(s) made:**
- "This vocational mechanic training may be directly useful for immediate employment opportunities in technical/production support roles, consistent with the respondent's plan to look for a job." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Delivery format is inconsistently documented across catalogue entries; exact schedule for a local offering is unknown.
- No fee, duration, or entry requirement details are provided in the course text given.
- Course document lacks explicit fee, location, and entry-requirement information.
- Motorcycle-specific training may be more narrowly focused than larger-scale manufacturing roles; applicability depends on the jobs the respondent targets.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


---

## 2. `nysc-4e38db03-e477-420e-9afd-d3f92b53995d` (Branch D)

**Case type:** Education/Science -> ADJACENT_MATCH + catalogue-gap case.

**Frozen profile membership(s):**
- `D_motivation` — Profile 2: "Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support" (Motivation and study experience)
- `D_economic` — Profile 1: "Economic profile 1: relatively lower household economic position" (Economic resources and household pressure)
- `D_educational_cultural` — Profile 2: "State-institution students without work exposure" (Educational trajectory and cultural capital)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `expected_highest_edu_d` (DIRECT_PREFERENCE_OR_INTENT) = Bachelor's degree
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Health, social work, and wellbeing
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Work for the government or public sector
- `plans_after_education` (DIRECT_PREFERENCE_OR_INTENT) = Look for a job
- `study_field_preference` (DIRECT_PREFERENCE_OR_INTENT) = Science or mathematics

**How profile context was used overall: REINFORCED**
> Both citations (state-institution attendance; goal-aligned motivation) are generic background supporting the plausibility of pursuing further training — neither reinforces nor contradicts the respondent's specific Science/Health-sector evidence, and played no role in the field/content decision (that came entirely from the direct study_field_preference answer).

**Recommendation status: RECOMMENDATIONS_AVAILABLE**
**Catalogue coverage note:** No strong direct programme match was found in the available NYSC catalogue for the respondent's stated field (Health, social work, and wellbeing / Science or mathematics). The following are adjacent options that may still be relevant.

### Rank 1: `COURSE-006` — National Diploma In Information & Communication Technology
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (The respondent's direct preferences (Science/math and Health sector) do not name ICT, so the match is inferential; however COURSE-006 clearly teaches transferable technical and data skills that plausibly support science- or health-adjacent employment, giving a reasonable convergence of course content and respondent goals.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** The respondent stated a study-field preference for Science or mathematics and an ideal sector in Health/social wellbeing. ICT training can provide transferable technical/data and digital skills that may support science-related work, public-sector roles, or health-sector information tasks (e.g. data handling, basic informatics). Given the respondent plans to look for a job and is already in higher education, ICT skills could plausibly strengthen employability for government/health-related administrative or technical roles.

**Why recommended:** Although the respondent named Science/mathematics and Health as primary interests (no explicit ICT preference), the ICT diploma offers practical STEM-adjacent technical skills (programming, databases, networks) that could plausibly complement science training and support entry into government or health-related administrative/technical roles. It therefore appears defensible as an adjacent option to improve job-readiness.

**Individual evidence that supported it:**
- `study_field_preference` = Science or mathematics — This is the respondent's stated field preference; ICT is proposed as a technical, STEM-adjacent skillset that may complement science/maths study and roles.
- `ideal_sector` = Health, social work, and wellbeing — Respondent prefers health/social sector; ICT can be relevant to administrative, data, or technical support roles in public health or government settings.
- `plans_after_education` = Look for a job — Respondent intends to seek employment; ICT skills are commonly used to improve job-readiness across sectors.

**Profile context cited for this specific course:**
- `D_educational_cultural_p2`: Many profile members study in government-funded/state institutions (the profile label: State-institution students without work exposure).

**Course facts used:**
- "Course covers system analysis & design, software programming, database systems, web programming, LAN and other ICT topics across two semesters." (source: COURSE-006)
- "This is a full time course which will be held on weekdays." (source: COURSE-006)
- "Language: English; completion maps to Competency Level 5 under national standards." (source: COURSE-006)

**LLM inference(s) made:**
- "This ICT diploma may be useful to the respondent as a STEM-adjacent, employability-focused option because it provides practical technical and data-related skills that could be applied in science-adjacent roles or in health-sector administrative/technical positions; this is an inference based on the respondent's stated science preference and health-sector interest." (hedged)
- "Because the course is offered in English and the respondent values command of languages, successful completion may help showcase communication and technical documentation ability to public-sector employers; this is a hedged inference." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The respondent did not explicitly state an interest in ICT; this recommendation is an adjacent (not direct) match.
- The course document does not state fees, exact location, entry requirements, or precise duration beyond 'full time' and 'weekdays'.
- No explicit entry requirements or fees are provided in the course text, so eligibility and affordability cannot be confirmed here.
- The course is full-time on weekdays; the respondent's actual ability to attend full-time was not asked and cannot be assumed.
- The bridge from Science/Health interest to ICT is inferential — the respondent may prefer purely science/clinical pathways that ICT would not satisfy.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-031` — National Diploma In Television Program Production
**ADJACENT_MATCH** | Evidence strength: **LIMITED** (There is little direct overlap between TV production content and the respondent's stated Science/Health preferences; any relevance relies on a narrow communications-use case (health education/media) and is therefore speculative.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** While the respondent's stated field is Science/mathematics and sector preference is Health/social wellbeing, television production is not a direct fit. It could be an adjacent option only in narrow cases (for example, public-sector communication, health education/media roles, or government information campaigns) where media production skills support health/social messaging or public-sector outreach.

**Why recommended:** This course is not a direct match for the respondent's stated Science/Health preferences, but it is included as a lower-strength adjacent option because media production skills can sometimes serve public-sector health communication or government outreach roles. It should be considered only if the respondent is interested in communication/media aspects of health or public service.

**Individual evidence that supported it:**
- `study_field_preference` = Science or mathematics — This is the respondent's stated field preference; TV production does not directly match but may be relevant for communication-focused public-sector roles tied to health education.
- `ideal_sector` = Health, social work, and wellbeing — Respondent's sector preference suggests potential value in roles that communicate health/social messages; media production could support those functions in some government/public-sector positions.

**Profile context cited for this specific course:**
- `D_motivation_p2`: Profile members are goal-aligned in study motivation with mixed competence and relatedness (supporting context for training-readiness).

**Course facts used:**
- "Course provides theoretical knowledge and job-oriented practical skills in TV programme & production technology; is full time and held on weekdays." (source: COURSE-031)
- "Language: Sinhala; completion yields Competency Level 5 under national standards." (source: COURSE-031)

**LLM inference(s) made:**
- "TV production training could be useful to the respondent only if they aim to work in public-sector communication, health education campaigns, or community outreach roles that use media; this is a hedged inference." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The respondent did not indicate any interest in media or television production specifically; recommending this course is therefore speculative.
- Course language is Sinhala while the respondent values command of languages; fit may depend on the respondent's preferred instruction language (not specified).
- The course document omits fees, exact location, entry requirements, and duration detail beyond 'full time' and 'weekdays'.
- No entry requirements, fees, or exact location are provided in the course text—these practical eligibility/attendance details must be confirmed separately.
- This is a full-time weekday course; the respondent's availability for full-time study was not established in Section 1.
- The connection to the respondent's science/math preference is indirect and depends on an assumed interest in public-sector communications.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


---

## 3. `nysc-0cba8a68-ebf6-47cb-bd45-e2a1d78ad74b` (Branch D)

**Case type:** Useful profile-context reasoning + structural profile-divergence case.

**Frozen profile membership(s):**
- `D_motivation` — Profile 1: "Consensus motivation profile 1: externally or uncertainly motivated, with moderate study support" (Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (Economic resources and household pressure)
- `D_educational_cultural` — Profile 4: "Work-experienced students, mainly in private institutions" (Educational trajectory and cultural capital)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `expected_highest_edu_d` (DIRECT_PREFERENCE_OR_INTENT) = Post-graduate degree
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Education and teaching
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Not sure yet
- `most_useful_quality_for_job` (INDIVIDUAL_CONTEXT_ONLY) = Communication and interpersonal skills
- `plans_after_education` (DIRECT_PREFERENCE_OR_INTENT) = Immediately go on to further education or training
- `study_field_preference` (DIRECT_PREFERENCE_OR_INTENT) = Science or mathematics

**How profile context was used overall: REINFORCED (not contrasted this round)**
> This respondent's frozen profile label itself ('externally or uncertainly motivated, with moderate study support') sits in real tension with their own clear, specific, goal-directed Section 1 answers (Education/teaching sector, immediate further study) — a genuine structural divergence. In this specific run, however, the model's profile citations (communication skills valued; IT/qualifications valued) are generic supporting colour and do not explicitly narrate that contrast — worth noting as an observation for human review, not a fabricated contrast the model didn't actually make.

**Recommendation status: RECOMMENDATIONS_AVAILABLE**
**Catalogue coverage note:** No strong direct programme match was found in the available NYSC catalogue for Education and teaching or for Science/Mathematics. The following are adjacent options that may still be relevant (communication/professional-English and office-skill programmes).

### Rank 1: `COURSE-003` — Certificate In English Communication Essentials.
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (Direct respondent evidence explicitly values communication skills and education/teaching; the course explicitly teaches practical English communication. The link is plausible and evidence-supported but not a direct subject-area match to teaching methodology or science/mathematics content.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** The respondent stated an ideal sector of 'Education and teaching' and valued 'Communication and interpersonal skills' (direct evidence). Strong classroom teaching and progression to further education often rely on clear English communication; this course explicitly develops practical English communication skills that may support the respondent's stated goal of working in education or continuing study in Science/Mathematics by improving teaching, presentation and academic language ability.

**Why recommended:** Although not a subject-specific education/teaching or science programme, this English communication certificate develops practical communication skills the respondent explicitly values and that are often useful for teaching roles and for succeeding in further academic study.

**Individual evidence that supported it:**
- `ideal_sector` = Education and teaching — Places the respondent's primary stated sector interest on which we seek course relevance.
- `study_field_preference` = Science or mathematics — Signals the respondent plans to continue in STEM fields; strong communication skills may support teaching or further study in these fields.
- `most_useful_quality_for_job` = Communication and interpersonal skills — Directly indicates the respondent values the very skillset this course teaches.
- `plans_after_education` = Immediately go on to further education or training — Shows intent to continue studying; an English communication qualification may support further academic progress.

**Profile context cited for this specific course:**
- `D_motivation_p1`: Within this profile, communication and interpersonal skills were commonly valued (profile distributions show communication ranked highly).

**Course facts used:**
- "Three-month, online (Zoom) delivery; structured curriculum combining theoretical knowledge with practical application; targeted at job aspirants, migrant workers, AL/OL completers and those pursuing higher education." (source: COURSE-003)
- "Aimed at improving English language proficiency for employment and further study." (source: COURSE-003)

**LLM inference(s) made:**
- "Because the respondent aims for education/teaching and further study in science/mathematics, improving academic and classroom English may help with both teaching and postgraduate study applications." (hedged)
- "The course's online delivery (Zoom) may be practical for a respondent who is currently attending higher education and worked part-time while studying." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document does not state explicit entry requirements or whether its content includes pedagogy or classroom-specific language for teachers.
- It is not documented whether the certificate is formally recognised by education employers for teaching posts; the catalogue card focuses on general employability and academic support.
- This is an ADJACENT_MATCH (supports teaching via communication skills) rather than a direct teacher-training or science/mathematics qualification.
- Some extracted text contained an [UNCLEAR] marker in the screenshot; course duration/format details are present but some lines were truncated in the source screenshot.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-004` — Professional English
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (Strong direct evidence the respondent values communication and plans further study; the course is explicitly Professional English, so relevance to teaching/further study is plausible though not a direct education/teacher credential.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** The respondent's stated interest in Education and teaching plus a preference for further study in Science/Mathematics suggests benefit from strengthened professional English. This course is a full-time Professional English offering that may support classroom communication, lecture delivery, and academic writing — skills useful for a future educator or postgraduate student.

**Why recommended:** Professional English is recommended as an adjacent option: it does not teach Education-sector subject matter, but it strengthens professional/academic English skills that are plausibly useful for a future teacher or postgraduate STEM student.

**Individual evidence that supported it:**
- `ideal_sector` = Education and teaching — Provides the sectoral anchor (education) used to justify recommending communication-focused programmes as adjacent options.
- `most_useful_quality_for_job` = Communication and interpersonal skills — Indicates the respondent places high value on communication skills this course aims to build.
- `plans_after_education` = Immediately go on to further education or training — Shows likely utility of a recognised professional English credential for further study.

**Profile context cited for this specific course:**
- `D_economic_p2`: Many members of this economic profile value IT and formal qualifications, suggesting professional-language credentials are used in further-education pathways (group-level context only).

**Course facts used:**
- "Full Time Professional English course, 06 Month duration, 25 students (catalogue card indicates full-time Professional English attendance)." (source: COURSE-004)

**LLM inference(s) made:**
- "Because the respondent expects to continue to higher education and values communication, a formal Professional English course may help with academic language demands and with later teaching responsibilities." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document is short and does not list specific modules (e.g., academic writing vs. classroom pedagogy), so precise alignment with teacher-training needs is uncertain.
- No explicit entry requirements, accreditation for teacher roles, or schedule details (beyond 'Full Time' on the catalogue card) are provided.
- This is an ADJACENT_MATCH, not a direct teacher-education qualification.
- The Professional English card is brief; missing module-level detail limits exact matching to the respondent's needs (e.g., English for teaching vs. general professional English).

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 3: `COURSE-035` — Secretary (Secretarial Practices)
**ADJACENT_MATCH** | Evidence strength: **LIMITED** (The course content includes communication and office skills that align with respondent-valued competencies, but the connection to the respondent's stated sector (Education and teaching) is indirect and depends on transferable-role assumptions.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** The respondent values communication skills and plans further education; this course includes communication skills, office IT (word, internet, email) and meetings/handling correspondence which could support transferable administrative and communication competencies useful in education settings (e.g., school administration, support roles) or while studying.

**Why recommended:** This course is an adjacent option that develops workplace communication and basic office-IT skills which could assist the respondent in education-sector support roles or in organising administrative aspects of further study.

**Individual evidence that supported it:**
- `ideal_sector` = Education and teaching — Used to justify why office/communication skills could be relevant in education-adjacent roles (administration or support in schools).
- `most_useful_quality_for_job` = Communication and interpersonal skills — Matches course content emphasizing communication skills.

**Profile context cited for this specific course:**
- `D_educational_cultural_p4`: This profile includes many work-experienced students and private-institution attendees; administrative/office skills sometimes support employment pathways for such students (group-level context only).

**Course facts used:**
- "Course modules list Communication Skills, Managing Office, Computer/Word/Internet/Email and handling correspondence." (source: COURSE-035)

**LLM inference(s) made:**
- "Because the respondent has work experience while studying and values communication, a secretarial/office-skills course may provide transferable skills useful for school administrative roles or to support study/work balance." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course is not a teacher-training programme nor does it teach science/math content.
- The course document does not state whether it includes any school-specific administrative practice.
- ADJACENT_MATCH only; relevance is via transferable administrative and communication skills rather than classroom teaching or science/maths content.
- No details on schedule compatibility with the respondent's current higher-education timetable beyond 'full time' being indicated.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS WITH CAUTION**
  - `most_useful_quality_for_job` (INDIVIDUAL_CONTEXT_ONLY): PASS WITH CAUTION — context-only variable given preference-like framing as a secondary citation
- Evidence-hierarchy audit: **PASS**


---

## 4. `nysc-25c345ec-5f45-4616-adb8-c96e31f3511c` (Branch D)

**Case type:** Profile-context differentiation on a complex/conflicting case.

**Frozen profile membership(s):**
- `D_motivation` — Profile 3: "Consensus motivation profile 3: highly self-directed, capable and connected" (Motivation and study experience)
- `D_economic` — Profile 1: "Economic profile 1: relatively lower household economic position" (Economic resources and household pressure)
- `D_educational_cultural` — Profile 1: "Re-entered students, often with degree-educated parents" (Educational trajectory and cultural capital)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `expected_highest_edu_d` (DIRECT_PREFERENCE_OR_INTENT) = O/L level
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Manufacturing or production
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Work for the government or public sector

**How profile context was used overall: REINFORCED + light differentiation**
> Most citations reinforce general job-search-readiness. One (COURSE-025, citing D_economic_p1's lower ICT-preference sub-finding) is used to help justify considering a non-ICT practical trade alongside the mechanic-family courses — a mild differentiation use, not a hard override of individual evidence, which remains the primary driver (ideal_sector = Manufacturing/production).

**Recommendation status: RECOMMENDATIONS_AVAILABLE**

### Rank 1: `COURSE-034` — Refrigeration & Air Conditioning Technician
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct individual preference for manufacturing/production maps closely to the course's industrial technical content and NVQ outcome (direct content overlap).)

**Why recommended:** Direct technical match: the course trains practical industrial/maintenance skills used in manufacturing and production environments (repair and maintenance of refrigeration and A/C equipment), which directly aligns with the respondent's stated ideal sector (Manufacturing or production).

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — The course is a technical/industrial trades programme (refrigeration & A/C) that fits within manufacturing/production sector work.

**Profile context cited for this specific course:**
- `D_motivation_p3`: Members more often reported useful employment/training contacts (may support job pathways after training)

**Course facts used:**
- "Course overview lists repair of refrigerators, deep freezers, display units, water coolers, repair of window and split A/C and operate and maintain central A/C system." (source: COURSE-034)
- "Described as a full time course held on weekdays and awards Competency Level 4 under NVQ standards." (source: COURSE-034)

**LLM inference(s) made:**
- "Because the respondent named Manufacturing or production as their ideal sector, a hands-on technical trades course (refrigeration & A/C) appears aligned with that sector and may support employment in manufacturing/production or maintenance roles." (hedged)
- "The course is full-time on weekdays; given the respondent has children, part-time or weekend delivery might be easier to combine with childcare, so schedule fit may require checking (this is an uncertainty rather than a disqualifier)." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Course fee information and exact local delivery location are not stated in the course document.
- Full-time weekday schedule may conflict with childcare or other responsibilities; respondent did not state training-availability constraints explicitly.
- The course document does not list fees or precise location information.
- Full-time weekday delivery is stated; whether the respondent can attend this schedule is unknown.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-005` — Automobile Mechanic
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct sector preference (manufacturing/production) aligns clearly with the course's technical/mechanical content and NVQ level outcome.)

**Why recommended:** Direct content fit: automobile mechanic training teaches practical vehicle maintenance and mechanical skills associated with manufacturing/production and maintenance roles, matching the respondent's stated sector preference.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Automobile mechanic skills are core industrial/production and maintenance trades commonly categorized within manufacturing/production-related occupations.

**Profile context cited for this specific course:**
- `D_educational_cultural_p1`: Members more often reported they are already searching for work (may indicate readiness to enter job-focused vocational training).

**Course facts used:**
- "Course covers engine, transmission, steering, braking and electrical systems; described as a full time course on weekdays and awards Competency Level 4 under NVQ standards." (source: COURSE-005)

**LLM inference(s) made:**
- "Because the respondent stated they are already searching for work and values a career in manufacturing/production, a full-time, NVQ-level automobile mechanic programme may accelerate entry into relevant jobs." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Course fee and exact training centre location are not provided in the course document.
- Course is full-time on weekdays; respondent's childcare and schooling situation may affect ability to attend.
- No fee or explicit entry requirements are provided in the course text.
- Full-time weekday delivery may be harder to combine with other responsibilities; schedule suitability must be confirmed with NYSC.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 3: `COURSE-025` — Electrician
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct overlap between respondent's stated sector (manufacturing/production) and the course's industrial electrical and PLC content; clear vocational alignment.)

**Why recommended:** Direct match: electrician skills (industrial/domestic installations, motor control, PLC) are core to manufacturing/production infrastructure and maintenance, aligning with the respondent's stated sector intention.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Electrician training (domestic and industrial electrical installation, motor control, PLC) is directly relevant to manufacturing, production, and factory maintenance roles.

**Profile context cited for this specific course:**
- `D_economic_p1`: Members less often reported ICT as preferred sector and show a broader spread of technical fields (supporting consideration of practical trades).

**Course facts used:**
- "Course covers domestic electrical installation, repair/service of motor generators, industrial electrical installation (motor controlling systems), PLC and security solutions; described as a full time course on weekdays with Competency Level 3,4 outcomes." (source: COURSE-025)

**LLM inference(s) made:**
- "Given the respondent's sector preference for manufacturing/production, electrician training (including industrial electrical installation and PLC) appears applicable to maintenance and production-plant roles in that sector." (hedged)
- "The course is listed as full-time on weekdays; the respondent has childcare responsibilities which may make weekend/part-time delivery preferable if available." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Course fee and specific location are not documented in the course text.
- Full-time schedule may conflict with respondent's other responsibilities; no direct statement about training-availability was provided by the respondent.
- No fee, exact venue, or entry-requirement information is available in the course document.
- Course delivery mode (full-time weekdays) may not match respondent's practical availability; alternative part-time offerings are not specified here.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 4: `COURSE-030` — Motorcycle Mechanic
**DIRECT_MATCH** | Evidence strength: **MODERATE** (Direct sector match is clear, but the evidence strength is downgraded slightly because delivery-mode documents conflict (part-time vs full-time) and because local schedule/venue/fee details are not present.)

**Why recommended:** Direct practical fit: motorcycle mechanic training teaches mechanical repair and maintenance skills that align with manufacturing/production and small-enterprise vehicle-repair roles in the respondent's stated sector.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Motorcycle mechanic training is a practical technical trade linked to vehicle repair and small-scale mechanical production/maintenance, fitting within manufacturing/production-type occupations.

**Profile context cited for this specific course:**
- `D_educational_cultural_p1`: Members more often reported they are already searching for work (may indicate readiness to apply vocational skills quickly).

**Course facts used:**
- "Course provides theoretical knowledge and job-oriented practical skills for motorbike repair and is described as a full time weekday course in some documents and part-time/weekend in others (both full-time and part-time variants appear in retrieved records)." (source: COURSE-030 / COURSE-078)

**LLM inference(s) made:**
- "Motorcycle mechanic skills may be useful for employment in local manufacturing/repair shops or small-scale production/maintenance businesses in the respondent's rural district." (hedged)
- "Some retrieved motorcycle-repair documents describe weekend/part-time delivery (COURSE-078) while others list full-time weekdays (COURSE-030); if the respondent needs more flexible timing because of childcare or study, a weekend/part-time offering might be preferable (schedule should be confirmed)." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Course fee, precise schedule variant at the respondent's location, and exact training venue are not provided in the course documents.
- There is some inconsistency across retrieved motorcycle course documents about part-time vs full-time delivery; local availability of the preferred format is unknown.
- No fee or explicit entry requirements are available in the retrieved course texts.
- Variation in documented delivery mode (full-time vs part-time/weekends) means the actual schedule for a Jaffna delivery would need confirmation.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


---

## 5. `nysc-4646cb19-0ac0-49ca-a00b-e2d8cb16b65e` (Branch F)

**Case type:** CONFIRMED occupation-as-preference fix (now ADJACENT_MATCH).

**Frozen profile membership(s):**
- `F_employment_security` — Profile 2: "Predominantly permanent employment with stronger security" (Employment security and formality)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `edu_status` (EDUCATION_AND_EXPERIENCE_CONTEXT) = Currently in higher education (degree or diploma)
- `expected_highest_edu_f` (DIRECT_PREFERENCE_OR_INTENT) = Post-graduate degree
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Not sure
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Not sure yet
- `occupational_class` (EDUCATION_AND_EXPERIENCE_CONTEXT) = Clerical or office work (data entry, receptionist, secretary, etc.)
- `plans_further_edu_f` (DIRECT_PREFERENCE_OR_INTENT) = Yes

**How profile context was used overall: REINFORCED**
> All five citations reference the same F_employment_security_p2 ('predominantly permanent, stronger security') finding as generic background for why structured/formal training might suit this respondent — consistent supporting colour across all five ADJACENT_MATCH courses, not used to select between them.

**Recommendation status: RECOMMENDATIONS_AVAILABLE**
**Catalogue coverage note:** No strong direct programme match was found in the available NYSC catalogue because the respondent did not state a specific preferred field or sector in their direct-preference answers. The following adjacent options were identified as plausibly relevant based on the respondent's clerical/office occupation and stated intent to pursue further education.

### Rank 1: `COURSE-035` — Secretary (Secretarial Practices)
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (Direct link between the course content (office/secretarial skills) and the respondent's current clerical occupation and intention to study further supports a plausible, defensible match, but the respondent did not explicitly request secretarial training.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** The respondent currently works in clerical/office work and is enrolled in higher education and plans further study; a secretarial/office-skills programme is plausibly useful to build job-relevant administrative and ICT skills that align with their current occupation and further-education intentions.

**Why recommended:** The Secretary (Secretarial Practices) course teaches administrative, communication and basic computer skills that align with the respondent's current clerical role and stated intention to pursue further education; this makes it a defensible adjacent option to strengthen job-relevant skills.

**Individual evidence that supported it:**
- `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.) — Shows current work is clerical/office-based; secretarial training directly relates to improving skills used in such roles.
- `edu_status` = Currently in higher education (degree or diploma) — Indicates ongoing study and openness to further structured learning that this course provides.
- `plans_further_edu_f` = Yes — Respondent explicitly intends to pursue further education, supporting relevance of a diploma/skills course.

**Profile context cited for this specific course:**
- `F_employment_security_p2`: Profile describes predominantly permanent employment with stronger security (group-level tendency).

**Course facts used:**
- "Course overview lists communication skills, managing office, meetings, filing, computer/Word/Internet and email, travel arrangements and handling correspondence." (source: COURSE-035)
- "This is described in the course text as a full time, weekday course and claims competency Level 4 under NVQ standards." (source: COURSE-035)

**LLM inference(s) made:**
- "Because the respondent currently works in a clerical/office role and values further education, a course teaching office communication, filing and basic computer/email skills could plausibly strengthen competencies directly used in their job and support career progression." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Respondent did not state a preferred training field or sector, so this is an adjacent (not directly requested) recommendation.
- Course document lists this offering as full time on weekdays; it is unclear whether the respondent can accommodate a weekday full-time schedule given current working hours.
- No fee, exact location, or entry requirements are documented in the course text provided.
- Course schedule (full-time, weekdays) may conflict with the respondent's current job but the respondent did not state training-availability constraints in Section 1.
- The course document does not state fees or entry requirements; those would need confirmation before enrolment.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-082` — Secretary (Secretarial Practices) [part-time / weekend variant]
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (Course content directly aligns with the respondent's clerical occupation and the weekend delivery improves practical fit; still an adjacent match because the respondent did not explicitly request secretarial training.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** Same occupational bridge as above (current clerical/office work); this variant explicitly lists a part-time/weekend delivery which may be more feasible to combine with ongoing employment.

**Why recommended:** The part-time/weekend Secretary course covers office and administrative skills that relate to the respondent's clerical work and may be more feasible to attend alongside employment due to weekend scheduling.

**Individual evidence that supported it:**
- `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.) — Current role aligns with secretarial/office skills taught by the course.
- `plans_further_edu_f` = Yes — Respondent is planning further education, indicating receptiveness to training.

**Profile context cited for this specific course:**
- `F_employment_security_p2`: Profile members often report formal, permanent employment (group-level tendency).

**Course facts used:**
- "Course overview lists secretarial duties, communication, meetings, mailing, handling correspondence and travel arrangements; described as a part time course held on weekends." (source: COURSE-082)

**LLM inference(s) made:**
- "Because the course is offered part-time on weekends and the respondent is employed with formal hours, the weekend format may be easier to combine with work, making this particular variant more practical for someone who wants to keep income/hours similar." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document does not state fees, precise location, or entry requirements.
- Respondent did not explicitly state they prefer weekend or part-time study; inference about feasibility is hedged.
- While the weekend format is stated in the course doc, details about total time commitment and exact schedule are not provided.
- No explicit confirmation that the respondent is available for weekend study; this is an inferred possibility.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 3: `COURSE-053` — Computer Applications Assistant
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (Course topics match routine skills for clerical and higher-education contexts the respondent occupies; lack of an explicit stated preference for ICT lowers the strength to moderate (adjacent rather than direct).)

**Inferential bridge (why this counts as ADJACENT_MATCH):** Respondent works in a clerical/data-entry role and the Computer Applications Assistant course explicitly teaches MS Office, internet and email skills which are directly useful for office-based clerical work and further academic study.

**Why recommended:** The Computer Applications Assistant course teaches MS Office, internet and email — practical skills commonly used in clerical and student contexts — making it a defensible adjacent option to strengthen the respondent's current and future academic/work capabilities.

**Individual evidence that supported it:**
- `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.) — MS Office, email and internet skills are typically core to clerical/data-entry duties.
- `plans_further_edu_f` = Yes — Indicates openness to taking a targeted ICT/office-skills course to support further education or career progression.

**Profile context cited for this specific course:**
- `F_employment_security_p2`: Within this profile, many members reported formal employment and use of employer-provided training (group-level tendency).

**Course facts used:**
- "Course overview lists ICT introduction, MS-Office, Using Internet & E-mail; described as a part-time weekend course." (source: COURSE-053)

**LLM inference(s) made:**
- "Because the respondent's job and study status likely require basic MS Office and email skills, this course may directly improve day-to-day job performance and academic work." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- No explicit training field was stated by the respondent; this is an adjacent recommendation based on occupation.
- Course fee, exact location, enrollment prerequisites and detailed schedule beyond 'weekends' are not provided in the document.
- The course is listed as part-time/weekend in the document; the respondent's willingness/ability to attend weekend classes was not directly stated.
- Information about certification level or employer recognition beyond the brief description is limited in the course text.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 4: `COURSE-006` — National Diploma In Information & Communication Technology
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (Strong course-to-occupation content overlap supports usefulness, but absence of an explicit respondent preference for ICT keeps the match as adjacent with moderate evidence strength.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** Although the respondent did not explicitly name IT as a desired sector, their clerical/data-entry occupation and ongoing higher-education status make an ICT diploma a defensible adjacent option to broaden technical skills and career pathways.

**Why recommended:** The National Diploma in ICT offers substantive technical skills that could broaden the respondent's career options beyond clerical tasks and support further academic study — a reasonable adjacent pathway given their background and plans to continue education.

**Individual evidence that supported it:**
- `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.) — Clerical roles often use software, databases and communication tools; an ICT diploma could expand technical competence relevant to office work.
- `plans_further_edu_f` = Yes — Respondent's stated intention to pursue further education supports recommending a diploma-level programme.

**Profile context cited for this specific course:**
- `F_employment_security_p2`: This profile's group distribution showed many members reporting higher formal employment and a tendency toward technical/IT occupational classes at the group level (group-level distribution).

**Course facts used:**
- "Course modules include System Analysis & Design, Software Programming, Database Systems, Web Programming, LAN and workplace communication — a broad ICT diploma covering technical and workplace ICT topics." (source: COURSE-006)
- "Course is described as full time (weekdays) and offers competency Level 5 under NVQ standards." (source: COURSE-006)

**LLM inference(s) made:**
- "Because the respondent is currently in higher education and employed in an office role, a diploma covering programming, databases and workplace ICT may support both academic progression and more technical office responsibilities." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Respondent did not explicitly request ICT training, so this is an adjacent recommendation.
- Course is full-time on weekdays; respondent's current working hours may limit feasibility unless employer support or schedule change occurs.
- No fee or explicit entry requirements are included in the course document.
- Full-time weekday delivery may conflict with ongoing employment; respondent did not state training-availability preferences.
- The course document does not state fees, entry criteria or exact campus/location details.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 5: `COURSE-008` — Computer Hardware Technician
**ADJACENT_MATCH** | Evidence strength: **LIMITED** (Course content is relevant to office-computer use but the respondent did not indicate an interest in hardware specifically; therefore the match is more speculative and evidence is weaker than for office-skills options.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** Respondent's clerical role likely involves interaction with computers; basic hardware, troubleshooting and maintenance skills could be a useful adjacent upskill to improve workplace effectiveness and broaden technical options.

**Why recommended:** Computer Hardware Technician training could give practical technical skills complementary to clerical work (reducing reliance on external IT support) and open alternative technical pathways; this makes it a defensible adjacent recommendation given the available evidence.

**Individual evidence that supported it:**
- `occupational_class` = Clerical or office work (data entry, receptionist, secretary, etc.) — Clerical/data-entry roles commonly rely on functioning computer hardware; hardware training could increase technical self-sufficiency and job value.
- `plans_further_edu_f` = Yes — Respondent's plan to continue education indicates openness to vocational/technical training.

**Profile context cited for this specific course:**
- `F_employment_security_p2`: Group-level tendency for formal employment and employer-paid training among profile members (supporting context only).

**Course facts used:**
- "Course overview lists assembling, disassembling, troubleshooting, preventive maintenance and estimating — practical computer hardware technician skills." (source: COURSE-008)
- "Course is full time and held on weekdays and claims competency Level 4 under NVQ standards." (source: COURSE-008)

**LLM inference(s) made:**
- "Because the respondent works in an office and uses computers, gaining hardware troubleshooting skills may be practically useful for daily work and could enable new technical roles, but this is inferred rather than directly requested by the respondent." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Respondent did not state a preference for technical or hardware training specifically.
- Course is full-time on weekdays which may conflict with the respondent's current job schedule.
- No fee, precise location, entry requirements or language-of-instruction suitability details (beyond 'English' in document) are fully specified for enrolment planning.
- Full-time schedule and weekday delivery may reduce practical feasibility while employed.
- Course documentation lacks fee and explicit entry-requirement details.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


---

## 6. `nysc-04134b0d-f3fe-4a25-916c-ee106362e150` (Branch F)

**Case type:** Second occupation + weak-preference case; also the grounding-typo case.

**Frozen profile membership(s):**
- `F_employment_security` — Profile 1: "Temporary/no-contract employment with uncertain security" (Employment security and formality)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `expected_highest_edu_f` (DIRECT_PREFERENCE_OR_INTENT) = Post-graduate degree
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Not sure
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Not sure yet
- `plans_further_edu_f` (DIRECT_PREFERENCE_OR_INTENT) = Yes
- `training_type_received` (EDUCATION_AND_EXPERIENCE_CONTEXT) = Training in new technologies
- `usual_hours_per_week` (FEASIBILITY_OR_CONSTRAINT_CONTEXT) = 40.0

**How profile context was used overall: REINFORCED**
> Citations describe the insecure-employment profile's general education/technical-occupation tendencies as background for the adjacent recommendations — consistent with, not contradicting, the respondent's own answers.

**Recommendation status: RECOMMENDATIONS_AVAILABLE**
**Catalogue coverage note:** No strong direct programme match was found in the available NYSC catalogue for a specific stated field because the respondent did not name an ideal sector or study field. The following adjacent options may still be relevant to the respondent's explicit plan for further education and their prior technology training.

### Rank 1: `COURSE-066` — Professional English (part-time, weekends)
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (There is a reasonable, defensible bridge from the respondent's explicit intention to pursue further/postgraduate study to an English preparatory course; the fit is plausible but not directly stated by the respondent, so evidence is not STRONG.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** The respondent said they plan further education (plans_further_edu_f = Yes) and expect to reach postgraduate study; English-language proficiency courses are commonly useful preparatory upskilling for further/higher study. The course is a part-time, weekend English offering which may be feasible alongside current work hours.

**Why recommended:** Although the respondent did not state a subject preference, they explicitly plan further education and aim for postgraduate study; a part-time Professional English course may support readiness for higher study and is offered on weekends, which fits better with substantial work hours.

**Individual evidence that supported it:**
- `plans_further_edu_f` = Yes — Shows the respondent intends further study, making preparatory academic/communication skills plausibly relevant.
- `expected_highest_edu_f` = Post-graduate degree — Indicates the respondent aspires to higher-level study where English proficiency can be helpful.
- `usual_hours_per_week` = 40.0 — Suggests the respondent works substantial hours; a part-time weekend course may be more feasible than a full-time weekday option.

**Profile context cited for this specific course:**
- `F_employment_security_p1`: Many profile members report currently being in higher education and most plan further education (profile: high rate of 'Currently in higher education'; plans_further_edu_f: Yes in 79.3% of the profile). This provides group-level context that members often combine study and work.

**Course facts used:**
- "English Language courses will give you theoretical knowledge as well as job oriented practical skills; this is a part time course which will be held on weekends." (source: COURSE-066)
- "Max students 25; Professional English; part time weekend delivery." (source: COURSE-066)

**LLM inference(s) made:**
- "This part-time, weekend English course may be easier to combine with the respondent's current ~40–50 hour work-week than a full-time weekday course, so it could support their stated intention to pursue further (postgraduate) education." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Respondent did not state any language-proficiency need or whether English is the barrier to further study; recommending English is an inference based on 'plans_further_edu_f' and postgraduate aspiration, not an explicit request.
- The course document does not state entry requirements, level prerequisites, exact fees, or schedule times beyond 'weekends'; these details are not available in the course text provided.
- No direct statement from the respondent that English training is desired; this is an adjacent inference, not an expressed content preference.
- Course duration, exact weekend times, fee, and location specifics are not provided in the retrieved course text.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-006` — National Diploma In Information & Communication Technology
**ADJACENT_MATCH** | Evidence strength: **MODERATE** (There is a meaningful link between the respondent's reported prior technology training and the ICT diploma content; however, the respondent did not explicitly request ICT study and the programme is full-time, so the match is plausible but not strongly direct.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** The respondent reported having received training in new technologies for their current job (education/experience evidence), and ICT/digital skills are commonly useful for both further study and professional advancement; the course's ICT content could therefore help build on prior technology training and support future education/career goals.

**Why recommended:** This ICT diploma aligns with the respondent's prior technology training and with stated plans for further education; it could provide recognised vocational/technical competence useful for study or career progression.

**Individual evidence that supported it:**
- `training_type_received` = Training in new technologies — Shows prior exposure to technology training, making further ICT study a plausible continuation or upskill.
- `plans_further_edu_f` = Yes — Indicates a desire for further education where ICT skills may be useful for study and employment.
- `expected_highest_edu_f` = Post-graduate degree — Signals ambition for advanced study; ICT competencies can be supportive for many postgraduate programmes and professional roles.

**Profile context cited for this specific course:**
- `F_employment_security_p1`: Within this profile, a substantial share reported technical/IT-type occupational class and many worked while studying (some via internships), which suggests group-level familiarity with technical training.

**Course facts used:**
- "Course covers System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network, Software Testing, and related workplace communication and planning; full-time weekday delivery; Competency Level 5." (source: COURSE-006)
- "Course described as theoretical knowledge and job-oriented practical necessary for employment and higher education." (source: COURSE-006)

**LLM inference(s) made:**
- "Because the respondent has already received training in new technologies, a formal ICT diploma may build on that background and help with both further study and employability." (hedged)
- "The course is full-time on weekdays; given the respondent's substantial weekly work hours (40–50), attending a full-time weekday programme may be challenging unless their schedule changes — this is a feasibility concern rather than disqualifying evidence." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Respondent did not explicitly request ICT training or name ICT as a preferred field; the connection is inferential (builds on prior training).
- The course is full-time on weekdays; the respondent currently works substantial hours, so schedule compatibility is uncertain.
- The course document does not list fees, exact location, entry requirements, or intake dates.
- Recommendation relies on education/experience evidence (past training in new technologies) rather than an explicit field preference — this makes it an adjacent, not direct, match.
- Practical feasibility (full-time weekday attendance) may conflict with the respondent's ongoing work; further scheduling/eligibility details would be needed.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


---

## 7. `nysc-3258dc18-84da-4092-82af-cfb84352536e` (Branch E)

**Case type:** CONFIRMED available_to_start fix.

**Frozen profile membership(s):**
- `E_learning_orientation` — Profile 2: "Moderate perceived utility and mixed learning ambition" (Education usefulness and further-learning orientation)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Manufacturing or production
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Work for a local private Sri Lankan company
- `job_type_sought` (DIRECT_PREFERENCE_OR_INTENT) = Manual or trade work
- `plans_further_edu` (DIRECT_PREFERENCE_OR_INTENT) = Do not know yet

**How profile context was used overall: REINFORCED**
> E_learning_orientation_p2's cited tendency (manufacturing/production among sectors of interest, technical/vocational training preference) happens to align with this respondent's own direct ideal_sector = Manufacturing/production and job_type_sought = Manual/trade work — genuine alignment, not used to override or substitute for the individual evidence, which remains the stated basis for every DIRECT_MATCH.

**Recommendation status: RECOMMENDATIONS_AVAILABLE**

### Rank 1: `COURSE-005` — Automobile Mechanic
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct overlap between the respondent's stated sector preference (manufacturing/production) and manual/trade job type with the course's mechanical, job-oriented practical content; course explicitly framed as vocational for employment.)

**Why recommended:** The Automobile Mechanic course directly teaches practical mechanical and trade skills that align with the respondent's stated interest in manufacturing/production and manual/trade work for local private companies.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — The course is a hands-on mechanical trade closely aligned with manufacturing/production and vehicle-related mechanical work.
- `job_type_sought` = Manual or trade work — The course teaches practical mechanical and trade skills appropriate for manual/trade employment.
- `ideal_work_type` = Work for a local private Sri Lankan company — Automobile mechanic roles are commonly offered by local private companies and garages, matching the respondent's preferred employer type.

**Profile context cited for this specific course:**
- `E_learning_orientation_p2`: Profile members often attend job fairs and show mixed further-learning ambition; the profile commonly lists manufacturing/production among sectors of interest.

**Course facts used:**
- "Course covers engine, transmission, steering, braking and electrical systems; described as job-oriented practical training and Competency Level 4 outcome." (source: COURSE-005)
- "Full time, weekday delivery (document shows full-time weekday variant in one screenshot)." (source: COURSE-005)

**LLM inference(s) made:**
- "Because the respondent seeks manual/trade work in manufacturing/production and prefers local private companies, a vocational course teaching vehicle mechanics may directly support rapid entry into local garages or production-related maintenance roles." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Course documents show at least one full-time weekday variant; the respondent's availability for full-time weekday study is unknown from Section 1 (feasibility schedule info is not provided).
- No explicit fee, exact location, or entry requirement information is present in the course document.
- Course schedule (full-time weekday) may conflict with the respondent's urgent need to start earning; actual part-time/weekday options and start-dates are not documented here.
- No documented fee or location details in the course text provided.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-030` — Motorcycle Mechanic
**DIRECT_MATCH** | Evidence strength: **MODERATE** (Strong content alignment with manual/trade preference, but some course metadata (schedule/level variants) is inconsistently presented across records, reducing certainty about delivery format.)

**Why recommended:** Motorcycle Mechanic is a trade-aligned vocational course with direct practical skills that match the respondent's manual/trade job preference within manufacturing/production-oriented local employment contexts.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Motorcycle/mechanical maintenance is a manual trade that fits production/repair-related roles common in manufacturing-adjacent small enterprises.
- `job_type_sought` = Manual or trade work — The course provides hands-on mechanical skills consistent with manual/trade employment.

**Profile context cited for this specific course:**
- `E_learning_orientation_p2`: Profile shows some members prefer technical and manual work and attend job fairs (possible route to local employers).

**Course facts used:**
- "Course provides theoretical and job-oriented practical skills for motorbike repair; competency Level 3/4 outcomes noted." (source: COURSE-030)
- "Document describes part-time/weekend variants in some records, though this course listing shows full-time weekday in one instance." (source: COURSE-030)

**LLM inference(s) made:**
- "A motorcycle mechanic qualification may allow the respondent to secure manual repair work or roles in small private enterprises in the local area, which aligns with their preference for local private employment." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Course schedule variants are inconsistently documented across catalogue screenshots; exact scheduling for this specific listing is uncertain.
- No fee or precise location details provided in the course document.
- If the respondent needs immediate income, time-to-completion and start-dates are not documented and may affect feasibility.
- No information on entry requirements or any practical prerequisites in the course text.

**Audit results:**
- Grounding audit: **PASS WITH CAUTION**
  - caution: course_fact 'Document describes part-time/weekend variants in some records, though this cours...' has low word-overlap (20%) with the retrieved COURSE-030 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 3: `COURSE-064` — Electrician
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct content overlap with manufacturing/production-relevant electrical skills and explicit manual/trade orientation in the respondent's preferences.)

**Why recommended:** The Electrician course teaches trade skills directly useful in manufacturing/production settings (industrial installations, motor control) and therefore matches the respondent's stated sector and job-type preferences.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Electrician skills (domestic and industrial electrical installation, motor control, PLC) align with technical/manual roles in manufacturing and production environments.
- `job_type_sought` = Manual or trade work — The course is a hands-on technical trade suitable for manual employment.

**Profile context cited for this specific course:**
- `E_learning_orientation_p2`: Profile members show interest in technical and vocational training among training-type preferences.

**Course facts used:**
- "Course lists domestic and industrial electrical installation, motor generator repair, PLC and security solutions; described as part-time weekend delivery in the document." (source: COURSE-064)

**LLM inference(s) made:**
- "Because the respondent wants manual/trade work in manufacturing/production, an electrician course that includes industrial electrical installation and PLC may be particularly relevant for plant/production maintenance roles." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document indicates part-time weekend delivery; whether that schedule aligns with the respondent's availability is unknown.
- No fee, exact venue, or entry-requirement details are provided in the course text.
- While the course includes industrial topics, the document does not specify workplace placement or employer links.
- No explicit entry requirements or prerequisites are documented.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 4: `COURSE-012` — Refrigeration & Air Conditioning Technician
**DIRECT_MATCH** | Evidence strength: **MODERATE** (Clear relevance to manual/trade and production-related maintenance tasks, but inconsistencies across retrieved listings about delivery format reduce certainty.)

**Why recommended:** Refrigeration & Air Conditioning Technician trains manual technical skills relevant to production and facilities maintenance in manufacturing or cold-storage operations, aligning with the respondent's sector and trade preferences.

**Individual evidence that supported it:**
- `ideal_sector` = Manufacturing or production — Refrigeration and A/C maintenance is a technical manual trade often required in production facilities, cold-storage and manufacturing settings.
- `job_type_sought` = Manual or trade work — The course describes practical repair and maintenance tasks, matching manual/trade work preference.

**Profile context cited for this specific course:**
- `E_learning_orientation_p2`: Profile members sometimes prefer practical vocational courses and attend job fairs (routes to local employers).

**Course facts used:**
- "Course teaches repair of refrigerators, deep freezers, display units, water coolers, window and split A/C, and operation/maintenance of central A/C systems; described as job-oriented practical skills and part-time weekend delivery in one listing." (source: COURSE-012)

**LLM inference(s) made:**
- "Because the respondent seeks manual/trade roles in manufacturing/production, refrigeration/A/C skills may enable employment in production facilities, cold-chain operations or local service businesses." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Two retrieved listings for this course show different delivery formats across screenshots (part-time weekend vs. full-time weekday); the exact schedule for this specific offering is unclear.
- No fee, precise location, or entry requirements are stated in the course document.
- Variation in course record (part-time vs full-time) introduces uncertainty about whether the available schedule fits the respondent's immediate-earnings needs.
- No placement, employer connection, or fees are documented in the provided text.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 5: `COURSE-029` — Mobile Phone Repair Technician
**ADJACENT_MATCH** | Evidence strength: **LIMITED** (Direct match to manual/trade preference exists, but the course's sector (consumer electronics repair) is not the respondent's explicitly stated manufacturing/production sector, making the connection inferential and less direct.)

**Inferential bridge (why this counts as ADJACENT_MATCH):** Respondent explicitly seeks manual/trade work; although mobile-phone repair is more service/repair-focused than core manufacturing, it is a practical technical trade that can provide immediate, locally-available manual employment in private-sector repair shops. This course is therefore an adjacent option offering transferable manual/technical skills relevant to the respondent's stated aim of securing paid manual/trade work locally.

**Why recommended:** Mobile Phone Repair provides practical manual technical skills that can lead to local private-sector repair jobs; it is an adjacent option because it is a service/repair trade rather than manufacturing/production per se, but still matches the respondent's manual/trade employment intent.

**Individual evidence that supported it:**
- `job_type_sought` = Manual or trade work — The course offers hands-on repair skills consistent with manual/trade employment the respondent seeks.
- `ideal_work_type` = Work for a local private Sri Lankan company — Mobile-phone repair roles frequently exist in local private repair shops and small enterprises matching this employer type preference.

**Profile context cited for this specific course:**
- `E_learning_orientation_p2`: Profile members sometimes list computer/IT or vocational training among helpful training types, indicating openness to technical short courses.

**Course facts used:**
- "Course provides theoretical and job-oriented practical skills in mobile phone repairing; one listing describes full-time weekday delivery and another listing shows part-time/weekend variants for similar courses elsewhere in the catalogue." (source: COURSE-029)

**LLM inference(s) made:**
- "Because the respondent needs income urgently and is seeking manual/trade work locally, a short technical repair course like mobile-phone repair may offer a faster route to paid work in local private repair shops, though it is not strictly within 'manufacturing/production'." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course is more service/repair oriented than manufacturing/production; it may or may not match employers in the respondent's intended manufacturing roles.
- No fee, exact schedule, or location details are present in the course text.
- This is an adjacent recommendation: it does not directly match the respondent's stated sector (manufacturing/production) but maps to their manual/trade job preference.
- No documented information about course duration, start-dates, or placement support is available.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


---

## 8. `nysc-8ae4a1d8-97c7-4bc4-9dc9-cb7eea0c897f` (Branch D)

**Case type:** CONFIRMED economic-affordability fix (the critical retest case).

**Frozen profile membership(s):**
- `D_motivation` — Profile 2: "Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support" (Motivation and study experience)
- `D_economic` — Profile 2: "Economic profile 2: relatively higher household economic position" (Economic resources and household pressure)
- `D_educational_cultural` — Profile 4: "Work-experienced students, mainly in private institutions" (Educational trajectory and cultural capital)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `expected_highest_edu_d` (DIRECT_PREFERENCE_OR_INTENT) = Bachelor's degree
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Creative, media, and arts
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Start my own business
- `most_useful_quality_for_job` (INDIVIDUAL_CONTEXT_ONLY) = Business and economic knowledge
- `study_field_preference` (DIRECT_PREFERENCE_OR_INTENT) = Literature, arts, or social sciences

**How profile context was used overall: REINFORCED**
> All five citations are now (post-fix) generic background about job-search methods and institution type, with zero affordability/fee language — confirmed by direct inspection. Supporting colour only, consistent with individual evidence, not contradicting or substituting for it.

**Recommendation status: RECOMMENDATIONS_AVAILABLE**

### Rank 1: `COURSE-068` — Graphics Designer
**DIRECT_MATCH** | Evidence strength: **STRONG** (DIRECT overlap between respondent's stated ideal sector (creative/media), study-field interest in arts, and the course's explicit graphic-design content and practical, part-time format.)

**Why recommended:** Direct match: the course teaches graphic-design skills in the creative/media area the respondent named, provides practical (job-oriented) training, and is offered part-time which may help combine study with starting a creative business.

**Individual evidence that supported it:**
- `ideal_sector` = Creative, media, and arts — The course is explicitly a graphic-designing programme in the creative/media sector, directly matching the respondent's stated ideal sector.
- `study_field_preference` = Literature, arts, or social sciences — The respondent's stated preference for arts/literature supports interest in arts-related practical skills such as graphic design.
- `ideal_work_type` = Start my own business — Graphics design skills are commonly used for freelance or entrepreneur-led creative businesses, aligning with the respondent's intention to start a business.

**Profile context cited for this specific course:**
- `D_educational_cultural_p4`: Work-experienced students, mainly in private institutions; many were already searching for work/business

**Course facts used:**
- "Graphic Designing courses will give you theoretical knowledge as well as job oriented practical skills that are necessary for employment and higher education." (source: COURSE-068)
- "This is a part time course which will be held on weekends." (source: COURSE-068)

**LLM inference(s) made:**
- "Because the respondent said they want to start their own business and the course explicitly teaches practical graphic-design skills and is offered part-time, this part-time graphics designer course may be particularly compatible with combining study and early entrepreneurial activity." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document does not state duration, fee, entry requirements, or exact timetable beyond 'part time / weekends' for COURSE-068.
- The respondent's availability for weekend study is not explicitly stated in Section 1.
- No explicit course fee, entry requirement, or precise schedule (beyond 'weekends') is provided in the course text.
- Recommendation assumes the respondent wants practical creative skills to support entrepreneurship; their longer-term study plans are 'Do not know yet.'

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-062` — Desktop Publisher
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct content overlap: course explicitly targets graphic/desktop-publishing skills within the creative/media domain the respondent named.)

**Why recommended:** Direct match: course content (desktop publishing and graphic tools) aligns with the respondent's stated creative/media and arts interests and offers practical skills useful for creative employment or entrepreneurship.

**Individual evidence that supported it:**
- `ideal_sector` = Creative, media, and arts — Desktop publishing/graphic-design tools are directly within the creative/media sector named by the respondent.
- `study_field_preference` = Literature, arts, or social sciences — Skills such as desktop publishing can support arts-related work (publishing, design, creative production) consistent with the respondent's field preference.

**Profile context cited for this specific course:**
- `D_economic_p2`: Profile members more often reported private-institution background and online job-search methods (supporting digital/creative vocational interest).

**Course facts used:**
- "Desktop Publishing & Graphic Designing course will give you theoretical knowledge as well as job oriented practical ... This is a part time course which will be held on weekends." (source: COURSE-062)
- "Lists training in Adobe Pagemaker, Corel Draw, Adobe Photoshop CS6, Adobe InDesign CS6, Adobe Illustrator CS6 (toolset for publishing/graphic work)." (source: COURSE-062)

**LLM inference(s) made:**
- "Because the respondent seeks creative/media work and has an interest in arts, acquiring desktop-publishing and industry-standard design tool skills may support both employment in creative roles and self-started creative businesses." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course text contains some [UNCLEAR] markers in the tool list; specific syllabus detail, fee, and entry requirements are not provided in the document.
- Exact course duration and precise schedule beyond 'weekends' are not stated.
- Some tool names in the course listing were marked [UNCLEAR] in the extracted text; verify the full syllabus with NYSC.
- No fee or explicit entry criteria are documented in the provided extract.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 3: `COURSE-031` — National Diploma In Television Program Production
**DIRECT_MATCH** | Evidence strength: **MODERATE** (Strong content match to creative/media interest, but weaker practical fit because the course is full-time weekdays while respondent's current commitments (working/attending education) may make full-time attendance more difficult.)

**Why recommended:** Direct match: the programme is explicitly in television/media production, matching the respondent's creative/media sector preference and offering practical, vocational training.

**Individual evidence that supported it:**
- `ideal_sector` = Creative, media, and arts — Television production is squarely within the creative/media sector the respondent selected.
- `study_field_preference` = Literature, arts, or social sciences — An arts/media-oriented diploma aligns with the respondent's stated study-field preference for arts.

**Profile context cited for this specific course:**
- `D_motivation_p2`: Profile members were goal-aligned with mixed study confidence; this could support taking a structured diploma if the respondent desires formal credentialing.

**Course facts used:**
- "National Diploma in TV Programme & Production Technology course will give you theoretical knowledge as well as job oriented practical that is necessary for employment and higher education." (source: COURSE-031)
- "This is a full time course which will be held on weekdays; completion can achieve competency Level 5 under the National Vocational Qualifications." (source: COURSE-031)

**LLM inference(s) made:**
- "Because the respondent is already searching for work and has creative/media sector interest, a vocational diploma in television production may support employability in media roles or provide technical skills useful in creative enterprises." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Course is full-time on weekdays; the respondent's current schedule and ability to attend a weekday full-time programme are not fully specified.
- No explicit fee or entry-requirement details are provided in the extract.
- Full-time weekday delivery may conflict with the respondent's other commitments (they report being employed/attending education); this is an observed uncertainty to check with the respondent before enrolment.
- Course duration and specific module breakdown beyond the high-level statement are not provided here.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 4: `COURSE-001` — Freelancer Of Web Design & Development
**DIRECT_MATCH** | Evidence strength: **STRONG** (The programme explicitly instructs in freelance web development and business-creation skills that map directly to the respondent's declared entrepreneurial intention and creative/digital sector interest.)

**Why recommended:** Direct match: course explicitly trains freelancing/web-business skills and advertises building one’s own business and online income — directly aligned with the respondent's stated desire to start a business within a creative/digital area.

**Individual evidence that supported it:**
- `ideal_sector` = Creative, media, and arts — Web design & development is commonly grouped with creative/digital media activities and aligns with a creative/media sector interest.
- `ideal_work_type` = Start my own business — The course explicitly markets building one's own income and business development, directly aligning with the respondent's stated intent to start a business.

**Profile context cited for this specific course:**
- `D_economic_p2`: Profile members more often used online job-search methods and reported high private-institution attendance; this supports relevance of online/digital freelancing skills as a viable pathway for similar respondents (group-level only).

**Course facts used:**
- "Course description emphasises developing own skill to earn locally and abroad, building a business, hosting/domain management, and creating Fiverr and other freelancer accounts." (source: COURSE-001)
- "Course length stated as months 03 (3 months) and fee explicitly listed in the text (20,000/=)." (source: COURSE-001)

**LLM inference(s) made:**
- "Because the respondent wants to start a business and the course explicitly teaches how to set up freelance/online earning channels (hosting, domain, Fiverr), this programme may directly support the respondent's entrepreneurial goal." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Although the course text lists a fee (20,000/=) and duration, other details (exact schedule, entry requirements, credential recognition) are not fully detailed in the extract.
- Some parts of the course text are in Sinhala and English mixture; confirm language-of-instruction preference.
- The course fee is documented here, but the respondent's willingness/ability to pay was not asked in Section 1, so affordability is not assessed.
- Further details (assessment, certification authority, and exact timetable) should be verified with NYSC before application.

**Audit results:**
- Grounding audit: **PASS WITH CAUTION**
  - caution: course_fact 'Course description emphasises developing own skill to earn locally and abroad, b...' has low word-overlap (33%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported); course_fact 'Course length stated as months 03 (3 months) and fee explicitly listed in the te...' has low word-overlap (33%) with the retrieved COURSE-001 document text — flagged for manual review (may be a legitimate paraphrase or may be unsupported)
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 5: `COURSE-049` — Business Managemant
**DIRECT_MATCH** | Evidence strength: **MODERATE** (Strong alignment between the respondent's clear entrepreneurial intention and the course subject, but the course description is high-level and lacks detailed syllabus/eligibility info; also business-management is a different domain than the respondent's arts field preference though consistent with their work-intent.)

**Why recommended:** Direct match: Business Management teaches practical business skills that directly support the respondent's stated intention to start their own business; the part-time, weekend offering may fit a schedule where the respondent continues other activities.

**Individual evidence that supported it:**
- `ideal_work_type` = Start my own business — The respondent explicitly intends to start a business; a Business Management course directly supports entrepreneurship skills.
- `most_useful_quality_for_job` = Business and economic knowledge — Although 'most_useful_quality_for_job' is an individual-context opinion (not a direct preference), it supports the relevance of business-knowledge training when combined with the direct intention to start a business.

**Profile context cited for this specific course:**
- `D_educational_cultural_p4`: Profile shows many respondents were already searching for work/business and had higher household income bands — group context that may make formal business training attractive (supporting context only).

**Course facts used:**
- "Business Management course will give you theoretical knowledge as well as job oriented practical that is necessary for employment and higher education. This is a part time course which will be held on weekends." (source: COURSE-049)

**LLM inference(s) made:**
- "Because the respondent wants to start a business and values business/economic knowledge, a part-time Business Management course may help build entrepreneurial skills while allowing time for other commitments." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document does not specify curriculum detail, duration, fees, or entry requirements beyond the high-level overview.
- The respondent's exact schedule constraints for weekend study are not specified.
- Course fee and entry requirements are not provided in the extracted text; confirm these with NYSC.
- While the respondent named 'business and economic knowledge' as a useful quality, that variable is an opinion-based item and cannot alone determine content preference—however, combined with the stated intention to start a business it supports recommending business training.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


---

## 9. `nysc-5242257e-4708-442a-a41f-1081109194a9` (Branch G)

**Case type:** Genuine NO_DEFENSIBLE_RECOMMENDATION control case.

**Frozen profile membership(s):**
- `G_economic_role` — Profile 2: "Predominantly self-income provider/contributor" (Household economic role and dependency)
- `G_future_engagement` — Profile 2: "Low/uncertain engagement, mostly no prior work experience" (Future engagement and prior work experience)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Not sure
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = I do not wish to work
- `wants_further_edu` (DIRECT_PREFERENCE_OR_INTENT) = Not sure yet
- `wants_to_work_future` (DIRECT_PREFERENCE_OR_INTENT) = No — I do not want to work

**How profile context was used overall: NOT USED**
> No recommendation was made, so no profile_context_used citation exists. The decline reason is built entirely from this respondent's own direct answers (ideal_sector = Not sure; ideal_work_type = I do not wish to work; wants_to_work_future = No) — profile context plays no role in the decision either way.

**Recommendation status: NO_DEFENSIBLE_RECOMMENDATION**
**Catalogue coverage note:** No strong direct programme match was found in the available NYSC catalogue for the respondent's stated field ('Not sure'). The retrieved courses (only an ICT National Diploma) do not directly correspond to any explicit training preference or sector named by the respondent.

**Retrieved options considered (1):** COURSE-006 (National Diploma In Information & Communication Technology)

**Why none was defensible (model's own stated reason):**
> The respondent did not state any direct training preference, sector, or study field (ideal_sector = 'Not sure'; wants_further_edu = 'Not sure yet'), and explicitly indicated they do not wish to work now or in the future (ideal_work_type = 'I do not wish to work'; wants_to_work_future = 'No — I do not want to work'). Under the decision standard, direct individual preference/intent answers are required to justify a course content/field match. The single retrieved course (National Diploma in ICT) cannot be classified as a DIRECT_MATCH because there is no respondent-stated interest in ICT or a related field. An ADJACENT_MATCH would require a defensible inferential bridge from the respondent's direct evidence (for example: an expressed desire to upskill in a specific technical area, or clear intent to change/enter work where ICT is relevant), which is absent. Therefore no defensible recommendation (direct or adjacent) can be made from the provided course documents.

**Audit results (respondent-level):**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**

---

## 10. `nysc-27c2ff48-e39c-4db3-aa11-a149d76be479` (Branch G)

**Case type:** Additional profile-context example, G branch diversity.

**Frozen profile membership(s):**
- `G_economic_role` — Profile 2: "Predominantly self-income provider/contributor" (Household economic role and dependency)
- `G_future_engagement` — Profile 1: "Work-and-education engaged, mostly prior work experience" (Future engagement and prior work experience)

**Most relevant ACTUAL survey answers (cited by the system, plus core direct-preference fields):**
- `edu_status` (EDUCATION_AND_EXPERIENCE_CONTEXT) = Currently in higher education (degree or diploma)
- `expected_highest_edu_g` (DIRECT_PREFERENCE_OR_INTENT) = Bachelor's degree
- `ideal_sector` (DIRECT_PREFERENCE_OR_INTENT) = Information technology and communications
- `ideal_work_type` (DIRECT_PREFERENCE_OR_INTENT) = Work for a local private Sri Lankan company
- `wants_further_edu` (DIRECT_PREFERENCE_OR_INTENT) = Yes
- `wants_to_work_future` (DIRECT_PREFERENCE_OR_INTENT) = Yes — I want to work at some point

**How profile context was used overall: REINFORCED**
> Citations (high self-efficacy, labour-market connection) describe generic engagement tendencies consistent with this respondent's own clear ICT-sector preference and active engagement — supporting colour, not a deciding factor.

**Recommendation status: RECOMMENDATIONS_AVAILABLE**

### Rank 1: `COURSE-006` — National Diploma In Information & Communication Technology
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct stated preference for IT plus course content explicitly covering core ICT subjects (programming, web, databases, LAN) produce a close, content-level match.)

**Why recommended:** The respondent explicitly wants work in Information Technology and further education. This National Diploma teaches a broad set of ICT skills (programming, databases, web, LAN) that map directly to that sector and to employers in local private companies.

**Individual evidence that supported it:**
- `ideal_sector` = Information technology and communications — The course is explicitly an ICT diploma and therefore directly matches the respondent's stated sector preference.
- `wants_further_edu` = Yes — Respondent expressed an intention to pursue further education, which supports taking a formal diploma program.
- `edu_status` = Currently in higher education (degree or diploma) — Respondent is already in higher education and may be positioned to combine or complement a diploma with current studies, making a formal ICT diploma relevant.

**Profile context cited for this specific course:**
- `G_future_engagement_p1`: This profile often reports high employment/training self-efficacy and strong connection to labour-market information, which is supporting context that such participants are likely to act on training opportunities.

**Course facts used:**
- "Course covers System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network, and workplace communication." (source: COURSE-006)
- "Described as a full time course held on weekdays and provides Competency Level 5 under NVQ standards." (source: COURSE-006)

**LLM inference(s) made:**
- "Because the respondent named IT as their ideal sector and the course contains core ICT subjects (programming, databases, web, LAN), this diploma appears directly relevant to the respondent's stated career direction." (hedged)
- "The course is full-time on weekdays; given the respondent reports family-determined time use (caregiving responsibilities), a weekday full-time schedule may require consideration or negotiation with family supports." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document does not state tuition/fee information (unclear whether fees apply or amount).
- Exact location, start dates, and entry requirements are not provided in the course text.
- Full-time weekday scheduling may conflict with the respondent's family-determined schedule; the document does not state any part-time or flexible delivery.
- No fee, precise location, or entry-requirement details are present in the course document.
- The recommendation assumes the respondent wishes to pursue practical, employer-oriented ICT training rather than only continuing academic degree study; their longer-term degree plans are not detailed here.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 2: `COURSE-073` — Java Programming With Software Applications Development
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct sector preference for IT and the course's clear programming/software-development content provide a close, direct match; part-time delivery also addresses feasibility considerations.)

**Why recommended:** The respondent named IT and digital skills as important; this course provides programming-focused, practical software development skills that align with that preference and with roles in private IT companies.

**Individual evidence that supported it:**
- `ideal_sector` = Information technology and communications — The respondent's stated IT sector interest aligns with a programming/software-development course.
- `wants_further_edu` = Yes — Respondent intends to pursue further education, consistent with enrolling in a technical programming course.

**Profile context cited for this specific course:**
- `G_future_engagement_p1`: Profile shows a tendency for high employment/training self-efficacy and good labour-market connection, which is supporting context for pursuing skills-based programming training.

**Course facts used:**
- "Course focuses on Java and software application development; offered part-time on weekends." (source: COURSE-073)

**LLM inference(s) made:**
- "Because the respondent seeks IT-sector work and values IT/digital skills, a Java/software development course may help build directly employable coding skills for local private companies." (hedged)
- "This course is part-time on weekends; given the respondent reports family-determined time use, the weekend format may be easier to combine with other responsibilities than a weekday full-time option." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- The course document does not list fees, entry requirements, or exact location.
- The document does not specify the programming experience level expected on entry (beginners vs prior coding experience).
- No explicit information on entry prerequisites or how this part-time course integrates with the respondent's current higher-education studies.
- While part-time weekends are likely convenient, exact schedule intensity and calendar are not shown.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 3: `COURSE-001` — Freelancer Of Web Design & Development
**DIRECT_MATCH** | Evidence strength: **MODERATE** (Direct content match to web/IT skills is strong, but the course targets freelancing and lists a fee (unique among retrieved docs) which introduces an affordability unknown; also the respondent expressed intent to attain a Bachelor's degree, so a short vocational course may be complementary rather than substitutive.)

**Why recommended:** The programme teaches web development and practical freelancing/hosting skills that directly map to IT sector roles the respondent expressed interest in; short duration may also help transition to work quickly.

**Individual evidence that supported it:**
- `ideal_sector` = Information technology and communications — Web design and development are core IT skills directly relevant to the respondent's stated sector.
- `wants_further_edu` = Yes — Respondent wants further education; this vocational/web development programme is an applicable practical pathway.

**Profile context cited for this specific course:**
- `G_economic_role_p2`: Profile often reports useful employment/training contacts and good labour-market connection, which is supporting context for market-oriented skills like web development.

**Course facts used:**
- "Covers web site development, hosting/domain management, and freelancing/marketplace account setup; lists a course fee of 20,000 and a 3-month duration." (source: COURSE-001)

**LLM inference(s) made:**
- "Because the respondent wants to work for local private companies and values IT/digital skills, practical web development and freelancing skills may be useful both for employment and for short-term income generation." (hedged)
- "The course's short (3-month) duration and explicit fee are potentially compatible with the respondent's plan to progress quickly toward employment, but the respondent's ability or willingness to pay the fee is not documented in Section 1 (so affordability cannot be assessed here)." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- Although a fee (20,000) is listed in the course text, the respondent's affordability is unknown and must not be inferred from profile-level economic context.
- No explicit entry requirements or exact schedule days/times beyond the stated duration are provided.
- Recommendation does not assume the respondent can or will pay the fee; affordability must be determined from direct individual evidence not present here.
- Course appears targeted at freelance income paths as well as employment; the respondent indicated a preference to work for a local company, so they should consider whether freelancing-focused content matches their exact career plan.

**Audit results:**
- Grounding audit: **PASS WITH CAUTION**
  - caution: inference marked uncertainty_language_used=True but no hedging word found in the text: 'The course's short (3-month) duration and explicit fee are potentially compatibl...'
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


### Rank 4: `COURSE-052` — Cisco Certified Network Associate
**DIRECT_MATCH** | Evidence strength: **STRONG** (Direct sector match to IT plus explicit networking/CISCO course content; weekend, part-time delivery also supports feasibility given the respondent's reported schedule constraints.)

**Why recommended:** Networking (Cisco) skills are a direct subfield of IT; the respondent's sector preference aligns with Cisco/ networking training that employers in private IT companies commonly value.

**Individual evidence that supported it:**
- `ideal_sector` = Information technology and communications — Network engineering and CCNA skills are directly within the IT sector the respondent selected.
- `wants_further_edu` = Yes — Respondent intends further training; a Cisco networking certificate is a concrete IT upskilling pathway.

**Profile context cited for this specific course:**
- `G_future_engagement_p1`: Profile evidence shows many members are engaged and have labour-market connections; this is supporting context for pursuing recognized vendor/network credentials.

**Course facts used:**
- "Course is described as CISCO Network Associate training, part-time on weekends." (source: COURSE-052)

**LLM inference(s) made:**
- "Because the respondent aims for IT-sector employment, vendor-networking skills (CCNA) may be directly relevant to local IT roles and employers." (hedged)
- "Weekend part-time delivery could be more compatible with the respondent's family-influenced schedule than weekday full-time options." (hedged)

**Uncertainty / catalogue limitations disclosed:**
- No fee, entry requirement, or precise location information is provided in the course text.
- The document does not state prerequisite knowledge level (beginner vs prior networking experience).
- No explicit statement about certification exam inclusion or employer linkages is present in the course text.
- Profile-level economic or scheduling context was used only as supporting context; it does not establish this respondent's affordability or absolute availability.

**Audit results:**
- Grounding audit: **PASS**
- Category-discipline audit: **PASS**
- Evidence-hierarchy audit: **PASS**


---
