"""Deterministic evidence analysis for the Programme Design Advisor.

This module is intentionally independent of the individual-member recommendation
pipeline.  It reads only privacy-safe aggregate survey evidence, curated labour-
market evidence, and the governed 84-course catalogue.  It does not call an AI
service and does not load participant-level survey files.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    from .corpus_v2 import resolve_document_path, verify_corpus
except ImportError:  # pragma: no cover - supports direct script execution
    from corpus_v2 import resolve_document_path, verify_corpus


BASE = Path(__file__).resolve().parents[2]
SURVEY_EVIDENCE_PATH = BASE / "outputs/programme_design_advisor/survey_evidence.json"
LABOUR_MARKET_EVIDENCE_PATH = BASE / "outputs/programme_design_advisor/labour_market_evidence.json"
COURSE_MATCHING_PATH = BASE / "outputs/rag_new_person_intake_v1/course_matching_layer.csv"

OPPORTUNITY_IMPROVE = "IMPROVE_EXISTING"
OPPORTUNITY_NEW = "CONSIDER_NEW_PROGRAMME"
OPPORTUNITY_INSUFFICIENT = "INSUFFICIENT_EVIDENCE"

TRAINING_AREAS = {
    "digital_ict": "Digital & ICT",
    "technical_vocational": "Technical & Vocational",
    "employability_career_readiness": "Employability & Career Readiness",
    "entrepreneurship_small_business": "Entrepreneurship & Small Business",
    "continuing_education_qualifications": "Continuing Education & Qualifications",
    "workplace_upskilling_job_progression": "Workplace Upskilling & Job Progression",
}

DESIGN_OBJECTIVES = {
    "employment_entry": "Prepare youth for entry-level employment",
    "entrepreneurship": "Support entrepreneurship and self-employment",
    "continuing_education": "Create progression to qualifications and further learning",
    "workplace_progression": "Support workplace upskilling and career progression",
    "future_skills_modernisation": "Modernise provision for emerging and future skills",
}

DEVELOPMENT_APPROACHES = {
    "improve_existing": "Improve or modernise related existing programmes",
    "consider_new": "Assess whether a new programme should be considered",
    "balanced_review": "Compare improvement and new-programme options",
}


# Direct skill-area links are intentionally conservative.  Additional name terms
# retrieve visibly related courses without claiming that their curricula cover an
# unmentioned topic.
AREA_COURSE_RULES = {
    "digital_ict": {
        "skill_areas": {"ICT & Computing"},
        "name_terms": {"computer", "ict", "python", "java", "web", "cisco", "software", "network"},
    },
    "technical_vocational": {
        "skill_areas": {
            "Automotive & Mechanical Engineering",
            "Electrical & Electronics",
            "Construction & Surveying",
            "Hospitality & Culinary Arts",
            "Agriculture & Environment",
            "Beauty, Fashion & Personal Care",
            "Creative Arts, Design & Media",
        },
        # "technician" is deliberately absent: it also names the ICT technician
        # courses, which belong to Digital & ICT.
        "name_terms": {"mechanic", "electrician", "welder", "plumber", "baker", "tailor"},
    },
    "employability_career_readiness": {
        "skill_areas": {"Languages & Communication", "Business, Management & Administration"},
        # "communication" alone would match "Information And Communication Technology".
        "name_terms": {"english", "language", "secretary", "office"},
    },
    "entrepreneurship_small_business": {
        "skill_areas": {"Business, Management & Administration"},
        "name_terms": {"business", "accounting", "management", "freelancer", "entrepreneur"},
    },
    "continuing_education_qualifications": {
        "skill_areas": set(),
        "name_terms": {"certificate", "diploma", "certified"},
        "requires_credential": True,
    },
    "workplace_upskilling_job_progression": {
        "skill_areas": {"ICT & Computing", "Languages & Communication", "Business, Management & Administration"},
        "name_terms": {"professional english", "management", "accounting", "computer"},
        # Part-time delivery suits working learners, so it raises the ranking of
        # an otherwise related course; it does not make an unrelated course related.
        "part_time_bonus": True,
    },
}

SURVEY_EVIDENCE_LIMIT = 6
COURSE_SELECTION_LIMIT = 8

OBJECTIVE_EVIDENCE_TYPES = {
    "employment_entry": {
        "explicit_perceived_training_demand": 10,
        "employment_barrier": 9,
        "historical_employment_barrier": 8,
        "job_aspiration": 6,
        "perceived_employability_skill": 5,
        "future_work_intent": 4,
    },
    "entrepreneurship": {
        "entrepreneurship_motivation": 10,
        "business_constraint": 9,
        "business_finance_source": 8,
        "career_aspiration": 7,
        "post_education_intention": 6,
        "perceived_employability_skill": 4,
    },
    "continuing_education": {
        "explicit_perceived_training_demand": 10,
        "upskilling_intent": 9,
        "future_training_intent": 9,
        "perceived_education_requirement": 7,
        "qualification_job_alignment": 5,
    },
    "workplace_progression": {
        "upskilling_intent": 10,
        "experienced_training": 8,
        "experienced_training_type": 8,
        "career_change_reason": 7,
        "career_change_intent": 6,
        "qualification_job_alignment": 6,
    },
    "future_skills_modernisation": {
        "perceived_employability_skill": 10,
        "experienced_training_type": 9,
        "explicit_perceived_training_demand": 7,
        "sector_aspiration": 5,
        "study_field_aspiration_or_current_field": 4,
    },
}

OBJECTIVE_TERMS = {
    "employment_entry": {"employment", "employability", "job", "work", "experience", "communication", "practical"},
    "entrepreneurship": {"entrepreneurship", "business", "market", "customer", "accounting", "freelancer", "growth"},
    "continuing_education": {"credential", "qualification", "certificate", "diploma", "learning", "modular", "recognition"},
    "workplace_progression": {"upskilling", "career", "workplace", "employer", "management", "progression", "transition"},
    "future_skills_modernisation": {"ai", "digital", "technology", "cybersecurity", "green", "emerging", "automation", "data"},
}

APPROACH_TERMS = {
    "improve_existing": {"existing", "modernise", "quality", "curriculum", "industry", "current"},
    "consider_new": {"emerging", "future", "new", "gap", "transition"},
}
APPROACH_TERMS["balanced_review"] = APPROACH_TERMS["improve_existing"] | APPROACH_TERMS["consider_new"]

# Design guidance passed to the AI so that the officer's objective and approach
# shape the proposal itself, not only which evidence is retrieved.
OBJECTIVE_DESIGN_FOCUS = {
    "employment_entry": (
        "Design for job entry: practical, employer-recognised skills, work-readiness, "
        "work-based learning or placements, and assessment that demonstrates job-ready performance."
    ),
    "entrepreneurship": (
        "Design for self-employment: business planning, costing and pricing, finance access, "
        "customer and market skills, and assessment through a viable business or product plan."
    ),
    "continuing_education": (
        "Design for progression: alignment with recognised qualification levels, credit or "
        "credential pathways, modular stackable units, and clear routes to further learning."
    ),
    "workplace_progression": (
        "Design for people already working: flexible or part-time delivery, applied upskilling "
        "for promotion or role change, employer involvement, and workplace-based assessment."
    ),
    "future_skills_modernisation": (
        "Design for emerging skills: current and emerging technologies and practices, digital and "
        "green skills where relevant, and a mechanism for keeping content up to date."
    ),
}

APPROACH_DESIGN_INSTRUCTIONS = {
    "improve_existing": (
        "Propose a modernised or improved version of the most relevant cited existing course(s): "
        "say what to keep, add, update, or restructure."
    ),
    "consider_new": (
        "Propose a new programme concept for investigation. Position it against the cited related "
        "courses so it complements rather than duplicates existing provision."
    ),
    "balanced_review": (
        "Compare an improvement option and a new-programme option in option_comparison, choose a "
        "preferred direction, and develop that preferred direction as the programme_design."
    ),
}

# These are the only published survey cells that provide an area-specific direct
# training-demand signal.  A protected/suppressed cell is never unpacked.
DIRECT_TRAINING_SIGNAL_LABELS = {
    "digital_ict": {"Computer and IT training"},
    "technical_vocational": {"Technical/vocational pathways (combined)"},
    "continuing_education_qualifications": {
        "University degree",
        "Technical/vocational pathways (combined)",
    },
}

_MODULE_START = re.compile(r"^\s*\d{1,2}[.)]\s+(.+?)\s*$")
_MODULE_STOP_PREFIXES = (
    "the national youth",
    "this is a",
    "this course",
    "it is our objective",
    "by completing",
    "language",
    "max students",
    "apply now",
    "course overview",
)


class ProgrammeDesignEvidenceError(ValueError):
    """Raised when governed evidence or officer inputs fail validation."""


def get_input_options() -> dict[str, list[dict[str, str]]]:
    """Return stable IDs and labels for a future UI/API without implementing it."""
    return {
        "training_areas": [{"id": key, "label": value} for key, value in TRAINING_AREAS.items()],
        "design_objectives": [{"id": key, "label": value} for key, value in DESIGN_OBJECTIVES.items()],
        "development_approaches": [
            {"id": key, "label": value} for key, value in DEVELOPMENT_APPROACHES.items()
        ],
    }


def _load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ProgrammeDesignEvidenceError(f"Unable to load governed evidence: {path}") from exc


def _validate_inputs(training_area: str, design_objective: str, development_approach: str) -> None:
    choices = (
        ("training_area", training_area, TRAINING_AREAS),
        ("design_objective", design_objective, DESIGN_OBJECTIVES),
        ("development_approach", development_approach, DEVELOPMENT_APPROACHES),
    )
    for field, value, allowed in choices:
        if value not in allowed:
            raise ProgrammeDesignEvidenceError(
                f"Unsupported {field}. Use one of: {', '.join(allowed)}"
            )


def _extract_modules(document_text: str) -> list[str]:
    """Extract clearly readable numbered module lines without filling omissions."""
    if "COMPLETE EXTRACTED COURSE TEXT" in document_text:
        document_text = document_text.split("COMPLETE EXTRACTED COURSE TEXT", 1)[1]
    modules: list[str] = []
    current: list[str] | None = None
    for raw_line in document_text.splitlines():
        line = raw_line.strip()
        match = _MODULE_START.match(line)
        if match:
            if current and "[UNCLEAR]" not in " ".join(current):
                modules.append(" ".join(current).strip())
            current = [match.group(1).strip()]
            continue
        if current is None or not line:
            continue
        lowered = line.lower().lstrip("→- ")
        if lowered.startswith(_MODULE_STOP_PREFIXES):
            if "[UNCLEAR]" not in " ".join(current):
                modules.append(" ".join(current).strip())
            current = None
            continue
        # Only join short wrapped fragments.  Narrative paragraphs are never
        # converted into module descriptions.
        if len(line) <= 80 and len(" ".join(current)) <= 120:
            current.append(line)
    if current and "[UNCLEAR]" not in " ".join(current):
        modules.append(" ".join(current).strip())
    return modules[:12]


def load_governed_courses() -> list[dict[str, Any]]:
    """Verify and load exactly the 84 governed, indexable catalogue parents."""
    manifest, _ = verify_corpus(verbose=False)
    try:
        with COURSE_MATCHING_PATH.open(newline="", encoding="utf-8-sig") as handle:
            matching_rows = list(csv.DictReader(handle))
    except OSError as exc:
        raise ProgrammeDesignEvidenceError("Course matching layer is unavailable") from exc

    matching = {row["rag_course_id"]: row for row in matching_rows}
    manifest_ids = {row["course_id"] for row in manifest}
    if len(manifest) != 84 or len(matching_rows) != 84 or set(matching) != manifest_ids:
        raise ProgrammeDesignEvidenceError(
            "Governed course manifest and 84-row matching layer do not reconcile"
        )

    courses: list[dict[str, Any]] = []
    for row in manifest:
        course_id = row["course_id"]
        structured = matching[course_id]
        document_path = resolve_document_path(row)
        text = document_path.read_text(encoding="utf-8")
        courses.append(
            {
                "course_id": course_id,
                "course_name": row["course_name"],
                "skill_area": structured["skill_area"],
                "attendance_type": structured["attendance_type"],
                "attendance_days": structured["attendance_days"],
                "duration_months": structured["duration_months"],
                "instruction_languages": structured["instruction_languages"],
                "nvq_level": structured["nvq_level"],
                "qualification_type": structured["qualification_type"],
                "review_status": row["review_status"],
                "unclear_marker_count": int(row["unclear_marker_count"]),
                "modules": _extract_modules(text),
                "document_path": row["document_path"],
                "document_sha256": row["document_sha256"],
            }
        )
    return courses


def _record_has_direct_signal(record: Mapping[str, Any], training_area: str) -> bool:
    if record.get("evidence_type") != "explicit_perceived_training_demand":
        return False
    allowed_labels = DIRECT_TRAINING_SIGNAL_LABELS.get(training_area, set())
    return any(
        cell.get("label") in allowed_labels and int(cell.get("count", 0)) >= 5
        for cell in record.get("distribution", [])
    )


def _survey_score(record: Mapping[str, Any], design_objective: str, development_approach: str) -> int:
    score = 10
    score += OBJECTIVE_EVIDENCE_TYPES[design_objective].get(record.get("evidence_type", ""), 0)
    if record.get("demand_classification") == "direct_training_demand_signal":
        score += 4
    if development_approach == "improve_existing" and record.get("evidence_type") in {
        "experienced_training",
        "experienced_training_type",
        "qualification_job_alignment",
        "employment_barrier",
        "historical_employment_barrier",
    }:
        score += 3
    if development_approach == "consider_new" and record.get("demand_classification") in {
        "direct_training_demand_signal",
        "training_intent_without_topic",
    }:
        score += 3
    return score


def _select_survey_evidence(
    survey: Mapping[str, Any], training_area: str, design_objective: str, development_approach: str
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    ranked: list[tuple[int, str, Mapping[str, Any]]] = []
    unavailable: list[dict[str, str]] = []
    for record in survey["evidence_records"]:
        if training_area not in record.get("training_area_ids", []):
            continue
        if not record.get("distribution"):
            unavailable.append(
                {
                    "question_id": record["question_id"],
                    "reason": record["privacy_note"],
                }
            )
            continue
        ranked.append(
            (
                _survey_score(record, design_objective, development_approach),
                record["question_id"],
                record,
            )
        )
    ranked.sort(key=lambda item: (-item[0], item[1]))

    selected_rows = ranked[:SURVEY_EVIDENCE_LIMIT]
    direct_rows = [row for row in ranked if _record_has_direct_signal(row[2], training_area)]
    if direct_rows and all(row[2]["question_id"] != direct_rows[0][2]["question_id"] for row in selected_rows):
        selected_rows = [*selected_rows[: SURVEY_EVIDENCE_LIMIT - 1], direct_rows[0]]
        selected_rows.sort(key=lambda item: (-item[0], item[1]))

    selected: list[dict[str, Any]] = []
    for score, _, record in selected_rows:
        selected.append(
            {
                "citation_id": f"SURVEY-{record['question_id']}",
                "source_path": "outputs/programme_design_advisor/survey_evidence.json",
                "question_id": record["question_id"],
                "variable": record["variable"],
                "question_wording": record["question_wording"],
                "cohort": record["cohort"],
                "applicable_count": record["applicable_count"],
                "answered_count": record["answered_count"],
                "missing_count": record["missing_count"],
                "percentage_denominator": record["percentage_denominator"],
                "evidence_type": record["evidence_type"],
                "demand_classification": record["demand_classification"],
                "is_area_specific_direct_training_demand": _record_has_direct_signal(record, training_area),
                "statistics": record["distribution"],
                "privacy_note": record["privacy_note"],
                "selection_score": score,
            }
        )
    return selected, unavailable


def _term_pattern(term: str) -> str:
    """Short terms must be whole words ("ai" never matches "maintain"); longer
    terms match word prefixes so that plurals and derived forms still count
    ("technology" matches "technologies", "digital" matches "digitalisation")."""
    escaped = re.escape(term.casefold())
    return rf"\b{escaped}\b" if len(term) <= 3 else rf"\b{escaped}"


def _word_term_score(text: str, terms: Iterable[str]) -> int:
    lowered = text.casefold()
    return sum(1 for term in terms if re.search(_term_pattern(term), lowered))


def _select_labour_evidence(
    labour: Mapping[str, Any], training_area: str, design_objective: str, development_approach: str
) -> list[dict[str, Any]]:
    area = next(
        item for item in labour["evidence_by_training_area"] if item["training_area_id"] == training_area
    )
    sources = {source["source_id"]: source for source in labour["sources"]}
    terms = OBJECTIVE_TERMS[design_objective] | APPROACH_TERMS[development_approach]
    ranked = []
    for item in area["evidence"]:
        searchable = " ".join(
            [item["finding"], item["programme_design_use"], *item.get("relevant_skills", [])]
        )
        score = 10 + (3 * _word_term_score(searchable, terms))
        if item["source_id"] in {"WEF_FOJ_2025", "LINKEDIN_SOTR_2026"}:
            score += 2
        if item["transferability"] == "sri_lanka_system_context":
            score += 2
        ranked.append((score, item["evidence_id"], item))
    ranked.sort(key=lambda value: (-value[0], value[1]))

    # Each area holds only a handful of curated findings, so all of them are
    # supplied; the ranking orders them by relevance to the officer's choices.
    selected = []
    for score, _, item in ranked:
        source = sources[item["source_id"]]
        selected.append(
            {
                "citation_id": item["evidence_id"],
                "source_id": item["source_id"],
                "source_title": source["title"],
                "publisher": source["publisher"],
                "publication_year": source["publication_year"],
                "url": source["url"],
                "geographic_scope": source["geographic_scope"],
                "source_locator": item["source_locator"],
                "finding": item["finding"],
                "relevant_skills": item["relevant_skills"],
                "programme_design_use": item["programme_design_use"],
                "transferability": item["transferability"],
                "limitation": item["limitation"],
                "selection_score": score,
            }
        )
    return selected


def _name_matches(name: str, terms: Iterable[str]) -> bool:
    """Word-boundary match so that, e.g., "ict" never matches inside another word."""
    lowered = name.casefold()
    return any(re.search(_term_pattern(term), lowered) for term in terms)


def _has_credential(course: Mapping[str, Any]) -> bool:
    return course["nvq_level"] != "NOT_STATED" or course["qualification_type"] != "NOT_STATED"


def _is_related_course(course: Mapping[str, Any], training_area: str) -> bool:
    rules = AREA_COURSE_RULES[training_area]
    direct_area = course["skill_area"] in rules["skill_areas"]
    name_match = _name_matches(course["course_name"], rules["name_terms"])
    credential_match = rules.get("requires_credential", False) and _has_credential(course)
    return bool(direct_area or name_match or credential_match)


def _course_score(
    course: Mapping[str, Any], training_area: str, design_objective: str, development_approach: str
) -> int:
    rules = AREA_COURSE_RULES[training_area]
    score = 0
    if course["skill_area"] in rules["skill_areas"]:
        score += 20
    if _name_matches(course["course_name"], rules["name_terms"]):
        score += 8
    if rules.get("requires_credential", False) and _has_credential(course):
        score += 18
    if rules.get("part_time_bonus", False) and course["attendance_type"] == "Part Time":
        score += 6
    searchable = " ".join(
        [course["course_name"], course["skill_area"], *course.get("modules", [])]
    )
    score += 3 * _word_term_score(searchable, OBJECTIVE_TERMS[design_objective])
    if course.get("modules"):
        # A documented curriculum gives the AI concrete content to build on.
        score += min(len(course["modules"]), 6)
        score += 3 if development_approach == "improve_existing" else 1
    if course["nvq_level"] != "NOT_STATED" or course["qualification_type"] != "NOT_STATED":
        score += 2
    return score


def _course_coverage(
    courses: Sequence[Mapping[str, Any]],
    training_area: str,
    design_objective: str,
    development_approach: str,
) -> dict[str, Any]:
    related = [course for course in courses if _is_related_course(course, training_area)]
    ranked = sorted(
        related,
        key=lambda course: (
            -_course_score(course, training_area, design_objective, development_approach),
            course["course_id"],
        ),
    )
    # Several centres offer the same course title; one entry per title keeps
    # the limited selection slots for distinct provision.
    distinct: list[Mapping[str, Any]] = []
    seen_names: set[str] = set()
    for course in ranked:
        name_key = course["course_name"].casefold().strip()
        if name_key in seen_names:
            continue
        seen_names.add(name_key)
        distinct.append(course)

    selected = []
    for course in distinct[:COURSE_SELECTION_LIMIT]:
        selected.append(
            {
                "course_id": course["course_id"],
                "course_name": course["course_name"],
                "skill_area": course["skill_area"],
                "attendance_type": course["attendance_type"],
                "attendance_days": course["attendance_days"],
                "duration_months": course["duration_months"],
                "instruction_languages": course["instruction_languages"],
                "nvq_level": course["nvq_level"],
                "qualification_type": course["qualification_type"],
                "module_descriptions_available": bool(course["modules"]),
                "module_descriptions": course["modules"],
                "review_status": course["review_status"],
                "unclear_marker_count": course["unclear_marker_count"],
                "citation": {
                    "course_id": course["course_id"],
                    "document_path": course["document_path"],
                    "document_sha256": course["document_sha256"],
                },
                "selection_score": _course_score(
                    course, training_area, design_objective, development_approach
                ),
            }
        )
    return {
        "governed_indexable_course_count": len(courses),
        "related_course_count": len(related),
        "related_courses_with_module_descriptions": sum(bool(course["modules"]) for course in related),
        "related_course_counts_by_skill_area": dict(
            sorted(Counter(course["skill_area"] for course in related).items())
        ),
        "selected_related_courses": selected,
        "documentation_caution": (
            "A missing or short module list means the governed catalogue does not describe the content; "
            "it is not evidence that the course lacks that content."
        ),
    }


def classify_opportunity(
    *,
    development_approach: str,
    survey_evidence_count: int,
    labour_evidence_count: int,
    has_area_specific_direct_training_demand: bool,
    related_course_count: int,
) -> tuple[str, str]:
    """Suggest a starting direction for the AI; the AI makes the final classification.

    The officer's chosen approach is respected. Evidence strength is reported in the
    rationale so the AI can calibrate confidence, rather than being used to withhold
    a proposal. INSUFFICIENT_EVIDENCE is reserved for a missing evidence layer.
    """
    if development_approach not in DEVELOPMENT_APPROACHES:
        raise ProgrammeDesignEvidenceError("Unsupported development_approach")
    if survey_evidence_count == 0 or labour_evidence_count == 0:
        return (
            OPPORTUNITY_INSUFFICIENT,
            "Relevant aggregate survey evidence or traceable labour-market evidence is missing, so any proposal is provisional.",
        )
    demand_note = (
        "The survey includes an area-specific direct training-demand signal."
        if has_area_specific_direct_training_demand
        else "The survey offers indirect signals (aspirations, barriers, skills perceptions) rather than an area-specific direct training-demand signal, so demand needs local validation."
    )
    if development_approach == "consider_new":
        if related_course_count > 0:
            return (
                OPPORTUNITY_NEW,
                "The officer asked to assess a new programme. Related governed courses exist, so the concept should complement rather than duplicate them. "
                + demand_note,
            )
        return (
            OPPORTUNITY_NEW,
            "The officer asked to assess a new programme and no related governed course was found. "
            + demand_note,
        )
    if related_course_count == 0:
        return (
            OPPORTUNITY_NEW,
            "No related governed course was found to improve, so a new programme concept is the starting direction. "
            + demand_note,
        )
    if development_approach == "improve_existing":
        return (
            OPPORTUNITY_IMPROVE,
            "Related governed courses exist and the officer asked to improve existing provision. "
            + demand_note,
        )
    return (
        OPPORTUNITY_IMPROVE,
        "Related governed courses exist, so improvement is the suggested starting direction; a new-programme alternative should be compared against it. "
        + demand_note,
    )


def build_evidence_package(
    training_area: str,
    design_objective: str,
    development_approach: str,
    *,
    survey_data: Mapping[str, Any] | None = None,
    labour_data: Mapping[str, Any] | None = None,
    courses: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a structured, citation-ready evidence package for a future AI call."""
    _validate_inputs(training_area, design_objective, development_approach)
    survey = dict(survey_data) if survey_data is not None else _load_json(SURVEY_EVIDENCE_PATH)
    labour = dict(labour_data) if labour_data is not None else _load_json(LABOUR_MARKET_EVIDENCE_PATH)
    loaded_courses = list(courses) if courses is not None else load_governed_courses()

    survey_areas = {item["id"]: item["label"] for item in survey["training_areas"]}
    labour_areas = {
        item["training_area_id"]: item["training_area_label"]
        for item in labour["evidence_by_training_area"]
    }
    if survey_areas != TRAINING_AREAS or labour_areas != TRAINING_AREAS:
        raise ProgrammeDesignEvidenceError("Evidence taxonomies do not match the six governed training areas")

    survey_evidence, withheld_survey = _select_survey_evidence(
        survey, training_area, design_objective, development_approach
    )
    labour_evidence = _select_labour_evidence(
        labour, training_area, design_objective, development_approach
    )
    coverage = _course_coverage(
        loaded_courses, training_area, design_objective, development_approach
    )
    has_direct_signal = any(
        item["is_area_specific_direct_training_demand"] for item in survey_evidence
    )
    status, rationale = classify_opportunity(
        development_approach=development_approach,
        survey_evidence_count=len(survey_evidence),
        labour_evidence_count=len(labour_evidence),
        has_area_specific_direct_training_demand=has_direct_signal,
        related_course_count=coverage["related_course_count"],
    )

    selected_survey_ids = [item["citation_id"] for item in survey_evidence]
    selected_labour_ids = [item["citation_id"] for item in labour_evidence]
    selected_course_ids = [
        item["course_id"] for item in coverage["selected_related_courses"]
    ]
    return {
        "schema_version": "1.0.0",
        "feature": "AI Programme Design Advisor",
        "officer_inputs": {
            "training_area": {"id": training_area, "label": TRAINING_AREAS[training_area]},
            "design_objective": {
                "id": design_objective,
                "label": DESIGN_OBJECTIVES[design_objective],
            },
            "programme_development_approach": {
                "id": development_approach,
                "label": DEVELOPMENT_APPROACHES[development_approach],
            },
        },
        "opportunity_assessment": {
            "classification": status,
            "rationale": rationale,
            "is_advisory": True,
            "has_area_specific_direct_training_demand": has_direct_signal,
            "decision_guardrails": [
                "Aspirations, intentions, barriers, and past training are not direct training demand.",
                "A missing catalogue module description is not evidence that training content is absent.",
                "International trends are context and do not prove Sri Lankan labour demand.",
                "CONSIDER_NEW_PROGRAMME is investigatory, not approval to create a programme.",
            ],
        },
        "design_brief": {
            "objective_focus": OBJECTIVE_DESIGN_FOCUS[design_objective],
            "approach_instruction": APPROACH_DESIGN_INSTRUCTIONS[development_approach],
            "option_comparison_required": development_approach == "balanced_review",
        },
        "survey_evidence": survey_evidence,
        "withheld_or_unavailable_survey_evidence": withheld_survey,
        "labour_market_evidence": labour_evidence,
        "course_coverage": coverage,
        "selection_trace": {
            "survey_citation_ids": selected_survey_ids,
            "labour_market_citation_ids": selected_labour_ids,
            "course_ids": selected_course_ids,
        },
        "package_limitations": [
            "Evidence selection and the suggested direction are deterministic guidance, not an AI recommendation.",
            "Survey percentages describe respondents who answered each question, not the national youth population.",
            "Course matches indicate related documented provision, not current availability, capacity, quality, or outcomes.",
            "Programme decisions require current employer, learner, delivery, cost, accreditation, and management validation.",
        ],
    }


__all__ = [
    "DEVELOPMENT_APPROACHES",
    "DESIGN_OBJECTIVES",
    "OPPORTUNITY_IMPROVE",
    "OPPORTUNITY_INSUFFICIENT",
    "OPPORTUNITY_NEW",
    "ProgrammeDesignEvidenceError",
    "TRAINING_AREAS",
    "build_evidence_package",
    "classify_opportunity",
    "get_input_options",
    "load_governed_courses",
]
