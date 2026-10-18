import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorsForCourse } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

const records = (courseId: string) => {
  const grouped = comparatorsForCourse(courseId);
  return [...grouped.sriLanka, ...grouped.developingEmerging, ...grouped.developed];
};

test("Step 22 Cake Decorator courses load only substantial verified comparators", async () => {
  for (const courseId of ["COURSE-050", "COURSE-051"]) {
    await loadCourseComparison(courseId);
    assert.deepEqual(records(courseId).map((record) => record.record_id), [
      "LK-TVEC-NCS-CAKE-DECORATOR-2022",
      "IN-DGT-CTS-BAKER-V2",
      "SG-ITE-HNITEC-PASTRY-2Y",
    ]);
  }
  assert.equal(coverageForCourse("COURSE-050")!.state, "FULL_COMPARISON");
  assert.ok(mappingForCourse("COURSE-050"));
  assert.equal(coverageForCourse("COURSE-051")!.state, "COMPARATORS_ONLY");
  assert.equal(mappingForCourse("COURSE-051"), null);
});

test("Step 22 Areas use the unchanged two-FULL-comparator, two-country rule", async () => {
  await loadCourseComparison("COURSE-050");
  assert.deepEqual(
    investigationAreas(mappingForCourse("COURSE-050")!).map((area) => area.competency_id),
    ["cake_food_safety_hygiene"],
  );
});

test("the Sri Lankan Cake Decorator source remains a pending-review occupational standard", async () => {
  await loadCourseComparison("COURSE-050");
  const record = records("COURSE-050").find((item) => item.record_id === "LK-TVEC-NCS-CAKE-DECORATOR-2022")!;
  assert.equal(record.record_type, "occupational_standard");
  assert.equal(record.delivering_provider_verified, false);
  assert.equal(record.verification.status, "source_inspected_pending_human_review");
  assert.equal(record.verification.human_reviewed, false);
});
