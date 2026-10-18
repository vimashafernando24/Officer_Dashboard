// Read-only access to the hand-curated competency mappings in
// outputs/programme_benchmarking/ (validated by test_competency_mapping.py),
// loaded on demand by comparisonData.ts into the registry below.
import { findBenchmarkRecord } from "./programmeBenchmarks.ts";

export type CompetencyStatus = "DOCUMENTED" | "NOT_EXPLICIT" | "INSUFFICIENT_DATA";

export interface CompetencyEvidence {
  module_index: number;
  /** "scope_verbatim" cites the record's verified qualification scope (module_index = passage index). */
  field: "title_verbatim" | "outcome_verbatim" | "scope_verbatim";
  code: string | null;
  /** Exact governed or stored source text. */
  text: string;
  /** A verified display correction of an NYSC heading; text keeps the governed original. */
  display_text?: string;
}

export type Coverage = "FULL" | "PARTIAL";

export interface CompetencyCell {
  status: CompetencyStatus;
  evidence: CompetencyEvidence[];
  note: string | null;
  /** Present on DOCUMENTED cells: FULL names every category component; PARTIAL names only some. */
  coverage?: Coverage;
  /** For PARTIAL cells: the component or limited activity the evidence supports. */
  supported_component?: string;
  /** The source covers a narrower equipment type or qualification scope; the note states it. */
  scope_limited?: boolean;
}

export interface MatrixColumn {
  column_id: string;
  kind: "nysc" | "benchmark";
  nysc_course_id?: string;
  record_id?: string;
  short_label: string;
}

export interface CompetencyMapping {
  nysc_course_id: string;
  human_reviewed: boolean;
  columns: MatrixColumn[];
  /** What each category requires: FULL names every component, PARTIAL only some. */
  category_components: Record<string, string[]>;
  competencies: { competency_id: string; label: string; cells: Record<string, CompetencyCell> }[];
}

export const STATUS_DETAILS: Record<CompetencyStatus, { symbol: string; label: string; meaning: string }> = {
  DOCUMENTED: {
    symbol: "✓",
    label: "Documented (full)",
    meaning: "Every component of the category is named in the stored text.",
  },
  NOT_EXPLICIT: {
    symbol: "–",
    label: "Not explicit",
    meaning: "Not documented within the available, assessed scope; this does not mean it is not taught.",
  },
  INSUFFICIENT_DATA: {
    symbol: "?",
    label: "Insufficient data",
    meaning: "Missing or incomplete material prevents a reliable assessment.",
  },
};

export const SCOPE_LIMITED_DETAILS = {
  symbol: "S",
  label: "Scope-limited",
  meaning: "The source covers a narrower equipment type or qualification scope; select the cell to read the limitation.",
};

/** The verified scope limitation of a cell, or null when the cell is not scope-limited. */
export function scopeLimitation(cell: CompetencyCell | undefined): string | null {
  return cell?.scope_limited ? cell.note ?? SCOPE_LIMITED_DETAILS.label : null;
}

export const PARTIAL_DETAILS = {
  symbol: "◐",
  label: "Documented (partial)",
  meaning: "Only a component of the category, or a limited activity, is named.",
};

/** Legend/cell presentation, distinguishing partial from full documentation. */
export function cellDisplay(cell: CompetencyCell): { key: CompetencyStatus | "PARTIAL"; symbol: string; label: string } {
  if (cell.status === "DOCUMENTED" && cell.coverage === "PARTIAL") {
    return { key: "PARTIAL", symbol: PARTIAL_DETAILS.symbol, label: PARTIAL_DETAILS.label };
  }
  const details = STATUS_DETAILS[cell.status];
  return { key: cell.status, symbol: details.symbol, label: details.label };
}

/** Only explicit FULL coverage counts as full support. */
export function isFullySupported(cell: CompetencyCell | undefined): boolean {
  return cell?.status === "DOCUMENTED" && cell.coverage === "FULL";
}

const MAPPINGS = new Map<string, CompetencyMapping>();

/** Adds a loaded competency mapping. */
export function registerMapping(mapping: CompetencyMapping): void {
  MAPPINGS.set(mapping.nysc_course_id, mapping);
}

/** The loaded mapping for a course, or null when none is curated or it is not loaded yet. */
export function mappingForCourse(courseId: string): CompetencyMapping | null {
  return MAPPINGS.get(courseId) ?? null;
}

/** A competency needs documented support from at least this many distinct comparator records... */
export const MIN_SUPPORTING_COMPARATORS = 2;
/** ...published in at least this many different countries. */
export const MIN_SUPPORTING_COUNTRIES = 2;

/** The published country of a comparator record, or undefined when the record is unknown or not loaded. */
export function recordCountry(recordId: string): string | undefined {
  return findBenchmarkRecord(recordId)?.country;
}

export interface InvestigationArea {
  competency_id: string;
  label: string;
  nysc_status: CompetencyStatus;
  /** Comparators documenting the competency with FULL coverage; only these are counted. */
  supporting_comparators: string[];
  /** Distinct countries of the FULL-coverage comparators, in column order. */
  supporting_countries: string[];
  /** Comparators documenting only part of the competency; shown, never counted. */
  partial_comparators: string[];
  /** Supporting comparators whose evidence is scope-limited (still counted). */
  scope_limited_comparators: string[];
}

/**
 * Deterministic areas to investigate: competencies the NYSC description does not
 * name (NOT_EXPLICIT) that at least two distinct comparator records, from at least
 * two different countries, document with FULL coverage. A record whose country is
 * unknown never counts towards the country threshold. PARTIAL evidence is reported
 * separately and never counted. INSUFFICIENT_DATA is never counted as absence, on
 * either side. Sorted by supporting-comparator count, then alphabetically by
 * competency name.
 */
export function investigationAreas(
  mapping: CompetencyMapping,
  countryOf: (recordId: string) => string | undefined = recordCountry,
): InvestigationArea[] {
  const nyscColumn = mapping.columns.find((column) => column.kind === "nysc");
  if (!nyscColumn) return [];
  const comparatorColumns = mapping.columns.filter((column) => column.kind === "benchmark");

  return mapping.competencies
    .filter((competency) => competency.cells[nyscColumn.column_id]?.status === "NOT_EXPLICIT")
    .map((competency) => {
      const supporting = new Map<string, string>();
      const countries = new Set<string>();
      const scopeLimited = new Set<string>();
      const partial = new Map<string, string>();
      for (const column of comparatorColumns) {
        if (!column.record_id) continue;
        const cell = competency.cells[column.column_id];
        if (isFullySupported(cell)) {
          supporting.set(column.record_id, column.short_label);
          const country = countryOf(column.record_id);
          if (country) countries.add(country);
          if (cell?.scope_limited) scopeLimited.add(column.short_label);
        } else if (cell?.status === "DOCUMENTED") {
          partial.set(column.record_id, column.short_label);
        }
      }
      return {
        competency_id: competency.competency_id,
        label: competency.label,
        nysc_status: competency.cells[nyscColumn.column_id].status,
        supporting_comparators: [...supporting.values()],
        supporting_countries: [...countries],
        partial_comparators: [...partial.values()],
        scope_limited_comparators: [...scopeLimited],
      };
    })
    .filter(
      (area) =>
        area.supporting_comparators.length >= MIN_SUPPORTING_COMPARATORS &&
        area.supporting_countries.length >= MIN_SUPPORTING_COUNTRIES,
    )
    .sort((a, b) =>
      b.supporting_comparators.length - a.supporting_comparators.length || a.label.localeCompare(b.label),
    );
}

export function matrixRowId(competencyId: string): string {
  return `pcd-matrix-row-${competencyId}`;
}
