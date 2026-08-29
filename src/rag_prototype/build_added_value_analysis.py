import csv, json

BASE = "/Users/vimashafernando/Desktop/ClusterRP"
OUT_DIR = f"{BASE}/outputs/rag_recommendation_prototype"

with open(f"{OUT_DIR}/test_recommendations.jsonl", encoding="utf-8") as f:
    recs = {json.loads(l)["respondent_id"]: json.loads(l) for l in f}

with open(f"{OUT_DIR}/baseline_sector_match.csv", newline="", encoding="utf-8-sig") as f:
    from collections import defaultdict
    baseline = defaultdict(list)
    for r in csv.DictReader(f):
        baseline[r["respondent_id"]].append(r["baseline_course_id"])

ANALYSIS = {
    "nysc-acaf63b5-6e8f-45fb-9d5a-cef8d615799b": dict(
        distinguished_within_field=True,
        distinguishing_evidence="study_field_preference (commerce/business/management) used directly, correctly ignoring the mis-mapped 'Education and teaching' sector baseline entirely",
        context_affected_recommendation=True,
        context_defensible=True,
        full_text_useful=True,
        full_text_example="Schedule (part-time/weekends) for both candidates, and HR module list, not present in a bare sector label",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="D_economic profile 1 (lower relative household position) roughly echoes the respondent's own stated moderate income; cited only as background, not used for content",
        unsupported_assumptions=False,
        baseline_would_differ=True,
        baseline_comparison="Baseline (approximate sector bridge 'Education and teaching'->Languages) returned 8 language courses, all irrelevant to the respondent's real stated field (commerce/business). RAG entirely avoided this baseline mapping error by using the respondent's actual field-preference text.",
        classification="HIGH",
        explanation="RAG used a specific stated field preference the sector-only baseline could not represent at all, and the baseline's own sector mapping was actively misleading here — a clear case where holistic reasoning outperformed category filtering.",
    ),
    "nysc-346623df-699b-4abb-a445-51abb3f16cc5": dict(
        distinguished_within_field=True,
        distinguishing_evidence="self-employment intent + stated skills-mismatch job-change reason + current occupational class, used to pick 2 of 17 same-sector baseline courses",
        context_affected_recommendation=True,
        context_defensible=True,
        full_text_useful=True,
        full_text_example="Course-001's fee/duration/age-range detail (from the raw screenshot text) and the explicit full-time-weekday schedule statement for COURSE-022, which directly informed the disclosed schedule-conflict finding",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="F_employment_security profile 1 label matches the respondent's own directly-stated temporary contract/security concern; background only",
        unsupported_assumptions=False,
        baseline_would_differ=True,
        baseline_comparison="Baseline returns all 17 ICT-sector courses undifferentiated. RAG narrowed to 2 using non-sector evidence (business intent, job-change reason) and surfaced a genuine schedule conflict (40hr/week job vs. full-time weekday course) that a sector filter has no way to detect.",
        classification="HIGH",
        explanation="Narrowed a 17-course undifferentiated sector list to 2 using multiple independent non-sector facts, and caught a real feasibility issue invisible to category filtering.",
    ),
    "nysc-131a2b60-1a70-4974-9dc0-8a1eaf51befd": dict(
        distinguished_within_field=True,
        distinguishing_evidence="named training-type preference ('professional/technical certification') and stated training-access barrier used to select and rank within the 17-course ICT baseline set",
        context_affected_recommendation=True,
        context_defensible=True,
        full_text_useful=True,
        full_text_example="NVQ level statements (Level 5 vs Level 4) distinguishing the two top courses, and the explicit part-time-vs-full-time schedule distinction between COURSE-008 and COURSE-055 (identical content, different schedule) — invisible without full text",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="E_learning_orientation profile label is weaker/less specific than the respondent's own direct answers (post-graduate intent, certification preference); correctly deferred to individual evidence",
        unsupported_assumptions=False,
        baseline_would_differ=True,
        baseline_comparison="Baseline returns the same 17-course undifferentiated ICT list. RAG identified 3 specific courses and distinguished a duplicate pair (COURSE-008/COURSE-055, same content, different schedule) that the baseline cannot tell apart at all.",
        classification="HIGH",
        explanation="Full course text was the only way to tell apart two identically-named, identically-mapped courses that differ only in schedule — a distinction structurally invisible to the reduced V2 dataset's course-level sector field and to the baseline.",
    ),
    "nysc-a04f7d96-0e1d-49f2-8443-5cb15eeb9bf9": dict(
        distinguished_within_field=False,
        distinguishing_evidence="No usable field evidence existed for either method",
        context_affected_recommendation=False,
        context_defensible=True,
        full_text_useful=False,
        full_text_example="Not applicable — no course was recommended",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="D_motivation profile 1 ('externally/uncertainly motivated') is consistent with the respondent's own direct 'not sure why I'm studying' answer, but was correctly NOT used to select any course",
        unsupported_assumptions=False,
        baseline_would_differ=False,
        baseline_comparison="Baseline also returns no meaningful match ('Not sure' maps to nothing). Both methods correctly produce no recommendation, but RAG additionally explains WHY and explicitly names the individual_context_only field ('IT and digital skills') it correctly declined to use as a substitute preference.",
        classification="MODERATE",
        explanation="No course-list value over the (also-empty) baseline, but real value in the auditable reasoning: RAG explicitly identified and rejected a plausible-looking but policy-prohibited shortcut (using an opinion field as a stand-in preference) rather than silently doing nothing.",
    ),
    "nysc-3a86d117-1b8c-4f8d-8d53-d6765b4a4034": dict(
        distinguished_within_field=True,
        distinguishing_evidence="self-employment intent ('start my own business') used to rank a freelance/entrepreneurship-focused course above generic ICT diploma/technician courses within the same 17-course sector baseline",
        context_affected_recommendation=True,
        context_defensible=True,
        full_text_useful=True,
        full_text_example="Course-001's fee (LKR 20,000), 3-month duration, age range 15-45, and government-certificate detail — none of which exist in the reduced V2 skill_keywords-only representation",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="D_educational_cultural profile 4 (work-experienced, private institutions) matches the respondent's own direct institution_type answer; background only",
        unsupported_assumptions=False,
        baseline_would_differ=True,
        baseline_comparison="Baseline returns the same undifferentiated 17-course ICT list with no way to prioritise. RAG used the self-employment preference (present in the respondent's evidence but absent from the sector-only baseline signal) to rank a specific freelance-focused course first.",
        classification="HIGH",
        explanation="Two independent stated preferences (sector + self-employment) converged on one specific course invisible to a sector-only filter, and full course text supplied concrete fee/duration/certification detail unavailable in the reduced dataset.",
    ),
    "nysc-0c6c34a2-a528-4c97-b06b-3b712f4ff24d": dict(
        distinguished_within_field=True,
        distinguishing_evidence="employer-provided 'training in new technologies' plus reported 60-hour work week used to narrow a 21-course two-skill-area baseline to 2 specific, schedule-compatible trades",
        context_affected_recommendation=True,
        context_defensible=True,
        full_text_useful=True,
        full_text_example="Part-time/weekend schedule statements for both selected courses, directly compared against the respondent's stated 60-hour work week",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="F_employment_security profile 2 (secure employment) background only",
        unsupported_assumptions=False,
        baseline_would_differ=True,
        baseline_comparison="Baseline's broad sector bridge ('Manufacturing or production' -> two skill areas) returns 21 undifferentiated courses spanning automotive, electrical, and appliance-repair trades. RAG narrowed to 2 using the respondent's reported work hours as a real, evidenced schedule filter.",
        classification="MODERATE",
        explanation="Meaningful narrowing (21->2) and a real schedule-compatibility check, but the underlying sector signal itself is broad and no specific sub-skill was ever stated by the respondent, so the final selection remains a sector-level match rather than a precise content match.",
    ),
    "nysc-33aaf2f7-dc2a-4530-ae73-3bfdf5be63ab": dict(
        distinguished_within_field=True,
        distinguishing_evidence="literal 'repair' term in the stated sector plus current IT-technician occupational classification used to identify repair-trade courses the baseline's category mapping could not represent at all",
        context_affected_recommendation=True,
        context_defensible=True,
        full_text_useful=True,
        full_text_example="'Mobile Phone Repairing Craftsman' title text confirming the repair-trade content and NVQ level, not derivable from a coarse sector label",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="F_employment_security profile 1 background only",
        unsupported_assumptions=False,
        baseline_would_differ=True,
        baseline_comparison="Baseline's sector bridge maps 'Wholesale, retail, or repair' only to Business/Management & Administration (5 store/HR/business courses) and structurally has no way to reach the repair trades, because the approximate sector-bridge table used for the baseline does not include a 'repair' mapping. RAG's lexical retrieval found the repair-trade courses directly by matching the actual word 'repair' in both the respondent's stated sector and the course titles.",
        classification="HIGH",
        explanation="This is the clearest case in the sample where the naive category baseline was not just less precise but structurally unable to surface the most relevant courses at all, while RAG's full-text lexical matching found them directly.",
    ),
    "nysc-00e2c251-39ad-4474-b077-2a2bbe78457a": dict(
        distinguished_within_field=True,
        distinguishing_evidence="course title wording ('Supervisor' vs 'Assistant') used to reason about likely seniority level relative to the respondent's O/L-only education and no prior work experience",
        context_affected_recommendation=True,
        context_defensible=True,
        full_text_useful=True,
        full_text_example="Full course text was checked for (and found to be missing) any stated entry requirement, which the recommendation explicitly and correctly reports as unknown rather than assumed",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="G_future_engagement profile 2 (no prior work experience) directly echoes the respondent's own ever_worked=No answer; background only",
        unsupported_assumptions=False,
        baseline_would_differ=True,
        baseline_comparison="Baseline returns 8 undifferentiated construction-sector courses. RAG narrowed to 2 and used the respondent's stated barrier (could not find suitable work) to motivate the recommendation, while explicitly disclosing the level-appropriateness uncertainty a category filter would silently ignore either way.",
        classification="MODERATE",
        explanation="Genuine narrowing and an honest disclosure of missing eligibility information, but the distinguishing evidence (a title-word inference about seniority) is thinner than the certification- or business-intent-based distinctions seen in other cases.",
    ),
    "nysc-465701ee-3d2d-4f85-a044-abff06ba2e45": dict(
        distinguished_within_field=False,
        distinguishing_evidence="No usable field evidence existed for either method",
        context_affected_recommendation=False,
        context_defensible=True,
        full_text_useful=False,
        full_text_example="Not applicable — no course was recommended",
        profile_added_info=False,
        profile_repeats_individual=False,
        profile_note="Profile context was not the deciding factor either way; the case turned entirely on the absence of a direct field preference",
        unsupported_assumptions=False,
        baseline_would_differ=False,
        baseline_comparison="Both methods correctly produce no meaningful recommendation. RAG additionally identifies and explicitly rejects the temptation to use an individual_context_only opinion field ('IT and digital skills is useful') as a substitute preference.",
        classification="MODERATE",
        explanation="Same value pattern as the other weak-evidence case: no course-list improvement over an equally-empty baseline, but real, auditable value in correctly declining to invent a preference.",
    ),
    "nysc-55bdfdcc-30fd-4115-9e2a-4620cde38963": dict(
        distinguished_within_field=True,
        distinguishing_evidence="self-employment intent ('start my own business') used to rank Baker (which has an explicit 'Baker Management' module) above the more generic Professional Cookery course, within the same small 5-course baseline",
        context_affected_recommendation=True,
        context_defensible=True,
        full_text_useful=True,
        full_text_example="The 'Baker Management' module line, which is the specific textual basis for ranking Baker above Cookery for this respondent's stated business intent — not visible in a bare sector/skill_keywords listing",
        profile_added_info=False,
        profile_repeats_individual=True,
        profile_note="G_economic_role profile 2 (self-income provider) matches the respondent's own direct primary_earner_status answer; background only",
        unsupported_assumptions=False,
        baseline_would_differ=True,
        baseline_comparison="Baseline returns the same 5 hospitality-sector courses with no ranking. RAG used the self-employment intent to rank Baker above Cookery specifically because of its documented management module — a within-category distinction the baseline cannot make.",
        classification="HIGH",
        explanation="A clean example of using full course-module text to rank within an already-small, correctly-identified category, based on a real stated preference (self-employment) that a sector filter alone cannot use.",
    ),
}

rows = []
for rid, a in ANALYSIS.items():
    rag_ids = [r["course_id"] for r in recs[rid]["recommendations"]]
    base_ids = baseline[rid]
    rows.append({
        "respondent_id": rid,
        "rag_course_ids": ";".join(rag_ids) if rag_ids else "(none — NO_DEFENSIBLE_RECOMMENDATION)",
        "n_rag_recommendations": len(rag_ids),
        "baseline_course_ids": ";".join(base_ids),
        "n_baseline_matches": len(base_ids) if base_ids != ["(none — no catalogue skill_area mapped to this sector)"] else 0,
        "q1_distinguished_within_same_field": a["distinguished_within_field"],
        "q2_distinguishing_evidence": a["distinguishing_evidence"],
        "q3_context_affected_recommendation": a["context_affected_recommendation"],
        "q4_context_reasoning_defensible": a["context_defensible"],
        "q5_full_course_text_useful_beyond_v2": a["full_text_useful"],
        "q5_example": a["full_text_example"],
        "q6_profile_context_added_information": a["profile_added_info"],
        "q7_profile_context_merely_repeated_individual_evidence": a["profile_repeats_individual"],
        "profile_note": a["profile_note"],
        "q8_unsupported_assumptions_detected": a["unsupported_assumptions"],
        "q9_baseline_would_produce_same_result": not a["baseline_would_differ"],
        "baseline_vs_rag_comparison": a["baseline_comparison"],
        "llm_added_value_classification": a["classification"],
        "llm_added_value_explanation": a["explanation"],
    })

fieldnames = list(rows[0].keys())
with open(f"{OUT_DIR}/llm_added_value_analysis.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow(r)

from collections import Counter
print("Wrote llm_added_value_analysis.csv")
print("Classification distribution:", dict(Counter(r["llm_added_value_classification"] for r in rows)))
