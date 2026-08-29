"""
Evidence-category-discipline audit — extends the grounding audit with a check the
existing mechanical audit does NOT perform: whether each cited respondent variable is
being USED in a way consistent with its evidence-policy category
(outputs/rag_respondent_evidence/respondent_variable_policy.csv), not just whether the
variable/value exists and isn't contradicted.

This is a NEW, ADDITIVE check. It does not modify grounding_audit_v2.py's existing
behaviour or overwrite any previously-saved audit CSV; it writes only the two new files
this task asks for. No new API calls, no retrieval/corpus/model changes.

Motivating case (must be caught): respondent nysc-465701ee..., recommendation
COURSE-006 in the gpt-5-mini run, cited `most_useful_quality_for_job` (policy category
INDIVIDUAL_CONTEXT_ONLY — a general opinion question, not a stated preference) as the
FIRST/primary evidence item for a STRONG-rated recommendation, using preference-framing
language ("explicitly values"). This is exactly the pattern this module is built to
catch mechanically.

METHOD AND ITS LIMITS:
For each `direct_respondent_evidence_used` item, its "role" (how the LLM is actually
using it) is inferred from simple, transparent keyword pattern-matching on the item's
own `relevance` text: PREFERENCE-framing (implies the respondent wants/prefers this,
i.e. driving programme CONTENT selection), FEASIBILITY-framing (schedule/format/
practical-combination language), EXPERIENCE-framing (builds-on-background language), or
UNCLEAR. List position (1 = first) is used as a proxy for "primary/leading" evidence,
consistent with the observed pattern that the model lists its strongest justification
first. This is a mechanical heuristic, not semantic understanding — it can miscategorise
novel phrasing, so PASS WITH CAUTION results should still get a human glance; FAIL
results were spot-checked by hand against the actual JSONL text before being reported.
"""
import csv, json, re
from pathlib import Path
from corpus_v2 import BASE

POLICY_CSV = BASE / "outputs/rag_respondent_evidence/respondent_variable_policy.csv"
RESPONDENT_EVIDENCE_JSONL = BASE / "outputs/rag_respondent_evidence/respondent_evidence.jsonl"

GPT5_JSONL = BASE / "outputs/rag_recommendation_prototype_api_v2/api_test_recommendations.jsonl"
GPT4O_JSONL = BASE / "outputs/rag_recommendation_prototype_api/api_test_recommendations.jsonl"

OUT_DIR = BASE / "outputs/rag_recommendation_prototype_api_v2"

PROTECTED_TECHNICAL = {"PROTECTED_OR_PROXY_DO_NOT_USE", "TECHNICAL_DO_NOT_USE"}

PREFERENCE_PATTERNS = [
    "aligns with", "align with", "matches", "match the", "directly relevant",
    "direct match", "explicitly values", "explicitly stated", "explicitly express",
    "priorit", "respondent wants", "stated preference", "respondent's interest",
    "core interest", "wants further", "stated interest", "values it", "prioritised",
    "prioritized",
]
FEASIBILITY_PATTERNS = [
    "schedule", "part-time", "part time", "full-time", "full time", "weekend",
    "weekday", "attend", "combine with", "responsibilit", "hours", "afford",
    "practical scheduling", "commute", "income responsibilit", "care", "household",
    "provider",
]
EXPERIENCE_PATTERNS = [
    "builds on", "build on", "prior experience", "previous experience", "already has",
    "already worked", "further develops", "existing skill", "background in",
]


def classify_role(relevance_text: str) -> str:
    t = (relevance_text or "").lower()
    if any(p in t for p in PREFERENCE_PATTERNS):
        return "preference_framing"
    if any(p in t for p in FEASIBILITY_PATTERNS):
        return "feasibility_framing"
    if any(p in t for p in EXPERIENCE_PATTERNS):
        return "experience_framing"
    return "unclear"


def load_policy():
    with open(POLICY_CSV, newline="", encoding="utf-8-sig") as f:
        return {r["variable"]: r for r in csv.DictReader(f)}


def load_respondents():
    out = {}
    with open(RESPONDENT_EVIDENCE_JSONL, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            out[r["respondent_id"]] = r
    return out


def evaluate_citation(category: str, role: str, position: int, adjacent_match_disclosed: bool = False):
    """
    Returns (status, severity, note) for one cited variable's usage.

    `adjacent_match_disclosed`: True when this citation belongs to a recommendation that
    (a) is classified match_relationship == "ADJACENT_MATCH", (b) has a non-empty
    adjacent_match_bridge_explanation, AND (c) also cites at least one genuine
    DIRECT_PREFERENCE_OR_INTENT variable elsewhere in the same recommendation. Added
    after the final targeted validation, where this exact audit produced a known false
    FAIL on a citation later confirmed by manual review to be the correctly-disclosed,
    intended "builds on experience"/upskilling use of a FEASIBILITY_OR_CONSTRAINT_CONTEXT
    or EDUCATION_AND_EXPERIENCE_CONTEXT variable within a properly labelled adjacent
    match — the pre-ADJACENT_MATCH-schema version of this audit could not distinguish
    that from a false direct-preference claim. Defaults to False, so older saved
    recommendations without match_relationship (pre-dating this schema field) are
    evaluated exactly as before — this parameter changes nothing for that historical data.
    INDIVIDUAL_CONTEXT_ONLY (e.g. general opinion/perception variables) deliberately does
    NOT get this exemption: an opinion question is not legitimate evidence for a content
    bridge either, direct or adjacent.
    """
    if category in PROTECTED_TECHNICAL:
        return "FAIL", "HIGH", "protected/technical variable must never appear as recommendation evidence"

    if category == "DIRECT_PREFERENCE_OR_INTENT":
        return "PASS", "NONE", "category explicitly permits driving programme content/field selection"

    if category == "FEASIBILITY_OR_CONSTRAINT_CONTEXT":
        if role == "preference_framing":
            if adjacent_match_disclosed:
                return "PASS", "NONE", ("used as disclosed supporting evidence for a properly-labelled "
                                        "ADJACENT_MATCH recommendation (co-cited with genuine direct-preference "
                                        "evidence and an explained bridge) — not a false direct-preference claim")
            if position == 1:
                return "FAIL", "HIGH", ("feasibility-only variable used as the PRIMARY justification for "
                                        "programme content/field match — violates 'must not independently "
                                        "determine programme content'")
            return "PASS WITH CAUTION", "MEDIUM", ("feasibility-only variable used with content-preference "
                                                    "framing as a secondary citation — materially influences "
                                                    "reasoning, should not be the deciding factor")
        return "PASS", "NONE", "used for feasibility reasoning, consistent with its category"

    if category == "EDUCATION_AND_EXPERIENCE_CONTEXT":
        if role == "preference_framing":
            if adjacent_match_disclosed:
                return "PASS", "NONE", ("used as disclosed supporting evidence for a properly-labelled "
                                        "ADJACENT_MATCH recommendation (co-cited with genuine direct-preference "
                                        "evidence and an explained bridge) — not a false direct-preference claim")
            if position == 1:
                return "FAIL", "HIGH", ("experience/background variable presented as a stated preference "
                                        "without an explicit respondent preference statement — violates "
                                        "'must not be presented as a stated preference unless the respondent "
                                        "explicitly expressed one'")
            return "PASS WITH CAUTION", "MEDIUM", ("experience/background variable given preference-like "
                                                    "framing as a secondary citation")
        return "PASS", "NONE", "used for builds-on-experience reasoning, consistent with its category"

    if category == "INDIVIDUAL_CONTEXT_ONLY":
        if role == "preference_framing" and position == 1:
            return "FAIL", "HIGH", ("context-only variable used as the PRIMARY reason with preference-like "
                                    "framing — violates 'must NOT be used as the primary reason for selecting "
                                    "or strongly ranking a programme'")
        if position == 1:
            return "PASS WITH CAUTION", "MEDIUM", ("individual-context-only variable is the primary "
                                                    "(first-listed) cited variable for this recommendation; "
                                                    "its category says it must not be the primary reason, "
                                                    "regardless of exact phrasing")
        if role == "preference_framing":
            return "PASS WITH CAUTION", "MEDIUM", ("context-only variable given preference-like framing as a "
                                                    "secondary citation")
        return "PASS", "NONE", "used as secondary supporting context/explanation, consistent with its category"

    return "PASS WITH CAUTION", "LOW", f"variable not found in policy CSV or category unrecognised: {category}"


def audit_recommendations(jsonl_path, policy, model_label):
    rows = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            rid = rec["respondent_id"]
            for r in rec.get("recommendations", []):
                cid = r.get("course_id")
                strength = r.get("evidence_strength")
                evidence_list = r.get("direct_respondent_evidence_used", [])

                # Backward-compatible: match_relationship/adjacent_match_bridge_explanation
                # are absent on pre-schema-update saved recommendations, so this is False
                # for all historical data and changes nothing about how it's audited.
                has_genuine_preference = any(
                    (policy.get(e.get("variable"), {}).get("evidence_category") == "DIRECT_PREFERENCE_OR_INTENT")
                    for e in evidence_list
                )
                adjacent_match_disclosed = bool(
                    r.get("match_relationship") == "ADJACENT_MATCH"
                    and (r.get("adjacent_match_bridge_explanation") or "").strip()
                    and has_genuine_preference
                )

                for pos, item in enumerate(evidence_list, start=1):
                    var = item.get("variable")
                    relevance = item.get("relevance", "")
                    policy_row = policy.get(var)
                    category = policy_row["evidence_category"] if policy_row else "UNKNOWN_VARIABLE"
                    role = classify_role(relevance)
                    status, severity, note = evaluate_citation(category, role, pos, adjacent_match_disclosed)
                    rows.append({
                        "model": model_label,
                        "respondent_id": rid,
                        "course_id": cid,
                        "recommendation_evidence_strength": strength,
                        "variable": var,
                        "policy_category": category,
                        "citation_position": pos,
                        "role_inferred_from_relevance_text": role,
                        "relevance_text": relevance,
                        "role_allowed_for_category": status == "PASS",
                        "status": status,
                        "severity": severity,
                        "note": note,
                    })
    return rows


DECLINE_CONTENT_JUDGEMENT_WORDS = ["sector", "field", "align", "match", "relevant to", "does not support",
                                    "does not directly", "not related to"]


def audit_declines(jsonl_path, policy, respondents, model_label):
    rows = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            rid = rec["respondent_id"]
            status_field = rec.get("recommendation_status")
            has_recs = bool(rec.get("recommendations"))
            if has_recs or status_field != "NO_DEFENSIBLE_RECOMMENDATION":
                continue
            reason = (rec.get("no_defensible_recommendation_reason") or "")
            reason_lower = reason.lower()
            respondent = respondents.get(rid, {})
            answered = {}
            for cat in ("feasibility_or_constraint_context", "education_and_experience_context",
                        "individual_context_only"):
                for var, e in respondent.get(cat, {}).items():
                    if e.get("status") == "answered" and e.get("value_label"):
                        answered[var] = e["value_label"]

            has_content_judgement = any(w in reason_lower for w in DECLINE_CONTENT_JUDGEMENT_WORDS)
            flagged_any = False
            for var, label in answered.items():
                if label.lower() in reason_lower and len(label) > 6:
                    policy_row = policy.get(var)
                    category = policy_row["evidence_category"] if policy_row else "UNKNOWN_VARIABLE"
                    if category in ("FEASIBILITY_OR_CONSTRAINT_CONTEXT", "EDUCATION_AND_EXPERIENCE_CONTEXT",
                                     "INDIVIDUAL_CONTEXT_ONLY") and has_content_judgement:
                        flagged_any = True
                        rows.append({
                            "model": model_label, "respondent_id": rid, "course_id": "(none — decline)",
                            "recommendation_evidence_strength": "",
                            "variable": var, "policy_category": category, "citation_position": "",
                            "role_inferred_from_relevance_text": "decline_text_cooccurrence",
                            "relevance_text": reason[:300],
                            "role_allowed_for_category": False,
                            "status": "PASS WITH CAUTION",
                            "severity": "LOW",
                            "note": (f"decline reason contains both a content/field-relevance judgement and "
                                     f"the respondent's answer to '{var}' ({category}); flagged for human "
                                     f"review of whether that context-only fact improperly shaped the content "
                                     f"judgement — co-occurrence is not proof of misuse"),
                        })
            if not flagged_any:
                rows.append({
                    "model": model_label, "respondent_id": rid, "course_id": "(none — decline)",
                    "recommendation_evidence_strength": "", "variable": "", "policy_category": "",
                    "citation_position": "", "role_inferred_from_relevance_text": "",
                    "relevance_text": reason[:300], "role_allowed_for_category": True,
                    "status": "PASS", "severity": "NONE",
                    "note": "no evidence-category-discipline concern detected in this decline reason",
                })
    return rows


if __name__ == "__main__":
    policy = load_policy()
    respondents = load_respondents()

    all_rows = []
    all_rows += audit_recommendations(GPT5_JSONL, policy, "gpt-5-mini")
    all_rows += audit_declines(GPT5_JSONL, policy, respondents, "gpt-5-mini")
    all_rows += audit_recommendations(GPT4O_JSONL, policy, "gpt-4o-mini")
    all_rows += audit_declines(GPT4O_JSONL, policy, respondents, "gpt-4o-mini")

    out_csv = OUT_DIR / "evidence_category_discipline_audit.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        w.writeheader()
        for r in all_rows:
            w.writerow(r)

    from collections import Counter
    print(f"Wrote {len(all_rows)} rows -> {out_csv}")
    print("By model+status:")
    for model in ("gpt-5-mini", "gpt-4o-mini"):
        sub = [r for r in all_rows if r["model"] == model]
        print(f"  {model}: {dict(Counter(r['status'] for r in sub))}")
