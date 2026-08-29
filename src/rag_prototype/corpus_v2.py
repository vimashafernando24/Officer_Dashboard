"""
Loads and verifies the FINAL RAG course corpus V2 (84 indexable parents, 4 excluded).

Verification is mandatory and mechanical: this module refuses to proceed silently if
the manifest doesn't match the expected 84/4/88 counts, and never falls back to the
old 79-course corpus from the previous prototype.
"""
import csv, hashlib, os
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]  # .../ClusterRP
MANIFEST_CSV = BASE / "outputs/rag_course_knowledge/final_rag_corpus_v2_manifest.csv"
EXCLUSIONS_CSV = BASE / "outputs/rag_course_knowledge/final_rag_corpus_v2_exclusions.csv"
CORPUS_DIR = BASE / "outputs/rag_course_knowledge/final_rag_corpus_v2"

EXPECTED_INDEXABLE = 84
EXPECTED_EXCLUDED = 4
EXPECTED_TOTAL = 88


class CorpusVerificationError(Exception):
    pass


def load_manifest():
    with open(MANIFEST_CSV, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_exclusions():
    with open(EXCLUSIONS_CSV, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def verify_corpus(verbose=True):
    """Hard-fails (raises) if the corpus does not match the expected V2 counts."""
    manifest = load_manifest()
    exclusions = load_exclusions()

    n_indexable = len(manifest)
    n_excluded = len(exclusions)
    n_total = n_indexable + n_excluded

    not_yes = [r["course_id"] for r in manifest if r["rag_indexable"] != "YES"]
    excluded_ids = {r["course_id"] for r in exclusions}
    manifest_ids = {r["course_id"] for r in manifest}
    overlap = manifest_ids & excluded_ids

    problems = []
    if n_indexable != EXPECTED_INDEXABLE:
        problems.append(f"expected {EXPECTED_INDEXABLE} indexable parents, found {n_indexable}")
    if n_excluded != EXPECTED_EXCLUDED:
        problems.append(f"expected {EXPECTED_EXCLUDED} excluded parents, found {n_excluded}")
    if n_total != EXPECTED_TOTAL:
        problems.append(f"expected {EXPECTED_TOTAL} total evidence-supported parents, found {n_total}")
    if not_yes:
        problems.append(f"{len(not_yes)} manifest rows are not marked rag_indexable=YES: {not_yes}")
    if overlap:
        problems.append(f"{len(overlap)} course_ids appear in BOTH the manifest and the exclusions file: {overlap}")

    for row in manifest:
        doc_path = BASE / row["document_path"]
        if not doc_path.exists():
            problems.append(f"manifest references missing file: {row['document_path']}")
            continue
        actual_hash = hashlib.sha256(doc_path.read_bytes()).hexdigest()
        if actual_hash != row["document_sha256"]:
            problems.append(f"SHA-256 mismatch for {row['course_id']} ({row['document_path']}) — file may have changed since the manifest was generated")

    if problems:
        raise CorpusVerificationError(
            "V2 corpus verification FAILED — refusing to build a retrieval index on an "
            "unverified corpus. Problems:\n  - " + "\n  - ".join(problems)
        )

    if verbose:
        print(f"V2 corpus verified: {n_indexable} indexable + {n_excluded} excluded = {n_total} total "
              f"evidence-supported parents. All {n_indexable} document hashes match the manifest.")

    return manifest, exclusions


def resolve_document_path(manifest_row):
    return BASE / manifest_row["document_path"]


if __name__ == "__main__":
    verify_corpus()
