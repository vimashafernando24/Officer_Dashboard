export interface Option {
  code: string;
  label: string;
}

export interface ClusterQuestion {
  variable: string;
  question: string;
  type: "choice" | "number";
  options?: Option[];
}

export interface ClusterQuestionGroup {
  model_id: string;
  questions: ClusterQuestion[];
}

export interface QuestionConfig {
  branch: string;
  branch_routing_question: { question: string; options: Option[] };
  cluster_questions: ClusterQuestionGroup[];
  ideal_sector_options: Option[];
  q1_options_by_skill_area: string; // JSON-encoded string, parse client-side
  sector_bridge: Record<string, string[]>;
  q2_options: string[];
  q3_options: string[];
  q4_options: string[];
  q5_options: string[];
}

export interface SurveyQuestion {
  question_id: string;
  section: string;
  framework: string;
  question_text: string;
}

export interface DistributionItem {
  value: string;
  count: number;
  percent: number;
}

export interface DistributionEntry {
  label?: string;
  variable?: string;
  type?: string;
  theme?: string;
  coverage_pct?: number;
  screened?: boolean;
  eligible_n?: number;
  median?: number;
  iqr_low?: number;
  iqr_high?: number;
  distribution?: DistributionItem[];
  raw_distribution?: string;
  raw?: string;
  parse_failed?: boolean;
  display?: "answer_percentages";
}

export interface Finding {
  profile_key: string;
  variable: string;
  finding: string;
  survey_question: SurveyQuestion | null;
  distribution: DistributionEntry | null;
}

export interface ProfileEntry {
  profile_key: string;
  profile_label: string;
  membership_similarity_percent: number;
  distance_tie: boolean;
  model_judgment: string;
  model_published_accuracy: number;
}

export type ContributionRole =
  | "REINFORCED"
  | "CONTRASTED"
  | "HELPED_DIFFERENTIATE"
  | "PROVIDED_CONTEXT"
  | "NOT_USED";

export interface ProfileContextContribution {
  role: ContributionRole;
  insight: string | null;
  contributing_findings: Finding[];
}

export interface ExplicitAnswerUsed {
  question: string;
  answer: string;
  relevance: string;
}

export interface CourseFactUsed {
  fact: string;
  source_reference: string;
}

export interface Recommendation {
  rank: number;
  course_id: string;
  course_name: string;
  match_type: "DIRECT_MATCH" | "ADJACENT_MATCH";
  bridge_explanation: string | null;
  why_matches_explicit_answers: string;
  explicit_answers_used: ExplicitAnswerUsed[];
  course_facts_used: CourseFactUsed[];
  profile_context_contribution: ProfileContextContribution;
  llm_inferences: string[];
  limitations: string[];
  evidence_strength: "STRONG" | "MODERATE" | "LIMITED";
  evidence_strength_reason: string;
}

export interface AboutPeopleLikeYou {
  why_assigned: string;
  narrative: string;
  supporting_findings: Finding[];
}

export interface DiscussionPrompt {
  prompt: string;
  grounded_in: string;
}

export interface CandidateSelection {
  skill_areas: string[];
  note: string;
  candidates: { course_id: string; course_name: string; score: number }[];
}

export interface EvidencePreviewFinding extends Finding {
  current_context_eligible: boolean;
  context_explanation: string | null;
}

export interface EvidencePreviewProfile extends ProfileEntry {
  eligible_findings: Finding[];
  retained_findings: EvidencePreviewFinding[];
  withheld_retained_count: number;
  approved_findings: Finding[];
  cluster_code: string | null;
}

export interface ClusterDimensionVariable {
  variable: string;
  question_id: string | null;
  question: string | null;
}

export interface ClusterCatalogueEntry {
  profile_key: string;
  cluster_code: string;
  cluster_name: string;
  model_id: string;
  dimension: string;
  common_description: string;
  cluster_defining_variables: ClusterDimensionVariable[];
}

export interface ClusterOfficerQuestion {
  question: string;
  why_ask: string;
  supporting_findings: Finding[];
}

export interface ClusterProfileBriefing {
  profile_key: string;
  cluster_code: string;
  why_assigned: string;
  research_description: string;
  supporting_findings: Finding[];
  officer_questions: ClusterOfficerQuestion[];
}

export interface EvidencePreview {
  error?: string;
  branch: string;
  assigned_profiles: AssignedProfile[];
  cluster_catalogue: ClusterCatalogueEntry[];
  research_tree: ResearchTreeBranch[];
}

export interface TeachingDistributionAnswer {
  answer: string;
  count: number | null;
  percentage: number | null;
  value: number | null;
  iqr: string | null;
}

export interface TeachingDistributionProfile {
  profile_key: string | null;
  profile_name: string;
  denominator: number | null;
  answers: TeachingDistributionAnswer[];
}

export interface ClusterResearchTeachingFinding {
  evidence_id: string;
  finding_order: number;
  finding_title: string;
  simple_conclusion: string;
  summary_clause: string;
  survey_question: {
    question_id: string | null;
    section: string | null;
    framework: string | null;
    question_text: string | null;
  };
  answer_categories: string[];
  distribution: {
    kind: "categorical_full" | "retained_comparison_only" | "numeric_summary";
    availability: "complete" | "limited" | "summary_only";
    note: string;
    unit: "percent" | "value";
    profiles: TeachingDistributionProfile[];
  };
  historical_profile_size: number;
  evidence_status: "fdr_supported" | "retained_descriptive";
  statistics: {
    exact_retained_finding: string;
    variable_type: string;
    total_model_n: number;
    eligible_n: number;
    coverage_pct: number;
    effect_size_name: string;
    effect_size: number;
    raw_p_value: number;
    fdr_adjusted_p_value: number;
    fdr_supported: boolean;
    conditional: boolean;
    gateway: string | null;
    sparse_cells: boolean;
    small_sample: boolean;
  };
  cautions: string[];
}

export interface ClusterResearchTeachingProfile {
  model_key: string;
  model_title: string;
  profile_key: string;
  canonical_profile_name: string;
  historical_profile_size: number;
  sibling_profiles: Array<{
    profile_key: string;
    canonical_profile_name: string;
    historical_profile_size: number;
  }>;
  comparison_summary: string;
  retained_findings: ClusterResearchTeachingFinding[];
}

export interface ClusterResearchTeachingModel {
  model_key: string;
  model_title: string;
  branch: string;
  profile_count: number;
  profiles: ClusterResearchTeachingProfile[];
}

export interface ClusterResearchTeachingLibrary {
  schema_version: string;
  model_count: number;
  profile_count: number;
  finding_count: number;
  source_files: Record<string, string>;
  models: ClusterResearchTeachingModel[];
}

export interface ResearchTreeModel {
  model_id: string;
  model_label: string;
  profiles: ClusterCatalogueEntry[];
}

export interface ResearchTreeBranch {
  branch_id: string;
  branch_label: string;
  models: ResearchTreeModel[];
}

export interface AssignedProfile {
  profile_key: string;
  model_id: string;
  cluster_code: string;
  cluster_name: string;
  common_description: string;
  model_published_accuracy: number;
  model_judgment: string;
  needs_review_model: boolean;
}

export interface SuggestedProgramme {
  rank: number;
  course_id: string;
  course_name: string;
  why_it_may_suit_this_user: string;
  cluster_finding_summary: string | null;
  questions_to_discuss: string[];
  important_mismatches: string[];
}

export interface RecommendResponse {
  error?: string;
  person_id: string;
  branch: string;
  assigned_profiles: AssignedProfile[];
  cluster_catalogue: ClusterCatalogueEntry[];
  recommendation_status: "RECOMMENDATIONS_AVAILABLE" | "NO_DEFENSIBLE_RECOMMENDATION";
  suggested_programmes: SuggestedProgramme[];
  no_recommendation_reason: string | null;
  candidate_programme_count: number;
  evidence_safeguard_violations: string[];
  token_usage: { total_tokens: number; input_tokens: number; output_tokens: number };
}

export interface IntakeState {
  step: number;
  branch: string | null;
  clusterAnswers: Record<string, string>;
  idealSectors: string[];
  skillsBySector: Record<string, string[]>;
  q2: string | null;
  q3: string | null;
  q4: string | null;
  q5: string | null;
}

// On-demand Sinhala translation of an existing recommendation result.
export interface RecommendationTranslationRequest {
  programmes: {
    course_name: string;
    why_it_may_suit_this_user: string;
    cluster_finding_summary: string | null;
    questions_to_discuss: string[];
  }[];
  no_recommendation_reason: string | null;
}

export interface ProgrammeTranslation {
  why_it_may_suit_this_user: string;
  cluster_finding_summary: string | null;
  questions_to_discuss: string[];
}

export interface RecommendationTranslation {
  language: "si";
  programmes: ProgrammeTranslation[];
  no_recommendation_reason: string | null;
}
