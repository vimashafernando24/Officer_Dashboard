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
                    "actual sector-skill choices and other answers, verified course facts, and only "
                    "material final-retained profile context. Historical context must remain group-level."
    )
    user_facts_used: List[UserFactCitation] = Field(default_factory=list)
    course_facts_used: List[CourseFactCitation] = Field(default_factory=list)
    profile_findings_used: List[ProfileFindingCitation] = Field(default_factory=list)


class NewPersonRecommendationResponse(BaseModel):
    recommendation_status: Literal["RECOMMENDATIONS_AVAILABLE", "NO_DEFENSIBLE_RECOMMENDATION"]
    suggested_programmes: List[SuggestedProgramme] = Field(
        default_factory=list,
        max_length=4,
        description="At most four distinct programmes, ordered from strongest to weakest holistic match.",
    )
    no_recommendation_reason: Optional[str] = None
