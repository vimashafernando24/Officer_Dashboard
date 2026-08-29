"""
BM25 retrieval over the V2 (84-parent) course corpus, for the SAME 10 respondents
used in the previous (manual-reasoning) prototype. Reuses the dependency-free BM25
implementation and query-construction approach validated in that prototype — retrieval
architecture is kept unchanged per the task instructions; only the underlying corpus
(79 -> 84 parents) is new.
"""
import csv, json
from pathlib import Path
from bm25 import BM25
from corpus_v2 import BASE

RESPONDENT_EVIDENCE_JSONL = BASE / "outputs/rag_respondent_evidence/respondent_evidence.jsonl"
MATCHING_CSV = BASE / "outputs/nysc_course_matching_dataset.csv"
API_OUT_DIR = BASE / "outputs/rag_recommendation_prototype_api"

# ---------------------------------------------------------------------------
# SAME 10 respondents as the previous (manual-reasoning) prototype — identical
# IDs, branches, and case-type tags, preserved verbatim for direct comparison.
# ---------------------------------------------------------------------------
SAMPLE = [
    ("nysc-acaf63b5-6e8f-45fb-9d5a-cef8d615799b", "D", "CASE2 (provider+care responsibility, clear field preference)"),
    ("nysc-3a86d117-1b8c-4f8d-8d53-d6765b4a4034", "D", "CASE1 (strong direct ICT field preference, provider, no children)"),
    ("nysc-a04f7d96-0e1d-49f2-8443-5cb15eeb9bf9", "D", "CASE6 (weak/unsure direct preference evidence)"),
    ("nysc-131a2b60-1a70-4974-9dc0-8a1eaf51befd", "E", "CASE1+CASE3 (strong ICT preference + training-availability barrier)"),
    ("nysc-346623df-699b-4abb-a445-51abb3f16cc5", "F", "CASE3 (employment insecurity + job-change intent + skills barrier)"),
    ("nysc-0c6c34a2-a528-4c97-b06b-3b712f4ff24d", "F", "CASE4 (secure employment, prior training/experience to build on, non-ICT sector)"),
    ("nysc-33aaf2f7-dc2a-4530-ae73-3bfdf5be63ab", "F", "CASE3 (insecure, self-employed, overqualification + training-access barrier)"),
    ("nysc-00e2c251-39ad-4474-b077-2a2bbe78457a", "G", "CASE5 (dual G profile membership, construction interest, employment barrier)"),
    ("nysc-465701ee-3d2d-4f85-a044-abff06ba2e45", "G", "CASE6+CASE5 (weak preference, dual G membership, care/home-duties context)"),
    ("nysc-55bdfdcc-30fd-4115-9e2a-4620cde38963", "G", "CASE2+CASE4 (provider+care, dual G membership, hospitality interest + prior work experience)"),
]

SECTOR_BRIDGE = {
    "information technology and communications": ["ICT & Computing"],
    "manufacturing or production": ["Automotive & Mechanical Engineering", "Electrical & Electronics"],
    "agriculture, forestry, and fishing": ["Agriculture & Environment"],
    "personal services (beauty, fitness, wellness)": ["Beauty, Fashion & Personal Care"],
    "hotels, restaurants, and hospitality": ["Hospitality & Culinary Arts"],
    "construction and building": ["Construction & Surveying"],
    "creative, media, and arts": ["Creative Arts, Design & Media"],
    "transport, storage, and logistics": ["Automotive & Mechanical Engineering"],
    "wholesale, retail, or repair": ["Business, Management & Administration"],
    "finance, banking, and insurance": ["Business, Management & Administration"],
    "education and teaching": ["Languages & Communication"],
}

QUERY_VARS_PRIORITY_1 = [
    "ideal_sector", "study_field_preference", "job_type_sought", "ideal_work_type",
    "training_type_would_help", "expected_highest_edu_d", "expected_highest_edu_e",
    "expected_highest_edu_f", "expected_highest_edu_g", "plans_after_education",
    "desire_for_work", "job_acceptance_conditions", "reason_wants_to_change",
]
QUERY_VARS_PRIORITY_2 = [
    "main_obstacle_finding_work", "obstacle_finding_this_job", "reason_not_in_labour_force",
    "main_business_obstacle", "current_activity_status", "employment_status",
    "occupational_class", "qualification_job_match", "worked_while_studying",
    "work_while_study_type", "received_training", "training_type_received",
    "highest_edu_completed", "edu_status",
]


def extract_answer(rec, var):
    for cat in ("direct_preference_or_intent", "feasibility_or_constraint_context",
                "education_and_experience_context", "individual_context_only"):
        e = rec.get(cat, {}).get(var)
        if e and e.get("status") == "answered":
            return e.get("value_label")
    return None


def load_respondents():
    out = {}
    with open(RESPONDENT_EVIDENCE_JSONL, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            out[rec["respondent_id"]] = rec
    return out


def load_skill_area_keywords():
    with open(MATCHING_CSV, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    kw = {}
    for r in rows:
        if r["skill_keywords"].strip():
            try:
                terms = json.loads(r["skill_keywords"])
            except Exception:
                terms = []
            kw.setdefault(r["skill_area"], set()).update(terms)
    return kw


def expansion_terms_for_sector(ideal_sector, skill_area_keywords):
    if not ideal_sector:
        return []
    areas = SECTOR_BRIDGE.get(ideal_sector.strip().lower(), [])
    terms = set()
    for area in areas:
        terms.update(skill_area_keywords.get(area, set()))
    return sorted(terms)


def build_query(rec, skill_area_keywords):
    parts_p1, parts_p2, used = [], [], {}
    for v in QUERY_VARS_PRIORITY_1:
        val = extract_answer(rec, v)
        if val and val.lower() not in ("not sure", "not sure yet", "no", "yes"):
            parts_p1.append(val)
            used[v] = val
    for v in QUERY_VARS_PRIORITY_2:
        val = extract_answer(rec, v)
        if val and val.lower() not in ("no", "yes"):
            parts_p2.append(val)
            used[v] = val
    expansion = expansion_terms_for_sector(extract_answer(rec, "ideal_sector"), skill_area_keywords)
    query_text = " ".join(parts_p1 * 3 + parts_p2 + expansion)
    summary = "; ".join(f"{k}={v}" for k, v in used.items())
    if expansion:
        summary += f"; [sector-vocabulary expansion terms: {', '.join(expansion)}]"
    return query_text, summary


TARGET_PARENTS_MAX = 15
TOP_K_CHUNKS = 60


def retrieve_parents(bm25, chunks, query_text):
    scores = bm25.score(query_text)
    ranked = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)
    seen_parents = {}
    ordered_hits = []
    for idx in ranked:
        if scores[idx] <= 0:
            break
        c = chunks[idx]
        pid = c["parent_course_id"]
        is_new = pid not in seen_parents
        if is_new and len(seen_parents) >= TARGET_PARENTS_MAX:
            continue
        ordered_hits.append((c["child_chunk_id"], pid, c["course_name"], c["section"], scores[idx]))
        if is_new:
            seen_parents[pid] = scores[idx]
        if len(ordered_hits) >= TOP_K_CHUNKS:
            break
    return ordered_hits, seen_parents


def run(chunks):
    respondents = load_respondents()
    skill_area_keywords = load_skill_area_keywords()
    bm25 = BM25([c["text"] for c in chunks])

    sample_rows, retrieval_audit_rows = [], []
    bundle = {}

    for rid, branch, case_tag in SAMPLE:
        rec = respondents[rid]
        assert rec["branch"] == branch, f"{rid} branch mismatch: expected {branch}, got {rec['branch']}"
        query_text, query_summary = build_query(rec, skill_area_keywords)
        chunk_hits, parent_scores = retrieve_parents(bm25, chunks, query_text)
        ranked_parents = sorted(parent_scores.items(), key=lambda kv: kv[1], reverse=True)

        sample_rows.append({
            "respondent_id": rid,
            "branch": branch,
            "case_type_rationale": case_tag,
            "n_profile_memberships": len(rec["frozen_profile_memberships"]),
            "profile_memberships": ";".join(f"{m['model_id']}:p{m['profile_id']}" for m in rec["frozen_profile_memberships"]),
            "n_retrieved_parents_v2": len(ranked_parents),
        })

        for rank, (chunk_id, pid, cname, section, score) in enumerate(chunk_hits, start=1):
            retrieval_audit_rows.append({
                "respondent_id": rid, "chunk_rank": rank, "child_chunk_id": chunk_id,
                "parent_course_id": pid, "course_name": cname, "section": section,
                "bm25_score": round(score, 4),
            })

        bundle[rid] = {
            "query_text": query_text,
            "query_summary": query_summary,
            "retrieved_parents_ranked": [pid for pid, _ in ranked_parents],
            "retrieved_parent_scores": {pid: round(s, 4) for pid, s in ranked_parents},
        }

    return sample_rows, retrieval_audit_rows, bundle


if __name__ == "__main__":
    from chunking_v2 import build_chunks_and_index
    chunks, _ = build_chunks_and_index()
    sample_rows, retrieval_audit_rows, bundle = run(chunks)

    API_OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(API_OUT_DIR / "test_sample.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sample_rows[0].keys()))
        w.writeheader()
        for r in sample_rows:
            w.writerow(r)

    with open(API_OUT_DIR / "v2_retrieval_audit.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(retrieval_audit_rows[0].keys()))
        w.writeheader()
        for r in retrieval_audit_rows:
            w.writerow(r)

    with open(API_OUT_DIR / "_v2_respondent_bundle.json", "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    print(f"Wrote test_sample.csv, v2_retrieval_audit.csv, _v2_respondent_bundle.json for {len(SAMPLE)} respondents.")
    for rid, branch, _ in SAMPLE:
        print(f"  {rid} ({branch}): {len(bundle[rid]['retrieved_parents_ranked'])} parents retrieved")
