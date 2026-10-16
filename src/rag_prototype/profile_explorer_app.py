"""
Local exploration tool: "what does the full assigned profile actually tell us
about this person, beyond the ideal_sector question we ask directly?"

Built because the new-person architecture (see new_person_profile_context.py)
was only surfacing 1-2 cherry-picked findings per profile — this exposes every
variable in every assigned profile's DIRECT_GROUP_DISTRIBUTIONS (30-58 per
profile, confirmed by profile_data_parser.py against all 17 real profile
docs), grouped by theme, next to the respondent's OWN actual answer for the
same variables where available — so it's visible, side by side, which group
patterns line up with what the person actually said and which don't.

Read-only exploration tool. Does not call the OpenAI API, does not write to
any output file, does not modify §0 (new_respondent_cluster_assignment.py,
reused unmodified) or any profile document.

Run: python3 profile_explorer_app.py
Then open http://127.0.0.1:5055/
"""
import csv
import json
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request, Response, send_from_directory
from flask_cors import CORS

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_v2 import BASE, verify_corpus
from env_config import get_production_model, verify_production_model
import context_pack_v2
import new_respondent_cluster_assignment as nrca
from profile_data_parser import parse_profile_document
import new_person_profile_context as npc
from new_person_profile_context import PUBLISHED_MODEL_ACCURACY
import new_person_candidate_selection as ncs
import new_person_context_pack as npcp
from new_person_recommendation_schema import NewPersonRecommendationResponse
from new_person_openai_client import call_new_person_recommendation_api
from retrieval_v2 import SECTOR_BRIDGE
from evidence_safeguards import (
    build_allowed_evidence_index, filter_authorized_findings, check_explicit_answers_not_fabricated,
)
from profile_response_distributions import profile_response_distribution
from cluster_catalogue import catalogue_for_branch, full_research_tree, metadata_for_profile
from officer_recommendation_service import generate_officer_briefing
import recommendation_translation

FEATURE_MANIFEST_CSV = BASE / "outputs/nysc_survey_feature_manifest.csv"
Q1_OPTIONS_PATH = BASE / "outputs/rag_new_person_intake_v1/q1_occupation_options_by_skill_area.json"

_survey_question_map = None


def load_survey_question_map() -> dict:
    """variable -> {question_id, section, framework, question_text}, sourced from
    outputs/nysc_survey_feature_manifest.csv — the real national School-to-Work
    Transition Survey (SWTS) question each clustering/profile variable came from."""
    global _survey_question_map
    if _survey_question_map is None:
        with open(FEATURE_MANIFEST_CSV, newline="", encoding="utf-8-sig") as f:
            _survey_question_map = {r["variable"]: r for r in csv.DictReader(f)}
    return _survey_question_map


def _normalize_profile_key(profile_key: str, known_keys) -> str:
    """Defense in depth: the model is instructed to return the bare key (e.g.
    'D_motivation_p2'), but has been observed to occasionally copy the whole
    decorated '------ PROFILE: key ------' marker line instead. Strip that
    decoration rather than let a formatting slip silently break the chart
    lookup — never trust prompt compliance alone for something with a cheap,
    reliable mechanical fix."""
    if profile_key in known_keys:
        return profile_key
    stripped = profile_key.replace("-", "").replace("PROFILE:", "").strip()
    return stripped if stripped in known_keys else profile_key


def enrich_finding(variable: str, profile_key: str, parsed_profiles_by_key: dict) -> dict:
    """Attaches, for one LLM-cited ProfileFinding, (a) the real survey question it came
    from and (b) the full observed distribution for that variable within that specific
    profile — so the frontend can render a chart instead of just quoting prose."""
    qmap = load_survey_question_map()
    question = qmap.get(variable)
    distribution_entry = None
    profile_key = _normalize_profile_key(profile_key, parsed_profiles_by_key.keys())
    parsed = parsed_profiles_by_key.get(profile_key)
    if parsed:
        for d in parsed["distributions"]:
            if d.get("variable") == variable:
                distribution_entry = dict(d)
                break
    if distribution_entry and distribution_entry.get("type") == "ordered":
        labelled = profile_response_distribution(profile_key, variable)
        source_n = distribution_entry.get("eligible_n")
        if source_n is not None and labelled["eligible_n"] != source_n:
            raise ValueError(
                f"{profile_key}/{variable}: labelled response n={labelled['eligible_n']} "
                f"does not match frozen profile summary n={source_n}"
            )
        distribution_entry["distribution"] = labelled["distribution"]
        distribution_entry["display"] = "answer_percentages"
    return {
        "survey_question": {
            "question_id": question["question_id"], "section": question["section"],
            "framework": question["framework"], "question_text": question["question_text"],
        } if question else None,
        "distribution": distribution_entry,
    }


VALUES_CSV = BASE / "outputs/nysc_survey_cleaned_values.csv"
LABELS_CSV = BASE / "outputs/nysc_survey_cleaned_labels.csv"

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

LEGACY_PARTICIPANT_EXPLORER_PATHS = frozenset({"/api/respondents", "/api/explore"})


@app.before_request
def guard_legacy_participant_explorer():
    if (
        request.path.rstrip("/") in LEGACY_PARTICIPANT_EXPLORER_PATHS
        and os.environ.get("ENABLE_LEGACY_PARTICIPANT_EXPLORER") != "true"
    ):
        return jsonify({"error": "Not found"}), 404

VAR_LISTS = {
    "D_motivation": ["study_motivation_type", "autonomy_in_study", "competence_in_study_field",
                      "relatedness_at_institution"],
    "D_economic": ["household_income", "household_size", "household_workers", "household_unemployed",
                    "primary_earner_status", "primary_income_source", "edu_funding_source"],
    "D_educational_cultural": ["father_edu", "mother_edu", "expected_highest_edu_d", "institution_type",
                                 "worked_while_studying", "re_entered_education"],
    "E_learning_orientation": ["past_edu_usefulness", "plans_further_edu", "expected_highest_edu_e"],
    "F_employment_security": ["contract_type", "job_security_12months", "sector_formality"],
    "G_economic_role": ["household_income", "household_size", "household_workers", "household_unemployed",
                          "primary_earner_status", "primary_income_source"],
    "G_future_engagement": ["reason_not_in_labour_force", "ever_worked", "wants_to_work_future",
                              "wants_further_edu"],
}

# Real, verified answer options per variable — pulled directly from
# outputs/nysc_survey_cleaned_values.csv / _labels.csv (see the extraction
# used to build this dict), not invented. Numeric (count) fields are typed
# "number" instead of a fixed choice list.
NUMBER_VARS = {"household_size", "household_workers", "household_unemployed"}

NUMBER_QUESTIONS = {
    "household_size": "How many people live in your household (including you)?",
    "household_workers": "How many people in your household are currently working (earning income)?",
    "household_unemployed": "How many people in your household are currently unemployed?",
}

VARIABLE_QUESTIONS = {
    "study_motivation_type": {"question": "Why are you studying your current subject?",
        "options": nrca._D_MOTIVATION_CANONICAL["study_motivation_type"]},
    "autonomy_in_study": {"question": "How much choice and control do you have over what/how you study?",
        "options": nrca._D_MOTIVATION_CANONICAL["autonomy_in_study"]},
    "competence_in_study_field": {"question": "How capable do you feel in your study field?",
        "options": nrca._D_MOTIVATION_CANONICAL["competence_in_study_field"]},
    "relatedness_at_institution": {"question": "How connected do you feel to your institution's community?",
        "options": nrca._D_MOTIVATION_CANONICAL["relatedness_at_institution"]},
    "household_income": {"question": "What is your household's monthly income?", "options": {
        1: "Below LKR 30,000", 2: "LKR 30,000 – 60,000", 3: "LKR 60,000 – 120,000",
        4: "LKR 120,000 – 200,000", 5: "Above LKR 200,000", 99: "Prefer not to say"}},
    "primary_earner_status": {"question": "Are you the main household income provider?", "options": {
        "no": "No — someone else is the main provider", "shared": "Shared — several people contribute roughly equally",
        "yes": "Yes — I provide the main household income"}},
    "primary_income_source": {"question": "What is your own main personal income source?", "options": {
        1: "My regular job or business", 2: "Unemployment or social security benefits",
        3: "An education grant, scholarship, or training allowance", 4: "My parents or family",
        5: "My partner or spouse", 6: "Casual or informal work", 99: "Other source"}},
    "edu_funding_source": {"question": "How is your current/most recent education funded?", "options": {
        1: "Government-funded or free of charge", 2: "Scholarship or grant", 3: "Paid for by my family",
        4: "I pay from my own earnings", 5: "Employer-sponsored", 99: "Other arrangement"}},
    "father_edu": {"question": "What is your father's highest completed education?", "options": {
        0: "No schooling", 1: "Primary/Elementary (Grade 1–5)", 2: "O/L level (Grade 9–11)",
        3: "A/L level (Grade 12–13)", 4: "Vocational certificate / NVQ", 5: "Diploma",
        6: "Bachelor's degree", 7: "Post-graduate (Masters/PhD)", 99: "Do not know / prefer not to say"}},
    "mother_edu": {"question": "What is your mother's highest completed education?", "options": {
        1: "Primary/Elementary (Grade 1–5)", 2: "O/L level (Grade 9–11)", 3: "A/L level (Grade 12–13)",
        4: "Vocational certificate / NVQ", 5: "Diploma", 6: "Bachelor's degree",
        7: "Post-graduate (Masters/PhD)", 99: "Do not know / prefer not to say"}},
    "expected_highest_edu_d": {"question": "What is the highest education you expect to complete?", "options": {
        1: "Primary school", 2: "O/L level", 3: "A/L level", 5: "Diploma", 6: "Bachelor's degree",
        7: "Post-graduate degree"}},
    "institution_type": {"question": "What type of institution are you currently studying at?", "options": {
        1: "Government school or state university", 2: "Government vocational/technical institute (NYSC, NAITA, VTA, etc.)",
        3: "Private school or private degree-awarding institute", 4: "International school or foreign university programme",
        5: "Online or distance learning programme", 99: "Other"}},
    "worked_while_studying": {"question": "Have you worked for pay while studying?",
        "options": {"no": "No", "yes": "Yes"}},
    "re_entered_education": {"question": "Did you re-enter education after a break?",
        "options": {"no": "No", "yes": "Yes"}},
    "past_edu_usefulness": {"question": "How useful has your education been for finding work?", "options": {
        1: "Very useful — directly relevant, employers value it", 2: "Somewhat useful — helps to some extent",
        3: "Not useful — little relevance to jobs I am looking for", 4: "Do not know"}},
    "plans_further_edu": {"question": "Do you plan to pursue further education/training?",
        "options": {"no": "No", "unsure": "Do not know yet", "yes": "Yes"}},
    "expected_highest_edu_e": {"question": "What is the highest education you expect to complete?", "options": {
        2: "O/L level", 4: "Vocational certificate or NVQ", 5: "Diploma", 6: "Bachelor's degree",
        7: "Post-graduate degree"}},
    "contract_type": {"question": "What is your current employment contract type?", "options": {
        1: "No contract at all", 2: "Oral contract — permanent/unlimited", 3: "Oral contract — temporary (12–36 months)",
        4: "Oral contract — temporary (under 12 months)", 5: "Written contract — permanent/unlimited",
        6: "Written contract — temporary (12–36 months)", 7: "Written contract — temporary (under 12 months)",
        8: "Do not know"}},
    "job_security_12months": {"question": "How likely is it you'll still have this job in 12 months?", "options": {
        1: "Very likely — my job is secure", 2: "Likely but not certain — I have some concern",
        3: "Not likely — I doubt I will still have this job", 4: "I do not know"}},
    "sector_formality": {"question": "How formal is your current employer?", "options": {
        1: "Fully formal — registered employer, written contract, statutory benefits",
        2: "Mostly formal — some documentation but not fully compliant",
        3: "Mixed — some formal, some informal aspects", 5: "Fully informal — no documentation, cash only"}},
    "reason_not_in_labour_force": {"question": "What best describes why you're not currently working?", "options": {
        1: "Own illness, injury, or pregnancy", 2: "Personal or family responsibilities (caring for children, elderly, etc.)",
        3: "Currently in education or training", 4: "Already found work to start in the future",
        5: "Already arranged self-employment to start in the future", 6: "Awaiting recall to a former job",
        7: "Awaiting the busy season (seasonal worker)", 8: "Believe there is no suitable work available in this area",
        9: "I do not meet employers' requirements — feel I lack qualifications",
        10: "Could not find suitable work after trying", 11: "Do not know how or where to look for work",
        12: "Have not started looking yet", 99: "Other reason"}},
    "ever_worked": {"question": "Have you ever worked for pay or profit before?",
        "options": {"no": "No — I have never worked", "yes": "Yes — I have worked before"}},
    "wants_to_work_future": {"question": "Do you want to work at some point in the future?",
        "options": {"no": "No — I do not want to work", "yes": "Yes — I want to work at some point"}},
    "wants_further_edu": {"question": "Do you want to pursue further education?",
        "options": {"no": "No", "unsure": "Not sure yet", "yes": "Yes"}},
}

BRANCH_ROUTING_QUESTION = {
    "question": "Which best describes your current situation?",
    "options": [
        {"code": "D", "label": "I'm currently in education (school, university, or a training programme)"},
        {"code": "E", "label": "I've finished or left education and I'm unemployed or searching for work"},
        {"code": "F", "label": "I'm currently employed (in paid work)"},
        {"code": "G", "label": "I'm not working, not studying, and not currently searching for work"},
    ],
}

IDEAL_SECTOR_OPTIONS = sorted(SECTOR_BRIDGE.keys()) + ["not sure"]
IDEAL_SECTOR_DISPLAY = {
    "information technology and communications": "Information technology and communications",
    "manufacturing or production": "Manufacturing or production",
    "agriculture, forestry, and fishing": "Agriculture, forestry, and fishing",
    "personal services (beauty, fitness, wellness)": "Personal services (beauty, fitness, wellness)",
    "hotels, restaurants, and hospitality": "Hotels, restaurants, and hospitality",
    "construction and building": "Construction and building",
    "creative, media, and arts": "Creative, media, and arts",
    "transport, storage, and logistics": "Transport, storage, and logistics",
    "wholesale, retail, or repair": "Wholesale, retail, or repair",
    "finance, banking, and insurance": "Finance, banking, and insurance",
    "education and teaching": "Education and teaching",
    "not sure": "Not sure",
}

_labels_cache = None
_values_cache = None


def load_all_rows():
    global _labels_cache, _values_cache
    if _labels_cache is None:
        with open(LABELS_CSV, newline="", encoding="utf-8-sig") as f:
            _labels_cache = {r["respondent_id"]: r for r in csv.DictReader(f)}
        with open(VALUES_CSV, newline="", encoding="utf-8-sig") as f:
            _values_cache = {r["respondent_id"]: r for r in csv.DictReader(f)}
    return _values_cache, _labels_cache


@app.route("/api/respondents")
def api_respondents():
    branch = request.args.get("branch", "D")
    values, labels = load_all_rows()
    out = []
    for rid, vrow in values.items():
        if vrow.get("branch") != branch or vrow.get("branch_routing_source") != "translated_final_active_branch":
            continue
        lrow = labels.get(rid, {})
        out.append({
            "respondent_id": rid,
            "ideal_sector": lrow.get("ideal_sector") or "(not stated)",
            "study_field_preference": lrow.get("study_field_preference") or "(not stated)",
        })
    out.sort(key=lambda r: r["ideal_sector"])
    return jsonify(out)


def build_answers_for_model(respondent_id: str, model_id: str, values: dict, labels: dict) -> dict:
    vrow = values.get(respondent_id, {})
    lrow = labels.get(respondent_id, {})
    answers = {}
    for var in VAR_LISTS[model_id]:
        code = vrow.get(var)
        if code not in (None, ""):
            answers[var] = {"value_code": code, "value_label": lrow.get(var)}
    return answers


@app.route("/api/explore")
def api_explore():
    branch = request.args.get("branch", "D")
    respondent_id = request.args.get("respondent_id")
    if not respondent_id:
        return jsonify({"error": "respondent_id required"}), 400

    values, labels = load_all_rows()
    if respondent_id not in values:
        return jsonify({"error": f"unknown respondent_id {respondent_id}"}), 404

    profile_index = context_pack_v2.load_profile_index()
    models = nrca.BRANCH_MODELS.get(branch, [])

    profiles_out = []
    all_vars_seen = set()
    for model_id in models:
        answers = build_answers_for_model(respondent_id, model_id, values, labels)
        result = nrca.assign_profile(model_id, answers)
        profile_key = f"{model_id}_p{result.profile_id}"
        doc_text = context_pack_v2.load_profile_doc(profile_key, profile_index)
        parsed = parse_profile_document(doc_text)
        for d in parsed["distributions"]:
            all_vars_seen.add(d.get("variable"))
        pub = PUBLISHED_MODEL_ACCURACY[model_id]

        profiles_out.append({
            "model_id": model_id,
            "profile_id": result.profile_id,
            "profile_label": result.profile_label,
            "profile_key": profile_key,
            "membership_similarity_percent": result.confidence_percent,
            "distance_tie": result.distance_tie,
            "model_published_accuracy": pub["accuracy"],
            "model_judgment": pub["judgment"],
            "cluster_forming_answers": {k: v["value_label"] for k, v in answers.items()},
            "parsed": parsed,
        })

    # respondent's own actual answer for every variable that appears in ANY
    # of their assigned profiles' distributions, so it can be shown side by
    # side with the group pattern.
    lrow = labels.get(respondent_id, {})
    vrow = values.get(respondent_id, {})
    own_answers = {}
    for var in sorted(all_vars_seen):
        label_val = lrow.get(var)
        if label_val not in (None, ""):
            own_answers[var] = label_val

    return jsonify({
        "respondent_id": respondent_id,
        "branch": branch,
        "own_ideal_sector": lrow.get("ideal_sector"),
        "own_study_field_preference": lrow.get("study_field_preference"),
        "own_answers_for_profile_variables": own_answers,
        "profiles": profiles_out,
    })


@app.route("/api/question_config")
def api_question_config():
    branch = request.args.get("branch", "D")
    models = nrca.BRANCH_MODELS.get(branch, [])
    cluster_questions = []
    for model_id in models:
        qs = []
        for var in VAR_LISTS[model_id]:
            qtype = "number" if var in NUMBER_VARS else "choice"
            if qtype == "number":
                q = {"variable": var, "question": NUMBER_QUESTIONS[var], "type": qtype}
            else:
                spec = VARIABLE_QUESTIONS[var]
                q = {"variable": var, "question": spec.get("question", var), "type": qtype,
                     "options": [{"code": str(k), "label": v} for k, v in spec["options"].items()]}
            qs.append(q)
        cluster_questions.append({"model_id": model_id, "questions": qs})

    return jsonify({
        "branch": branch,
        "branch_routing_question": BRANCH_ROUTING_QUESTION,
        "cluster_questions": cluster_questions,
        "ideal_sector_options": [{"code": k, "label": IDEAL_SECTOR_DISPLAY[k]} for k in IDEAL_SECTOR_OPTIONS],
        "q1_options_by_skill_area": Q1_OPTIONS_PATH.read_text(encoding="utf-8"),
        "sector_bridge": SECTOR_BRIDGE,
        "q2_options": ["Get a job", "Improve skills in my current job", "Start my own business",
                       "Continue on to further education", "Build general skills, not sure about the next step yet"],
        "q3_options": ["Full-time, weekdays", "Part-time, weekends", "No strong preference"],
        "q4_options": ["Sinhala", "English", "No strong preference"],
        "q5_options": ["Yes, I want a formal NVQ or qualification", "Not necessarily — I mainly want the practical skills", "Not sure"],
    })


def decode_new_person_intake(body: dict) -> tuple[str, dict, list[str], dict]:
    """Decode the shared intake payload for both preview and generation.

    Keeping this path shared is important: the no-cost preview must show the
    exact profile assignment and evidence set that the paid GPT call receives.
    """
    branch = body["branch"]
    if branch not in nrca.BRANCH_MODELS:
        raise ValueError(f"Unknown branch '{branch}'")

    cluster_answers = {}
    for var, code in body.get("cluster_answers", {}).items():
        spec = VARIABLE_QUESTIONS.get(var)
        if var in NUMBER_VARS:
            label = str(code)
        elif spec:
            options = {str(k): v for k, v in spec["options"].items()}
            label = options.get(str(code), str(code))
        else:
            raise ValueError(f"Unknown background variable '{var}'")
        cluster_answers[var] = {"value_code": code, "value_label": label}

    multi_value_request = "ideal_sectors" in body
    raw_sector_values = body.get("ideal_sectors") if multi_value_request else [body.get("ideal_sector")]
    if not isinstance(raw_sector_values, list):
        raise ValueError("ideal_sectors must be a list")
    sector_codes = []
    for raw_sector in raw_sector_values:
        code = str(raw_sector or "").strip().lower()
        if not code:
            continue
        if code not in IDEAL_SECTOR_DISPLAY and multi_value_request:
            raise ValueError(f"Unknown sector '{raw_sector}'")
        if code not in sector_codes:
            sector_codes.append(code)
    if not sector_codes:
        raise ValueError("Select at least one sector")
    if len(sector_codes) > 3:
        raise ValueError("Select no more than three sectors")
    if "not sure" in sector_codes and len(sector_codes) > 1:
        raise ValueError("'Not sure' cannot be combined with another sector")

    raw_skills_by_sector = body.get("skills_by_sector") or {}
    if not isinstance(raw_skills_by_sector, dict):
        raise ValueError("skills_by_sector must be an object")
    options_by_area = json.loads(Q1_OPTIONS_PATH.read_text(encoding="utf-8"))
    selected_skills_by_sector = {}
    skill_preference_unsure_by_sector = {}
    selected_skills = []
    unsure_skill_sentinels = {
        "Not sure", "Not sure yet", "Not sure / open to more than one"
    }
    for sector_code in sector_codes:
        sector_label = IDEAL_SECTOR_DISPLAY.get(sector_code, sector_code)
        valid_skills = {
            skill
            for area in SECTOR_BRIDGE.get(sector_code, [])
            for skill in options_by_area.get(area, [])
        }
        raw_skills = raw_skills_by_sector.get(sector_code, [])
        if not raw_skills and not multi_value_request and body.get("q1"):
            raw_skills = [body.get("q1")]
        if not isinstance(raw_skills, list):
            raise ValueError(f"Skills for '{sector_label}' must be a list")
        normalized_values = []
        for raw_skill in raw_skills:
            skill = str(raw_skill or "").strip()
            if not skill or skill in normalized_values:
                continue
            normalized_values.append(skill)

        skill_preference_unsure = sector_code == "not sure" or any(
            value in unsure_skill_sentinels for value in normalized_values
        )
        real_skill_values = [
            value for value in normalized_values
            if value not in unsure_skill_sentinels
        ]
        if skill_preference_unsure and real_skill_values:
            raise ValueError(
                f"'Not sure yet' cannot be combined with specific skills for '{sector_label}'"
            )
        skills = []
        for skill in real_skill_values:
            if skill not in valid_skills:
                raise ValueError(f"Unknown skill '{skill}' for sector '{sector_label}'")
            skills.append(skill)
        if len(skills) > 3:
            raise ValueError(f"Select no more than three skills for '{sector_label}'")
        if multi_value_request and valid_skills and not skills and not skill_preference_unsure:
            raise ValueError(f"Select at least one skill for '{sector_label}'")
        if skills:
            selected_skills_by_sector[sector_label] = skills
            selected_skills.extend(skill for skill in skills if skill not in selected_skills)
        elif skill_preference_unsure:
            selected_skills_by_sector[sector_label] = []
            skill_preference_unsure_by_sector[sector_label] = True

    ideal_sector_labels = [IDEAL_SECTOR_DISPLAY.get(code, code) for code in sector_codes]
    officer_context = {
        "ideal_sector": "; ".join(ideal_sector_labels),
        "q1_occupation_focus": "; ".join(selected_skills),
        "preferred_sectors": ideal_sector_labels,
        "preferred_skills_by_sector": selected_skills_by_sector,
        "skill_preference_unsure_by_sector": skill_preference_unsure_by_sector,
        "selected_skills": selected_skills,
        "q2_reason": body.get("q2"),
        "q3_schedule": body.get("q3"),
        "q4_language": body.get("q4"),
        "q5_qualification": body.get("q5"),
    }
    return branch, cluster_answers, ideal_sector_labels, officer_context


@app.route("/api/new_person_evidence_preview", methods=["POST"])
def api_new_person_evidence_preview():
    """No-cost assignment preview. Research evidence remains server-side."""
    try:
        body = request.get_json(force=True)
        branch, cluster_answers, _, officer_context = decode_new_person_intake(body)
        profile_entries = npc.build_profile_context(branch, cluster_answers, officer_context)
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    catalogue = catalogue_for_branch(branch, load_survey_question_map())
    assigned = []
    for entry in profile_entries:
        metadata = metadata_for_profile(entry.profile_key)
        assigned.append({
            "profile_key": entry.profile_key,
            "model_id": entry.model_id,
            "cluster_code": metadata["cluster_code"],
            "cluster_name": metadata["cluster_name"],
            "common_description": metadata["common_description"],
            "model_published_accuracy": entry.model_published_accuracy,
            "model_judgment": entry.model_judgment,
            "needs_review_model": entry.model_judgment == "NEEDS REVIEW",
        })

    return jsonify({
        "branch": branch,
        "assigned_profiles": assigned,
        "cluster_catalogue": catalogue,
        "research_tree": full_research_tree(load_survey_question_map()),
    })


@app.route("/api/new_person_recommend", methods=["POST"])
def api_new_person_recommend():
    try:
        body = request.get_json(force=True)
        branch, cluster_answers, ideal_sector_label, officer_context = decode_new_person_intake(body)
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    person_id = "webapp-" + str(abs(hash(str(body))))[:10]
    response, status = generate_officer_briefing(
        person_id=person_id,
        branch=branch,
        cluster_answers=cluster_answers,
        ideal_sector_label=ideal_sector_label,
        officer_context=officer_context,
        raw_body=body,
        question_map=load_survey_question_map(),
    )
    return jsonify(response), status


@app.route("/api/new_person_translate_recommendations", methods=["POST"])
def api_new_person_translate_recommendations():
    """Translate an already-generated recommendation result's explanation text.

    Separate from /api/new_person_recommend: it never generates, ranks or
    filters programmes, and accepts only the fixed translation schema.
    """
    if request.content_length is None or request.content_length > recommendation_translation.MAX_REQUEST_BYTES:
        body, status = recommendation_translation.safe_error("invalid_request")
        return jsonify(body), 413 if request.content_length else status
    body = request.get_json(silent=True)
    response, status = recommendation_translation.translate_recommendations(body)
    return jsonify(response), status


def _legacy_api_new_person_recommend():
    """Previous verbose serializer retained temporarily for migration reference only."""
    body = request.get_json(force=True)
    branch, cluster_answers, ideal_sector_label, officer_context = decode_new_person_intake(body)
    person_id = "webapp-" + str(abs(hash(str(body))))[:10]

    manifest, _ = verify_corpus(verbose=False)
    manifest_by_id = {r["course_id"]: r for r in manifest}

    profile_entries = npc.build_profile_context(branch, cluster_answers, officer_context)
    parsed_profiles_by_key = {e.profile_key: parse_profile_document(e.profile_document_text)
                               for e in profile_entries}
    allowed_evidence_index = build_allowed_evidence_index(profile_entries)
    approved_dossier_evidence_index = {
        entry.profile_key: {
            (finding["variable"], finding["finding"])
            for finding in (entry.research_dossier or {}).get(
                "approved_post_cluster_findings", []
            )
        }
        for entry in profile_entries if entry.research_dossier
    }
    approved_dossiers_by_key = {
        entry.profile_key: entry.research_dossier
        for entry in profile_entries if entry.research_dossier
    }
    evidence_safeguard_violations = []
    selection = ncs.select_candidates({
        "ideal_sector": ideal_sector_label,
        "q1_occupation_focus": body.get("q1"),
        "q3_schedule": body.get("q3"),
        "q4_language": body.get("q4"),
        "q5_qualification": body.get("q5"),
    })
    input_text = npcp.build_new_person_input_text(
        person_id, branch, ideal_sector_label,
        {"q1_occupation_focus": body.get("q1"), "q2_reason": body.get("q2"),
         "q3_schedule": body.get("q3"), "q4_language": body.get("q4"), "q5_qualification": body.get("q5")},
        profile_entries, selection, manifest_by_id,
    )

    model = get_production_model()
    verify_production_model(model)
    api_result = call_new_person_recommendation_api(
        person_id, input_text, model, npcp.GOVERNANCE_INSTRUCTIONS, NewPersonRecommendationResponse,
    )

    profiles_json = [{
        "profile_key": e.profile_key, "profile_label": e.profile_label,
        "membership_similarity_percent": e.membership_similarity_percent,
        "distance_tie": e.distance_tie, "model_judgment": e.model_judgment,
        "model_published_accuracy": e.model_published_accuracy,
    } for e in profile_entries]

    if not api_result.success:
        return jsonify({"error": api_result.error_message, "profiles": profiles_json,
                         "selection": {"skill_areas": selection["skill_areas"], "note": selection["note"]}}), 502

    def serialize_finding(f):
        clean_key = _normalize_profile_key(f.profile_key, parsed_profiles_by_key.keys())
        enrichment = enrich_finding(f.variable, f.profile_key, parsed_profiles_by_key)
        return {"profile_key": clean_key, "variable": f.variable, "finding": f.finding, **enrichment}

    def authorized_findings(findings, context_label):
        # Normalize profile_key first (a model can still copy the decorated
        # marker line despite instructions — see _normalize_profile_key) so
        # the authorization check isn't defeated by that same formatting slip.
        for f in findings:
            f.profile_key = _normalize_profile_key(f.profile_key, allowed_evidence_index.keys())
        kept, violations = filter_authorized_findings(findings, allowed_evidence_index, context_label)
        evidence_safeguard_violations.extend(violations)
        return kept

    collected_section1_answers = {
        "ideal_sector": ideal_sector_label, "q1": body.get("q1"), "q2": body.get("q2"),
        "q3": body.get("q3"), "q4": body.get("q4"), "q5": body.get("q5"),
    }

    parsed = api_result.parsed
    def authorized_dossier_findings(findings, context_label, expected_profile_key):
        allowed = approved_dossier_evidence_index.get(expected_profile_key, set())
        kept = []
        for finding in findings:
            finding.profile_key = _normalize_profile_key(
                finding.profile_key, approved_dossier_evidence_index.keys()
            )
            citation = (finding.variable, finding.finding)
            if finding.profile_key != expected_profile_key or citation not in allowed:
                evidence_safeguard_violations.append(
                    f"{context_label}: removed finding because profile + variable + exact text did not "
                    "match the assigned Branch D dossier."
                )
                continue
            kept.append(finding)
        return kept

    cluster_profile_briefings_json = []
    seen_profile_briefings = set()
    for briefing in parsed.cluster_profile_briefings:
        profile_key = _normalize_profile_key(
            briefing.profile_key, approved_dossier_evidence_index.keys()
        )
        if profile_key not in approved_dossier_evidence_index or profile_key in seen_profile_briefings:
            evidence_safeguard_violations.append(
                f"cluster profile briefing {briefing.profile_key}: dropped because it was not a unique "
                "assigned Branch D dossier."
            )
            continue
        kept_findings = authorized_dossier_findings(
            briefing.supporting_findings,
            f"cluster profile briefing {profile_key}",
            profile_key,
        )
        if not kept_findings:
            evidence_safeguard_violations.append(
                f"cluster profile briefing {profile_key}: dropped because its research description had "
                "no exact approved dossier citation."
            )
            continue
        expected_cluster_code = approved_dossiers_by_key[profile_key]["profile"]["cluster_code"]
        if briefing.cluster_code != expected_cluster_code:
            evidence_safeguard_violations.append(
                f"cluster profile briefing {profile_key}: replaced cluster code with the governed dossier code."
            )
        questions = []
        for index, question in enumerate(briefing.officer_questions, start=1):
            question_findings = authorized_dossier_findings(
                question.supporting_findings,
                f"cluster profile briefing {profile_key} question {index}",
                profile_key,
            )
            if not question_findings:
                evidence_safeguard_violations.append(
                    f"cluster profile briefing {profile_key} question {index}: dropped because it had "
                    "no exact approved dossier citation."
                )
                continue
            questions.append({
                "question": question.question,
                "why_ask": question.why_ask,
                "supporting_findings": [serialize_finding(f) for f in question_findings],
            })
        cluster_profile_briefings_json.append({
            "profile_key": profile_key,
            "cluster_code": expected_cluster_code,
            "why_assigned": briefing.why_assigned,
            "research_description": briefing.research_description,
            "supporting_findings": [serialize_finding(f) for f in kept_findings],
            "officer_questions": questions,
        })
        seen_profile_briefings.add(profile_key)

    missing_profile_briefings = set(approved_dossier_evidence_index) - seen_profile_briefings
    if branch == "D" and missing_profile_briefings:
        evidence_safeguard_violations.append(
            "cluster profile briefing missing for assigned dossier(s): "
            + ", ".join(sorted(missing_profile_briefings))
        )

    recs_json = []
    for r in parsed.recommendations:
        evidence_safeguard_violations.extend(
            check_explicit_answers_not_fabricated(
                r.explicit_answers_used, collected_section1_answers, f"course {r.course_id}"
            )
        )
        contribution = r.profile_context_contribution
        kept_contribution_findings = authorized_findings(
            contribution.contributing_findings, f"course {r.course_id}",
        )
        contribution_role = contribution.role
        contribution_insight = contribution.insight
        if contribution_role != "NOT_USED" and not kept_contribution_findings:
            evidence_safeguard_violations.append(
                f"course {r.course_id}: removed profile insight because it had no exact authorized "
                "retained + current-context finding."
            )
            contribution_role = "NOT_USED"
            contribution_insight = None
        recs_json.append({
            "rank": r.rank, "course_id": r.course_id, "course_name": r.course_name,
            "match_type": r.match_type, "bridge_explanation": r.bridge_explanation,
            "why_matches_explicit_answers": r.why_matches_explicit_answers,
            "explicit_answers_used": [{"question": a.question, "answer": a.answer, "relevance": a.relevance}
                                       for a in r.explicit_answers_used],
            "course_facts_used": [{"fact": c.fact, "source_reference": c.source_reference}
                                   for c in r.course_facts_used],
            "profile_context_contribution": {
                "role": contribution_role,
                "insight": contribution_insight,
                "contributing_findings": [
                    serialize_finding(f) for f in kept_contribution_findings
                ],
            },
            "llm_inferences": r.llm_inferences, "limitations": r.limitations,
            "evidence_strength": r.evidence_strength, "evidence_strength_reason": r.evidence_strength_reason,
        })

    # Mechanical safeguard, not just a prompt instruction: a model can still
    # emit the same course_id twice despite being told not to. Detected and
    # surfaced, never silently deduplicated — consistent with this project's
    # audit layers, which flag rather than quietly rewrite model output.
    seen_ids, duplicate_course_ids = set(), []
    for r in recs_json:
        if r["course_id"] in seen_ids:
            duplicate_course_ids.append(r["course_id"])
        seen_ids.add(r["course_id"])

    about_json = None
    if parsed.about_people_like_you:
        kept_about_findings = authorized_findings(
            parsed.about_people_like_you.supporting_findings, "about_people_like_you",
        )
        about_json = {
            "why_assigned": parsed.about_people_like_you.why_assigned,
            "narrative": (
                parsed.about_people_like_you.narrative if kept_about_findings else
                "No retained historical profile findings were eligible for this intake context."
            ),
            "supporting_findings": [serialize_finding(f) for f in kept_about_findings],
        }

    discussion_prompts_json = []
    for index, prompt in enumerate(parsed.officer_discussion_prompts, start=1):
        kept_prompt_findings = authorized_findings(
            prompt.supporting_findings, f"officer_discussion_prompt {index}",
        )
        if not kept_prompt_findings:
            evidence_safeguard_violations.append(
                f"officer_discussion_prompt {index}: dropped because it had no exact authorized "
                "retained + current-context finding."
            )
            continue
        discussion_prompts_json.append({"prompt": prompt.prompt, "grounded_in": prompt.grounded_in})

    return jsonify({
        "person_id": person_id, "branch": branch,
        "profiles": profiles_json,
        "cluster_profile_briefings": cluster_profile_briefings_json,
        "about_people_like_you": about_json,
        "officer_discussion_prompts": discussion_prompts_json,
        "selection": {"skill_areas": selection["skill_areas"], "note": selection["note"],
                      "candidates": [{"course_id": c["course_id"], "course_name": c["course_name"],
                                      "score": c["score"]} for c in selection["candidates"]]},
        "recommendation_status": parsed.recommendation_status,
        "catalogue_coverage_note": parsed.catalogue_coverage_note,
        "no_defensible_recommendation_reason": parsed.no_defensible_recommendation_reason,
        "recommendations": recs_json,
        "duplicate_course_ids_detected": duplicate_course_ids,
        "evidence_safeguard_violations": evidence_safeguard_violations,
        "token_usage": {"total_tokens": api_result.total_tokens, "input_tokens": api_result.input_tokens,
                        "output_tokens": api_result.output_tokens},
    })


INDEX_HTML_PATH = Path(__file__).resolve().parent / "profile_explorer_static" / "index.html"
WALKTHROUGH_HTML_PATH = Path(__file__).resolve().parent / "profile_explorer_static" / "walkthrough.html"
FRONTEND_DIST_PATH = Path(__file__).resolve().parent / "frontend" / "dist"


@app.route("/")
def index():
    vite_index = FRONTEND_DIST_PATH / "index.html"
    if vite_index.exists():
        return Response(vite_index.read_text(encoding="utf-8"), mimetype="text/html")
    return jsonify({"error": "Not found"}), 404


@app.route("/assets/<path:asset_path>")
def frontend_asset(asset_path):
    """Serve Vite's hashed production assets when Flask is hosted on Vercel."""
    return send_from_directory(FRONTEND_DIST_PATH / "assets", asset_path)


@app.route("/favicon.svg")
def frontend_favicon():
    return send_from_directory(FRONTEND_DIST_PATH, "favicon.svg")


@app.route("/new-person")
def new_person_page():
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    print("Profile explorer running at http://127.0.0.1:5055/")
    app.run(host="127.0.0.1", port=5055, debug=False)
