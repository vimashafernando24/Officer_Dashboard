"""Governed retrieval over the final accepted cluster-profiling corpus.

The corpus is deliberately small, static, and auditable, so a local TF-IDF
retriever is sufficient and avoids another paid embedding call.  Metadata
filtering is mandatory: a finding can only be retrieved for an exactly
assigned profile.  Retrieval orders every accepted finding; it does not use a
top-k cut-off that could hide retained research from the wizard.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re

from research_wizard_evidence_registry import EXPECTED_FINDING_COUNT


BASE = Path(__file__).resolve().parents[2]
CORPUS_PATH = BASE / "outputs/rag_cluster_research_wizard/findings.jsonl"
MANIFEST_PATH = BASE / "outputs/rag_cluster_research_wizard/manifest.json"
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a", "about", "and", "are", "as", "at", "be", "been", "but", "by",
    "for", "from", "had", "has", "have", "in", "into", "is", "it", "more",
    "of", "on", "or", "other", "profile", "reported", "than", "that", "the",
    "their", "this", "to", "was", "were", "while", "with",
}


def _tokens(value: object) -> list[str]:
    return [
        token for token in TOKEN_RE.findall(str(value or "").lower())
        if len(token) > 1 and token not in STOPWORDS
    ]


@lru_cache(maxsize=1)
def load_research_corpus() -> tuple[list[dict], dict]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    corpus_text = CORPUS_PATH.read_text(encoding="utf-8")
    actual_hash = hashlib.sha256(corpus_text.encode("utf-8")).hexdigest()
    if actual_hash != manifest["corpus_sha256"]:
        raise ValueError("Research-wizard corpus hash does not match its manifest")
    records = [json.loads(line) for line in corpus_text.splitlines() if line.strip()]
    if len(records) != EXPECTED_FINDING_COUNT:
        raise ValueError(
            f"Research-wizard corpus expected {EXPECTED_FINDING_COUNT} findings, "
            f"found {len(records)}"
        )
    if len({item["evidence_id"] for item in records}) != len(records):
        raise ValueError("Research-wizard corpus contains duplicate evidence IDs")
    return records, manifest


def _query_text(cluster_answers: dict, officer_context: dict) -> str:
    answer_labels = [
        value.get("value_label") if isinstance(value, dict) else value
        for value in cluster_answers.values()
    ]
    context_values = [
        officer_context.get("ideal_sector"),
        officer_context.get("q1_occupation_focus"),
        officer_context.get("q2_reason"),
        officer_context.get("q3_schedule"),
        officer_context.get("q4_language"),
        officer_context.get("q5_qualification"),
    ]
    return " ".join(str(value) for value in answer_labels + context_values if value)


def _document_text(record: dict) -> str:
    question = record.get("survey_question", {}).get("question_text") or ""
    return " ".join((
        record["dimension"], record["theme_label"], record["label"],
        record["finding"], question,
    ))


def _tfidf_scores(records: list[dict], query: str) -> dict[str, float]:
    documents = {record["evidence_id"]: Counter(_tokens(_document_text(record))) for record in records}
    query_counts = Counter(_tokens(query))
    if not query_counts:
        return {record["evidence_id"]: 0.0 for record in records}

    document_frequency = Counter()
    for counts in documents.values():
        document_frequency.update(counts.keys())
    total_documents = len(documents)

    def vector(counts: Counter) -> dict[str, float]:
        return {
            token: count * (math.log((1 + total_documents) / (1 + document_frequency[token])) + 1)
            for token, count in counts.items()
        }

    query_vector = vector(query_counts)
    query_norm = math.sqrt(sum(value * value for value in query_vector.values())) or 1.0
    scores = {}
    for evidence_id, counts in documents.items():
        document_vector = vector(counts)
        document_norm = math.sqrt(sum(value * value for value in document_vector.values())) or 1.0
        dot = sum(
            query_vector[token] * document_vector.get(token, 0.0)
            for token in query_vector
        )
        scores[evidence_id] = dot / (query_norm * document_norm)
    return scores


def _known_member_facts(cluster_answers: dict, officer_context: dict) -> dict[str, dict]:
    known = {}
    for variable, raw in cluster_answers.items():
        answer = raw.get("value_label") if isinstance(raw, dict) else raw
        if answer not in (None, ""):
            known[variable] = {
                "source": "cluster_assignment_answer",
                "answer": str(answer),
                "do_not_ask_again": True,
            }
    sectors = officer_context.get("preferred_sectors") or []
    if sectors:
        known["ideal_sector"] = {
            "source": "programme_intake_answer",
            "answer": "; ".join(str(value) for value in sectors),
            "do_not_ask_again": True,
        }
    return known


def retrieve_profile_findings(
    *, assigned_profile_keys: list[str], cluster_answers: dict, officer_context: dict,
) -> tuple[list[dict], dict]:
    """Return all governed findings for assigned profiles, ordered by relevance."""
    corpus, manifest = load_research_corpus()
    assigned = set(assigned_profile_keys)
    records = [record for record in corpus if record["profile_key"] in assigned]
    found_profiles = {record["profile_key"] for record in records}
    if found_profiles != assigned:
        missing = sorted(assigned - found_profiles)
        raise ValueError(f"No research-wizard findings for assigned profile(s): {missing}")

    lexical_scores = _tfidf_scores(records, _query_text(cluster_answers, officer_context))
    known_facts = _known_member_facts(cluster_answers, officer_context)
    retrieved = []
    for record in records:
        known_fact = known_facts.get(record["variable"])
        relevance_score = lexical_scores[record["evidence_id"]]
        # Unanswered profiling topics are more useful for an officer question;
        # FDR support is a small ordering signal, never a validity gate.
        relevance_score += 0.12 if not known_fact else 0.0
        relevance_score += 0.03 if record["statistical_support"]["fdr_supported"] else 0.0
        retrieved.append({
            **record,
            "retrieval": {
                "relevance_score": round(relevance_score, 6),
                "member_fact_status": "already_recorded" if known_fact else "not_recorded",
                "known_member_fact": known_fact,
                "question_allowed": not bool(known_fact),
                "reason": (
                    "The member already answered this topic; use it only as context and do not ask again."
                    if known_fact else
                    "This accepted profiling topic was not answered in the intake and may be explored."
                ),
            },
        })

    retrieved.sort(key=lambda item: (
        -item["retrieval"]["relevance_score"],
        item["profile_key"],
        item["finding_order"],
    ))
    return retrieved, manifest

