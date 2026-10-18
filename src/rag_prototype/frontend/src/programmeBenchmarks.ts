// Read-only access to the curated benchmarking records. The files stay in
// outputs/programme_benchmarking/ (validated by test_programme_benchmarking_records.py)
// and are loaded on demand by comparisonData.ts, per selected course, into the
// registry below; the helpers here read whatever has been loaded.
import comparatorLinks from "../../../../outputs/programme_benchmarking/course_comparator_links.json" with { type: "json" };

export type BenchmarkRecordType = "programme" | "national_curriculum" | "occupational_standard" | "national_qualification";
export type CountryGroup = "sri_lanka" | "developing_emerging" | "developed";

export interface BenchmarkModule {
  published_ref: string | null;
  code: string | null;
  title_verbatim: string;
  outcome_verbatim: string | null;
  group: string | null;
}

export interface BenchmarkRecord {
  record_id: string;
  country: string;
  country_group: CountryGroup;
  institution: string;
  record_type: BenchmarkRecordType;
  delivering_provider_verified: boolean;
  title_verbatim: string;
  framework?: string;
  level_as_published: string | null;
  /** Verified qualification-scope passages, citable as evidence. */
  scope_verbatim?: string[] | null;
  duration_as_published: string | null;
  modules: BenchmarkModule[];
  content_fidelity: string;
  source: { url: string; publication_or_revision: string | null; retrieved_date: string };
  verification: { status: string; method: string; human_reviewed: boolean };
  /** Stored research notes, including source currency (e.g. a passed review date). */
  notes?: string[];
}

export interface CourseComparators {
  sriLanka: BenchmarkRecord[];
  developingEmerging: BenchmarkRecord[];
  developed: BenchmarkRecord[];
}

export const RECORD_TYPE_LABELS: Record<BenchmarkRecordType, string> = {
  programme: "Delivered Programme",
  national_curriculum: "National Curriculum",
  occupational_standard: "Occupational Standard",
  national_qualification: "National Qualification",
};

const VERIFICATION_LABELS: Record<string, string> = {
  source_inspected_pending_human_review: "Source inspected · pending human review",
  needs_manual_verbatim: "Exact wording not yet captured",
  search_only: "Search result only",
  human_verified: "Human verified",
};

const FIDELITY_LABELS: Record<string, string> = {
  verbatim: "Exact published wording",
  verbatim_whitespace_normalised: "Exact published wording (PDF spacing repaired)",
  verbatim_via_page_tool_pending_check: "Published wording, pending check against the source",
};

/**
 * Display rules re-applied at runtime: a record claiming to be a delivered
 * programme needs a verified provider, and paraphrased content never appears
 * as modules.
 */
export function isDisplayable(record: BenchmarkRecord): boolean {
  if (record.record_type === "programme" && !record.delivering_provider_verified) return false;
  if (record.content_fidelity === "paraphrased_needs_manual_copy" && record.modules.length > 0) return false;
  return true;
}

/** Displayable records loaded so far, in dataset order (filled by registerRecordDataset). */
export const BENCHMARK_RECORDS: BenchmarkRecord[] = [];

const RECORDS_BY_ID = new Map<string, BenchmarkRecord>();
const DATASETS = new Map<string, BenchmarkRecord[]>();

/**
 * Adds a loaded record dataset. Datasets are kept in the given order, so the
 * record list is stable however many courses have been viewed. Records shared
 * by several courses are stored once.
 */
export function registerRecordDataset(key: string, records: BenchmarkRecord[], order: string[]): void {
  if (DATASETS.has(key)) return;
  DATASETS.set(key, records.filter(isDisplayable));
  const ordered = [...DATASETS.keys()].sort((a, b) => order.indexOf(a) - order.indexOf(b));
  BENCHMARK_RECORDS.length = 0;
  for (const datasetKey of ordered) BENCHMARK_RECORDS.push(...DATASETS.get(datasetKey)!);
  for (const record of DATASETS.get(key)!) RECORDS_BY_ID.set(record.record_id, record);
}

/** A loaded, displayable record, or undefined. */
export function findBenchmarkRecord(recordId: string): BenchmarkRecord | undefined {
  return RECORDS_BY_ID.get(recordId);
}

const LINKED_IDS_BY_COURSE = new Map(
  comparatorLinks.links.map((link) => [link.nysc_course_id, link.record_ids]),
);

const CAVEAT_BY_COURSE = new Map(
  comparatorLinks.links.flatMap((link) =>
    "comparison_caveat" in link && link.comparison_caveat ? [[link.nysc_course_id, link.comparison_caveat]] : [],
  ),
);

export function comparatorsForCourse(courseId: string): CourseComparators {
  const records = (LINKED_IDS_BY_COURSE.get(courseId) ?? [])
    .map((recordId) => RECORDS_BY_ID.get(recordId))
    .filter((record): record is BenchmarkRecord => record !== undefined);
  return {
    sriLanka: records.filter((record) => record.country_group === "sri_lanka"),
    developingEmerging: records.filter((record) => record.country_group === "developing_emerging"),
    developed: records.filter((record) => record.country_group === "developed"),
  };
}

/** Only a completed human review is reported as verified. */
export function verificationLabel(record: BenchmarkRecord): string {
  if (record.verification.status === "human_verified" && !record.verification.human_reviewed) {
    return VERIFICATION_LABELS.source_inspected_pending_human_review;
  }
  return VERIFICATION_LABELS[record.verification.status] ?? record.verification.status;
}

export function fidelityLabel(record: BenchmarkRecord): string | null {
  return FIDELITY_LABELS[record.content_fidelity] ?? null;
}

/** Modules in published order, grouped under their published heading. */
export function groupModules(modules: BenchmarkModule[]): { group: string | null; modules: BenchmarkModule[] }[] {
  const groups: { group: string | null; modules: BenchmarkModule[] }[] = [];
  for (const module of modules) {
    const last = groups.at(-1);
    if (last && last.group === module.group) {
      last.modules.push(module);
    } else {
      groups.push({ group: module.group, modules: [module] });
    }
  }
  return groups;
}

export function comparatorCounts(comparators: CourseComparators): {
  sriLanka: number;
  developingEmerging: number;
  developed: number;
} {
  return {
    sriLanka: comparators.sriLanka.length,
    developingEmerging: comparators.developingEmerging.length,
    developed: comparators.developed.length,
  };
}

export interface ComparisonCaveat {
  text: string;
  /** Comparators whose records do not state a qualification level or duration. */
  unstated: { record: BenchmarkRecord; fields: string[] }[];
}

/** The course's comparison caveat, qualified by any comparator facts left unstated. */
export function comparisonCaveat(courseId: string): ComparisonCaveat | null {
  const text = CAVEAT_BY_COURSE.get(courseId);
  if (!text) return null;
  const { sriLanka, developingEmerging, developed } = comparatorsForCourse(courseId);
  const unstated = [...sriLanka, ...developingEmerging, ...developed]
    .map((record) => ({
      record,
      fields: [
        !record.level_as_published?.trim() && "qualification level",
        !record.duration_as_published?.trim() && "duration",
      ].filter((field): field is string => Boolean(field)),
    }))
    .filter(({ fields }) => fields.length > 0);
  return { text, unstated };
}

// ---- Display-only formatting. These never alter the stored record text. ----

export const MODULE_PREVIEW_LIMIT = 5;

export type ModulePreviewMode = "full" | "core-preview" | "first-items";

/**
 * The group of core units when a record explicitly publishes Basic, Common and
 * Core groups (the TESDA training-regulation structure); otherwise null. Nothing
 * is inferred about importance for records without that published structure.
 */
export function coreCompetencyGroup(modules: BenchmarkModule[]): string | null {
  const groups = [...new Set(modules.map((module) => module.group ?? ""))];
  const find = (prefix: RegExp) => groups.find((group) => prefix.test(group) && /competenc/i.test(group));
  return find(/^basic\b/i) && find(/^common\b/i) ? find(/^core\b/i) ?? null : null;
}

/**
 * Modules to show for a card. Expanded: every stored module in published order.
 * Collapsed: up to five core competencies for Basic/Common/Core records, else the
 * first five modules. The preview is never presented as the complete curriculum.
 */
export function modulePreview(
  modules: BenchmarkModule[],
  expanded: boolean,
): { mode: ModulePreviewMode; modules: BenchmarkModule[] } {
  if (expanded || modules.length <= MODULE_PREVIEW_LIMIT) return { mode: "full", modules };
  const core = coreCompetencyGroup(modules);
  if (core) {
    return { mode: "core-preview", modules: modules.filter((module) => module.group === core).slice(0, MODULE_PREVIEW_LIMIT) };
  }
  return { mode: "first-items", modules: modules.slice(0, MODULE_PREVIEW_LIMIT) };
}

/** Label and expanded state for the show-all / show-fewer control, or null when not needed. */
export function moduleDisclosure(total: number, expanded: boolean): { label: string; ariaExpanded: boolean } | null {
  if (total <= MODULE_PREVIEW_LIMIT) return null;
  return expanded
    ? { label: "Show fewer", ariaExpanded: true }
    : { label: `Show all ${total} modules / competencies`, ariaExpanded: false };
}

const WORD_NUMBERS: Record<string, string> = {
  one: "1", two: "2", three: "3", four: "4", five: "5", six: "6",
};

function count(token: string): string {
  return WORD_NUMBERS[token.toLowerCase()] ?? token;
}

function unit(value: string, singular: string): string {
  return `${value} ${singular}${value === "1" ? "" : "s"}`;
}

/**
 * A concise duration summary. It only restates a period or a total that the
 * published wording itself states; anything else is shown exactly as published.
 * `details` holds the original wording when the summary shortens it.
 */
export function durationDisplay(published: string | null): { summary: string; details: string | null } {
  const text = published?.trim();
  if (!text) return { summary: "Not stated", details: null };
  let summary: string | null = null;

  const fullTime = text.match(/^Full Time,\s*(\d+)\s*(Years?|Months?)$/i);
  const totalWithSil = text.match(/(\d+)\s*TOTAL HOURS$/i) ?? text.match(/(\d+)\s*Hours?\s*-\s*Total training duration$/i);
  const nominalTotal = text.match(/^Nominal Training Hours:.*Total(?: Course Hours)?:?\s*(\d+)\s*Hours$/i);
  const years = text.match(/^(\d+|one|two|three|four|five|six)\s+years?\b/i);

  if (fullTime) {
    summary = `${unit(fullTime[1], fullTime[2].toLowerCase().startsWith("year") ? "year" : "month")} (full-time)`;
  } else if (totalWithSil && /\bSIL\b/.test(text)) {
    // The published total combines nominal training hours and supervised industry learning (SIL).
    summary = `${totalWithSil[1]} total hours (including supervised industry learning)`;
  } else if (nominalTotal) {
    summary = `${nominalTotal[1]} nominal training hours`;
  } else if (years) {
    summary = unit(count(years[1]), "year");
  }

  if (!summary) return { summary: text, details: null };
  // Details are shown only when the published wording adds information the summary omits.
  const restatesOnly = Boolean(fullTime) || (years !== null && years[0].length === text.length);
  return { summary, details: restatesOnly ? null : text };
}

/**
 * Qualification shown with its own national framework, so levels from different
 * countries are never presented as equivalent. Only spacing and casing are
 * standardised; the level itself is never changed or inferred.
 */
export function qualificationDisplay(record: Pick<BenchmarkRecord, "level_as_published" | "framework">): {
  label: string;
  framework: string | null;
  code: string | null;
} {
  const level = record.level_as_published?.trim();
  if (!level) return { label: "Not stated", framework: null, code: null };
  const nsqf = level.match(/^NSQF\s*Level\s*[-:]?\s*(\d+)$/i);
  if (nsqf) return { label: `NSQF Level ${nsqf[1]}`, framework: record.framework ?? null, code: null };
  const coded = level.match(/^(.+?)\s*\(national code (\w+)\)$/i);
  if (coded) return { label: coded[1], framework: record.framework ?? null, code: coded[2] };
  return { label: level, framework: record.framework ?? null, code: null };
}
