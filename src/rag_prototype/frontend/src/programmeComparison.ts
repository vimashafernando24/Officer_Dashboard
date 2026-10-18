import catalogue from "./data/nyscCourseCatalogue.json" with { type: "json" };

export interface NyscCourse {
  course_id: string;
  course_name: string;
  skill_area: string;
  attendance_type: string;
  nvq_level: string;
  qualification_type: string;
  duration_months: string;
  modules: string[];
  module_display_corrections: {
    module_index: number;
    original: string;
    displayed: string;
    removed_fragments: string[];
    rule: string;
    /** Present when the heading was verified against the course's own source screenshot. */
    source_screenshot?: string;
    source_screenshot_sha256?: string;
  }[];
  module_review_flags: { module_index: number; text: string; reason: string }[];
}

export interface DisplayModule {
  text: string;
  /** The governed heading, when a display-only correction was applied. */
  original: string | null;
  /** Why the heading still needs manual review, if it does. */
  reviewReason: string | null;
  /** The course's own source screenshot the correction was verified against, if any. */
  verifiedAgainst: string | null;
}

export type ComparisonTab = "overview" | "sri-lanka" | "international";

export const COMPARISON_TABS: { id: ComparisonTab; label: string }[] = [
  { id: "overview", label: "Overview" },
  { id: "sri-lanka", label: "Sri Lankan Programmes" },
  { id: "international", label: "International Programmes" },
];

const NOT_STATED = "NOT_STATED";

export const NYSC_COURSES: NyscCourse[] = catalogue.courses;

export function sectorLabel(skillArea: string): string {
  return skillArea === NOT_STATED ? "Sector not stated" : skillArea;
}

/** Sectors in alphabetical order, with an unstated sector listed last. */
export function listSectors(courses: NyscCourse[] = NYSC_COURSES): string[] {
  return [...new Set(courses.map((course) => course.skill_area))].sort((a, b) => {
    if (a === NOT_STATED) return 1;
    if (b === NOT_STATED) return -1;
    return a.localeCompare(b);
  });
}

export function coursesInSector(sector: string, courses: NyscCourse[] = NYSC_COURSES): NyscCourse[] {
  return courses
    .filter((course) => course.skill_area === sector)
    .sort((a, b) => a.course_name.localeCompare(b.course_name) || a.course_id.localeCompare(b.course_id));
}

/** Several centres publish the same title, so the label carries attendance and ID. */
export function courseOptionLabel(course: NyscCourse): string {
  const attendance = course.attendance_type === NOT_STATED ? null : course.attendance_type;
  return [course.course_name, attendance, course.course_id].filter(Boolean).join(" · ");
}

export function findCourse(courseId: string, courses: NyscCourse[] = NYSC_COURSES): NyscCourse | null {
  return courses.find((course) => course.course_id === courseId) ?? null;
}

function stated(value: string): string | null {
  return value && value !== NOT_STATED ? value : null;
}

/** Catalogue facts for the course summary; unstated fields read "Not stated". */
export function courseSummaryFacts(course: NyscCourse): { label: string; value: string }[] {
  const qualification = [stated(course.qualification_type), stated(course.nvq_level)]
    .filter(Boolean)
    .join(" · ");
  const months = stated(course.duration_months);
  return [
    { label: "Qualification", value: qualification || "Not stated" },
    { label: "Duration", value: months ? `${months} month${months === "1" ? "" : "s"}` : "Not stated" },
    { label: "Attendance", value: stated(course.attendance_type) ?? "Not stated" },
  ];
}

/**
 * Module headings for display. Governed text is shown unchanged unless the
 * snapshot records a verified display-only correction, which keeps the original.
 */
export function displayModules(course: NyscCourse): DisplayModule[] {
  const corrections = new Map(course.module_display_corrections.map((c) => [c.module_index, c]));
  const flags = new Map(course.module_review_flags.map((f) => [f.module_index, f]));
  return course.modules.map((module, index) => {
    const correction = corrections.get(index);
    return {
      text: correction?.displayed ?? module,
      original: correction ? correction.original : null,
      reviewReason: flags.get(index)?.reason ?? null,
      verifiedAgainst: correction?.source_screenshot ?? null,
    };
  });
}
