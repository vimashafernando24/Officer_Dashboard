import assert from "node:assert/strict";
import test from "node:test";

import { HOUSEHOLD_COUNT_MAX, validateNumberAnswers } from "../src/householdValidation.ts";

const VARS = ["household_size", "household_workers", "household_unemployed"];

function check(size: string, workers: string, unemployed: string) {
  return validateNumberAnswers(
    { household_size: size, household_workers: workers, household_unemployed: unemployed },
    VARS,
  );
}

test("valid consistent counts have no errors", () => {
  assert.deepEqual(check("4", "2", "1"), {});
  assert.deepEqual(check("4", "2", "2"), {});
  assert.deepEqual(check("1", "0", "0"), {});
});

test("empty answers are not reported as errors", () => {
  assert.deepEqual(check("", "", ""), {});
  assert.deepEqual(check("3", "", ""), {});
});

test("decimals and non-numbers are rejected", () => {
  assert.equal(check("2.5", "1", "0").household_size?.key, "household.notWholeNumber");
  assert.equal(check("3", "abc", "0").household_workers?.key, "household.notWholeNumber");
});

test("negative counts are rejected", () => {
  assert.equal(check("3", "-1", "0").household_workers?.key, "household.negative");
  assert.equal(check("3", "0", "-2").household_unemployed?.key, "household.negative");
});

test("household size must include the member", () => {
  assert.equal(check("0", "0", "0").household_size?.key, "household.sizeMin");
});

test("counts above the maximum are rejected", () => {
  const errors = check(String(HOUSEHOLD_COUNT_MAX + 1), "1", "0");
  assert.equal(errors.household_size?.key, "household.max");
  assert.deepEqual(errors.household_size?.vars, { max: HOUSEHOLD_COUNT_MAX });
});

test("workers or unemployed cannot exceed household size", () => {
  assert.equal(check("3", "4", "0").household_workers?.key, "household.exceedsSize");
  assert.equal(check("3", "0", "5").household_unemployed?.key, "household.exceedsSize");
});

test("working plus unemployed cannot exceed household size", () => {
  const errors = check("4", "3", "2");
  assert.equal(errors.household_unemployed?.key, "household.sumExceedsSize");
  assert.deepEqual(errors.household_unemployed?.vars, { size: 4, workers: 3, unemployed: 2 });
  assert.equal(errors.household_workers, undefined);
});
