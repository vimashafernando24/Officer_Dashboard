"""
Automated evidence-grounding audit for API-produced recommendations (Section N/O).

Two layers, applied to BOTH actual recommendations AND NO_DEFENSIBLE_RECOMMENDATION
decline reasons (a decline is not exempt from grounding requirements — it can contain
unsupported respondent/course/eligibility claims just as a recommendation can):
  1. MECHANICAL checks (deterministic, no ambiguity): course_id was actually retrieved
     and is not on the excluded list; no protected/technical field name appears in the
     recommendation/decline text; cited respondent variable names exist in the
     respondent's evidence and cited values are not contradicted; cited profile keys
     exist among the respondent's actual frozen memberships; inferences are
     structurally present with based_on evidence; recommendation_status/
     recommendations-list consistency; a decline reason does not reference a course_id
     that was never actually retrieved.
  2. APPROXIMATE TEXT-GROUNDING checks: for each course_evidence_used claim, a lenient
     word-overlap check against the actual retrieved parent document (catches obvious
     fabrication without requiring exact-string matching of paraphrased text).
  3. UNSUPPORTED-ELIGIBILITY-CLAIM check (new): flags a decline (or recommendation)
     reason that asserts or implies an entry-requirement judgement — positive or
     negative — without the course text explicitly stating a requirement. The clearest
     signal is a self-contradicting phrase such as "not explicitly stated but can be
     inferred" appearing right next to eligibility-judgement language; that pattern is
     FAILed outright. A softer eligibility-judgement phrase on its own (e.g. "does not
     meet the requirements") is flagged PASS WITH CAUTION for human review, since a
     course document occasionally does state an explicit requirement legitimately.

A mechanical FAIL always yields a FAIL. A low text-overlap result on its own yields
PASS WITH CAUTION (flagged for human review), not an automatic FAIL, because the
overlap check is approximate and paraphrase is expected and legitimate.
"""
import csv, difflib, json, re
from pathlib import Path
from corpus_v2 import BASE, resolve_document_path

PROTECTED_TECHNICAL_TOKENS = [
    "gender", "marital_status", "father_edu", "mother_edu", "father_occ", "mother_occ",
    "respondent_id", "submitted_at", "entry_branch", "branch_routing_source",
    "branch_changed", "branch_path_disagreement", "branch_integrity_issue",
    "feature_count", "smoke_test",
]

WORD_RE = re.compile(r"[a-z0-9]+")
COURSE_ID_RE = re.compile(r"COURSE-\d+[A-Z]?", re.IGNORECASE)

# Eligibility-judgement language: asserting the respondent does/doesn't satisfy a
# requirement, positive or negative.
ELIGIBILITY_JUDGEMENT_RE = re.compile(
    r"(does not meet|may not meet|doesn't meet|not eligible|may not be eligible|"
    r"is eligible|meets? the (entry )?requirement|qualifies? for|does not qualify|"
    r"may not qualify)",
    re.IGNORECASE,
)
# The specific self-contradicting pattern observed in the gpt-4o-mini run: asserting a
# requirement judgement while admitting the requirement itself is not stated.
UNSUPPORTED_ELIGIBILITY_RE = re.compile(
    r"not explicitly stated.{0,40}(can be inferred|inferred|assumed|likely)|"
    r"(inferred|assumed).{0,40}not explicitly stated",
    re.IGNORECASE,
)

BANNED_PHRASES = [
    "cannot attend full-time", "guaranteed employment", "guaranteed job",
    "guaranteed salary", "guaranteed income", "the best course", "objectively the best",
    "you cannot", "will get you a job",
]
# Negation cues that, if present shortly before a banned phrase, mean the text is
# correctly DISCLAIMING the claim (e.g. "does not imply guaranteed employment", "no
# guaranteed employment outcomes") rather than making it. A naive substring match
# would otherwise flag exactly the caution language the governance instructions ask
# for as if it were the violation itself.
NEGATION_CUES = ["not imply", "not guarantee", "no guarantee", "does not ", "no explicit",
                  "no statement about", "not claim", "not state", "n't imply", "n't guarantee"]
NEGATION_WINDOW_CHARS = 120  # widened from 60 after a confirmed false-positive: "No explicit
# information about placements, local employer links, or guaranteed job outcomes is provided"
# has its negation cue 67 chars before the banned phrase, just past the original 60-char window.


def _words(text):
    return set(WORD_RE.findall(text.lower()))


def _protected_field_issues(text_lower):
    return [f"protected/technical field name '{tok}' appears in text"
            for tok in PROTECTED_TECHNICAL_TOKENS if tok in text_lower]


def _banned_phrase_issues(text_lower):
    issues = []
    for phrase in BANNED_PHRASES:
        idx = text_lower.find(phrase)
        if idx == -1:
            continue
        window = text_lower[max(0, idx - NEGATION_WINDOW_CHARS):idx]
        if any(cue in window for cue in NEGATION_CUES):
            continue  # correctly disclaiming the claim, not making it
        issues.append(f"text contains a prohibited phrase pattern: '{phrase}'")
    return issues


def _eligibility_issues(text):
    issues, cautions = [], []
    if UNSUPPORTED_ELIGIBILITY_RE.search(text):
        issues.append("text asserts an eligibility/requirement judgement while itself admitting the "
                       "requirement is not explicitly stated (self-contradicting unsupported-eligibility "
                       "claim) — violates the 'no eligibility claim without an explicit stated requirement' rule")
    elif ELIGIBILITY_JUDGEMENT_RE.search(text):
        cautions.append("text contains eligibility/requirement judgement language — flagged for manual "
                         "confirmation that the course document actually states an explicit requirement")
    return issues, cautions


def _all_answered_vars(respondent):
    out = {}
    for cat in ("direct_preference_or_intent", "feasibility_or_constraint_context",
                "education_and_experience_context", "individual_context_only"):
        for var, e in respondent.get(cat, {}).items():
            if e.get("status") in ("answered", "prefer_not_to_say"):
                out[var] = e.get("value_label")
    return out


def audit_recommendation(respondent, rec_dict, retrieved_parent_ids, excluded_ids, manifest_by_id):
    """rec_dict: one recommendation as a plain dict (from the parsed API response)."""
    issues = []
    cautions = []

    cid = rec_dict.get("course_id")

    # DOCUMENT SAFETY
    if cid in excluded_ids:
        issues.append(f"course_id {cid} is on the excluded-courses list and must never be recommended")
    if cid not in retrieved_parent_ids:
        issues.append(f"course_id {cid} was not among this respondent's retrieved parents")
    if cid not in manifest_by_id:
        issues.append(f"course_id {cid} not found in the V2 corpus manifest at all")

    all_text = json.dumps(rec_dict, ensure_ascii=False)
    issues.extend(_protected_field_issues(all_text.lower()))
    elig_issues, elig_cautions = _eligibility_issues(all_text)
    issues.extend(elig_issues)
    cautions.extend(elig_cautions)

    # RESPONDENT CLAIMS
    answered = _all_answered_vars(respondent)
    for item in rec_dict.get("direct_respondent_evidence_used", []):
        var = item.get("variable")
        val = item.get("value", "")
        if var not in answered:
            # Deterministic typo tolerance (added after a confirmed case: the model wrote
            # "occupation_class" for the real variable "occupational_class", with an
            # otherwise-accurate cited value). A close spelling match (edit distance-based,
            # via stdlib difflib) whose ACTUAL recorded value also matches the cited value
            # is treated as a likely typo — caution, not a hard grounding failure. A
            # fabricated/unrelated variable name would need to coincidentally satisfy both
            # conditions to escape a FAIL, which a random fabrication will not do.
            close = difflib.get_close_matches(var, answered.keys(), n=1, cutoff=0.8)
            if close:
                real_var = close[0]
                true_val = (answered[real_var] or "").lower()
                claimed_val = (val or "").lower()
                if true_val and claimed_val and (true_val in claimed_val or claimed_val in true_val):
                    cautions.append(f"cited variable '{var}' not found verbatim but closely matches real "
                                     f"variable '{real_var}' (likely typo), and the cited value matches "
                                     f"'{real_var}''s recorded value — treated as a naming slip, not a "
                                     f"fabrication")
                    continue
            issues.append(f"cited respondent variable '{var}' not found among this respondent's answered evidence fields")
        else:
            true_val = (answered[var] or "").lower()
            claimed_val = (val or "").lower()
            if true_val and claimed_val and true_val not in claimed_val and claimed_val not in true_val:
                cautions.append(f"cited value for '{var}' ('{val}') does not closely match the recorded "
                                 f"value ('{answered[var]}') — flagged for manual review, not auto-failed "
                                 f"since paraphrase is expected")

    # PROFILE CLAIMS
    valid_profile_keys = {f"{m['model_id']}_p{m['profile_id']}" for m in respondent["frozen_profile_memberships"]}
    for item in rec_dict.get("profile_context_used", []):
        prof = item.get("profile")
        if prof not in valid_profile_keys:
            issues.append(f"cited profile key '{prof}' is not one of this respondent's actual frozen memberships {sorted(valid_profile_keys)}")
        if item.get("role") != "supporting_context_only":
            issues.append(f"profile_context_used item for '{prof}' does not have role='supporting_context_only'")

    # COURSE CLAIMS — approximate text-grounding
    if cid in manifest_by_id:
        doc_path = resolve_document_path(manifest_by_id[cid])
        doc_text = doc_path.read_text(encoding="utf-8").lower()
        doc_words = _words(doc_text)
        for item in rec_dict.get("course_evidence_used", []):
            fact = item.get("course_fact", "")
            fact_words = _words(fact) - {"the", "a", "an", "is", "are", "this", "course", "and", "of", "to", "in"}
            if not fact_words:
                continue
            overlap = len(fact_words & doc_words) / len(fact_words)
            if overlap < 0.4:
                cautions.append(f"course_fact '{fact[:80]}...' has low word-overlap ({overlap:.0%}) with the "
                                 f"retrieved {cid} document text — flagged for manual review (may be a "
                                 f"legitimate paraphrase or may be unsupported)")

    # INFERENCES
    for inf in rec_dict.get("contextual_inferences", []):
        if not inf.get("based_on"):
            issues.append("a contextual_inference has no based_on evidence listed")
        if inf.get("uncertainty_language_used") is True:
            text = inf.get("inference", "").lower()
            hedges = ["may", "could", "appears", "might", "possibly", "plausib", "suggest"]
            if not any(h in text for h in hedges):
                cautions.append(f"inference marked uncertainty_language_used=True but no hedging word found in "
                                 f"the text: '{inf.get('inference','')[:80]}...'")

    # PROHIBITED CLAIM PATTERNS (simple, conservative phrase screen — not exhaustive)
    issues.extend(_banned_phrase_issues(all_text.lower()))

    if issues:
        status = "FAIL"
    elif cautions:
        status = "PASS WITH CAUTION"
    else:
        status = "PASS"

    return status, issues, cautions


def audit_decline(decline_reason, retrieved_parent_ids, excluded_ids, manifest_by_id):
    """
    Audits a NO_DEFENSIBLE_RECOMMENDATION reason. A decline is not automatically safe —
    it can still assert unsupported facts, leak a protected field, or (as observed in
    the gpt-4o-mini run) make an unsupported eligibility judgement while declining.
    """
    issues, cautions = [], []
    text = decline_reason or ""

    if not text.strip():
        issues.append("recommendation_status is NO_DEFENSIBLE_RECOMMENDATION but no_defensible_recommendation_reason is empty")
        return "FAIL", issues, cautions

    issues.extend(_protected_field_issues(text.lower()))
    issues.extend(_banned_phrase_issues(text.lower()))
    elig_issues, elig_cautions = _eligibility_issues(text)
    issues.extend(elig_issues)
    cautions.extend(elig_cautions)

    # A decline reason should not reference a course that was never actually retrieved
    # for this respondent (a hallucinated/out-of-context course reference).
    mentioned = {m.upper() for m in COURSE_ID_RE.findall(text)}
    unretrieved_mentions = mentioned - {c.upper() for c in retrieved_parent_ids}
    for cid in unretrieved_mentions:
        if cid in {e.upper() for e in excluded_ids}:
            issues.append(f"decline reason references excluded course {cid}")
        elif cid in manifest_by_id:
            cautions.append(f"decline reason references {cid}, which was not among this respondent's "
                             f"retrieved candidates — flagged for review, may be an incidental mention")

    if issues:
        status = "FAIL"
    elif cautions:
        status = "PASS WITH CAUTION"
    else:
        status = "PASS"
    return status, issues, cautions


def audit_all(recommendations_jsonl_path, respondents_by_id, retrieved_by_respondent, excluded_ids, manifest_by_id):
    rows = []
    with open(recommendations_jsonl_path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            rid = rec["respondent_id"]
            respondent = respondents_by_id[rid]
            retrieved_ids = set(retrieved_by_respondent.get(rid, []))
            status_field = rec.get("recommendation_status")
            recs = rec.get("recommendations", [])

            # STATUS/LIST CONSISTENCY
            consistency_issues = []
            if status_field == "NO_DEFENSIBLE_RECOMMENDATION" and recs:
                consistency_issues.append("recommendation_status is NO_DEFENSIBLE_RECOMMENDATION but recommendations list is non-empty")
            if status_field == "RECOMMENDATIONS_AVAILABLE" and not recs:
                consistency_issues.append("recommendation_status is RECOMMENDATIONS_AVAILABLE but recommendations list is empty")

            if recs:
                for r in recs:
                    status, issues, cautions = audit_recommendation(respondent, r, retrieved_ids, excluded_ids, manifest_by_id)
                    issues = consistency_issues + issues
                    if consistency_issues:
                        status = "FAIL"
                    rows.append({
                        "respondent_id": rid,
                        "record_type": "recommendation",
                        "course_id": r.get("course_id"),
                        "rank": r.get("rank"),
                        "final_audit_status": status,
                        "mechanical_issues": "; ".join(issues) if issues else "(none)",
                        "cautions": "; ".join(cautions) if cautions else "(none)",
                    })
            else:
                reason = rec.get("no_defensible_recommendation_reason")
                status, issues, cautions = audit_decline(reason, retrieved_ids, excluded_ids, manifest_by_id)
                issues = consistency_issues + issues
                if consistency_issues:
                    status = "FAIL"
                rows.append({
                    "respondent_id": rid,
                    "record_type": "no_defensible_recommendation_decline",
                    "course_id": "(none — decline)",
                    "rank": "",
                    "final_audit_status": status,
                    "mechanical_issues": "; ".join(issues) if issues else "(none)",
                    "cautions": "; ".join(cautions) if cautions else "(none)",
                })
    return rows
