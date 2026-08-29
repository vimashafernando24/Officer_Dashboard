"""
STEP 4 prototype — course corpus preparation.

Reads the already-validated, already-audited course documents and traceability file
(outputs/rag_course_knowledge/*) and builds:

  outputs/rag_recommendation_prototype/course_child_chunks.jsonl
  outputs/rag_recommendation_prototype/course_retrieval_index_metadata.csv

Only documents whose validation_status != NEEDS_MANUAL_REVIEW_DO_NOT_INDEX are chunked.
No frozen course-knowledge file is modified.
"""
import csv, json, os, re

BASE = "/Users/vimashafernando/Desktop/ClusterRP"
TRACE_CSV = f"{BASE}/outputs/rag_course_knowledge/course_source_traceability.csv"
VALIDATED_DIR = f"{BASE}/outputs/rag_course_knowledge/validated_documents"
OUT_DIR = f"{BASE}/outputs/rag_recommendation_prototype"
os.makedirs(OUT_DIR, exist_ok=True)

with open(TRACE_CSV, newline="", encoding="utf-8-sig") as f:
    trace_rows = list(csv.DictReader(f))

EXCLUDED_STATUS = "NEEDS_MANUAL_REVIEW_DO_NOT_INDEX"
safe_rows = [r for r in trace_rows if r["validation_status"] != EXCLUDED_STATUS]
excluded_rows = [r for r in trace_rows if r["validation_status"] == EXCLUDED_STATUS]

print(f"Validated course parents total: {len(trace_rows)}")
print(f"Excluded (NEEDS_MANUAL_REVIEW_DO_NOT_INDEX): {len(excluded_rows)}")
print(f"Safe to index: {len(safe_rows)}")

HEADER_FIELD_RE = re.compile(r"^([A-Z][A-Z /()_-]+):\s*(.*)$")

def parse_document(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    marker = "COMPLETE EXTRACTED COURSE TEXT"
    if marker not in text:
        return {}, text.strip()
    header_part, body_part = text.split(marker, 1)
    header = {}
    for line in header_part.splitlines():
        line = line.strip()
        if not line:
            continue
        m = HEADER_FIELD_RE.match(line)
        if m:
            header[m.group(1).strip()] = m.group(2).strip()
    body = body_part.strip()
    return header, body

def split_body_sections(body):
    """
    Structure-aware split, matching the pattern observed across the validated corpus:
    course name / LANGUAGE / MAX STUDENTS block -> 'Course Overview' -> numbered module
    list -> narrative paragraph(s). Falls back gracefully if the pattern is absent.
    Returns a dict of section_name -> text for sections that were reliably detected.
    """
    sections = {}
    lines = body.splitlines()

    overview_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().lower() == "course overview":
            overview_idx = i
            break

    if overview_idx is not None:
        identity_lines = lines[:overview_idx]
        if identity_lines:
            sections["identity_and_schedule_snippet"] = "\n".join(identity_lines).strip()

        rest = lines[overview_idx + 1:]
        numbered_re = re.compile(r"^\s*\d+\.")
        # The observed, consistent pattern across the corpus: a numbered module/overview
        # list immediately follows "Course Overview", and the narrative boilerplate
        # paragraph reliably begins with "The National Youth Service Council...".
        # Split at the first line starting with "The " once at least one numbered line
        # has already been seen; this is a conservative, structure-based rule, not an
        # arbitrary size cut.
        narrative_start = None
        seen_numbered = False
        for i, ln in enumerate(rest):
            if numbered_re.match(ln):
                seen_numbered = True
                continue
            if seen_numbered and ln.strip().startswith("The "):
                narrative_start = i
                break
        if narrative_start is not None:
            module_lines = rest[:narrative_start]
            narrative_lines = rest[narrative_start:]
        else:
            module_lines = rest if seen_numbered else []
            narrative_lines = [] if seen_numbered else rest

        module_text = "\n".join(module_lines).strip()
        if module_text:
            sections["modules_or_overview_list"] = module_text
        narrative = "\n".join(narrative_lines).strip()
        if narrative:
            sections["narrative_description"] = narrative
    return sections

chunk_records = []
index_rows = []

for row in safe_rows:
    doc_id = row["course_document_id"]
    course_name = row["course_name"]
    rel_path = row["validated_document_path"]
    abs_path = os.path.join(BASE, rel_path) if not os.path.isabs(rel_path) else rel_path
    if not os.path.exists(abs_path):
        # fall back to filename lookup inside validated_documents
        candidates = [p for p in os.listdir(VALIDATED_DIR) if p.startswith(doc_id.lower())]
        abs_path = os.path.join(VALIDATED_DIR, candidates[0]) if candidates else None
    if not abs_path or not os.path.exists(abs_path):
        print(f"WARNING: could not locate file for {doc_id}, skipping")
        continue

    header, body = parse_document(abs_path)
    source_screens = header.get("SOURCE SCREENSHOT FILENAME(S)", "")
    uncertainty_present = "[UNCLEAR]" in body
    uncertainty_count = body.count("[UNCLEAR]")

    # Child 1: always the whole validated body (safety-net retrieval unit)
    whole_id = f"{doc_id}::whole"
    chunk_records.append({
        "child_chunk_id": whole_id,
        "parent_course_id": doc_id,
        "course_name": course_name,
        "section": "whole_document",
        "text": body,
        "source_document": os.path.relpath(abs_path, BASE),
        "source_screenshots": source_screens,
        "uncertainty_flag": uncertainty_present,
    })

    # Additional section-aware children where the structural pattern is reliably found
    sections = split_body_sections(body)
    for sec_name, sec_text in sections.items():
        if not sec_text or len(sec_text) < 8:
            continue
        cid = f"{doc_id}::{sec_name}"
        chunk_records.append({
            "child_chunk_id": cid,
            "parent_course_id": doc_id,
            "course_name": course_name,
            "section": sec_name,
            "text": sec_text,
            "source_document": os.path.relpath(abs_path, BASE),
            "source_screenshots": source_screens,
            "uncertainty_flag": "[UNCLEAR]" in sec_text,
        })

    index_rows.append({
        "parent_course_id": doc_id,
        "course_name": course_name,
        "validation_status": row["validation_status"],
        "structured_crosscheck_course_id": row["structured_crosscheck_course_id"],
        "n_child_chunks": 1 + len(sections),
        "sections_detected": ";".join(sections.keys()) if sections else "(whole-document only)",
        "uncertainty_marker_count": uncertainty_count,
        "source_conflict": row["source_conflict"],
        "source_document": os.path.relpath(abs_path, BASE),
    })

CHUNKS_PATH = f"{OUT_DIR}/course_child_chunks.jsonl"
with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
    for c in chunk_records:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

INDEX_PATH = f"{OUT_DIR}/course_retrieval_index_metadata.csv"
with open(INDEX_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["parent_course_id", "course_name", "validation_status",
                                       "structured_crosscheck_course_id", "n_child_chunks",
                                       "sections_detected", "uncertainty_marker_count",
                                       "source_conflict", "source_document"])
    w.writeheader()
    for r in index_rows:
        w.writerow(r)

print(f"Wrote {len(chunk_records)} child chunks for {len(index_rows)} indexable parents -> {CHUNKS_PATH}")
print(f"Wrote index metadata -> {INDEX_PATH}")

with_sections = sum(1 for r in index_rows if r["n_child_chunks"] > 1)
print(f"Parents with detected section-aware children beyond whole-document: {with_sections}")
