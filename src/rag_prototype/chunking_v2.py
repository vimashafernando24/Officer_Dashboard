"""
Section-aware parent-child chunking for the V2 course corpus (84 indexable parents).

Same structural strategy validated in the previous prototype (see
outputs/rag_course_knowledge/rag_chunking_strategy.md): every parent gets a
whole_document child; where the corpus's consistent
"Course Overview -> numbered list -> narrative" structure is detected, additional
section-aware children are also produced. No chunk is created for an excluded course
— chunking only ever runs over corpus_v2.verify_corpus()'s returned manifest rows.
"""
import json, re
from pathlib import Path
from corpus_v2 import verify_corpus, resolve_document_path, BASE

HEADER_FIELD_RE = re.compile(r"^([A-Z][A-Z /()_-]+):\s*(.*)$")
MARKER = "COMPLETE EXTRACTED COURSE TEXT"


def parse_document(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARKER not in text:
        return {}, text.strip()
    header_part, body_part = text.split(MARKER, 1)
    header = {}
    for line in header_part.splitlines():
        line = line.strip()
        if not line:
            continue
        m = HEADER_FIELD_RE.match(line)
        if m:
            header[m.group(1).strip()] = m.group(2).strip()
    return header, body_part.strip()


def split_body_sections(body: str):
    sections = {}
    lines = body.splitlines()
    overview_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().lower() == "course overview":
            overview_idx = i
            break
    if overview_idx is None:
        return sections

    identity_lines = lines[:overview_idx]
    if identity_lines:
        sections["identity_and_schedule_snippet"] = "\n".join(identity_lines).strip()

    rest = lines[overview_idx + 1:]
    numbered_re = re.compile(r"^\s*\d+\.")
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


def build_chunks_and_index():
    manifest, _exclusions = verify_corpus(verbose=False)
    chunk_records = []
    index_rows = []

    for row in manifest:
        doc_id = row["course_id"]
        course_name = row["course_name"]
        abs_path = resolve_document_path(row)
        header, body = parse_document(abs_path)
        source_screens = header.get("SOURCE SCREENSHOT FILENAME(S)", "")
        uncertainty_present = "[UNCLEAR]" in body
        uncertainty_count = body.count("[UNCLEAR]")

        whole_id = f"{doc_id}::whole"
        chunk_records.append({
            "child_chunk_id": whole_id,
            "parent_course_id": doc_id,
            "course_name": course_name,
            "section": "whole_document",
            "text": body,
            "source_document": str(abs_path.relative_to(BASE)),
            "source_screenshots": source_screens,
            "uncertainty_flag": uncertainty_present,
        })

        sections = split_body_sections(body)
        for sec_name, sec_text in sections.items():
            if not sec_text or len(sec_text) < 8:
                continue
            chunk_records.append({
                "child_chunk_id": f"{doc_id}::{sec_name}",
                "parent_course_id": doc_id,
                "course_name": course_name,
                "section": sec_name,
                "text": sec_text,
                "source_document": str(abs_path.relative_to(BASE)),
                "source_screenshots": source_screens,
                "uncertainty_flag": "[UNCLEAR]" in sec_text,
            })

        index_rows.append({
            "parent_course_id": doc_id,
            "course_name": course_name,
            "review_status": row["review_status"],
            "rag_indexable": row["rag_indexable"],
            "n_child_chunks": 1 + len(sections),
            "sections_detected": ";".join(sections.keys()) if sections else "(whole-document only)",
            "uncertainty_marker_count": uncertainty_count,
            "document_sha256": row["document_sha256"],
            "source_document": str(abs_path.relative_to(BASE)),
        })

    return chunk_records, index_rows


if __name__ == "__main__":
    chunks, index_rows = build_chunks_and_index()
    out_dir = BASE / "outputs/rag_recommendation_prototype_api"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "v2_course_child_chunks.jsonl", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    import csv
    with open(out_dir / "v2_course_retrieval_index_metadata.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(index_rows[0].keys()))
        w.writeheader()
        for r in index_rows:
            w.writerow(r)

    print(f"Wrote {len(chunks)} child chunks for {len(index_rows)} indexable parents.")
    with_sections = sum(1 for r in index_rows if r["n_child_chunks"] > 1)
    print(f"Parents with section-aware children beyond whole-document: {with_sections}")
