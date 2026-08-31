"""Offline integrity checks for the complete research-wizard corpus."""
from build_research_wizard_corpus import build_corpus
from research_wizard_evidence_registry import (
    EXPECTED_FINDING_COUNT,
    EXPECTED_PROFILE_COUNT,
    WIZARD_PROFILING_VARIABLES_BY_MODEL,
)


records = build_corpus()
assert len(records) == EXPECTED_FINDING_COUNT == 89
assert len({record["profile_key"] for record in records}) == EXPECTED_PROFILE_COUNT == 17
assert len({record["evidence_id"] for record in records}) == len(records)
assert {record["model_id"] for record in records} == set(WIZARD_PROFILING_VARIABLES_BY_MODEL)
assert all(record["finding"] and record["interpretation_guard"] for record in records)
assert all(record["provenance"]["retention_source"] for record in records)
assert all(record["survey_question"]["question_text"] for record in records)
assert sum(record["statistical_support"]["fdr_supported"] for record in records) == 42
assert sum(not record["statistical_support"]["fdr_supported"] for record in records) == 47

# The approved secondary Branch F finding must be in the wizard even though it
# is deliberately absent from the narrower programme evidence registry.
work_type = [record for record in records if record["variable"] == "work_while_study_type"]
assert len(work_type) == 2
assert all(not record["is_programme_relevant_subset"] for record in work_type)
assert any("internships/apprenticeships" in record["finding"] for record in work_type)
assert any("ordinary paid private-company work" in record["finding"] for record in work_type)

print("RESEARCH WIZARD CORPUS CHECK PASSED — 89 governed findings across all 17 profiles")

