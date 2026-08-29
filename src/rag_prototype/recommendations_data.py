# Hand-authored (Claude-reasoned, source-grounded) recommendation outputs for the
# STEP 4 RAG prototype. Each entry was produced by reading the respondent's full
# context pack (direct evidence + profile documents + retrieved full course
# documents) in outputs/rag_recommendation_prototype/_context_packs/ and reasoning
# holistically, per the task's Section M-O instructions. No chain-of-thought is
# stored — only the auditable evidence+inference+recommendation record itself.

RECOMMENDATIONS = {}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-acaf63b5-6e8f-45fb-9d5a-cef8d615799b"] = {
    "recommendations": [
        {
            "rank": 1,
            "course_id": "COURSE-049",
            "course_name": "Business Managemant",
            "direct_respondent_evidence_used": [
                "study_field_preference = Commerce, business, or management",
                "primary_earner_status = Yes — I provide the main household income",
                "has_children = Yes (num_children = 3.0)",
                "worked_while_studying = Yes; work_while_study_hours = 5 to 10 hours (already balancing paid work with study)",
            ],
            "profile_context_used": [
                "GROUP-LEVEL: D_economic profile 1 (relatively lower household economic position, n=44) is broadly consistent with this respondent's own moderate household income band, but is not used to determine content or schedule — the respondent's own direct answers already establish the relevant facts.",
            ],
            "course_evidence_used": [
                "Course text: 'Business Management course will give you theoretical knowledge as well as job oriented practical that is necessary for employment and higher education.'",
                "Course text: 'This is a part time course which will be held on weekends.'",
            ],
            "contextual_inferences": [
                "INFERENCE: because the respondent is the primary household earner and already combines paid work with post-graduate study, a weekend/part-time course format may be easier to fit alongside existing income and study commitments than a full-time course would be. This is an inference about practicality, not a claim that the respondent cannot attend full-time — no full-time alternative was retrieved to compare against, and the respondent never stated a schedule constraint directly.",
            ],
            "why_recommended": "Directly matches the respondent's own stated study-field preference (commerce/business/management); the course's part-time/weekend format is plausibly compatible with, though not confirmed necessary for, their existing work-and-study load.",
            "uncertainties": [
                "The course document states no entry-qualification level, minimum education requirement, or intended student level, so whether a part-time vocational business course is an appropriate STEP for someone already enrolled in post-graduate studies cannot be determined from the available course text.",
                "The respondent's stated ideal_sector is 'Education and teaching,' which no course in the retrieved or excluded corpus addresses — this recommendation matches the stated FIELD (commerce/business/management) but not the stated target SECTOR (teaching), and that gap is not resolved by any available evidence.",
            ],
            "limitations": [
                "No fee, cost, or subsidy information is available in the course document.",
                "No course location is stated.",
                "No entry requirement or NVQ/qualification level is stated for this specific course.",
                "No employer or placement information is available.",
            ],
            "evidence_strength": "MODERATE",
            "evidence_strength_reason": "Strong direct-field match (respondent's own stated preference), but no data exists to confirm level-appropriateness or to resolve the stated-sector gap (teaching vs. business), so this is not STRONG.",
        },
        {
            "rank": 2,
            "course_id": "COURSE-071",
            "course_name": "Human Recources Management",
            "direct_respondent_evidence_used": [
                "study_field_preference = Commerce, business, or management",
                "primary_earner_status = Yes — I provide the main household income",
                "has_children = Yes (num_children = 3.0)",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text (readable modules despite one [UNCLEAR] marker and broken two-column layout): 'Introduction to Management and HRM', 'JD, JA Recruitment, Selection, Hiring, Induction', 'Discripline Management, PE System, T and D', 'LR System, Employee welfare, Labour law'.",
                "Course text: 'This is a part time course which will be held on weekends.'",
            ],
            "contextual_inferences": [
                "INFERENCE: as with COURSE-049, the weekend/part-time format may be more practical to combine with the respondent's existing paid work and post-graduate study than a full-time course, without this being a confirmed schedule requirement.",
            ],
            "why_recommended": "A second, more specialised business/management-field course (human resources specifically) matching the same directly-stated study-field preference, offering a distinct specialisation from the general Business Management course above.",
            "uncertainties": [
                "This source document is marked VALIDATED_WITH_LIMITATIONS and contains one unresolved [UNCLEAR] marker and a broken two-column reading order; the module list reconstructed above is the readable portion and should be treated as probably-but-not-certainly complete.",
                "Same sector gap and level-appropriateness uncertainty as COURSE-049.",
            ],
            "limitations": [
                "No fee, cost, location, entry-requirement, or placement information available.",
                "Text extraction quality for this specific document is lower than average for the corpus (uncertainty marker present).",
            ],
            "evidence_strength": "LIMITED",
            "evidence_strength_reason": "Same direct-field match as COURSE-049, but the source document's own extraction-quality flag (VALIDATED_WITH_LIMITATIONS, one [UNCLEAR] marker) reduces confidence relative to rank 1.",
        },
    ],
    "no_defensible_recommendation": False,
    "no_defensible_recommendation_reason": None,
}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-346623df-699b-4abb-a445-51abb3f16cc5"] = {
    "recommendations": [
        {
            "rank": 1,
            "course_id": "COURSE-001",
            "course_name": "Freelancer Of Web Design & Development",
            "direct_respondent_evidence_used": [
                "ideal_sector = Information technology and communications",
                "ideal_work_type = Start my own business",
                "occupational_class = Technical work (IT technician, lab technician, etc.)",
                "hopes_to_change_job = Yes — I want to change; reason_wants_to_change = The work does not match my skills or qualifications",
            ],
            "profile_context_used": [
                "GROUP-LEVEL: F_employment_security profile 1 ('temporary/no-contract employment with uncertain security') — used only as background context consistent with this respondent's own directly-stated temporary contract and 'some concern' about 12-month job security; not used to select this course's content.",
            ],
            "course_evidence_used": [
                "Course text: 3-month freelance web-development course explicitly covering building an independent income through web development, domain/hosting management, and freelance-platform account setup; government-recognised certificate; ages 15–45.",
            ],
            "contextual_inferences": [
                "INFERENCE: the respondent already works in a technical/IT role but directly stated their current work does not match their skills or qualifications and that they want to start their own business in ICT — a self-employment-oriented ICT course is a plausible way to redirect existing technical background toward the self-employment path they explicitly named, though this connects two separate direct statements (skills-mismatch complaint + business intent) rather than being stated by the respondent as one combined plan.",
            ],
            "why_recommended": "Matches the respondent's explicitly stated intent to start their own business in ICT, and offers an alternative to their current unsatisfying employed role without requiring a claim about what specifically is wrong with their current job.",
            "uncertainties": [
                "Course schedule (weekday/weekend) is not clearly stated in the extracted Sinhala-language text for this respondent's document, so it cannot be confirmed whether this fits alongside the respondent's current 40-hour/week job.",
                "It is not established whether the respondent's skills-mismatch complaint means they are over- or under-qualified for their current job; this recommendation does not depend on resolving that ambiguity, only on the separately-stated business intent.",
            ],
            "limitations": [
                "No employer-connection or placement information available.",
                "Course content is presented mostly in Sinhala; the respondent's language preference was not captured in the available evidence.",
            ],
            "evidence_strength": "MODERATE",
            "evidence_strength_reason": "The self-employment/ICT match is directly evidenced, but connecting it to the respondent's job-change reason requires bridging two separate statements, and schedule compatibility with their existing job could not be checked.",
        },
        {
            "rank": 2,
            "course_id": "COURSE-022",
            "course_name": "Computer Network Technician",
            "direct_respondent_evidence_used": [
                "ideal_sector = Information technology and communications",
                "occupational_class = Technical work (IT technician, lab technician, etc.)",
                "reason_wants_to_change = The work does not match my skills or qualifications",
                "usual_hours_per_week = 40.0 / actual_hours_last_week = 40.0",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: full-time course held on weekdays, English/Sinhala, leads to NVQ Competency Level 4, network-technician module focus.",
            ],
            "contextual_inferences": [
                "INFERENCE: because the respondent directly reported their current work does not match their skills or qualifications, and this course offers a specific, certifiable technical specialisation (networking) within their stated ICT sector, it may help address that stated skills-mismatch — this is an inference connecting a stated barrier to a stated sector, not a claim that this exact course was requested.",
            ],
            "why_recommended": "A certifiable, sector-matching technical specialisation that could plausibly address the respondent's stated reason for wanting to change jobs.",
            "uncertainties": [
                "This course is explicitly full-time on weekdays. The respondent directly reported currently working 40 hours per week under a temporary 12-36 month contract. This is a genuine, directly-evidenced scheduling tension (not an assumption): attending a full-time weekday course while holding a full-time weekday job is difficult on its face, though the respondent's actual capacity to arrange this (e.g. leave, resignation, employer agreement) is unknown and not assumed here either way.",
            ],
            "limitations": [
                "No part-time equivalent of this specific course was found in the retrieved set.",
                "No fee, location, or placement information available.",
            ],
            "evidence_strength": "LIMITED",
            "evidence_strength_reason": "Content match to the stated skills-mismatch barrier is plausible but inferred, and there is a concrete, directly-evidenced schedule conflict with the respondent's current full-time job that is not resolved by any available information.",
        },
    ],
    "no_defensible_recommendation": False,
    "no_defensible_recommendation_reason": None,
}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-131a2b60-1a70-4974-9dc0-8a1eaf51befd"] = {
    "recommendations": [
        {
            "rank": 1,
            "course_id": "COURSE-006",
            "course_name": "National Diploma In Information & Communication Technology",
            "direct_respondent_evidence_used": [
                "ideal_sector = Information technology and communications",
                "job_type_sought = Technical work",
                "training_type_would_help = Professional/technical certification",
                "main_obstacle_finding_work = No suitable training available nearby",
            ],
            "profile_context_used": [
                "GROUP-LEVEL: E_learning_orientation profile 2 ('moderate perceived utility and mixed learning ambition') — used only as background; the respondent's own direct answer (plans_further_edu = Yes, expected_highest_edu_e = Post-graduate degree) is stronger and more specific individual evidence and takes priority over the group tendency.",
            ],
            "course_evidence_used": [
                "Course text: full-time diploma, English-taught, technical module list (System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network), leads to NVQ Competency Level 5.",
            ],
            "contextual_inferences": [
                "INFERENCE: the respondent directly named 'professional/technical certification' as the training type that would help them, and this course leads to a stated NVQ level (a formal competency certification) in their stated sector — a reasonably close match between the TYPE of training they said would help and what this course actually provides.",
            ],
            "why_recommended": "Matches both the respondent's stated sector (ICT) and their specifically-named training-type preference (professional/technical certification), and the stated barrier (no suitable training available nearby) is directly addressed if this course is accessible to them.",
            "uncertainties": [
                "The document does not state course duration, so it cannot be confirmed or ruled out whether this course fits within the respondent's stated urgency window (income_urgency = 'Soon — within the next 3 months').",
                "Course location is not stated, so it is not possible to confirm this addresses the respondent's stated barrier ('no suitable training available nearby') for their specific district (Gampaha).",
            ],
            "limitations": [
                "No fee/cost information available.",
                "No stated location to check against the respondent's willingness to relocate only within the same province.",
            ],
            "evidence_strength": "STRONG",
            "evidence_strength_reason": "Multiple independent direct-evidence points (sector, job type, named training-type preference, and a directly-relevant stated barrier) all converge on the same course without requiring a long inference chain.",
        },
        {
            "rank": 2,
            "course_id": "COURSE-008",
            "course_name": "Computer Hardware Technician",
            "direct_respondent_evidence_used": [
                "ideal_sector = Information technology and communications",
                "job_type_sought = Technical work",
                "training_type_would_help = Professional/technical certification",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: full-time, weekdays, English-taught, module list (Introduction, Assembling, Disassembling, Trouble shooting, Preventive Maintenance, Estimating), leads to NVQ Competency Level 4.",
            ],
            "contextual_inferences": [],
            "why_recommended": "A more specialised, hands-on technical/certification match to the same stated sector and job-type preference, at a hardware-focused technical level distinct from the broader diploma above.",
            "uncertainties": [
                "Duration not stated (same limitation as rank 1).",
            ],
            "limitations": [
                "No fee, location, or placement information available.",
            ],
            "evidence_strength": "STRONG",
            "evidence_strength_reason": "Same direct-evidence convergence as rank 1 (sector, job type, certification preference), with clean, unambiguous course text.",
        },
        {
            "rank": 3,
            "course_id": "COURSE-055",
            "course_name": "Computer Hardware Technician",
            "direct_respondent_evidence_used": [
                "ideal_sector = Information technology and communications",
                "worked_while_studying = Yes",
                "current_activity_status = I have a job but was temporarily away from it last week",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: same module content as COURSE-008 (PC assembling, maintenance/repair, device configuration, software installation, network/internet), but explicitly stated as 'a part time course which will be held on weekends,' unlike COURSE-008.",
            ],
            "contextual_inferences": [
                "INFERENCE: this is the same technical content as rank 2, offered on a part-time/weekend schedule instead of full-time/weekdays. Because the respondent has recent work history and described themselves as having a job to return to only conditionally (has_job_to_return = No, but looking_while_absent = Yes, wanted_to_work = Yes), a weekend format may be easier to combine with job-search activity or future part-time work than a weekday full-time course — this is offered as an alternative schedule option, not a claim that the respondent cannot attend full-time.",
            ],
            "why_recommended": "Presented as the part-time-schedule counterpart to rank 2, so the respondent can compare both delivery formats for the same technical content before choosing.",
            "uncertainties": [
                "No direct evidence states a schedule preference either way; the inference above is offered as a practical option, not a confirmed need.",
            ],
            "limitations": [
                "No fee, location, or placement information available.",
                "No duration stated.",
            ],
            "evidence_strength": "MODERATE",
            "evidence_strength_reason": "Content match is identical to rank 2 (strong), but its distinguishing feature (part-time format) rests on an inference rather than a directly stated schedule preference, so overall confidence is lower than ranks 1-2.",
        },
    ],
    "no_defensible_recommendation": False,
    "no_defensible_recommendation_reason": None,
}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-a04f7d96-0e1d-49f2-8443-5cb15eeb9bf9"] = {
    "recommendations": [],
    "no_defensible_recommendation": True,
    "no_defensible_recommendation_reason": (
        "This respondent's direct evidence contains no usable field, sector, or work-direction "
        "preference: ideal_sector = 'Not sure', ideal_work_type = 'Not sure yet', and "
        "study_field_preference = 'Other field' (the specific field was never named). There is no "
        "prior work experience (worked_while_studying = No) and no stated training interest to "
        "substitute for a sector preference. The only retrieved candidates (a television-production "
        "diploma, an ICT diploma, and two agricultural/survey field-assistant courses) were surfaced "
        "by generic context terms (institution type, online-job-search method) that carry no genuine "
        "topical signal — recommending any of them would require inventing a field interest the "
        "respondent never expressed, which is prohibited. The respondent's own group-level profile "
        "context (D_motivation profile 1: 'externally or uncertainly motivated, with moderate study "
        "support' — consistent with this respondent's own direct answer that they are 'not sure why' "
        "they are studying their current path) reinforces rather than resolves this uncertainty, and "
        "per the task's evidence policy, group tendencies must never be used to select programme "
        "content in place of a missing direct preference. The scientifically correct action is to "
        "decline to recommend rather than construct a plausible-sounding but unsupported match. If "
        "this respondent were being served in practice, the appropriate next step is to ask them "
        "directly what field or type of work interests them before any course match is attempted."
    ),
}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-3a86d117-1b8c-4f8d-8d53-d6765b4a4034"] = {
    "recommendations": [
        {
            "rank": 1,
            "course_id": "COURSE-001",
            "course_name": "Freelancer Of Web Design & Development",
            "direct_respondent_evidence_used": [
                "ideal_sector = Information technology and communications",
                "study_field_preference = ICT or computing",
                "ideal_work_type = Start my own business",
                "already_job_searching = Yes — I am already searching",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: course is titled 'Freelancer Of Web Design & Development,' 3-month duration ('පාඨමාලා කාලය මාස 03'), fee LKR 20,000 ('පාඨමාලා ගාස්තුව 20,000/='), open to ages 15–45, leads to a government-recognised certificate, taught by an instructor with over 6 years of industry experience, and explicitly covers building a personal freelance income through web development, domain/hosting management, and freelance-platform account setup (e.g. Fiverr).",
                "Language field states English and Sinhala, but the course narrative itself is written almost entirely in Sinhala.",
            ],
            "contextual_inferences": [
                "INFERENCE: because the respondent directly stated they want to start their own business and specifically named ICT/computing as their field, a course whose explicit purpose is training freelance web-development entrepreneurs is a close content match to both stated preferences simultaneously (sector AND self-employment intent), not just the sector alone.",
            ],
            "why_recommended": "This is the closest available content match to two of the respondent's own direct statements at once: wanting to work in ICT, and wanting to start their own business, and the full course text — unlike the reduced structured dataset — reveals fee, duration, age-eligibility and certification detail that materially supports this being a genuine, concrete offering rather than a generic ICT course.",
            "uncertainties": [
                "The respondent's language comprehension or preference (Sinhala vs. English) was not captured anywhere in the available survey evidence for this respondent, and this specific course's content is overwhelmingly in Sinhala despite being labelled 'English and Sinhala' — whether this is a good fit on language grounds cannot be confirmed or ruled out from the available evidence.",
                "No evidence indicates whether the respondent has any prior web-design/coding exposure specifically (their evidence shows general ICT/computing interest, not a stated skill level).",
            ],
            "limitations": [
                "Course location is not stated.",
                "No explicit entry qualification (beyond the stated 15–45 age range) is given.",
                "Placement or employer-connection information is not stated — the course describes self-employment/freelance income methods, not job placement.",
            ],
            "evidence_strength": "STRONG",
            "evidence_strength_reason": "Two independent, directly-stated respondent preferences (ICT sector AND self-employment) both map onto explicit, concrete course content (not inferred), and the course document itself supplies unusually rich, specific detail (fee, duration, age range, certification) that corroborates it as a real, well-specified offering.",
        },
        {
            "rank": 2,
            "course_id": "COURSE-006",
            "course_name": "National Diploma In Information & Communication Technology",
            "direct_respondent_evidence_used": [
                "ideal_sector = Information technology and communications",
                "study_field_preference = ICT or computing",
                "expected_highest_edu_d = Bachelor's degree",
            ],
            "profile_context_used": [
                "GROUP-LEVEL: D_educational_cultural profile 4 ('work-experienced students, mainly in private institutions', n=66) — this respondent's group tendency toward private-institution study is consistent with their own directly-stated institution_type ('Private school or private degree-awarding institute'), used here only as corroborating context, not as the basis for this recommendation.",
            ],
            "course_evidence_used": [
                "Course text: full-time diploma, English-taught, module list covers System Analysis & Design, Software Programming, Database Systems, Web Programming, Local Area Network, and leads to NVQ Competency Level 5.",
            ],
            "contextual_inferences": [],
            "why_recommended": "A direct, uncomplicated content match to the respondent's stated ICT/computing field preference, at a higher formal qualification level (NVQ 5) than the more narrowly-scoped alternatives, which may better suit a respondent who is currently pursuing a Bachelor's degree.",
            "uncertainties": [
                "The course document does not state minimum entry requirements, so whether NVQ Level 5 entry is compatible with the respondent's current Bachelor's-level study is not confirmed either way.",
            ],
            "limitations": [
                "No fee or cost information is stated.",
                "No location is stated.",
            ],
            "evidence_strength": "MODERATE",
            "evidence_strength_reason": "Clear, direct sector/field match with clean, unambiguous course text, but the self-employment aspect of the respondent's stated preference is not addressed by this course, unlike rank 1.",
        },
        {
            "rank": 3,
            "course_id": "COURSE-009",
            "course_name": "Information And Communication Technolory Technician",
            "direct_respondent_evidence_used": [
                "ideal_sector = Information technology and communications",
                "study_field_preference = ICT or computing",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text module list: file/folder management, word processing, spreadsheets, presentations, databases, internet/email, operating-system installation, network troubleshooting, graphics for online/print media, static web page design, basic software development.",
            ],
            "contextual_inferences": [],
            "why_recommended": "Content matches the respondent's stated ICT/computing interest via a broad general-ICT-technician module list.",
            "uncertainties": [
                "This specific source document's narrative paragraph appears to contain text bled in from a different course ('Quantity Surveyor will give you theoretical knowledge...' inside an ICT Technician document) — the document is marked VALIDATED_WITH_LIMITATIONS for this reason. Only the module list and course title are treated as reliable here; the schedule statement ('full time... weekdays') appearing in that same suspect paragraph is reported but flagged as lower-confidence rather than treated as certain.",
            ],
            "limitations": [
                "Narrative/schedule portion of this specific document has a known text-quality issue (see uncertainties).",
                "No fee, cost, or location information available.",
            ],
            "evidence_strength": "LIMITED",
            "evidence_strength_reason": "Genuine content match on module list, but the source document's own quality flag and an apparent cross-course text contamination materially reduce confidence in this specific document's remaining claims.",
        },
    ],
    "no_defensible_recommendation": False,
    "no_defensible_recommendation_reason": None,
}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-0c6c34a2-a528-4c97-b06b-3b712f4ff24d"] = {
    "recommendations": [
        {
            "rank": 1,
            "course_id": "COURSE-040",
            "course_name": "Automobile Mechanic",
            "direct_respondent_evidence_used": [
                "ideal_sector = Manufacturing or production",
                "training_type_received = Training in new technologies (employer-provided, on-the-job)",
                "usual_hours_per_week = 60.0 / actual_hours_last_week = 60.0",
            ],
            "profile_context_used": [
                "GROUP-LEVEL: F_employment_security profile 2 ('predominantly permanent employment with stronger security') — background context only; not used to select course content.",
            ],
            "course_evidence_used": [
                "Course text: part-time course held on weekends, English-taught, modules on engine systems (petrol and diesel), transmission, steering, braking, and suspension systems.",
            ],
            "contextual_inferences": [
                "INFERENCE: automotive mechanical repair is a manufacturing/production-adjacent technical trade, offered as a broad sector-level match to the respondent's stated interest — the respondent did not name automotive work specifically, so this connects a stated sector to one plausible trade within it, not a stated skill.",
                "INFERENCE: because the respondent directly reported working 60 hours per week, the fact that this course is offered part-time on weekends (rather than full-time) means it does not have an evidenced schedule conflict with their current job, unlike a full-time weekday alternative would. This is a direct comparison of two stated facts, not a claim the respondent cannot attend full-time.",
            ],
            "why_recommended": "A specific, named technical trade within the respondent's stated broad sector (manufacturing/production), offered on a schedule with no evidenced conflict against their reported work hours.",
            "uncertainties": [
                "'Manufacturing or production' is a broad sector label; the respondent did not state a specific sub-skill or trade, so this is a sector-level match, not a specific stated-skill match.",
                "Whether the respondent's employer-provided 'training in new technologies' relates to automotive mechanics specifically is not stated anywhere in the evidence.",
            ],
            "limitations": [
                "No fee, cost, location, or entry-requirement information available.",
            ],
            "evidence_strength": "MODERATE",
            "evidence_strength_reason": "A specific, named technical course with a real (not merely coincidental) schedule fit to the respondent's reported work hours, but the sector-to-trade connection remains at the broad-sector level rather than a specific stated skill.",
        },
        {
            "rank": 2,
            "course_id": "COURSE-012",
            "course_name": "Refrigeration & Air Conditioning Technician",
            "direct_respondent_evidence_used": [
                "ideal_sector = Manufacturing or production",
                "usual_hours_per_week = 60.0 / actual_hours_last_week = 60.0",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: part-time course held on weekends, module list covering repair of refrigerators/freezers/display units/water coolers, cost estimation, window/split A/C repair, and central A/C system operation and maintenance.",
            ],
            "contextual_inferences": [
                "INFERENCE: refrigeration/air-conditioning technical work is another manufacturing/production-adjacent trade, offered as an alternative sector-level match to rank 1.",
                "INFERENCE: same schedule-compatibility observation as rank 1 (part-time/weekend course, no evidenced conflict with the respondent's reported 60-hour work week).",
            ],
            "why_recommended": "A second specific technical trade within the respondent's stated sector, offered on the same compatible part-time schedule, for comparison against rank 1.",
            "uncertainties": [
                "Same broad-sector-only match limitation as rank 1.",
            ],
            "limitations": [
                "No fee, cost, or location information available.",
                "This specific source document has a minor text-corruption artifact at the very end of its narrative paragraph (an inserted, out-of-place word); the module list itself is clean and was relied upon, the corrupted closing phrase was not.",
            ],
            "evidence_strength": "LIMITED",
            "evidence_strength_reason": "Same sector-only match strength as rank 1, with an additional minor source text-quality issue.",
        },
    ],
    "no_defensible_recommendation": False,
    "no_defensible_recommendation_reason": None,
}


# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-33aaf2f7-dc2a-4530-ae73-3bfdf5be63ab"] = {
    "recommendations": [
        {
            "rank": 1,
            "course_id": "COURSE-029",
            "course_name": "Mobile Phone Repair Technician",
            "direct_respondent_evidence_used": [
                "ideal_sector = Wholesale, retail, or repair",
                "occupational_class = Technical work (IT technician, lab technician, etc.)",
                "reason_wants_to_change = To get better career prospects and advancement",
                "usual_hours_per_week = 12.0 / actual_hours_last_week = 5.0",
            ],
            "profile_context_used": [
                "GROUP-LEVEL: F_employment_security profile 1 ('temporary/no-contract employment with uncertain security') — consistent with this respondent's own directly-stated oral, temporary contract and 'not likely' 12-month job security; background context only.",
            ],
            "course_evidence_used": [
                "Course text: full-time course held on weekdays, Sinhala-taught, leads to NVQ Competency Level 4, focused on mobile phone repair.",
            ],
            "contextual_inferences": [
                "INFERENCE: the respondent's current occupation is classified as technical/IT-adjacent work, and their stated target sector explicitly includes 'repair' — a certified repair-technician course is a specific, named-sector match that also plausibly builds on their existing technical occupational background, rather than starting a new field from zero.",
                "INFERENCE: the respondent directly reported working only 12 hours per week normally (5 hours in the most recent week), so a full-time weekday course would not obviously conflict with their current job's time demands, unlike respondents in this sample who reported 40-60 hour work weeks. This is a direct comparison of two stated facts, not an assumption about the respondent's overall availability or preferences.",
            ],
            "why_recommended": "Directly matches the 'repair' component of the respondent's stated target sector and their existing technical occupational background, with a certifiable NVQ outcome, and no evidenced schedule conflict with their current (low-hours) job.",
            "uncertainties": [
                "The respondent's stated reason for wanting to change jobs is career advancement, not necessarily a change of field — it is not confirmed whether they want to deepen their existing IT-technical path or pivot toward retail/repair specifically; this course addresses the sector-and-occupation overlap either way.",
            ],
            "limitations": [
                "No fee, cost, or location information available.",
                "Course is Sinhala-taught; the respondent's language preference was not captured in the available evidence.",
            ],
            "evidence_strength": "STRONG",
            "evidence_strength_reason": "A specific, literal sector-term match ('repair') combined with a plausible occupational-background fit and no evidenced schedule conflict.",
        },
        {
            "rank": 2,
            "course_id": "COURSE-008",
            "course_name": "Computer Hardware Technician",
            "direct_respondent_evidence_used": [
                "occupational_class = Technical work (IT technician, lab technician, etc.)",
                "obstacle_finding_this_job = No suitable training available nearby",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: full-time, weekdays, English-taught, hardware assembly/maintenance/troubleshooting modules, leads to NVQ Competency Level 4.",
            ],
            "contextual_inferences": [
                "INFERENCE: hardware repair/maintenance training is closely adjacent to the respondent's existing IT-technician occupational classification, offered as an alternative technical-repair specialisation to rank 1.",
            ],
            "why_recommended": "A second technical-repair option consistent with the respondent's existing occupational background, in case computer hardware (rather than mobile devices) better matches their actual prior experience.",
            "uncertainties": [
                "This is a broader, more generic match ('technical work' occupational class) than rank 1's literal sector-term match ('repair'), so it is offered as a secondary option rather than an equally strong first choice.",
            ],
            "limitations": [
                "No fee, cost, or location information available.",
            ],
            "evidence_strength": "MODERATE",
            "evidence_strength_reason": "Plausible occupational-background fit, but a weaker direct textual match to the respondent's stated target sector than rank 1.",
        },
    ],
    "no_defensible_recommendation": False,
    "no_defensible_recommendation_reason": None,
}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-00e2c251-39ad-4474-b077-2a2bbe78457a"] = {
    "recommendations": [
        {
            "rank": 1,
            "course_id": "COURSE-023",
            "course_name": "Construction Site Supervisor",
            "direct_respondent_evidence_used": [
                "ideal_sector = Construction and building",
                "ideal_work_type = Work for a local private Sri Lankan company",
                "reason_not_in_labour_force = Could not find suitable work after trying",
                "wants_to_work_future = Yes — I want to work at some point",
            ],
            "profile_context_used": [
                "GROUP-LEVEL: G_future_engagement profile 2 ('low/uncertain engagement, mostly no prior work experience') is consistent with this respondent's own direct answer that they have never worked (ever_worked = No); used only as corroborating background, not as a driver of course content.",
                "GROUP-LEVEL: G_economic_role profile 1 ('predominantly family/partner-supported non-provider') — background only.",
            ],
            "course_evidence_used": [
                "Course text: full-time course held on weekdays, English-taught, leads to NVQ Competency Level 4.",
            ],
            "contextual_inferences": [
                "INFERENCE: the respondent directly stated they could not find suitable work despite trying, and directly stated they want to work in construction — a certified construction-sector course may help address that stated barrier by providing a recognised qualification in their stated field of interest. This connects a stated barrier to a stated sector preference via a documented course outcome (NVQ 4), not an assumption about what the respondent needs.",
            ],
            "why_recommended": "Directly matches the respondent's stated sector, offers a formal NVQ qualification, and plausibly addresses their directly-stated difficulty finding suitable work.",
            "uncertainties": [
                "The course title ('Site Supervisor') may imply a supervisory role, but no entry requirement, minimum prior experience, or minimum education level is stated anywhere in the course document — it is therefore unknown, not confirmed either way, whether this course is designed for entry-level candidates like this respondent (O/L-level education, no prior work experience) or expects some existing construction background.",
                "The respondent's language comprehension (the course is English-taught) was not captured in the available evidence.",
            ],
            "limitations": [
                "No fee, cost, or location information available.",
                "No stated entry requirement to confirm or rule out eligibility.",
            ],
            "evidence_strength": "MODERATE",
            "evidence_strength_reason": "Strong sector-content match and a plausible barrier-addressing rationale, but genuine, unresolved uncertainty about whether the course's apparent seniority level suits a first-time jobseeker with no prior work experience.",
        },
        {
            "rank": 2,
            "course_id": "COURSE-019",
            "course_name": "Quantity Surveying Assistant",
            "direct_respondent_evidence_used": [
                "ideal_sector = Construction and building",
                "reason_not_in_labour_force = Could not find suitable work after trying",
                "highest_edu_completed = O/L level (Grade 10-11)",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: full-time course held on weekdays, English-taught, leads to NVQ Competency Level 4. The course title itself designates an 'Assistant' role.",
            ],
            "contextual_inferences": [
                "INFERENCE: the 'Assistant' designation in the course title is offered as a mildly more entry-appropriate signal than the 'Supervisor' title in rank 1, though this is inferred from the course name only — no explicit entry-level statement is present in the text.",
            ],
            "why_recommended": "A second construction-sector course, offered because its title suggests a more junior/entry-appropriate role than rank 1, which may better suit a first-time jobseeker.",
            "uncertainties": [
                "As with rank 1, no entry requirement is explicitly stated, so the 'Assistant' level-appropriateness inference above is not confirmed by the document itself.",
            ],
            "limitations": [
                "No fee, cost, or location information available.",
            ],
            "evidence_strength": "LIMITED",
            "evidence_strength_reason": "Same sector match as rank 1, with a weaker, title-only basis for its distinguishing rationale (entry-level appropriateness).",
        },
    ],
    "no_defensible_recommendation": False,
    "no_defensible_recommendation_reason": None,
}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-465701ee-3d2d-4f85-a044-abff06ba2e45"] = {
    "recommendations": [],
    "no_defensible_recommendation": True,
    "no_defensible_recommendation_reason": (
        "This respondent directly expresses genuine future engagement intent (wants_to_work_future = "
        "Yes, wants_further_edu = Yes, expected_highest_edu_g = Post-graduate degree), which "
        "distinguishes this case from a purely unmotivated one — but no field, sector, or work-type "
        "preference was ever stated (ideal_sector = 'Not sure', ideal_work_type = 'Not sure yet'), and "
        "there is no prior work-content evidence to substitute for one (worked_while_studying = No; "
        "current_activity_status = home duties). The individual_context_only field "
        "'most_useful_quality_for_job = IT and digital skills' might look like a hint toward an ICT "
        "recommendation, but per the evidence policy this field records a general OPINION about what "
        "is useful for finding work in general, not a stated personal interest or preference for this "
        "respondent, and using it to select a course would convert an explanation-only field into a "
        "content driver, which is prohibited. The retrieved candidates (a television-production "
        "diploma, an ICT diploma, and a secretarial-practices course) were surfaced only by generic "
        "background terms (education level, household context) and do not represent a defensible "
        "content match. As with the other weak-preference case in this sample, the scientifically "
        "correct response is to decline a specific course recommendation and note that a direct "
        "follow-up question about field/sector interest is needed before matching can proceed."
    ),
}

# ---------------------------------------------------------------------------
RECOMMENDATIONS["nysc-55bdfdcc-30fd-4115-9e2a-4620cde38963"] = {
    "recommendations": [
        {
            "rank": 1,
            "course_id": "COURSE-011",
            "course_name": "Baker",
            "direct_respondent_evidence_used": [
                "ideal_sector = Hotels, restaurants, and hospitality",
                "ideal_work_type = Start my own business",
                "ever_worked = Yes — I have worked before",
                "reason_not_in_labour_force = Could not find suitable work after trying",
            ],
            "profile_context_used": [
                "GROUP-LEVEL: G_economic_role profile 2 ('predominantly self-income provider/contributor') is consistent with this respondent's own direct answer that they are the primary household earner; background context only, not used to select course content.",
            ],
            "course_evidence_used": [
                "Course text: full-time course held on weekdays, Sinhala-taught, modules 'Produce Bread', 'Produce Cake', 'Produce Pastry', 'Baker Management', leads to NVQ Competency Level 4.",
            ],
            "contextual_inferences": [
                "INFERENCE: the course's 'Baker Management' module plausibly supports the respondent's directly-stated intent to start their own business, in addition to matching their stated hospitality sector — the course's practical management content is a documented course property, not an assumption about what a bakery business requires.",
            ],
            "why_recommended": "Directly matches the respondent's stated sector (hospitality) and stated intent (start own business) via a course whose own module list explicitly includes small-business-relevant management content, and offers a formal NVQ qualification.",
            "uncertainties": [
                "The respondent's record contains two seemingly inconsistent status fields (spell1_is_current = 'Yes — this is still my current situation' for a wage/salary job, versus current_activity_status = 'Not working or looking for work for another reason'); both are reported here as directly recorded, without resolving the apparent tension, since inventing an explanation is not permitted.",
                "Respondent's language comprehension was not captured in the available evidence; this course is Sinhala-taught.",
            ],
            "limitations": [
                "No fee, cost, or location information available.",
                "No stated entry requirement to confirm eligibility.",
            ],
            "evidence_strength": "STRONG",
            "evidence_strength_reason": "Both major directly-stated preferences (sector and self-employment intent) are matched by specific, named course content, not just a broad sector label.",
        },
        {
            "rank": 2,
            "course_id": "COURSE-007",
            "course_name": "Professional Cookery",
            "direct_respondent_evidence_used": [
                "ideal_sector = Hotels, restaurants, and hospitality",
                "ever_worked = Yes — I have worked before",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: full-time course held on weekdays, Sinhala-taught, modules covering Western and Eastern menus, fish/meat items, beverages, stocks/sauces/soups/salads, sweets and desserts.",
            ],
            "contextual_inferences": [],
            "why_recommended": "A broader culinary-skills match to the respondent's stated hospitality sector, complementing the more business-specific Baker course above.",
            "uncertainties": [
                "This specific source document shows minor text-quality issues at its end (a corrupted closing phrase and a stray 'Screenshot' artifact); the module list itself is clean and was used with confidence, but the exact final sentence of the narrative was not relied upon.",
            ],
            "limitations": [
                "No fee, cost, or location information available.",
            ],
            "evidence_strength": "MODERATE",
            "evidence_strength_reason": "Clear sector match via a specific module list, but does not address the respondent's self-employment intent as directly as rank 1.",
        },
        {
            "rank": 3,
            "course_id": "COURSE-050",
            "course_name": "Cake & Cake Structure",
            "direct_respondent_evidence_used": [
                "ideal_sector = Hotels, restaurants, and hospitality",
                "primary_earner_status = Yes — I provide the main household income",
                "has_children = Yes (num_children = 2.0)",
            ],
            "profile_context_used": [],
            "course_evidence_used": [
                "Course text: part-time course held on weekends, modules on icing methods, cake decoration, icing structures, and specialty cakes (birthday, wedding, engagement, eggless, homecoming, gateau).",
            ],
            "contextual_inferences": [
                "INFERENCE: this is a narrower specialisation within the same hospitality/baking sector as ranks 1-2, offered on a part-time/weekend schedule. Given the respondent is the household's primary earner with two children, a weekend format may be easier to combine with existing income and care responsibilities than a full-time weekday course — offered as a practical scheduling note, not a claim that the respondent cannot attend full-time.",
            ],
            "why_recommended": "A specialised, narrower hospitality/baking option offered on a different (part-time) schedule than ranks 1-2, for comparison.",
            "uncertainties": [
                "No direct evidence states a schedule preference; the scheduling inference above is offered as an option, not a confirmed need.",
            ],
            "limitations": [
                "No fee, cost, or location information available.",
            ],
            "evidence_strength": "LIMITED",
            "evidence_strength_reason": "Narrower content match than ranks 1-2 (cake decoration specifically, not general baking or cookery), and its distinguishing rationale rests on an unconfirmed scheduling inference.",
        },
    ],
    "no_defensible_recommendation": False,
    "no_defensible_recommendation_reason": None,
}
