"""
Assemble, for each of the 10 selected respondents, a clearly-sectioned context pack
(direct respondent facts / group-level profile context / retrieved full course
documents) for the LLM reasoning stage. Writes one .txt per respondent under
outputs/rag_recommendation_prototype/_context_packs/ for direct reading, plus keeps
provenance so every claim can later be checked against source files.
"""
import csv, json, os

BASE = "/Users/vimashafernando/Desktop/ClusterRP"
OUT_DIR = f"{BASE}/outputs/rag_recommendation_prototype"
PACK_DIR = f"{OUT_DIR}/_context_packs"
os.makedirs(PACK_DIR, exist_ok=True)

EVIDENCE_JSONL = f"{BASE}/outputs/rag_respondent_evidence/respondent_evidence.jsonl"
PROFILE_INDEX_CSV = f"{BASE}/outputs/rag_profile_knowledge/profile_document_index.csv"
VALIDATED_DIR = f"{BASE}/outputs/rag_course_knowledge/validated_documents"
TRACE_CSV = f"{BASE}/outputs/rag_course_knowledge/course_source_traceability.csv"

with open(EVIDENCE_JSONL, encoding="utf-8") as f:
    respondents = {json.loads(l)["respondent_id"]: json.loads(l) for l in f}

with open(PROFILE_INDEX_CSV, newline="", encoding="utf-8-sig") as f:
    profile_index = {r["profile_key"]: r for r in csv.DictReader(f)}

with open(TRACE_CSV, newline="", encoding="utf-8-sig") as f:
    trace_by_id = {r["course_document_id"]: r for r in csv.DictReader(f)}

with open(f"{OUT_DIR}/_respondent_bundle.json", encoding="utf-8") as f:
    bundle = json.load(f)

CAT_LABELS = {
    "direct_preference_or_intent": "DIRECT PREFERENCE / INTENT (respondent explicitly stated what they want)",
    "feasibility_or_constraint_context": "FEASIBILITY / CONSTRAINT CONTEXT (respondent explicitly reported a circumstance)",
    "education_and_experience_context": "EDUCATION AND EXPERIENCE CONTEXT (actual background)",
    "individual_context_only": "INDIVIDUAL CONTEXT ONLY (explanation-supporting, must not independently drive ranking)",
}

def format_evidence_section(rec):
    lines = []
    for cat, label in CAT_LABELS.items():
        lines.append(f"--- {label} ---")
        entries = rec.get(cat, {})
        any_answered = False
        for var, e in entries.items():
            if e.get("status") == "answered":
                lines.append(f"  {var}: {e.get('value_label')}")
                any_answered = True
            elif e.get("status") == "prefer_not_to_say":
                lines.append(f"  {var}: [respondent selected 'Prefer not to say']")
                any_answered = True
        if not any_answered:
            lines.append("  (no answered fields in this category for this respondent)")
        lines.append("")
    return "\n".join(lines)

def load_profile_doc(profile_key):
    row = profile_index.get(profile_key)
    if not row:
        return f"[ERROR: profile document not found for key {profile_key}]"
    path = os.path.join(BASE, row["document_path"])
    with open(path, encoding="utf-8") as f:
        return f.read()

def load_course_doc(course_id):
    row = trace_by_id.get(course_id)
    if not row:
        return f"[ERROR: course {course_id} not found in traceability file]"
    path = os.path.join(BASE, row["validated_document_path"])
    with open(path, encoding="utf-8") as f:
        return f.read()

for rid, rec in respondents.items():
    if rid not in bundle:
        continue
    b = bundle[rid]
    parts = []
    parts.append("=" * 100)
    parts.append(f"CONTEXT PACK FOR RESPONDENT {rid}  (branch {rec['branch']})")
    parts.append("=" * 100)
    parts.append("")
    parts.append("SECTION 1: DIRECT RESPONDENT FACTS")
    parts.append("(Source: outputs/rag_respondent_evidence/respondent_evidence.jsonl — protected/proxy and")
    parts.append(" technical fields already excluded upstream. 'answered' fields only; anything not listed")
    parts.append(" was missing, structurally not applicable, or routing-conditional in the source record —")
    parts.append(" it must NOT be treated as a 'No'.)")
    parts.append("")
    parts.append(format_evidence_section(rec))

    parts.append("SECTION 2: GROUP-LEVEL PROFILE CONTEXT — NOT INDIVIDUAL FACT")
    parts.append("(These documents describe the RESEARCH PROFILE(S) this respondent was statistically")
    parts.append(" assigned to, based on frozen clustering of OTHER survey questions. Every percentage or")
    parts.append(" tendency below describes the GROUP, not this individual. If a group tendency conflicts")
    parts.append(" with this respondent's own Section 1 answer, the Section 1 answer always takes priority.)")
    parts.append("")
    for m in rec["frozen_profile_memberships"]:
        key = f"{m['model_id']}_p{m['profile_id']}"
        parts.append(f"------ PROFILE DOCUMENT: {key} ({m['retained_dimension']}) ------")
        parts.append(load_profile_doc(key))
        parts.append("")

    parts.append("SECTION 3: RETRIEVED FULL NYSC COURSE DOCUMENTS")
    parts.append("(Source: outputs/rag_course_knowledge/validated_documents/ — retrieved via BM25 lexical")
    parts.append(" search over section-aware child chunks, deduplicated to parent course. RETRIEVAL RANK/")
    parts.append(" SCORE IS NOT SUITABILITY — some retrieved courses may be lexically matched but not")
    parts.append(" actually relevant; judge each on its full text below, not on its rank.)")
    parts.append("")
    for rank, cid in enumerate(b["retrieved_parents_ranked"], start=1):
        score = b["retrieved_parent_scores"][cid]
        parts.append(f"------ RANK {rank} (BM25 score {score}): {cid} ------")
        parts.append(load_course_doc(cid))
        parts.append("")

    parts.append("SECTION 4: RECOMMENDATION INSTRUCTIONS")
    parts.append("Considering the respondent's actual reported circumstances, preferences, education/work/")
    parts.append("training history, future intentions and barriers (Section 1); their group-level research")
    parts.append("profile context (Section 2); and the complete available information about the retrieved")
    parts.append("NYSC programmes (Section 3), identify the programmes that appear most suitable for this")
    parts.append("respondent. Reason holistically. Make reasonable contextual inferences where justified, but")
    parts.append("label them as inferences and connect each to both a real respondent/context fact and a real")
    parts.append("documented course property. Do not invent respondent or programme information. Return up to")
    parts.append("~3-5 recommendations where evidence supports them; return fewer, or NO_DEFENSIBLE_")
    parts.append("RECOMMENDATION with reasons, if the evidence does not support more.")

    with open(f"{PACK_DIR}/{rid}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

print(f"Wrote {len(bundle)} context packs to {PACK_DIR}")
