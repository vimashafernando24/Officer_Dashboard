import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

for (const courseId of ["COURSE-013", "COURSE-079", "COURSE-080", "COURSE-081"]) {
  await loadCourseComparison(courseId);
}

const ids = (courseId: string) => {
  const grouped = comparatorsForCourse(courseId);
  return [...grouped.sriLanka, ...grouped.developingEmerging, ...grouped.developed].map((record) => record.record_id);
};

test("electronics courses load only occupation-specific servicing evidence", () => {
  const expected = ["LK-TVEC-NCS-ELECTRONIC-APPLIANCES-2017", "IN-DGT-CTS-MCEA-V2", "PH-TESDA-EPAS-NC2"];
  assert.deepEqual(ids("COURSE-013"), expected);
  assert.deepEqual(ids("COURSE-081"), expected);
  assert.equal(coverageForCourse("COURSE-013")!.state, "COMPARATORS_ONLY");
  assert.equal(mappingForCourse("COURSE-013"), null);
  assert.equal(coverageForCourse("COURSE-081")!.state, "FULL_COMPARISON");
});

test("motor control and winding exclude general-installation-only evidence", () => {
  assert.deepEqual(ids("COURSE-079"), [
    "LK-CGTTI-POWER-ELEC", "IN-DGT-CTS-ELEC-V3", "PH-TESDA-EIM-NC3", "AU-TAFENSW-UEE30820",
  ]);
  assert.deepEqual(ids("COURSE-080"), [
    "LK-TVEC-NCS-ELECTRIC-MOTOR-WINDER", "LK-CGTTI-POWER-ELEC", "IN-DGT-CTS-ELEC-V3", "AU-TGA-UEE30625",
  ]);
  for (const courseId of ["COURSE-079", "COURSE-080"]) {
    assert.equal(coverageForCourse(courseId)!.state, "COMPARATORS_ONLY");
    assert.equal(mappingForCourse(courseId), null);
    assert.ok(!ids(courseId).includes("PH-TESDA-EIM-NC2"));
  }
});

test("COURSE-081 areas use the unchanged two-record two-country rule", () => {
  assert.deepEqual(investigationAreas(mappingForCourse("COURSE-081")!).map((item) => item.competency_id), [
    "rtv_fault_diagnosis",
    "rtv_power_supply_repair",
    "rtv_audio_amplifier_repair",
  ]);
});

test("new records remain pending human review and are not presented as delivery", () => {
  for (const recordId of [
    "LK-TVEC-NCS-ELECTRONIC-APPLIANCES-2017", "IN-DGT-CTS-MCEA-V2", "PH-TESDA-EPAS-NC2",
    "LK-TVEC-NCS-ELECTRIC-MOTOR-WINDER", "AU-TGA-UEE30625",
  ]) {
    const record = findBenchmarkRecord(recordId)!;
    assert.equal(record.verification.status, "source_inspected_pending_human_review", recordId);
    assert.equal(record.verification.human_reviewed, false, recordId);
    assert.equal(record.delivering_provider_verified, false, recordId);
  }
});
