"""Structured response for context-aware programme ranking and explanation."""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class UserFactCitation(BaseModel):
    question: str = Field(description="Question or constraint label from user.questionnaire_answers.")
    answer: str = Field(
        description="One actual scalar answer copied verbatim from the JSON payload. For a sector-skill "
                    "match, cite the sector and relevant skill as separate scalar citations; do not "
                    "serialize a mapping or array into this string."
    )


class CourseFactCitation(BaseModel):
    fact: str = Field(description="A course fact copied from the candidate programme record.")
    source_reference: str = Field(description="The exact candidate course_id.")


class ProfileFindingCitation(BaseModel):
    profile_key: str = Field(description="Exact assigned profile key from the JSON payload.")
    variable: str = Field(description="Exact validated profiling variable from the JSON payload.")
    finding: str = Field(description="Exact retained finding text copied verbatim from the JSON payload.")


class SuggestedProgramme(BaseModel):
    rank: int
    course_id: str
    course_name: str
    why_it_may_suit_this_user: str = Field(
        description="Two or three concise sentences explaining the holistic match using this member's "
                    "actual sector-skill choices, other answers, and verified course facts. Keep any "
                    "historical cluster tendency out of this field; put it in cluster_finding_summary."
    )
    user_facts_used: List[UserFactCitation] = Field(default_factory=list)
    course_facts_used: List[CourseFactCitation] = Field(default_factory=list)
    profile_findings_used: List[ProfileFindingCitation] = Field(default_factory=list)
    cluster_finding_summary: Optional[str] = Field(
        default=None,
        description="Required when profile_findings_used is non-empty; otherwise null. One or two short, "
                    "plain-language sentences describing the relevant tendency among people in the "
                    "matched profile and how it supported or qualified this programme decision. Do not "
                    "include percentages, sample sizes, statistics, variable names, profile keys, codes, "
                    "or JSON. Never present the tendency as a personal fact about this member."
    )
    questions_to_discuss: List[str] = Field(
        min_length=2,
        max_length=3,
        description="Two or three short questions the officer can ask specifically about this programme. "
                    "Each question must resolve a genuine open decision: a mismatch, missing course fact, "
                    "desired work outcome, willingness to consider a related route, or whether a cited "
                    "historical tendency applies. Never ask the member to reconfirm a questionnaire answer "
                    "that already matches a verified course fact. Use plain language; never expose research "
                    "variables, statistics, profile keys, internal codes, or JSON."
    )


class NewPersonRecommendationResponse(BaseModel):
    recommendation_status: Literal["RECOMMENDATIONS_AVAILABLE", "NO_DEFENSIBLE_RECOMMENDATION"]
    suggested_programmes: List[SuggestedProgramme] = Field(
        default_factory=list,
        max_length=9,
        description="At most nine distinct programmes, ordered from strongest to weakest holistic match. "
                    "After direct-evidence matches, remaining positions may contain defensible "
                    "profile-informed related options grounded in exact retained findings. Every "
                    "required_course_id in required_selected_skill_coverage must be included.",
    )
    no_recommendation_reason: Optional[str] = None
