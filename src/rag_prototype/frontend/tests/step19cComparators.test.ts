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

test("Step 19C courses lazy-load only their verified datasets and presentation modes", async () => {
  for (const [courseId, count] of [["COURSE-010", 4], ["COURSE-046", 4], ["COURSE-048", 4], ["COURSE-014", 3], ["COURSE-069", 3], ["COURSE-035", 4], ["COURSE-082", 4]] as const) {
    await loadCourseComparison(courseId);
    assert.equal(records(courseId).length, count, courseId);
  }
  for (const courseId of ["COURSE-010", "COURSE-046", "COURSE-014", "COURSE-035", "COURSE-082"]) {
    assert.equal(coverageForCourse(courseId)!.state, "FULL_COMPARISON", courseId);
    assert.ok(mappingForCourse(courseId), courseId);
  }
  for (const courseId of ["COURSE-048", "COURSE-069"]) {
    assert.equal(coverageForCourse(courseId)!.state, "COMPARATORS_ONLY", courseId);
    assert.equal(mappingForCourse(courseId), null, courseId);
  }
});

test("Step 19C Areas are derived from two FULL records in two countries", async () => {
  for (const courseId of ["COURSE-010", "COURSE-046", "COURSE-014", "COURSE-035", "COURSE-082"]) await loadCourseComparison(courseId);
  const ids = (courseId: string) => investigationAreas(mappingForCourse(courseId)!).map((area) => area.competency_id);
  assert.deepEqual(ids("COURSE-010"), ["hair_removal", "salon_hygiene_safety", "client_consultation"]);
  assert.deepEqual(ids("COURSE-046"), ["hair_removal", "salon_hygiene_safety", "client_consultation"]);
  assert.deepEqual(ids("COURSE-014"), ["hair_salon_safety"]);
  assert.deepEqual(ids("COURSE-035"), ["diary_appointments"]);
  assert.deepEqual(ids("COURSE-082"), ["diary_appointments", "filing_records", "office_software"]);
});

test("standards and qualifications remain distinct from delivered programmes", async () => {
  await loadCourseComparison("COURSE-010");
  const byId = new Map(records("COURSE-010").map((record) => [record.record_id, record]));
  assert.equal(byId.get("LK-TVEC-NCS-BEAUTICIAN-2020")!.record_type, "occupational_standard");
  assert.equal(byId.get("IN-DGT-CTS-COSMETOLOGY-V2")!.record_type, "national_curriculum");
  assert.equal(byId.get("SG-ITE-HNITEC-BEAUTY-2Y")!.record_type, "programme");
  assert.equal(byId.get("AU-TGA-SHB40121")!.record_type, "national_qualification");
});
