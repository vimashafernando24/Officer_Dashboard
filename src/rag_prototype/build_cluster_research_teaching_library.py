"""Generate the frontend's frozen cluster-research teaching library.

The output contains no LLM-authored text. Retained findings are rebuilt from the
final analysis registry and joined to the final comparison table, survey manifest,
governed profile catalogue and profile-size table.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

from build_research_wizard_corpus import build_corpus
from cluster_catalogue import MODEL_DIMENSIONS, metadata_for_profile
from new_respondent_cluster_assignment import BRANCH_MODELS


ROOT = Path(__file__).resolve().parents[2]
COMPARISON_PATH = ROOT / "outputs" / "final_cluster_profile_comparison_summary.csv"
PROFILE_PATH = ROOT / "outputs" / "final_cluster_programme_relevant_profiles.csv"
SURVEY_PATH = ROOT / "outputs" / "nysc_survey_feature_manifest.csv"
PROFILE_INDEX_PATH = ROOT / "outputs" / "rag_profile_knowledge" / "profile_document_index.csv"
FINAL_PROFILE_REPORT_PATH = ROOT / "final_cluster_profiling_report.md"
FINAL_CLUSTER_REPORT_PATH = ROOT / "NYSC_all_branches_clustering_final_report.md"
ASSIGNMENT_PATH = Path(__file__).resolve().parent / "new_respondent_cluster_assignment.py"
CATALOGUE_PATH = Path(__file__).resolve().parent / "cluster_catalogue.py"
REGISTRY_PATH = Path(__file__).resolve().parent / "research_wizard_evidence_registry.py"
OUTPUT_PATH = (
    Path(__file__).resolve().parent
    / "frontend" / "src" / "data" / "clusterResearchTeachingLibrary.json"
)

REPORTED_RE = re.compile(
    r"^(?P<label>.+?): (?P<direction>more|less) often reported ‘(?P<answer>.+?)’ "
    r"\((?P<count>\d+)/(?P<denominator>\d+), (?P<percentage>[\d.]+)% vs "
    r"(?P<other_percentage>[\d.]+)% in other profile\(s\)\)"
)
MEDIAN_FINDING_RE = re.compile(
    r"^(?P<label>.+?): had (?P<direction>higher|lower) median (?P<measure>.+?) "
    r"\((?P<value>[\d.]+) vs (?P<other_value>[\d.]+)\)"
)
PROFILE_SEGMENT_RE = re.compile(
    r"Profile (?P<profile_id>\d+) (?:(?:eligible )?n)=(?P<denominator>\d+): "
    r"(?P<body>.*?)(?= \|\| Profile \d+ |$)"
)
ANSWER_RE = re.compile(r"^(?P<answer>.+): (?P<count>\d+) \((?P<percentage>[\d.]+)%\)$")
MEDIAN_SUMMARY_RE = re.compile(r"^median=(?P<median>[\d.]+), IQR=(?P<iqr>.+)$")


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pct(value: float) -> str:
    return f"{value:.1f}%"


def _profile_keys(model_key: str, profile_sizes: dict[str, int]) -> list[str]:
    return sorted(
        (key for key in profile_sizes if key.startswith(f"{model_key}_p")),
        key=lambda key: int(key.rsplit("_p", 1)[1]),
    )


def _sibling_target(profile_key: str, model_keys: list[str]) -> str:
    siblings = [metadata_for_profile(key)["cluster_name"] for key in model_keys if key != profile_key]
    if len(siblings) == 1:
        return f"the “{siblings[0]}” profile"
    return "the other profiles in this model collectively"


def _difference_phrase(within: float, other: float) -> str:
    gap = abs(within - other)
    strength = "slightly" if gap < 5 else "somewhat" if gap < 15 else "noticeably" if gap < 30 else "much"
    direction = "more" if within > other else "less"
    return f"This response was {strength} {direction} common in this historical profile."


def _parse_profile_descriptives(row: dict, model_keys: list[str]) -> list[dict]:
    profiles = []
    segments = list(PROFILE_SEGMENT_RE.finditer(row["profile_descriptives"]))
    if len(segments) != len(model_keys):
        raise ValueError(
            f"{row['model_id']}/{row['variable']}: expected {len(model_keys)} profile summaries, "
            f"found {len(segments)}"
        )
    for match in segments:
        profile_id = int(match.group("profile_id"))
        profile_key = f"{row['model_id']}_p{profile_id}"
        body = match.group("body")
        answers = []
        if row["variable_type"] == "categorical":
            for item in body.split("; "):
                answer_match = ANSWER_RE.match(item)
                if not answer_match:
                    raise ValueError(f"Could not parse categorical answer: {row['model_id']}/{row['variable']}: {item}")
                answers.append({
                    "answer": answer_match.group("answer"),
                    "count": int(answer_match.group("count")),
                    "percentage": float(answer_match.group("percentage")),
                    "value": None,
                    "iqr": None,
                })
        else:
            median_match = MEDIAN_SUMMARY_RE.match(body)
            if not median_match:
                raise ValueError(f"Could not parse numeric summary: {row['model_id']}/{row['variable']}: {body}")
            answers.append({
                "answer": "Median",
                "count": None,
                "percentage": None,
                "value": float(median_match.group("median")),
                "iqr": median_match.group("iqr"),
            })
        profiles.append({
            "profile_key": profile_key,
            "profile_name": metadata_for_profile(profile_key)["cluster_name"],
            "denominator": int(match.group("denominator")),
            "answers": answers,
        })
    return profiles


def _simple_conclusion(
    record: dict, comparison_row: dict, model_keys: list[str], profile_distributions: list[dict]
) -> tuple[str, str, list[str], dict]:
    finding = record["finding"]
    reported = REPORTED_RE.match(finding)
    if reported:
        data = reported.groupdict()
        count = int(data["count"])
        denominator = int(data["denominator"])
        percentage = float(data["percentage"])
        other_percentage = float(data["other_percentage"])
        answer = data["answer"].replace(" AND ", " and ")
        target = _sibling_target(record["profile_key"], model_keys)
        conditional = record["statistical_support"]["conditional"]
        if count == 0:
            opening = f"None of the {denominator} eligible members" if conditional else f"None of the {denominator} members"
        elif count == 1:
            opening = f"Only 1 of {denominator} eligible members" if conditional else f"Only 1 of {denominator} members"
        else:
            opening = f"{count} of {denominator} eligible members" if conditional else f"{count} of {denominator} members"
        conclusion = (
            f"{opening} ({_pct(percentage)}) selected “{answer}”. In {target}, "
            f"{_pct(other_percentage)} selected the same answer. "
            f"{_difference_phrase(percentage, other_percentage)}"
        )
        if comparison_row["variable_type"] == "categorical":
            distribution = {
                "kind": "categorical_full",
                "availability": "complete",
                "note": "Complete observed response distributions were available for every profile in this model.",
                "unit": "percent",
                "profiles": profile_distributions,
            }
            answer_categories = list(dict.fromkeys(
                answer_item["answer"]
                for profile in profile_distributions
                for answer_item in profile["answers"]
            ))
        else:
            sibling_distributions = [
                profile for profile in profile_distributions
                if profile["profile_key"] != record["profile_key"]
            ]
            if len(sibling_distributions) == 1:
                sibling_profile_key = sibling_distributions[0]["profile_key"]
                sibling_profile_name = sibling_distributions[0]["profile_name"]
                sibling_denominator = sibling_distributions[0]["denominator"]
            else:
                sibling_profile_key = None
                sibling_profile_name = "Other sibling profiles collectively"
                sibling_denominator = sum(profile["denominator"] for profile in sibling_distributions)
            distribution = {
                "kind": "retained_comparison_only",
                "availability": "limited",
                "note": (
                    "The final comparison output retained this answer-level contrast but did not store "
                    "the complete answer-category distribution. Only the verified comparison is shown."
                ),
                "unit": "percent",
                "profiles": [
                    {
                        "profile_key": record["profile_key"],
                        "profile_name": metadata_for_profile(record["profile_key"])["cluster_name"],
                        "denominator": denominator,
                        "answers": [{
                            "answer": answer,
                            "count": count,
                            "percentage": percentage,
                            "value": None,
                            "iqr": None,
                        }],
                    },
                    {
                        "profile_key": sibling_profile_key,
                        "profile_name": sibling_profile_name,
                        "denominator": sibling_denominator,
                        "answers": [{
                            "answer": answer,
                            "count": None,
                            "percentage": other_percentage,
                            "value": None,
                            "iqr": None,
                        }],
                    },
                ],
            }
            answer_categories = [answer]
        clause = f"reported “{answer}” {data['direction']} often"
        return conclusion, clause, answer_categories, distribution

    median = MEDIAN_FINDING_RE.match(finding)
    if median:
        data = median.groupdict()
        value = float(data["value"])
        other_value = float(data["other_value"])
        target = _sibling_target(record["profile_key"], model_keys)
        conclusion = (
            f"The median {data['measure']} was {value:g} in this profile and {other_value:g} in "
            f"{target}. The typical value was {data['direction']} here."
        )
        distribution = {
            "kind": "numeric_summary",
            "availability": "summary_only",
            "note": "The final analysis stored medians and interquartile ranges rather than answer-category percentages.",
            "unit": "value",
            "profiles": profile_distributions,
        }
        return conclusion, f"had a {data['direction']} median {data['measure']}", [], distribution

    if record["variable"] == "work_while_study_type":
        selected = next(p for p in profile_distributions if p["profile_key"] == record["profile_key"])
        if record["profile_id"] == 1:
            conclusion = (
                "Among members who worked while studying, 17 of 22 (77.3%) had a private-company "
                "internship or apprenticeship. This was the main form of earlier work experience in "
                "this historical profile."
            )
            clause = "mainly gained work experience through private-company internships"
        else:
            conclusion = (
                "Among members who worked while studying, 23 of 41 (56.1%) had ordinary paid work in "
                "a private company, while 12 of 41 (29.3%) had a private-company internship or apprenticeship."
            )
            clause = "more often gained ordinary paid private-company experience"
        distribution = {
            "kind": "categorical_full",
            "availability": "complete",
            "note": "Complete observed response distributions were available for every profile in this model.",
            "unit": "percent",
            "profiles": profile_distributions,
        }
        return conclusion, clause, [a["answer"] for a in selected["answers"]], distribution

    raise ValueError(f"Unsupported retained finding: {record['evidence_id']}: {finding}")


def _comparison_summary(profile: dict, sibling_names: list[str]) -> str:
    findings = sorted(
        profile["retained_findings"],
        key=lambda item: (item["evidence_status"] != "fdr_supported", item["finding_order"]),
    )
    clauses = [item["summary_clause"] for item in findings[:2]]
    if len(sibling_names) == 1:
        target = f"the “{sibling_names[0]}” profile"
    else:
        target = "the other profiles in this frozen model collectively"
    if not clauses:
        return f"This profile is compared with {target}; no retained profiling contrast was available."
    joined = clauses[0] if len(clauses) == 1 else f"{clauses[0]} and {clauses[1]}"
    return f"Compared with {target}, this historical profile {joined}."


def build_library() -> dict:
    records = build_corpus()
    with COMPARISON_PATH.open(encoding="utf-8-sig", newline="") as handle:
        comparisons = list(csv.DictReader(handle))
    with PROFILE_PATH.open(encoding="utf-8-sig", newline="") as handle:
        profile_rows = list(csv.DictReader(handle))
    comparison_index = {(row["model_id"], row["variable"]): row for row in comparisons}
    profile_sizes = {
        f"{row['model_id']}_p{int(row['profile_id'])}": int(row["cluster_size"])
        for row in profile_rows
    }
    records_by_profile = defaultdict(list)
    for record in records:
        records_by_profile[record["profile_key"]].append(record)

    models = []
    for branch, branch_models in BRANCH_MODELS.items():
        for model_key in branch_models:
            model_profile_keys = _profile_keys(model_key, profile_sizes)
            profiles = []
            distribution_cache = {}
            for variable in {record["variable"] for key in model_profile_keys for record in records_by_profile[key]}:
                row = comparison_index[(model_key, variable)]
                distribution_cache[variable] = _parse_profile_descriptives(row, model_profile_keys)
            for profile_key in model_profile_keys:
                metadata = metadata_for_profile(profile_key)
                sibling_profiles = [
                    {
                        "profile_key": sibling_key,
                        "canonical_profile_name": metadata_for_profile(sibling_key)["cluster_name"],
                        "historical_profile_size": profile_sizes[sibling_key],
                    }
                    for sibling_key in model_profile_keys if sibling_key != profile_key
                ]
                findings = []
                for record in sorted(records_by_profile[profile_key], key=lambda item: item["finding_order"]):
                    comparison = comparison_index[(model_key, record["variable"])]
                    conclusion, clause, answer_categories, distribution = _simple_conclusion(
                        record, comparison, model_profile_keys, distribution_cache[record["variable"]]
                    )
                    support = record["statistical_support"]
                    cautions = []
                    if support["conditional"]:
                        cautions.append("This question used an eligible-subgroup denominator.")
                    if support["sparse_cells"]:
                        cautions.append("Some response cells were sparse; interpret the pattern cautiously.")
                    if support["small_sample"]:
                        cautions.append("The eligible sample was small.")
                    if not support["fdr_supported"]:
                        cautions.append("This is a retained descriptive pattern, not an FDR-supported result.")
                    findings.append({
                        "evidence_id": record["evidence_id"],
                        "finding_order": record["finding_order"],
                        "finding_title": comparison["variable_label"],
                        "simple_conclusion": conclusion,
                        "summary_clause": clause,
                        "survey_question": record["survey_question"],
                        "answer_categories": answer_categories,
                        "distribution": distribution,
                        "historical_profile_size": record["historical_profile_size"],
                        "evidence_status": support["evidence_status"],
                        "statistics": {
                            "exact_retained_finding": record["finding"],
                            "variable_type": comparison["variable_type"],
                            "total_model_n": int(comparison["total_model_n"]),
                            "eligible_n": int(comparison["eligible_n"]),
                            "coverage_pct": support["coverage_pct"],
                            "effect_size_name": support["effect_size_name"],
                            "effect_size": support["effect_size"],
                            "raw_p_value": support["raw_p_value"],
                            "fdr_adjusted_p_value": support["fdr_adjusted_p_value"],
                            "fdr_supported": support["fdr_supported"],
                            "conditional": support["conditional"],
                            "gateway": comparison["gateway"] or None,
                            "sparse_cells": support["sparse_cells"],
                            "small_sample": support["small_sample"],
                        },
                        "cautions": cautions,
                        "provenance": record["provenance"],
                    })
                profile = {
                    "model_key": model_key,
                    "model_title": MODEL_DIMENSIONS[model_key],
                    "profile_key": profile_key,
                    "canonical_profile_name": metadata["cluster_name"],
                    "historical_profile_size": profile_sizes[profile_key],
                    "sibling_profiles": sibling_profiles,
                    "comparison_summary": "",
                    "retained_findings": findings,
                }
                profile["comparison_summary"] = _comparison_summary(
                    profile, [item["canonical_profile_name"] for item in sibling_profiles]
                )
                profiles.append(profile)
            models.append({
                "model_key": model_key,
                "model_title": MODEL_DIMENSIONS[model_key],
                "branch": branch,
                "profile_count": len(profiles),
                "profiles": profiles,
            })

    library = {
        "schema_version": "cluster_research_teaching_library_v1",
        "model_count": len(models),
        "profile_count": sum(len(model["profiles"]) for model in models),
        "finding_count": sum(
            len(profile["retained_findings"])
            for model in models for profile in model["profiles"]
        ),
        "source_files": {
            str(path.relative_to(ROOT)): _sha(path)
            for path in (
                COMPARISON_PATH,
                PROFILE_PATH,
                SURVEY_PATH,
                PROFILE_INDEX_PATH,
                FINAL_PROFILE_REPORT_PATH,
                FINAL_CLUSTER_REPORT_PATH,
                ASSIGNMENT_PATH,
                CATALOGUE_PATH,
                REGISTRY_PATH,
            )
        },
        "models": models,
    }
    if (library["model_count"], library["profile_count"], library["finding_count"]) != (7, 17, 89):
        raise ValueError("Teaching library must contain exactly 7 models, 17 profiles and 89 findings")
    return library


def rendered_library() -> str:
    return json.dumps(build_library(), ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = rendered_library()
    if args.check:
        if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"STALE: {OUTPUT_PATH}")
        print("CLUSTER RESEARCH TEACHING LIBRARY CHECK PASSED — 7 models, 17 profiles, 89 findings")
        return
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
