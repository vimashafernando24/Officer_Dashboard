"""Offline retrieval checks for assigned-profile scope and known-answer handling."""
from research_wizard_retriever import retrieve_profile_findings


retrieved, manifest = retrieve_profile_findings(
    assigned_profile_keys=["D_economic_p1", "D_educational_cultural_p2", "D_motivation_p3"],
    cluster_answers={
        "institution_type": {"value_label": "Government vocational/technical institute"},
        "household_income": {"value_label": "LKR 60,000 – 120,000"},
    },
    officer_context={
        "preferred_sectors": ["Hotels, restaurants, and hospitality"],
        "ideal_sector": "Hotels, restaurants, and hospitality",
        "q1_occupation_focus": "Cake Decorator",
        "q2_reason": "Get a job",
        "q3_schedule": "Part-time, weekends",
        "q4_language": "English",
        "q5_qualification": "Yes, I want a formal NVQ or qualification",
    },
)

assert manifest["finding_count"] == 89
assert len(retrieved) == 11
assert {record["profile_key"] for record in retrieved} == {
    "D_economic_p1", "D_educational_cultural_p2", "D_motivation_p3",
}
assert {record["variable"] for record in retrieved} >= {
    "social_capital_in_edu_access", "primary_earner_status", "employment_network_quality",
}

by_variable = {record["variable"]: record for record in retrieved}
assert not by_variable["institution_type"]["retrieval"]["question_allowed"]
assert not by_variable["household_income"]["retrieval"]["question_allowed"]
assert not by_variable["ideal_sector"]["retrieval"]["question_allowed"]
assert by_variable["social_capital_in_edu_access"]["retrieval"]["question_allowed"]
assert retrieved == sorted(
    retrieved,
    key=lambda item: (
        -item["retrieval"]["relevance_score"], item["profile_key"], item["finding_order"],
    ),
)

print("RESEARCH WIZARD RETRIEVAL CHECK PASSED — exact assigned scope, all findings, relevance order")
