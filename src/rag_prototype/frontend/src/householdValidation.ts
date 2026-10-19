// Validation for the household-count cluster questions. The rules mirror
// _household_counts_valid in new_respondent_cluster_assignment.py (and the
// original 08_/24_ clustering scripts): counts are whole, non-negative, the
// household has at least one member, and working + unemployed cannot exceed
// the household size. The backend silently treats violating answers as
// missing; this surfaces them to the officer before submission instead.

export const HOUSEHOLD_COUNT_MAX = 30;

export type HouseholdErrorKey =
  | "household.notWholeNumber"
  | "household.negative"
  | "household.sizeMin"
  | "household.max"
  | "household.exceedsSize"
  | "household.sumExceedsSize";

export interface FieldError {
  key: HouseholdErrorKey;
  vars?: Record<string, string | number>;
}

const SIZE = "household_size";
const WORKERS = "household_workers";
const UNEMPLOYED = "household_unemployed";

function parseCount(raw: string | undefined): { value: number | null; error: FieldError | null } {
  if (raw === undefined || raw.trim() === "") return { value: null, error: null };
  const value = Number(raw);
  if (!Number.isFinite(value) || !Number.isInteger(value)) {
    return { value: null, error: { key: "household.notWholeNumber" } };
  }
  if (value < 0) return { value: null, error: { key: "household.negative" } };
  if (value > HOUSEHOLD_COUNT_MAX) {
    return { value: null, error: { key: "household.max", vars: { max: HOUSEHOLD_COUNT_MAX } } };
  }
  return { value, error: null };
}

/**
 * Returns an error per numeric variable that currently has an invalid answer.
 * Empty answers are not errors here; the step's completeness check covers them.
 */
export function validateNumberAnswers(
  answers: Record<string, string>,
  numberVariables: string[],
): Record<string, FieldError> {
  const errors: Record<string, FieldError> = {};
  const values: Record<string, number | null> = {};

  for (const variable of numberVariables) {
    const { value, error } = parseCount(answers[variable]);
    values[variable] = value;
    if (error) errors[variable] = error;
  }

  const size = values[SIZE];
  if (size === 0) {
    errors[SIZE] = { key: "household.sizeMin" };
    return errors;
  }
  if (size == null) return errors;

  const workers = values[WORKERS];
  const unemployed = values[UNEMPLOYED];
  if (workers != null && workers > size) {
    errors[WORKERS] = { key: "household.exceedsSize", vars: { size } };
  }
  if (unemployed != null && unemployed > size) {
    errors[UNEMPLOYED] = { key: "household.exceedsSize", vars: { size } };
  }
  if (
    workers != null &&
    unemployed != null &&
    !errors[WORKERS] &&
    !errors[UNEMPLOYED] &&
    workers + unemployed > size
  ) {
    errors[UNEMPLOYED] = { key: "household.sumExceedsSize", vars: { size, workers, unemployed } };
  }
  return errors;
}
