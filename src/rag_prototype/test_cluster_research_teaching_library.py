"""Integrity checks for the generated officer teaching library."""
from collections import Counter

from build_cluster_research_teaching_library import build_library
from cluster_catalogue import metadata_for_profile


library = build_library()
assert (library["model_count"], library["profile_count"], library["finding_count"]) == (7, 17, 89)

profiles = [profile for model in library["models"] for profile in model["profiles"]]
findings = [finding for profile in profiles for finding in profile["retained_findings"]]
assert len({profile["profile_key"] for profile in profiles}) == 17
assert len({finding["evidence_id"] for finding in findings}) == 89
assert Counter(finding["evidence_status"] for finding in findings) == {
    "fdr_supported": 42,
    "retained_descriptive": 47,
}
assert Counter(finding["distribution"]["availability"] for finding in findings) == {
    "complete": 48,
    "limited": 37,
    "summary_only": 4,
}

for model in library["models"]:
    model_keys = {profile["profile_key"] for profile in model["profiles"]}
    for profile in model["profiles"]:
        assert profile["canonical_profile_name"] == metadata_for_profile(profile["profile_key"])["cluster_name"]
        assert {sibling["profile_key"] for sibling in profile["sibling_profiles"]} == model_keys - {profile["profile_key"]}
        assert profile["historical_profile_size"] > 0
        assert profile["retained_findings"]
        if model["profile_count"] == 2:
            assert profile["sibling_profiles"][0]["canonical_profile_name"] in profile["comparison_summary"]
        else:
            assert "collectively" in profile["comparison_summary"]

for finding in findings:
    assert finding["survey_question"]["question_text"]
    assert finding["simple_conclusion"]
    assert finding["statistics"]["exact_retained_finding"]
    distribution = finding["distribution"]
    if distribution["availability"] == "complete":
        assert distribution["kind"] == "categorical_full"
        assert finding["answer_categories"]
        assert all(item["denominator"] is not None for item in distribution["profiles"])
        assert all(
            answer["count"] is not None and answer["percentage"] is not None
            for item in distribution["profiles"] for answer in item["answers"]
        )
    elif distribution["availability"] == "limited":
        assert "did not store the complete answer-category distribution" in distribution["note"]
        assert any(
            answer["count"] is None
            for item in distribution["profiles"] for answer in item["answers"]
        )
    else:
        assert distribution["kind"] == "numeric_summary"
        assert "medians and interquartile ranges" in distribution["note"]

print("CLUSTER RESEARCH TEACHING LIBRARY TEST PASSED — 7 models, 17 profiles, 89 findings")
