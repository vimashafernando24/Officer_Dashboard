"""Build the shared, model-level survey evidence used by leaf popups.

The source teaching library is itself rebuilt from the governed final profiling
registry, comparison table, survey manifest, profile catalogue and frozen
profile-size records. This transformation removes mirrored leaf duplicates but
does not calculate or invent any new research result.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path

from build_cluster_research_teaching_library import build_library
from cluster_catalogue import metadata_for_profile


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = (
    Path(__file__).resolve().parent
    / "frontend"
    / "src"
    / "data"
    / "clusterSurveyEvidenceLibrary.json"
)

REPORTED_CLAUSE_RE = re.compile(r"^reported “(?P<answer>.+)” (?P<direction>more|less) often$")
MEDIAN_CLAUSE_RE = re.compile(r"^had a (?P<direction>higher|lower) median (?P<measure>.+)$")


def _profile_code(profile_key: str) -> str:
    return metadata_for_profile(profile_key)["cluster_code"].removeprefix("Cluster ")


def _status_label(status: str) -> str:
    if status == "fdr_supported":
        return "FDR-supported"
    if status == "retained_descriptive":
        return "Retained descriptive"
    raise ValueError(f"Unexpected evidence status: {status}")


def _shared_cautions(findings: list[dict]) -> list[str]:
    cautions: list[str] = []
    for finding in findings:
        for caution in finding["cautions"]:
            if caution.startswith("This is a retained descriptive pattern"):
                continue
            if caution not in cautions:
                cautions.append(caution)
    return cautions


def _full_distribution(distribution: dict) -> list[dict]:
    answer_categories = list(OrderedDict.fromkeys(
        answer["answer"]
        for profile in distribution["profiles"]
        for answer in profile["answers"]
    ))
    rows = []
    for answer in answer_categories:
        values = []
        for profile in distribution["profiles"]:
            observed = next((item for item in profile["answers"] if item["answer"] == answer), None)
            values.append({
                "profile_key": profile["profile_key"],
                "count": observed["count"] if observed else 0,
                "denominator": profile["denominator"],
                "percentage": observed["percentage"] if observed else 0.0,
            })
        rows.append({"answer": answer, "profile_values": values})
    return rows


def _categorical_conclusion(finding: dict, model: dict) -> str:
    retained = REPORTED_CLAUSE_RE.match(finding["summary_clause"])
    if not retained:
        return finding["simple_conclusion"]
    data = retained.groupdict()
    focus_key = finding["evidence_id"].split(":", 1)[0]
    focus_code = _profile_code(focus_key)
    if model["profile_count"] == 2:
        sibling_key = next(
            profile["profile_key"] for profile in model["profiles"]
            if profile["profile_key"] != focus_key
        )
        target = _profile_code(sibling_key)
    else:
        target = "the other profiles collectively"
    return f'“{data["answer"]}” was {data["direction"]} common in {focus_code} than in {target}.'


def _retained_contrast(finding: dict) -> dict:
    distribution = finding["distribution"]
    answer = distribution["profiles"][0]["answers"][0]["answer"]
    return {
        "source_evidence_id": finding["evidence_id"],
        "answer": answer,
        "focus_profile_key": distribution["profiles"][0]["profile_key"],
        "profile_values": [
            {
                "profile_key": profile["profile_key"],
                "profile_label": profile["profile_name"],
                "count": profile["answers"][0]["count"],
                "denominator": profile["denominator"],
                "percentage": profile["answers"][0]["percentage"],
            }
            for profile in distribution["profiles"]
        ],
    }


def _retained_conclusion(contrasts: list[dict]) -> str:
    strongest = max(
        contrasts,
        key=lambda contrast: abs(
            contrast["profile_values"][0]["percentage"]
            - contrast["profile_values"][1]["percentage"]
        ),
    )
    focus, comparison = strongest["profile_values"][:2]
    direction = "more" if focus["percentage"] > comparison["percentage"] else "less"
    focus_code = _profile_code(focus["profile_key"])
    target = (
        _profile_code(comparison["profile_key"])
        if comparison["profile_key"]
        else "the other profiles collectively"
    )
    return f'“{strongest["answer"]}” was {direction} common in {focus_code} than in {target}.'


def _numeric_values(distribution: dict) -> list[dict]:
    return [
        {
            "profile_key": profile["profile_key"],
            "denominator": profile["denominator"],
            "median": profile["answers"][0]["value"],
            "iqr": profile["answers"][0]["iqr"],
        }
        for profile in distribution["profiles"]
    ]


def _numeric_conclusion(finding: dict, model: dict) -> str:
    retained = MEDIAN_CLAUSE_RE.match(finding["summary_clause"])
    if not retained:
        return finding["simple_conclusion"]
    data = retained.groupdict()
    focus_key = finding["evidence_id"].split(":", 1)[0]
    focus_code = _profile_code(focus_key)
    if model["profile_count"] == 2:
        sibling_key = next(
            profile["profile_key"] for profile in model["profiles"]
            if profile["profile_key"] != focus_key
        )
        target = _profile_code(sibling_key)
    else:
        target = "the other profiles collectively"
    return f'The typical {data["measure"]} was {data["direction"]} in {focus_code} than in {target}.'


def _shared_finding(model: dict, variable: str, findings: list[dict]) -> dict:
    first = findings[0]
    statuses = {finding["evidence_status"] for finding in findings}
    kinds = {finding["distribution"]["kind"] for finding in findings}
    questions = {finding["survey_question"]["question_text"] for finding in findings}
    if len(statuses) != 1 or len(kinds) != 1 or len(questions) != 1:
        raise ValueError(f"Inconsistent mirrored evidence for {model['model_key']}:{variable}")

    shared = {
        "evidence_id": f"{model['model_key']}:{variable}",
        "source_evidence_ids": [finding["evidence_id"] for finding in findings],
        "title": first["finding_title"],
        "survey_question": first["survey_question"]["question_text"],
        "question_id": first["survey_question"]["question_id"],
        "evidence_status": _status_label(first["evidence_status"]),
        "cautions": _shared_cautions(findings),
    }
    distribution = first["distribution"]
    if distribution["kind"] == "categorical_full":
        answer_distribution = _full_distribution(distribution)
        shared.update({
            "comparison_type": "full_categorical_distribution",
            "answer_categories": [item["answer"] for item in answer_distribution],
            "answer_distribution": answer_distribution,
            "simple_conclusion": _categorical_conclusion(first, model),
        })
    elif distribution["kind"] == "retained_comparison_only":
        selected_findings = findings[:1] if model["profile_count"] == 2 else findings
        contrasts = [_retained_contrast(finding) for finding in selected_findings]
        shared.update({
            "comparison_type": "retained_category_contrast",
            "answer_categories": list(OrderedDict.fromkeys(item["answer"] for item in contrasts)),
            "retained_contrasts": contrasts,
            "simple_conclusion": _retained_conclusion(contrasts),
        })
    elif distribution["kind"] == "numeric_summary":
        values = _numeric_values(distribution)
        shared.update({
            "comparison_type": "numeric_summary",
            "numeric_values": values,
            "simple_conclusion": _numeric_conclusion(first, model),
        })
    else:
        raise ValueError(f"Unsupported distribution kind: {distribution['kind']}")
    return shared


def build_shared_library() -> dict:
    teaching = build_library()
    models = {}
    source_evidence_ids: set[str] = set()
    for model in teaching["models"]:
        findings_by_variable: OrderedDict[str, list[dict]] = OrderedDict()
        for profile in model["profiles"]:
            for finding in profile["retained_findings"]:
                variable = finding["evidence_id"].split(":", 1)[1]
                findings_by_variable.setdefault(variable, []).append(finding)
                source_evidence_ids.add(finding["evidence_id"])
        models[model["model_key"]] = {
            "dimension_title": model["model_title"],
            "profiles": [
                {
                    "profile_key": profile["profile_key"],
                    "profile_code": _profile_code(profile["profile_key"]),
                    "profile_name": profile["canonical_profile_name"],
                    "historical_profile_size": profile["historical_profile_size"],
                }
                for profile in model["profiles"]
            ],
            "findings": [
                _shared_finding(model, variable, findings)
                for variable, findings in findings_by_variable.items()
            ],
        }

    finding_count = sum(len(model["findings"]) for model in models.values())
    if len(models) != 7 or finding_count != 39 or len(source_evidence_ids) != 89:
        raise ValueError(
            "Shared evidence library must contain 7 models, 39 deduplicated topics and all 89 retained source findings"
        )
    return {
        "schema_version": "cluster_survey_evidence_library_v1",
        "model_count": len(models),
        "finding_count": finding_count,
        "retained_source_finding_count": len(source_evidence_ids),
        "source_files": teaching["source_files"],
        "models": models,
    }


def rendered_library() -> str:
    return json.dumps(build_shared_library(), ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = rendered_library()
    if args.check:
        if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"STALE: {OUTPUT_PATH}")
        print("CLUSTER SURVEY EVIDENCE CHECK PASSED — 7 models, 39 shared topics, 89 retained source findings")
        return
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
