"""
§5 — NEW-person recommendation runner. This is a per-person feature, not a
cohort batch job: it is never invoked against the historical 362 respondents
(see run_full_cohort.py for that, frozen and untouched). Each call here is
for exactly one new intake person.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_v2 import verify_corpus, BASE
from env_config import get_production_model, verify_production_model
import new_person_candidate_selection as candidate_selection
import new_person_context_pack as context_pack
import new_person_profile_context as profile_context
from new_person_recommendation_schema import NewPersonRecommendationResponse
from new_person_openai_client import call_new_person_recommendation_api

VALUES_CSV = BASE / "outputs/nysc_survey_cleaned_values.csv"
LABELS_CSV = BASE / "outputs/nysc_survey_cleaned_labels.csv"
OUT_DIR = BASE / "outputs/rag_new_person_intake_v1"


def load_donor_cluster_answers(respondent_id: str, variables: list[str]) -> dict:
    """Borrows a REAL respondent's cluster-forming answers (for §0 validity only —
    these are ordinary, already-existing profiling-survey items, not the new
    programme-matching questions under test) so synthetic test people have
    realistic, validly-encoded §0 input. The actual scenario under test is the
    ideal_sector/Q1-Q5 override applied by the caller, not these borrowed values."""
    with open(VALUES_CSV, newline="", encoding="utf-8-sig") as f:
        vrow = next(r for r in csv.DictReader(f) if r["respondent_id"] == respondent_id)
    with open(LABELS_CSV, newline="", encoding="utf-8-sig") as f:
        lrow = next(r for r in csv.DictReader(f) if r["respondent_id"] == respondent_id)
    return {v: {"value_code": vrow[v], "value_label": lrow.get(v)} for v in variables if vrow.get(v)}


def run_one(spec: dict, model_by_id: dict, call_api: bool = True) -> dict:
    """spec: {
        "person_id": str, "branch": str, "cluster_answers": dict (§0 shape),
        "ideal_sector": str or None, "q1_occupation_focus", "q2_reason",
        "q3_schedule", "q4_language", "q5_qualification": str or None,
        "case_description": str,
    }
    """
    officer_context = {
        "ideal_sector": spec.get("ideal_sector"),
        "q1_occupation_focus": spec.get("q1_occupation_focus"),
        "q2_reason": spec.get("q2_reason"),
        "q3_schedule": spec.get("q3_schedule"),
        "q4_language": spec.get("q4_language"),
        "q5_qualification": spec.get("q5_qualification"),
    }
    profile_entries = profile_context.build_profile_context(
        spec["branch"], spec["cluster_answers"], officer_context,
    )
    selection = candidate_selection.select_candidates({
        "ideal_sector": spec.get("ideal_sector"),
        "q1_occupation_focus": spec.get("q1_occupation_focus"),
        "q3_schedule": spec.get("q3_schedule"),
        "q4_language": spec.get("q4_language"),
        "q5_qualification": spec.get("q5_qualification"),
    })
    input_text = context_pack.build_new_person_input_text(
        spec["person_id"], spec["branch"], spec.get("ideal_sector"),
        {"q1_occupation_focus": spec.get("q1_occupation_focus"), "q2_reason": spec.get("q2_reason"),
         "q3_schedule": spec.get("q3_schedule"), "q4_language": spec.get("q4_language"),
         "q5_qualification": spec.get("q5_qualification")},
        profile_entries, selection, model_by_id,
    )

    result = {"spec": spec, "profile_entries": profile_entries, "selection": selection,
              "input_text": input_text, "api_result": None}

    if call_api:
        model = get_production_model()
        verify_production_model(model)
        api_result = call_new_person_recommendation_api(
            spec["person_id"], input_text, model,
            context_pack.GOVERNANCE_INSTRUCTIONS, NewPersonRecommendationResponse,
        )
        result["api_result"] = api_result

    return result


def format_human_readable(result: dict) -> str:
    spec = result["spec"]
    profile_entries = result["profile_entries"]
    selection = result["selection"]
    api_result = result["api_result"]

    out = [f"# Your NYSC Programme Recommendations", f"(Test person: {spec['person_id']} — {spec.get('case_description', '')})", ""]

    out.append("## YOUR YOUTH PROFILE\n")
    if not profile_entries:
        out.append("No profile could be assigned for this branch.\n")
    for e in profile_entries:
        out.append(f"- **{e.profile_label}** (`{e.profile_key}`)")
        out.append(f"  - Assignment similarity: {e.membership_similarity_percent}% "
                    f"(distance-based similarity to this profile vs. the next-closest one — "
                    f"NOT a validated accuracy figure)")
        out.append(f"  - Model reliability: {e.model_judgment} "
                    f"(published accuracy {e.model_published_accuracy:.1%} on known cases)")
        if e.distance_tie:
            out.append("  - NOTE: this was a near/exact tie between two profiles — treat as low-confidence.")
    out.append("")

    out.append("## PEOPLE WITH SIMILAR PROFILE PATTERNS\n")
    for e in profile_entries:
        if e.validated_evidence:
            out.append(f"**{e.profile_key}:**")
            for evidence in e.validated_evidence[:2]:
                out.append(f"  {evidence['finding']}")
    out.append("")
    out.append("*These percentages describe patterns observed in the group and do not mean that "
                "every person in the profile has these characteristics.*\n")

    out.append("## WHAT YOU TOLD US\n")
    out.append(f"- [YOUR ANSWER] Sector: {spec.get('ideal_sector') or 'Not sure'}")
    out.append(f"- [YOUR ANSWER] Occupation/course focus: {spec.get('q1_occupation_focus') or 'Not sure'}")
    out.append(f"- [YOUR ANSWER] Main reason for training: {spec.get('q2_reason') or 'Not stated'}")
    out.append(f"- [YOUR ANSWER] Schedule preference: {spec.get('q3_schedule') or 'No strong preference'}")
    out.append(f"- [YOUR ANSWER] Language preference: {spec.get('q4_language') or 'No strong preference'}")
    out.append(f"- [YOUR ANSWER] Qualification preference: {spec.get('q5_qualification') or 'Not sure'}\n")

    out.append("## RECOMMENDED NYSC PROGRAMMES\n")
    out.append(f"*Candidate selection note: {selection['note']}*\n")

    if api_result is None:
        out.append("*(Offline run — no LLM call made; showing deterministic candidate selection only.)*")
        for c in selection["candidates"]:
            out.append(f"- `{c['course_id']}` — {c['course_name']} (score {c['score']}: "
                        f"{', '.join(c['score_breakdown']) or 'no scored match'})")
        return "\n".join(out)

    if not api_result.success:
        out.append(f"*(API call failed: {api_result.error_message})*")
        return "\n".join(out)

    parsed: NewPersonRecommendationResponse = api_result.parsed
    out.append(f"**Status: {parsed.recommendation_status}**")
    if parsed.catalogue_coverage_note:
        out.append(f"*{parsed.catalogue_coverage_note}*")
    out.append("")

    if parsed.recommendation_status == "NO_DEFENSIBLE_RECOMMENDATION":
        out.append(f"No defensible recommendation: {parsed.no_defensible_recommendation_reason}")
        return "\n".join(out)

    for rec in parsed.recommendations:
        out.append(f"### {rec.rank}. {rec.course_name} (`{rec.course_id}`)")
        out.append(f"**{rec.match_type}** | Evidence strength: {rec.evidence_strength} — {rec.evidence_strength_reason}")
        if rec.bridge_explanation:
            out.append(f"\n**Bridge (why this is a defensible ADJACENT_MATCH):** {rec.bridge_explanation}")
        out.append(f"\n**Why this matches what you told us:** {rec.why_matches_explicit_answers}")
        out.append("\n**[YOUR ANSWER] evidence used:**")
        for a in rec.explicit_answers_used:
            out.append(f"- {a.question}: {a.answer} — {a.relevance}")
        out.append("\n**[COURSE FACT] evidence used:**")
        for cf in rec.course_facts_used:
            out.append(f"- \"{cf.fact}\" (source: {cf.source_reference})")
        out.append(f"\n**[PROFILE PATTERN] contribution:** {rec.profile_context_contribution.role}")
        if rec.profile_context_contribution.insight:
            out.append(f"  {rec.profile_context_contribution.insight}")
        if rec.profile_context_contribution.contributing_findings:
            out.append("  <details>evidence trail:")
            for f in rec.profile_context_contribution.contributing_findings:
                out.append(f"  - `{f.variable}`: {f.finding}")
        if rec.llm_inferences:
            out.append("\n**[LLM REASONING]:**")
            for inf in rec.llm_inferences:
                out.append(f"- {inf}")
        if rec.limitations:
            out.append("\n**Limitations/unknowns:**")
            for lim in rec.limitations:
                out.append(f"- {lim}")
        out.append("")

    return "\n".join(out)
