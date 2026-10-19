import assert from "node:assert/strict";
import test from "node:test";

import {
  comparatorsForCourse,
  comparisonCaveat,
  plainCaveatSummary,
  technicalCaveatText,
} from "../src/programmeBenchmarks.ts";
import type { BenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";
import { loadAllComparisonData } from "../src/comparisonData.ts";
import coverageIndex from "../src/data/coverageIndex.json" with { type: "json" };

await loadAllComparisonData();

const record = (type: BenchmarkRecord["record_type"]) => ({ record_type: type }) as BenchmarkRecord;

function summaryFor(courseId: string): string[] | null {
  const caveat = comparisonCaveat(courseId);
  const state = coverageForCourse(courseId)?.state;
  if (!caveat || (state !== "FULL_COMPARISON" && state !== "COMPARATORS_ONLY")) return null;
  const { sriLanka, developingEmerging, developed } = comparatorsForCourse(courseId);
  return plainCaveatSummary({
    state,
    records: [...sriLanka, ...developingEmerging, ...developed],
    unstatedCount: caveat.unstated.length,
  });
}

test("every course with a caveat gets a plain summary", () => {
  const withCaveat = Object.keys(coverageIndex.courses).filter((id) => comparisonCaveat(id));
  assert.equal(withCaveat.length, 75);
  for (const courseId of withCaveat) {
    const summary = summaryFor(courseId);
    assert.ok(summary, `${courseId} has no plain summary`);
    const text = summary.join(" ");
    assert.doesNotMatch(text, /COMPARATORS_ONLY|FULL_COMPARISON|governed/, courseId);
  }
});

test("the summary states the comparison mode from the coverage state", () => {
  assert.match(summaryFor("COURSE-005")![0], /^The NYSC course's published module headings are compared with 5 related training records\.$/);
  const comparatorsOnly = Object.keys(coverageIndex.courses).find((id) => coverageForCourse(id)?.state === "COMPARATORS_ONLY")!;
  assert.match(summaryFor(comparatorsOnly)![0], /^NYSC has not published a module list for this course/);
});

test("record types are counted, not inferred from the caveat text", () => {
  const mixed = plainCaveatSummary({
    state: "COMPARATORS_ONLY",
    records: [record("programme"), record("occupational_standard"), record("national_qualification")],
    unstatedCount: 0,
  });
  assert.ok(mixed.includes("2 of them are national standards, curricula or qualifications."));
  const allStandards = plainCaveatSummary({
    state: "COMPARATORS_ONLY",
    records: [record("occupational_standard"), record("national_curriculum")],
    unstatedCount: 0,
  });
  assert.ok(allStandards.includes("All of them are national standards, curricula or qualifications."));
  const delivered = plainCaveatSummary({ state: "FULL_COMPARISON", records: [record("programme")], unstatedCount: 0 });
  assert.ok(!delivered.some((line) => /standard/.test(line)));
});

test("missing length or level is reported from the unstated fields", () => {
  const caveat = comparisonCaveat("COURSE-025")!;
  assert.equal(caveat.unstated.length, 2);
  assert.ok(summaryFor("COURSE-025")!.some((line) => line === "Length or level is not published for 2 of them."));
});

test("technical text keeps the stored caveat and drops only the status code", () => {
  assert.equal(
    technicalCaveatText("COMPARATORS_ONLY: the governed NYSC course has no published headings to map."),
    "The governed NYSC course has no published headings to map.",
  );
  const unchanged = "Different programme duration and qualification levels; curriculum content comparison only.";
  assert.equal(technicalCaveatText(unchanged), unchanged);
});
