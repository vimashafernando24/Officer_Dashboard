"""
§2 — Consolidate course-matching knowledge for the NEW-person recommendation
architecture.

Builds a structured matching layer over the validated 84-course RAG corpus
(corpus_v2, unchanged, authoritative). This is a retrieval/scoring AID only:
- The full validated parent document remains the authoritative course text
  for any factual claim (used verbatim in Section 3 of the LLM input).
- Structured fields here are sourced from outputs/nysc_course_matching_dataset.csv
  via the existing crosswalk (course_source_traceability.csv), never invented.
- Every row keeps its rag_course_id so provenance back to the original
  document is always traceable.
- Missing/unavailable structured info is represented explicitly as
  "NOT_STATED", never silently defaulted or guessed.

Does not modify final_rag_corpus_v2/, its manifest, or
nysc_course_matching_dataset.csv. Writes new, additive output only.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_v2 import verify_corpus, BASE

OUT_DIR = BASE / "outputs/rag_new_person_intake_v1"
MATCHING_CSV = BASE / "outputs/nysc_course_matching_dataset.csv"
TRACEABILITY_CSV = BASE / "outputs/rag_course_knowledge/course_source_traceability.csv"

NOT_STATED = "NOT_STATED"

STRUCTURED_FIELDS = [
    "skill_area", "attendance_type", "attendance_days", "duration_months",
    "instruction_languages", "nvq_level", "qualification_type",
]


def load_matching_rows():
    with open(MATCHING_CSV, newline="", encoding="utf-8-sig") as f:
        return {r["course_id"]: r for r in csv.DictReader(f)}


def load_crosswalk():
    with open(TRACEABILITY_CSV, newline="", encoding="utf-8-sig") as f:
        return {r["course_document_id"]: r for r in csv.DictReader(f)}


def build_base_course_name_options(matching_rows, indexable_ids_by_matching_id):
    """For Q1's answer options: distinct base course names per skill_area,
    generated from the corpus so they never drift from what's actually
    retrievable (only courses that DO resolve to an indexable RAG doc)."""
    by_skill_area = {}
    for matching_id, rag_id in indexable_ids_by_matching_id.items():
        row = matching_rows[matching_id]
        area = row["skill_area"]
        name = row["course_name"]
        # Strip common delivery-variant suffixes so duplicates collapse to one option.
        base = name
        for suffix in [" (Full Time)", " (Part Time)",
                       " (Full Time – English)", " (Full Time – Sinhala)",
                       " (Full Time - English)", " (Full Time - Sinhala)",
                       " (Part Time – English)", " (Part Time – Sinhala)",
                       " (English)", " (Sinhala)"]:
            base = base.replace(suffix, "")
        by_skill_area.setdefault(area, set()).add(base.strip())
    return {area: sorted(names) for area, names in by_skill_area.items()}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: verifying the validated 84-course corpus is unchanged...")
    manifest, exclusions = verify_corpus(verbose=False)
    manifest_by_id = {r["course_id"]: r for r in manifest}
    indexable_ids = set(manifest_by_id.keys())
    assert len(indexable_ids) == 84, f"expected 84 indexable courses, got {len(indexable_ids)}"
    print(f"  OK — {len(indexable_ids)} indexable courses confirmed (SHA-256 verified).")

    matching_rows = load_matching_rows()
    crosswalk = load_crosswalk()

    rows_out = []
    indexable_ids_by_matching_id = {}
    unmatched = []
    for rag_id in sorted(indexable_ids):
        trace = crosswalk.get(rag_id)
        matching_id = trace["structured_crosscheck_course_id"].strip() if trace else ""
        row = {
            "rag_course_id": rag_id,
            "rag_course_name": manifest_by_id[rag_id]["course_name"],
            "structured_matching_course_id": matching_id or NOT_STATED,
            "provenance": (
                f"crosswalked via course_source_traceability.csv "
                f"(structured_crosscheck_status={trace['structured_crosscheck_status']})"
                if trace and matching_id else
                "no structured crosswalk row found for this RAG document"
            ),
        }
        if matching_id and matching_id in matching_rows:
            m = matching_rows[matching_id]
            for field in STRUCTURED_FIELDS:
                val = m.get(field, "").strip()
                row[field] = val if val else NOT_STATED
            indexable_ids_by_matching_id[matching_id] = rag_id
        else:
            for field in STRUCTURED_FIELDS:
                row[field] = NOT_STATED
            unmatched.append(rag_id)
        rows_out.append(row)

    with open(OUT_DIR / "course_matching_layer.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["rag_course_id", "rag_course_name", "structured_matching_course_id",
                      "provenance"] + STRUCTURED_FIELDS
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    skill_area_options = build_base_course_name_options(matching_rows, indexable_ids_by_matching_id)
    with open(OUT_DIR / "q1_occupation_options_by_skill_area.json", "w", encoding="utf-8") as f:
        json.dump(skill_area_options, f, indent=2, ensure_ascii=False)

    n_matched = len(rows_out) - len(unmatched)
    print(f"Step 2: structured matching layer built — {n_matched}/{len(rows_out)} indexable "
          f"courses have structured attributes; {len(unmatched)} explicitly marked NOT_STATED "
          f"(no reliable crosswalk): {unmatched}")
    print(f"  Q1 answer-option lists built for {len(skill_area_options)} skill areas.")
    print(f"Wrote: {OUT_DIR / 'course_matching_layer.csv'}")
    print(f"Wrote: {OUT_DIR / 'q1_occupation_options_by_skill_area.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
