"""
Structured-output schema for the API recommendation pipeline, matching the concepts
required by the task spec (Section L) as a Pydantic model so the OpenAI Responses API
can be asked to fill it directly (no brittle regex/prose parsing).
"""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class DirectEvidenceItem(BaseModel):
    variable: str = Field(description="The exact respondent_evidence.jsonl variable name used, e.g. 'ideal_sector'")
    value: str = Field(description="The exact value recorded for the respondent for this variable")
    relevance: str = Field(description="One sentence on why this fact is relevant to this recommendation")


class ProfileContextItem(BaseModel):
    profile: str = Field(description="Which profile document this came from, e.g. 'D_motivation_p3'")
    finding: str = Field(description="The specific group-level finding or tendency cited")
    role: Literal["supporting_context_only"] = "supporting_context_only"


class CourseEvidenceItem(BaseModel):
    course_fact: str = Field(description="The specific fact taken from the course document")
    source_reference: str = Field(description="Which retrieved course_id this fact came from")


class ContextualInference(BaseModel):
    inference: str = Field(description="The inference itself, phrased with uncertainty language (may/could/appears...)")
    based_on: List[str] = Field(description="The specific respondent fact(s) and/or course fact(s) this inference is built on")
    uncertainty_language_used: bool = Field(description="True only if the inference text itself uses hedged/uncertain phrasing")


class CourseRecommendation(BaseModel):
    rank: int
    course_id: str = Field(description="Must exactly match a course_id from the retrieved Section 3 documents")
    course_name: str
    match_relationship: Literal["DIRECT_MATCH", "ADJACENT_MATCH"] = Field(
        description="DIRECT_MATCH: direct individual evidence (stated field/goal/training interest/work "
                    "intention) connects the respondent to this programme. ADJACENT_MATCH: the programme does "
                    "not directly correspond to a stated field, but has a defensible, explained relationship "
                    "to the respondent's goals/circumstances.")
    adjacent_match_bridge_explanation: Optional[str] = Field(
        default=None, description="Required and non-null when match_relationship is ADJACENT_MATCH: the "
                                   "specific inferential bridge connecting the respondent's actual evidence to "
                                   "this programme. Must be null when match_relationship is DIRECT_MATCH.")
    direct_respondent_evidence_used: List[DirectEvidenceItem]
    profile_context_used: List[ProfileContextItem] = Field(
        default_factory=list, description="May be empty. Group-level context only, never an individual fact.")
    course_evidence_used: List[CourseEvidenceItem]
    contextual_inferences: List[ContextualInference] = Field(default_factory=list)
    why_recommended: str
    uncertainties: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    evidence_strength: Literal["STRONG", "MODERATE", "LIMITED"]
    evidence_strength_reason: str = Field(description="Brief justification for the chosen evidence_strength label")


class RespondentRecommendationResponse(BaseModel):
    respondent_id: str
    recommendation_status: Literal["RECOMMENDATIONS_AVAILABLE", "NO_DEFENSIBLE_RECOMMENDATION"]
    recommendations: List[CourseRecommendation] = Field(
        default_factory=list, description="0 to 5 items. Must be empty if recommendation_status is NO_DEFENSIBLE_RECOMMENDATION.")
    catalogue_coverage_note: Optional[str] = Field(
        default=None, description="Set this when no DIRECT_MATCH exists among the retrieved courses for this "
                                   "respondent's stated field, whether or not ADJACENT_MATCH options are being "
                                   "returned. State plainly, e.g. 'No strong direct programme match was found "
                                   "in the available NYSC catalogue for [stated field]. The following are "
                                   "adjacent options that may still be relevant.' or, if no adjacent option is "
                                   "defensible either, explain the catalogue gap. Leave null when a DIRECT_MATCH "
                                   "was found and returned.")
    no_defensible_recommendation_reason: Optional[str] = Field(
        default=None, description="Required and non-null only when recommendation_status is NO_DEFENSIBLE_RECOMMENDATION")
