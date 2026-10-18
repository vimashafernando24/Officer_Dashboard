// Coverage state for each governed NYSC course, from the compact coverage index
// (src/data/coverageIndex.json), generated from coverage_register.json and validated
// by test_coverage_register.py. The state is derived from verified, stored evidence
// only: linked records and completed mappings. A proposed future mode is never
// presented as coverage. No comparator data is needed to compute it.
import coverageIndex from "./data/coverageIndex.json" with { type: "json" };

export type CoverageState = "FULL_COMPARISON" | "COMPARATORS_ONLY" | "RESEARCH_PENDING" | "EVIDENCE_UNAVAILABLE";
// NO_DEFENSIBLE_COMPARATOR: researched, but no defensible official comparator with inspectable content was found.
export type ResearchStatus = "COMPLETE" | "NOT_RESEARCHED" | "IN_PROGRESS" | "BLOCKED" | "NO_DEFENSIBLE_COMPARATOR";
export type EvidenceAvailability = "HEADINGS_AVAILABLE" | "NO_HEADINGS" | "HEADINGS_UNUSABLE";

export interface CoverageIndexEntry {
  state: string;
  research: string;
  headings: string;
  verified_headings: number;
  records: string[];
  datasets: string[];
  mapping: boolean;
  blocking_evidence?: string;
  research_note?: string;
}

export interface CourseCoverage {
  courseId: string;
  state: CoverageState;
  researchStatus: ResearchStatus;
  evidenceAvailability: EvidenceAvailability;
  verifiedHeadingCount: number;
  comparatorCount: number;
  hasMapping: boolean;
  blockingEvidence: string | null;
  /** Documented reason why research found no defensible comparator (NO_DEFENSIBLE_COMPARATOR only). */
  researchNote: string | null;
}

const INDEX = coverageIndex.courses as Record<string, CoverageIndexEntry>;

/** The compact index entry for a course, or null for an unknown course. */
export function indexEntry(courseId: string): CoverageIndexEntry | null {
  return Object.hasOwn(INDEX, courseId) ? INDEX[courseId] : null;
}

/** The index's recorded current mode, used by tests to check the derivation agrees with it. */
export function registerCurrentMode(courseId: string): string | null {
  return indexEntry(courseId)?.state ?? null;
}

/**
 * The state to show. Verified comparators decide whether anything is compared;
 * research status only distinguishes pending research from documented insufficiency.
 */
export function deriveCoverageState(input: {
  comparatorCount: number;
  hasMapping: boolean;
  researchStatus: ResearchStatus;
}): CoverageState {
  if (input.comparatorCount > 0) return input.hasMapping ? "FULL_COMPARISON" : "COMPARATORS_ONLY";
  return input.researchStatus === "BLOCKED" ? "EVIDENCE_UNAVAILABLE" : "RESEARCH_PENDING";
}

export function coverageForCourse(courseId: string): CourseCoverage | null {
  const entry = indexEntry(courseId);
  if (!entry) return null;
  const comparatorCount = entry.records.length;
  const hasMapping = entry.mapping;
  const researchStatus = entry.research as ResearchStatus;
  return {
    courseId,
    state: deriveCoverageState({ comparatorCount, hasMapping, researchStatus }),
    researchStatus,
    evidenceAvailability: entry.headings as EvidenceAvailability,
    verifiedHeadingCount: entry.verified_headings,
    comparatorCount,
    hasMapping,
    blockingEvidence: entry.blocking_evidence ?? null,
    researchNote: entry.research_note ?? null,
  };
}

/** Which parts of the comparison a state may show. */
export function coveragePresentation(state: CoverageState): {
  showComparators: boolean;
  showMatrix: boolean;
  showAreas: boolean;
} {
  return {
    showComparators: state === "FULL_COMPARISON" || state === "COMPARATORS_ONLY",
    showMatrix: state === "FULL_COMPARISON",
    showAreas: state === "FULL_COMPARISON",
  };
}

export const MISSING_COMPARISON_CAUTION =
  "A missing comparison does not mean that suitable programmes do not exist.";

/** Dashboard-level notice: comparator evidence is drawn from official sources but has not been independently reviewed. */
export const EVIDENCE_REVIEW_NOTICE =
  "Comparator records are taken from official published sources and have not yet been independently reviewed by a human reviewer. Treat comparisons as provisional.";

/** What NYSC publishes for the course: about its own headings only, never about external evidence. */
export function headingsMessage(coverage: CourseCoverage): string {
  switch (coverage.evidenceAvailability) {
    case "HEADINGS_AVAILABLE": {
      const n = coverage.verifiedHeadingCount;
      return `NYSC module headings: ${n} usable heading${n === 1 ? "" : "s"} published for this course.`;
    }
    case "HEADINGS_UNUSABLE":
      return "NYSC module headings: the published heading names no curriculum content, so a competency matrix cannot be assessed from it.";
    default:
      return "NYSC module headings: none published for this course, so a competency matrix cannot be assessed from the governed catalogue.";
  }
}

/** The state of external comparator evidence: separate from NYSC's own headings. */
export function researchMessage(coverage: CourseCoverage): string {
  switch (coverage.state) {
    case "FULL_COMPARISON":
      return "Comparator programmes: verified records and a completed competency mapping are available.";
    case "COMPARATORS_ONLY":
      return coverage.evidenceAvailability === "HEADINGS_AVAILABLE"
        ? "Comparator programmes: verified records are shown, but the competency mapping has not been completed yet."
        : "Comparator programmes: verified records are shown without a competency matrix, because no defensible NYSC mapping is available.";
    case "EVIDENCE_UNAVAILABLE":
      return `Comparator programmes: research was attempted, but the documented evidence is insufficient${coverage.blockingEvidence ? `: ${coverage.blockingEvidence}` : "."}`;
    default:
      if (coverage.researchStatus === "NO_DEFENSIBLE_COMPARATOR") {
        return "Comparator programmes: research was carried out, but no official comparator with inspectable curriculum content could be defensibly matched to this course.";
      }
      return coverage.researchStatus === "IN_PROGRESS"
        ? "Comparator programmes: research is in progress; no comparator records have been verified yet."
        : "Comparator programmes: comparison research has not yet been completed, so no comparator records have been verified for this course.";
  }
}

const TITLES: Record<CoverageState, string> = {
  FULL_COMPARISON: "Full comparison available",
  COMPARATORS_ONLY: "Comparator programmes only",
  RESEARCH_PENDING: "Comparison research not yet completed",
  EVIDENCE_UNAVAILABLE: "Comparison evidence insufficient",
};

/** The status note shown in place of a comparison that is not (fully) available. */
export function coverageNote(coverage: CourseCoverage): { title: string; lines: string[] } {
  const lines = [researchMessage(coverage), headingsMessage(coverage)];
  if (coverage.state === "RESEARCH_PENDING" || coverage.state === "EVIDENCE_UNAVAILABLE") {
    lines.push(MISSING_COMPARISON_CAUTION);
  }
  if (coverage.researchNote) lines.push(`Research note: ${coverage.researchNote}`);
  const title = coverage.state === "RESEARCH_PENDING" && coverage.researchStatus === "NO_DEFENSIBLE_COMPARATOR"
    ? "No defensible comparison found"
    : TITLES[coverage.state];
  return { title, lines };
}

/** Areas to Investigate need a completed competency comparison. */
export function areasUnavailableMessage(coverage: CourseCoverage): string {
  if (coverage.state === "COMPARATORS_ONLY") {
    return "Areas to Investigate need a completed competency comparison against NYSC module headings, which is not available for this course.";
  }
  if (coverage.researchStatus === "NO_DEFENSIBLE_COMPARATOR") {
    return "Areas to Investigate are not available because research found no defensible comparator for this course.";
  }
  return "Areas to Investigate will be identified once comparison research is completed and a competency comparison is available.";
}
