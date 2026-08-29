"""
NEW, ADDITIVE audit module for the targeted evidence-hierarchy refinement (Section 11
of the task). Does NOT modify grounding_audit_v2.py or evidence_category_discipline_audit.py
— those existing safeguards run unchanged, in addition to these new checks.

Checks implemented, each mechanical and independently reportable:
  1. available_to_start misuse — cited to justify training/schedule/study availability
     rather than job-start availability.
  2. Economic-profile -> individual-affordability overreach — a D_economic/G_economic_role
     profile citation whose finding text asserts or implies individual affordability/
     capacity-to-pay/capacity-to-attend, rather than remaining explicitly group-level.
  3. Current-occupation-as-preference overreach — occupational_class/employment_status
     cited as the PRIMARY (position-1-equivalent: first evidence item) justification for
     a recommendation's field, when no genuine DIRECT_PREFERENCE_OR_INTENT variable is
     also cited for that same recommendation.
  4. match_relationship defensibility — DIRECT_MATCH requires at least one
     DIRECT_PREFERENCE_OR_INTENT citation; ADJACENT_MATCH requires a non-empty
     adjacent_match_bridge_explanation and must NOT also claim a DIRECT_PREFERENCE_OR_INTENT
     citation as its sole/primary justification (that would make it a DIRECT_MATCH by the
     model's own stated rules).
  5. Profile-context overreach (general) — a profile_context_used finding phrased as an
     unhedged individual fact (e.g. "this respondent is/has/needs..." without "may",
     "consistent with", "group-level", "profile members", "tendency", etc.).
  6. Catalogue-gap visibility — when no DIRECT_MATCH exists among a respondent's
     recommendations (or the respondent declined), confirms catalogue_coverage_note or
     the decline reason actually says so rather than leaving the gap implicit.
"""
import csv, json, re
from pathlib import Path
from corpus_v2 import BASE

POLICY_CSV = BASE / "outputs/rag_respondent_evidence/respondent_variable_policy.csv"

AFFORDABILITY_PATTERNS = [
    "can afford", "cannot afford", "afford", "capacity to pay", "capacity to attend",
    "capacity to pursue", "fee-paying", "willingness to pay", "financial capacity",
    "able to pay", "unable to pay",
]

TRAINING_AVAILABILITY_PATTERNS = [
    "readiness to undertake training", "readiness for training", "available for training",
    "available to study", "availability for training", "training readiness",
    "ready to start the course", "ready to begin training", "weekday availability",
    "full-time-study availability", "start the course immediately", "undertake training",
]

UNHEDGED_INDIVIDUAL_FACT_RE = re.compile(
    r"\bthis respondent (is|has|needs|requires|cannot|can only|must)\b", re.IGNORECASE
)
HEDGE_MARKERS = ["may", "might", "could", "consistent with", "group-level", "group level",
                 "profile members", "tendency", "does not establish", "supporting context",
                 "background context", "broader pattern", "within this profile", "profile-level"]


def load_policy():
    with open(POLICY_CSV, newline="", encoding="utf-8-sig") as f:
        return {r["variable"]: r for r in csv.DictReader(f)}


def check_available_to_start(rec_dict):
    issues = []
    for e in rec_dict.get("direct_respondent_evidence_used", []):
        if e.get("variable") != "available_to_start":
            continue
        relevance = (e.get("relevance") or "").lower()
        if any(p in relevance for p in TRAINING_AVAILABILITY_PATTERNS):
            issues.append(
                f"available_to_start (job-start availability) cited with training/schedule-availability "
                f"framing: \"{e.get('relevance')}\" — confirmed misuse pattern"
            )
    return issues


def check_economic_profile_affordability(rec_dict):
    """
    STRICT, NO-EXCEPTION check (tightened after the final targeted validation): ANY
    economic/resource-profile citation that touches affordability/fee/payment-capacity
    language is a FAIL, regardless of hedging. An earlier version of this check
    downgraded explicitly-hedged instances (e.g. "...but this is group-level context
    only") to a caution — that carve-out is exactly what the tightened governance rule
    (see context_pack_v2.py, "ABSOLUTE RULE") now explicitly forbids: hedging does not
    make an affordability-flavoured economic-profile citation acceptable. There is no
    caution tier for this check any more; every hit is a FAIL.
    """
    issues = []
    for p in rec_dict.get("profile_context_used", []):
        prof = (p.get("profile") or "").lower()
        if "economic" not in prof:
            continue
        finding = p.get("finding") or ""
        finding_lower = finding.lower()
        if any(pat in finding_lower for pat in AFFORDABILITY_PATTERNS):
            issues.append(
                f"economic/resource profile '{p.get('profile')}' finding touches affordability/fee/"
                f"payment-capacity language (no hedging exception applies): \"{finding}\" — profile "
                f"economic position must never be connected to individual affordability in any form"
            )
    return issues


def check_occupation_as_preference(rec_dict, policy):
    issues = []
    evidence = rec_dict.get("direct_respondent_evidence_used", [])
    if not evidence:
        return issues
    has_genuine_preference = any(
        policy.get(e.get("variable"), {}).get("evidence_category") == "DIRECT_PREFERENCE_OR_INTENT"
        for e in evidence
    )
    first = evidence[0]
    if first.get("variable") in ("occupational_class", "employment_status") and not has_genuine_preference:
        issues.append(
            f"'{first.get('variable')}' (current occupation) is the PRIMARY (first-listed) evidence for this "
            f"recommendation, and no genuine DIRECT_PREFERENCE_OR_INTENT variable is also cited — current "
            f"occupation alone must not establish desired training field"
        )
    return issues


def check_match_relationship(rec_dict, policy):
    issues = []
    match = rec_dict.get("match_relationship")
    bridge = rec_dict.get("adjacent_match_bridge_explanation")
    evidence = rec_dict.get("direct_respondent_evidence_used", [])
    has_genuine_preference = any(
        policy.get(e.get("variable"), {}).get("evidence_category") == "DIRECT_PREFERENCE_OR_INTENT"
        for e in evidence
    )
    if match == "DIRECT_MATCH" and not has_genuine_preference:
        issues.append("classified DIRECT_MATCH but no DIRECT_PREFERENCE_OR_INTENT variable is cited as evidence")
    if match == "ADJACENT_MATCH" and not (bridge and bridge.strip()):
        issues.append("classified ADJACENT_MATCH but adjacent_match_bridge_explanation is empty/missing")
    if match == "DIRECT_MATCH" and bridge:
        issues.append("classified DIRECT_MATCH but adjacent_match_bridge_explanation is non-null (should be null)")
    if match is None:
        issues.append("match_relationship missing entirely")
    return issues


def check_profile_overreach(rec_dict):
    cautions = []
    for p in rec_dict.get("profile_context_used", []):
        finding = p.get("finding") or ""
        if UNHEDGED_INDIVIDUAL_FACT_RE.search(finding):
            has_hedge = any(h in finding.lower() for h in HEDGE_MARKERS)
            if not has_hedge:
                cautions.append(
                    f"profile '{p.get('profile')}' finding uses unhedged individual-fact phrasing without a "
                    f"group-level qualifier: \"{finding}\""
                )
    return cautions


def audit_recommendation_hierarchy(rec_dict, policy):
    issues, cautions = [], []
    issues.extend(check_available_to_start(rec_dict))
    issues.extend(check_economic_profile_affordability(rec_dict))
    issues.extend(check_occupation_as_preference(rec_dict, policy))
    issues.extend(check_match_relationship(rec_dict, policy))
    cautions.extend(check_profile_overreach(rec_dict))

    if issues:
        status = "FAIL"
    elif cautions:
        status = "PASS WITH CAUTION"
    else:
        status = "PASS"
    return status, issues, cautions


def audit_catalogue_gap_visibility(resp_record):
    """Respondent-level check: if every returned recommendation is ADJACENT_MATCH (or the
    respondent declined), was the catalogue gap actually disclosed?"""
    status_field = resp_record.get("recommendation_status")
    recs = resp_record.get("recommendations", [])
    if status_field == "NO_DEFENSIBLE_RECOMMENDATION":
        reason = resp_record.get("no_defensible_recommendation_reason") or ""
        if not reason.strip():
            return "FAIL", ["NO_DEFENSIBLE_RECOMMENDATION with an empty reason — catalogue gap not disclosed"]
        return "PASS", []
    if recs and all(r.get("match_relationship") == "ADJACENT_MATCH" for r in recs):
        note = resp_record.get("catalogue_coverage_note")
        if not (note and note.strip()):
            return "FAIL", ["all recommendations are ADJACENT_MATCH but catalogue_coverage_note was not set"]
        return "PASS", []
    return "PASS", []


def audit_all(recommendations_jsonl_path, policy):
    rows = []
    with open(recommendations_jsonl_path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            rid = rec["respondent_id"]

            gap_status, gap_issues = audit_catalogue_gap_visibility(rec)
            rows.append({
                "respondent_id": rid, "check": "catalogue_gap_visibility", "course_id": "(respondent-level)",
                "status": gap_status, "issues": "; ".join(gap_issues) if gap_issues else "(none)",
            })

            for r in rec.get("recommendations", []):
                status, issues, cautions = audit_recommendation_hierarchy(r, policy)
                rows.append({
                    "respondent_id": rid, "check": "evidence_hierarchy", "course_id": r.get("course_id"),
                    "status": status,
                    "issues": "; ".join(issues) if issues else ("; ".join(f"CAUTION: {c}" for c in cautions) if cautions else "(none)"),
                })
    return rows


if __name__ == "__main__":
    import sys
    from collections import Counter
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not path:
        print("usage: python3 evidence_hierarchy_audit.py <recommendations.jsonl>")
        sys.exit(1)
    policy = load_policy()
    rows = audit_all(path, policy)
    print(dict(Counter(r["status"] for r in rows)))
    for r in rows:
        if r["status"] != "PASS":
            print(r)
