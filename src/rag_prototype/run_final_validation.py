"""
FINAL targeted reasoning-refinement validation (Section 10-14 of the task).

Unchanged: gpt-5-mini (hardcoded below, NOT read from .env — .env's
OPENAI_RECOMMENDATION_MODEL was found changed to gpt-4o-mini on disk during this task,
which is NOT what was requested; this script hardcodes the model to guarantee the
correct one is used regardless of .env state), the 84-course V2 corpus, BM25 retrieval
(retrieval is REUSED byte-for-byte from the already-saved 30-person batch — not
recomputed), frozen clustering/profile assignments, respondent evidence source, and the
two existing audits (run unchanged, in addition to the new evidence-hierarchy audit).

Changed: the governance prompt (context_pack_v2.py — evidence hierarchy, profile-context
discipline, available_to_start fix, economic-affordability fix, occupation-as-preference
fix, DIRECT_MATCH/ADJACENT_MATCH classification) and the recommendation schema (added
match_relationship, adjacent_match_bridge_explanation, catalogue_coverage_note).

Sample: 10 respondents, ALL drawn from the existing 30-person validation batch (no new
respondents), selected because their "before" (30-batch) output demonstrates one of the
specific patterns this refinement targets.

Auditability improvement (Section 13): for every call, saves a full snapshot —
constructed input text, a hash of the governance instructions actually used, model name,
respondent ID, retrieved course IDs, profile document references, course corpus
manifest hash, and token usage — sufficient to reproduce exactly what the model saw
without relying on deterministic reconstruction from separately-frozen files.
"""
import csv, hashlib, json, sys, functools
from pathlib import Path

print = functools.partial(print, flush=True)

from env_config import has_api_key, describe_key_status
from corpus_v2 import verify_corpus, BASE
import context_pack_v2

MODEL = "gpt-5-mini"  # HARDCODED — see module docstring. Do not read from .env for this run.

OLD_BATCH_JSONL = BASE / "outputs/rag_recommendation_validation_30/api_recommendations_30.jsonl"
RESPONDENT_EVIDENCE_JSONL = BASE / "outputs/rag_respondent_evidence/respondent_evidence.jsonl"
OUT_DIR = BASE / "outputs/rag_recommendation_final_validation"

# ---------------------------------------------------------------------------
# 10 respondents, all from the existing 30-person batch, each selected for a
# specific targeted-refinement reason (documented here for the report).
# ---------------------------------------------------------------------------
TARGETED_10 = [
    ("nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88", "D",
     "Strong direct match control case (Manufacturing/production) — confirm the refinement "
     "did not weaken clean, well-grounded direct matches."),
    ("nysc-4e38db03-e477-420e-9afd-d3f92b53995d", "D",
     "Education/Science -> adjacent-match test + catalogue-gap test. Was NO_DEFENSIBLE_RECOMMENDATION "
     "before (Health/social-work/wellbeing has no catalogue match); tests whether ADJACENT_MATCH now "
     "surfaces a defensible STEM-adjacent option instead, or correctly still declines."),
    ("nysc-0cba8a68-ebf6-47cb-bd45-e2a1d78ad74b", "D",
     "Useful profile-context reasoning + individual-diverges-from-profile-tendency. In "
     "D_motivation profile 1 ('externally or uncertainly motivated'), yet has clear, specific, "
     "goal-directed direct preferences — a genuine divergence from the profile's own framing."),
    ("nysc-25c345ec-5f45-4616-adb8-c96e31f3511c", "D",
     "Profile-context differentiation test on a deliberately complex/conflicting case (has "
     "children, never studied, ambivalent 'stay at home' intent, yet states a sector preference); "
     "'before' already showed good hedged reasoning — confirms it still does."),
    ("nysc-4646cb19-0ac0-49ca-a00b-e2d8cb16b65e", "F",
     "CONFIRMED occupation-as-preference overreach in the 'before' output: ideal_sector = 'Not "
     "sure', yet ALL THREE prior recommendations were primarily justified by current "
     "occupational_class ('Clerical or office work') alone."),
    ("nysc-04134b0d-f3fe-4a25-916c-ee106362e150", "F",
     "Second occupation + weak-preference case (professional occupational_class, sector 'Not "
     "sure'); was NO_DEFENSIBLE_RECOMMENDATION before — confirms correct behaviour is preserved "
     "under the new rules, not just avoided in the confirmed-overreach case above."),
    ("nysc-3258dc18-84da-4092-82af-cfb84352536e", "E",
     "CONFIRMED available_to_start misuse in the 'before' output: cited as \"Indicates readiness "
     "to undertake training\" — the exact job-start-vs-training-availability conflation this "
     "refinement targets."),
    ("nysc-8ae4a1d8-97c7-4bc4-9dc9-cb7eea0c897f", "D",
     "CONFIRMED economic-profile/affordability overreach in the 'before' output: a "
     "D_economic_p2 ('relatively higher household economic position') profile citation stated "
     "this 'may indicate capacity to pursue part-time, fee-paying training if desired.'"),
    ("nysc-5242257e-4708-442a-a41f-1081109194a9", "G",
     "Genuine NO_DEFENSIBLE_RECOMMENDATION control case (sector 'Not sure', does not wish to "
     "work) — confirms the refinement has not reintroduced excessive recommending."),
    ("nysc-27c2ff48-e39c-4db3-aa11-a149d76be479", "G",
     "Additional profile-context usage example on a G respondent (economic_role_p2, caregiving + "
     "shared provider) for branch/profile diversity beyond the D/F-heavy targeted cases above."),
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_respondents():
    out = {}
    with open(RESPONDENT_EVIDENCE_JSONL, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            out[rec["respondent_id"]] = rec
    return out


def load_before_retrieval_and_recs():
    """Pulls each targeted respondent's SAVED retrieval (reused, not recomputed) and
    their 'before' recommendation record from the 30-person batch."""
    before = {}
    with open(OLD_BATCH_JSONL, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec["respondent_id"] in {rid for rid, _, _ in TARGETED_10}:
                before[rec["respondent_id"]] = rec
    return before


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "call_snapshots").mkdir(exist_ok=True)

    print("Step 1: verifying V2 corpus is unchanged (84 indexable + 4 excluded = 88)...")
    manifest, exclusions = verify_corpus(verbose=True)
    manifest_by_id = {r["course_id"]: r for r in manifest}
    excluded_ids = {r["course_id"] for r in exclusions}
    corpus_manifest_hash = sha256_text(json.dumps(manifest, sort_keys=True))

    print("Step 2: loading SAVED retrieval + 'before' recommendations from the 30-person batch "
          "(retrieval reused byte-for-byte, not recomputed)...")
    before = load_before_retrieval_and_recs()
    missing = [rid for rid, _, _ in TARGETED_10 if rid not in before]
    if missing:
        raise SystemExit(f"Respondents not found in the 30-person batch (must all be reused, not new): {missing}")
    print(f"  Loaded 'before' data for {len(before)} respondents.")

    print(f"Step 3: checking OPENAI_API_KEY... {describe_key_status()}")
    if not has_api_key():
        print("OPENAI_API_KEY REQUIRED BEFORE EXECUTION")
        return 2

    instructions_hash = sha256_text(context_pack_v2.GOVERNANCE_INSTRUCTIONS)
    print(f"Governance instructions hash (this run): {instructions_hash[:16]}...")

    print(f"Step 4: calling OpenAI API (model={MODEL}, refined prompt+schema) for {len(TARGETED_10)} respondents...")
    from openai_client import call_recommendation_api
    from recommendation_schema import RespondentRecommendationResponse
    respondents = load_respondents()
    profile_index = context_pack_v2.load_profile_index()

    usage_rows, after_records = [], []
    for i, (rid, branch, reason) in enumerate(TARGETED_10, start=1):
        print(f"  [{i}/{len(TARGETED_10)}] calling for {rid} ({branch})...")
        respondent = respondents[rid]
        b = before[rid]["retrieval"]
        retrieved_ids = b["retrieved_course_ids"]
        retrieved_scores = b["retrieval_scores"]

        input_text = context_pack_v2.build_input_text(
            respondent, retrieved_ids, retrieved_scores, manifest_by_id, profile_index,
        )
        result = call_recommendation_api(rid, input_text, model=MODEL)

        usage_rows.append({
            "respondent_id": rid, "model": result.model, "success": result.success,
            "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
            "total_tokens": result.total_tokens, "cached_input_tokens": result.cached_input_tokens,
            "reasoning_tokens": result.reasoning_tokens, "duration_seconds": result.duration_seconds,
            "retry_count": result.retry_count, "response_id": result.response_id,
            "error_message": result.error_message,
        })

        # Auditability snapshot (Section 13) — saved regardless of success/failure.
        profile_doc_refs = [f"{m['model_id']}_p{m['profile_id']}" for m in respondent["frozen_profile_memberships"]]
        snapshot = {
            "respondent_id": rid,
            "model": MODEL,
            "governance_instructions_sha256": instructions_hash,
            "constructed_input_text": input_text,
            "retrieved_course_ids": retrieved_ids,
            "retrieved_course_scores": retrieved_scores,
            "profile_document_refs": profile_doc_refs,
            "course_corpus_manifest_sha256": corpus_manifest_hash,
            "response_id": result.response_id,
            "token_usage": {
                "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
                "total_tokens": result.total_tokens, "cached_input_tokens": result.cached_input_tokens,
                "reasoning_tokens": result.reasoning_tokens,
            },
            "success": result.success,
            "error_message": result.error_message,
        }
        with open(OUT_DIR / "call_snapshots" / f"{rid}.json", "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        if result.success:
            parsed: RespondentRecommendationResponse = result.parsed
            after_records.append({
                "respondent_id": rid, "branch": branch,
                "selection_reason": reason,
                "profile_memberships": respondent["frozen_profile_memberships"],
                "retrieval": {"retrieved_course_ids": retrieved_ids, "retrieval_scores": retrieved_scores},
                "recommendation_status": parsed.recommendation_status,
                "catalogue_coverage_note": parsed.catalogue_coverage_note,
                "recommendations": [r.model_dump() for r in parsed.recommendations],
                "no_defensible_recommendation_reason": parsed.no_defensible_recommendation_reason,
            })
            print(f"  {rid}: OK ({parsed.recommendation_status}, {len(parsed.recommendations)} recs, "
                  f"{result.total_tokens} tokens)")
        else:
            print(f"  {rid}: FAILED after {result.retry_count} retries — {result.error_message}")

        with open(OUT_DIR / "api_recommendations_final.jsonl", "w", encoding="utf-8") as f:
            for r in after_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        write_csv(OUT_DIR / "api_usage_final.csv", usage_rows)

    print("Step 5: running BOTH existing audits (unchanged) plus the NEW evidence-hierarchy audit...")
    from grounding_audit_v2 import audit_all as grounding_audit_all
    retrieved_by_respondent = {rid: before[rid]["retrieval"]["retrieved_course_ids"] for rid, _, _ in TARGETED_10}
    grounding_rows = grounding_audit_all(OUT_DIR / "api_recommendations_final.jsonl", respondents,
                                          retrieved_by_respondent, excluded_ids, manifest_by_id)
    write_csv(OUT_DIR / "grounding_audit_final.csv", grounding_rows)

    from evidence_category_discipline_audit import load_policy, audit_recommendations, audit_declines
    policy = load_policy()
    cat_rows = audit_recommendations(OUT_DIR / "api_recommendations_final.jsonl", policy, "gpt-5-mini-final")
    cat_rows += audit_declines(OUT_DIR / "api_recommendations_final.jsonl", policy, respondents, "gpt-5-mini-final")
    write_csv(OUT_DIR / "evidence_category_audit_final.csv", cat_rows)

    import evidence_hierarchy_audit as eha
    hierarchy_rows = eha.audit_all(OUT_DIR / "api_recommendations_final.jsonl", policy)
    write_csv(OUT_DIR / "evidence_hierarchy_audit_final.csv", hierarchy_rows)

    from collections import Counter
    print(f"  Grounding audit: {dict(Counter(r['final_audit_status'] for r in grounding_rows))}")
    print(f"  Category-discipline audit: {dict(Counter(r['status'] for r in cat_rows))}")
    print(f"  Evidence-hierarchy audit: {dict(Counter(r['status'] for r in hierarchy_rows))}")

    n_success = sum(1 for r in usage_rows if r["success"])
    print()
    print(f"Done. {n_success}/{len(usage_rows)} API calls succeeded with model={MODEL}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
