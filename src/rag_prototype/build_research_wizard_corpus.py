"""Build the governed finding-level corpus for the cluster research wizard."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import context_pack_v2
from profile_data_parser import parse_profile_document
from retained_cluster_evidence_registry import (
    PROFILE_RETAINED_VARIABLES,
    _interpretation_guard,
)
from research_wizard_evidence_registry import (
    EXPECTED_FINDING_COUNT,
    EXPECTED_PROFILE_COUNT,
    FINAL_WIZARD_SOURCE_COLUMNS,
    SUPPLEMENTAL_SURVEY_QUESTIONS,
    THEME_LABELS,
    WIZARD_PROFILING_VARIABLES_BY_MODEL,
)


BASE = Path(__file__).resolve().parents[2]
FINAL_PROFILE_CSV = BASE / "outputs/final_cluster_programme_relevant_profiles.csv"
FINAL_COMPARISON_CSV = BASE / "outputs/final_cluster_profile_comparison_summary.csv"
FEATURE_MANIFEST_CSV = BASE / "outputs/nysc_survey_feature_manifest.csv"
OUTPUT_DIR = BASE / "outputs/rag_cluster_research_wizard"
CORPUS_PATH = OUTPUT_DIR / "findings.jsonl"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def _split_findings(value: str) -> list[str]:
    return [
        item.strip()
        for item in value.split(" | ")
        if item.strip() and not item.strip().startswith("No clear")
    ]


def _final_profile_findings(row: dict) -> tuple[list[str], dict[str, list[str]]]:
    findings: list[str] = []
    source_fields: dict[str, list[str]] = {}
    for column in FINAL_WIZARD_SOURCE_COLUMNS:
        for finding in _split_findings(row[column]):
            source_fields.setdefault(finding, []).append(column)
            if finding not in findings:
                findings.append(finding)
    return findings, source_fields


def _statistical_record(row: dict) -> dict:
    fdr_supported = _truthy(row["supporting_fdr_lt_0_05"])
    return {
        "evidence_status": "fdr_supported" if fdr_supported else "retained_descriptive",
        "fdr_supported": fdr_supported,
        "coverage_pct": float(row["coverage_pct"]),
        "effect_size_name": row["effect_size_name"],
        "effect_size": float(row["effect_size"]),
        "raw_p_value": float(row["p_value"]),
        "fdr_adjusted_p_value": float(row["p_adjusted_bh"]),
        "conditional": _truthy(row["conditional"]),
        "sparse_cells": _truthy(row["sparse_cells"]),
        "small_sample": _truthy(row["small_sample_flag"]),
        "programme_relevance": row["programme_relevance"],
    }


def build_corpus() -> list[dict]:
    with FINAL_PROFILE_CSV.open(encoding="utf-8-sig", newline="") as handle:
        profile_rows = list(csv.DictReader(handle))
    with FINAL_COMPARISON_CSV.open(encoding="utf-8-sig", newline="") as handle:
        comparison_rows = list(csv.DictReader(handle))
    with FEATURE_MANIFEST_CSV.open(encoding="utf-8-sig", newline="") as handle:
        question_map = {row["variable"]: row for row in csv.DictReader(handle)}
    question_map.update(SUPPLEMENTAL_SURVEY_QUESTIONS)

    if len(profile_rows) != EXPECTED_PROFILE_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_PROFILE_COUNT} final profiles, found {len(profile_rows)}"
        )
    comparison_index = {
        (row["model_id"], row["variable"]): row for row in comparison_rows
    }
    profile_index = context_pack_v2.load_profile_index()
    records: list[dict] = []

    for row in profile_rows:
        model_id = row["model_id"]
        profile_id = int(row["profile_id"])
        profile_key = f"{model_id}_p{profile_id}"
        expected_variables = WIZARD_PROFILING_VARIABLES_BY_MODEL[model_id]
        final_findings, source_fields = _final_profile_findings(row)
        if len(final_findings) != len(expected_variables):
            raise ValueError(
                f"{profile_key}: final finding count {len(final_findings)} does not match "
                f"registry count {len(expected_variables)}"
            )

        parsed = parse_profile_document(
            context_pack_v2.load_profile_doc(profile_key, profile_index)
        )
        stats_by_variable = {
            item["variable"]: item
            for item in parsed["supported_findings"]["statistical_detail"]
        }
        programme_subset = set(PROFILE_RETAINED_VARIABLES[profile_key])

        for position, (variable, finding) in enumerate(
            zip(expected_variables, final_findings), start=1
        ):
            stat = stats_by_variable.get(variable)
            if not stat:
                raise ValueError(f"{profile_key}: no profile statistic for {variable}")
            if variable != "work_while_study_type" and not finding.startswith(
                f"{stat['label']}:"
            ):
                raise ValueError(
                    f"{profile_key}: finding/variable order mismatch at {variable}"
                )
            comparison = comparison_index.get((model_id, variable))
            if not comparison:
                raise ValueError(f"{profile_key}: no final comparison row for {variable}")
            question = question_map.get(variable, {})
            theme_code = comparison["theme"]
            records.append({
                "schema_version": "research_wizard_finding_v1",
                "evidence_id": f"{profile_key}:{variable}",
                "branch": row["branch"],
                "model_id": model_id,
                "dimension": row["dimension"],
                "profile_id": profile_id,
                "profile_key": profile_key,
                "profile_label": row["profile_label"],
                "historical_profile_size": int(row["cluster_size"]),
                "finding_order": position,
                "variable": variable,
                "label": stat["label"],
                "theme": theme_code,
                "theme_label": THEME_LABELS.get(theme_code, theme_code.replace("_", " ").title()),
                "finding": finding,
                "interpretation_guard": _interpretation_guard(variable, finding, parsed),
                "is_programme_relevant_subset": variable in programme_subset,
                "statistical_support": _statistical_record(comparison),
                "survey_question": {
                    "question_id": question.get("question_id"),
                    "section": question.get("section"),
                    "framework": question.get("framework"),
                    "question_text": question.get("question_text"),
                },
                "profile_cautions": parsed["cautions_text"],
                "prohibited_inferences": parsed["prohibited_inferences_text"],
                "provenance": {
                    "retention_source": (
                        "outputs/final_cluster_programme_relevant_profiles.csv row "
                        f"model_id={model_id}, profile_id={profile_id}, columns="
                        + ",".join(source_fields[finding])
                    ),
                    "analysis_source": (
                        "30_final_cluster_profile_analysis.ipynb -> "
                        "final_cluster_profiling_report.md"
                    ),
                    "statistical_source": (
                        "outputs/final_cluster_profile_comparison_summary.csv row "
                        f"model_id={model_id}, variable={variable}"
                    ),
                },
            })

    if len(records) != EXPECTED_FINDING_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_FINDING_COUNT} findings, built {len(records)}"
        )
    evidence_ids = [record["evidence_id"] for record in records]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("Duplicate research-wizard evidence IDs")
    return records


def write_corpus(records: list[dict]) -> dict:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    corpus_text = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        for record in records
    )
    CORPUS_PATH.write_text(corpus_text, encoding="utf-8")
    manifest = {
        "schema_version": "research_wizard_corpus_v1",
        "profile_count": len({record["profile_key"] for record in records}),
        "finding_count": len(records),
        "fdr_supported_count": sum(
            record["statistical_support"]["fdr_supported"] for record in records
        ),
        "descriptive_count": sum(
            not record["statistical_support"]["fdr_supported"] for record in records
        ),
        "corpus_sha256": hashlib.sha256(corpus_text.encode("utf-8")).hexdigest(),
        "source_sha256": {
            str(path.relative_to(BASE)): _sha256(path)
            for path in (
                FINAL_PROFILE_CSV,
                FINAL_COMPARISON_CSV,
                FEATURE_MANIFEST_CSV,
            )
        },
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":
    built = build_corpus()
    result = write_corpus(built)
    print(
        f"Wrote {result['finding_count']} governed findings for "
        f"{result['profile_count']} profiles to {CORPUS_PATH.relative_to(BASE)}"
    )
