"""
Deterministic candidate-course selection for the NEW-person recommendation
architecture, driven by the respondent's explicit Q1-Q5 programme-matching
answers (§1) scored against the structured matching layer (§2). No BM25, no
randomness — the same answers always produce the same candidate set, which is
the whole point: narrow the LLM's job to explaining/ranking an already
well-matched short list, not discovering relevance from 84 loosely-related
documents each call.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_v2 import BASE
from retrieval_v2 import SECTOR_BRIDGE

MATCHING_LAYER_CSV = BASE / "outputs/rag_new_person_intake_v1/course_matching_layer.csv"
NOT_STATED = "NOT_STATED"

MAX_CANDIDATES = 8
UNSURE_SKILL_VALUES = {
    "not sure", "not sure yet", "not sure / open to more than one",
}
UNSURE_SECTOR_VALUES = {"not sure", "not sure yet"}


def _strip_variant_suffix(name: str) -> str:
    base = name
    for suffix in [" (Full Time)", " (Part Time)",
                   " (Full Time – English)", " (Full Time – Sinhala)",
                   " (Full Time - English)", " (Full Time - Sinhala)",
                   " (Part Time – English)", " (Part Time – Sinhala)",
                   " (English)", " (Sinhala)"]:
        base = base.replace(suffix, "")
    return base.strip()


def load_matching_layer() -> list[dict]:
    with open(MATCHING_LAYER_CSV, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _as_distinct_strings(value) -> list[str]:
    if value is None:
        return []
    values = value if isinstance(value, (list, tuple, set)) else [value]
    result = []
    for item in values:
        text = str(item).strip()
        if text and text not in result:
            result.append(text)
    return result


def skill_areas_for_ideal_sector(ideal_sector_label: str) -> list[str]:
    if not ideal_sector_label:
        return []
    return SECTOR_BRIDGE.get(ideal_sector_label.strip().lower(), [])


def skill_areas_for_ideal_sectors(ideal_sector_labels) -> list[str]:
    areas = []
    for sector in _as_distinct_strings(ideal_sector_labels):
        for area in skill_areas_for_ideal_sector(sector):
            if area not in areas:
                areas.append(area)
    return areas


def retrieve_sector_catalogue(answers: dict) -> dict:
    """Retrieve the complete governed catalogue slice for the selected sectors.

    This is deliberately retrieval, not final recommendation ranking.  Every
    verified course in a skill area bridged from any selected sector is
    returned.  No numeric suitability score and no top-N truncation are
    applied before the LLM has seen the member, research, and course context.
    """
    rows = load_matching_layer()
    sectors = _as_distinct_strings(
        answers.get("ideal_sectors") or answers.get("ideal_sector")
    )
    skills_by_sector = answers.get("preferred_skills_by_sector") or {}
    if not isinstance(skills_by_sector, dict):
        skills_by_sector = {}

    sector_skill_areas = {
        sector: skill_areas_for_ideal_sector(sector)
        for sector in sectors
        if skill_areas_for_ideal_sector(sector)
    }
    skill_areas = []
    for areas in sector_skill_areas.values():
        for area in areas:
            if area not in skill_areas:
                skill_areas.append(area)

    sector_preference_unsure = bool(sectors) and all(
        sector.casefold() in UNSURE_SECTOR_VALUES for sector in sectors
    )
    if not skill_areas and sector_preference_unsure:
        skill_areas = sorted({
            row["skill_area"] for row in rows
            if row["skill_area"] != NOT_STATED
        })
    elif not skill_areas:
        return {
            "retrieval_method": "selected-sector catalogue scope",
            "sector_skill_areas": {},
            "skill_areas": [],
            "selected_skills_by_sector": skills_by_sector,
            "candidates": [],
            "note": (
                "No verified catalogue area is mapped to the selected sector. "
                "No programme can be ranked from the governed catalogue."
            ),
        }

    candidates = []
    for row in rows:
        skill_area = row["skill_area"]
        if skill_area == NOT_STATED or skill_area not in skill_areas:
            continue
        matched_sectors = [
            sector for sector, areas in sector_skill_areas.items()
            if skill_area in areas
        ]
        candidates.append({
            "course_id": row["rag_course_id"],
            "course_name": row["rag_course_name"],
            "matched_selected_sectors": matched_sectors,
            "selected_skills_in_those_sectors": {
                sector: _as_distinct_strings(skills_by_sector.get(sector))
                for sector in matched_sectors
            },
            "exact_selected_skill_matches": [
                {"sector": sector, "skill": skill}
                for sector in matched_sectors
                for skill in _as_distinct_strings(skills_by_sector.get(sector))
                if _strip_variant_suffix(row["rag_course_name"]).casefold() == skill.casefold()
            ],
            "structured_attributes": {
                key: row[key] for key in (
                    "skill_area", "attendance_type", "attendance_days",
                    "duration_months", "instruction_languages", "nvq_level",
                    "qualification_type",
                )
            },
        })

    candidates.sort(key=lambda candidate: candidate["course_id"])

    def preference_fit(candidate: dict) -> tuple[int, str]:
        """Choose one governed catalogue variant per exact selected skill.

        This is a coverage decision, not the final recommendation ranking. It
        prevents an exact user-selected course from disappearing merely because
        several catalogue variants share its name.
        """
        attributes = candidate["structured_attributes"]
        score = 0
        schedule = str(answers.get("q3_schedule") or "").lower()
        attendance = str(attributes.get("attendance_type") or "").lower()
        days = str(attributes.get("attendance_days") or "").lower()
        if schedule and "no strong preference" not in schedule and NOT_STATED.lower() not in attendance:
            wants_part_time = "part-time" in schedule or "weekend" in schedule
            is_part_time = "part time" in attendance or "weekend" in days
            score += 2 if wants_part_time == is_part_time else -2
        language = str(answers.get("q4_language") or "").strip().lower()
        course_languages = str(attributes.get("instruction_languages") or "").lower()
        if language and "no strong preference" not in language and course_languages != NOT_STATED.lower():
            score += 2 if language in course_languages else -2
        qualification = str(answers.get("q5_qualification") or "").strip().lower()
        if qualification.startswith("yes"):
            stated = attributes.get("qualification_type") not in (NOT_STATED, "", None)
            score += 1 if stated else -1
        return score, candidate["course_id"]

    required_skill_coverage = []
    for sector in sectors:
        for skill in _as_distinct_strings(skills_by_sector.get(sector)):
            matching_candidates = [
                candidate for candidate in candidates
                if any(
                    match["sector"] == sector and match["skill"] == skill
                    for match in candidate["exact_selected_skill_matches"]
                )
            ]
            if not matching_candidates:
                continue
            selected = max(matching_candidates, key=preference_fit)
            required_skill_coverage.append({
                "sector": sector,
                "selected_skill": skill,
                "required_course_id": selected["course_id"],
                "available_exact_course_ids": [
                    candidate["course_id"] for candidate in matching_candidates
                ],
            })
    retrieval_method = (
        "complete verified catalogue fallback for unspecified sector"
        if sector_preference_unsure
        else "complete verified catalogue slice for selected sectors"
    )
    note = (
        f"The member did not specify a sector. Retrieved all {len(candidates)} verified "
        "catalogue courses so the existing ranking flow can use the other questionnaire "
        "answers and validated profile context. No suitability score or pre-ranking was applied."
        if sector_preference_unsure
        else (
            f"Retrieved all {len(candidates)} verified courses in the catalogue areas "
            f"mapped from the selected sectors. No suitability score or pre-ranking was applied."
        )
    )
    return {
        "retrieval_method": retrieval_method,
        "sector_skill_areas": sector_skill_areas,
        "skill_areas": skill_areas,
        "selected_skills_by_sector": skills_by_sector,
        "required_selected_skill_coverage": required_skill_coverage,
        "candidates": candidates,
        "note": note,
    }


def select_candidates(answers: dict) -> dict:
    """answers: {
        "ideal_sectors": list[str],             # preferred sectors (legacy ideal_sector also accepted)
        "selected_skills": list[str],           # selected course/skill names (legacy Q1 also accepted)
        "q3_schedule": str,                     # "Full-time, weekdays" / "Part-time, weekends" / "No strong preference"
        "q4_language": str,                     # "Sinhala" / "English" / "No strong preference"
        "q5_qualification": str,                # "Yes" / "Not necessarily" / "Not sure"
    }
    Returns {"skill_areas": [...], "candidates": [{"course_id", "score", "score_breakdown"}], "note": str}
    """
    rows = load_matching_layer()
    sectors = _as_distinct_strings(answers.get("ideal_sectors") or answers.get("ideal_sector"))
    selected_skills = _as_distinct_strings(
        answers.get("selected_skills") or answers.get("q1_occupation_focus")
    )
    skill_areas = skill_areas_for_ideal_sectors(sectors)

    if not skill_areas:
        return {"skill_areas": [], "selected_skills": selected_skills, "candidates": [],
                "note": "No skill area could be determined from the selected sectors "
                        "(respondent answered 'Not sure' or an unbridged sector). "
                        "No candidates were selected — this is expected to lead to "
                        "NO_DEFENSIBLE_RECOMMENDATION unless other evidence justifies an exception."}

    pool = [r for r in rows if r["skill_area"] in skill_areas and r["skill_area"] != NOT_STATED]
    selected_skills_lower = {
        skill.lower() for skill in selected_skills
        if skill.lower() not in UNSURE_SKILL_VALUES
    }

    scored = []
    for r in pool:
        score = 0
        breakdown = []
        if selected_skills_lower:
            if _strip_variant_suffix(r["rag_course_name"]).lower() in selected_skills_lower:
                score += 3
                breakdown.append("course-name match (+3)")

        q3 = (answers.get("q3_schedule") or "").strip().lower()
        if q3 and "no strong preference" not in q3 and r["attendance_type"] != NOT_STATED:
            wants_ft = "full-time" in q3 or "weekday" in q3
            is_ft = r["attendance_type"] == "Full Time"
            if wants_ft == is_ft:
                score += 2
                breakdown.append("schedule match (+2)")

        q4 = (answers.get("q4_language") or "").strip().lower()
        if q4 and "no strong preference" not in q4 and r["instruction_languages"] != NOT_STATED:
            if q4 in r["instruction_languages"].lower():
                score += 2
                breakdown.append("language match (+2)")

        q5 = (answers.get("q5_qualification") or "").strip().lower()
        if q5.startswith("yes") and r["qualification_type"] not in (NOT_STATED, ""):
            score += 1
            breakdown.append("qualification match (+1)")

        scored.append({
            "course_id": r["rag_course_id"],
            "course_name": r["rag_course_name"],
            "score": score,
            "score_breakdown": breakdown,
            "structured_attributes": {k: r[k] for k in
                                       ["skill_area", "attendance_type", "attendance_days",
                                        "duration_months", "instruction_languages",
                                        "nvq_level", "qualification_type"]},
        })

    scored.sort(key=lambda c: (-c["score"], c["course_id"]))
    candidates = scored[:MAX_CANDIDATES]

    all_zero_score = candidates and all(c["score"] == 0 for c in candidates)
    note = (f"{len(pool)} courses in bridged skill area(s) {skill_areas}; "
            f"{len(candidates)} selected deterministically by score.")
    if not pool:
        note = f"No courses found in bridged skill area(s) {skill_areas} — unexpected, check the crosswalk."
    elif all_zero_score:
        note += (" None scored above 0 (selected skills and schedule/language/qualification answers were "
                  "all unspecified/no preference, or "
                  "didn't match any pool course) — these are the top courses by ID within the sector only, "
                  "not preference-matched; disclose this to the respondent rather than presenting them as "
                  "personally tailored.")

    return {
        "skill_areas": skill_areas,
        "selected_skills": selected_skills,
        "candidates": candidates,
        "note": note,
    }
