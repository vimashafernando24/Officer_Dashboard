import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

const EXPECTED: Record<string, string[]> = {
  "COURSE-002": ["IN-DGT-CTS-COPA-V3", "IN-DGT-CTS-AIPA-V1"],
  "COURSE-043": ["IN-DGT-ATS-CADCAM-OPERATOR-PROGRAMMER", "PH-TESDA-TECHNICAL-DRAFTING-NC2"],
  "COURSE-062": ["LK-TVEC-NCS-GRAPHIC-DESIGNER-2025", "PH-TESDA-VGD-NC3", "SG-ITE-HNITEC-COMMDESIGN-2Y", "IN-DGT-CTS-DTPO-V2"],
  "COURSE-073": ["PH-TESDA-PROGRAMMING-JAVA-NC3-2021"],
  "COURSE-076": ["IN-DGT-ATS-MECHANIC-EMBEDDED-PLC"],
};

for (const courseId of Object.keys(EXPECTED)) await loadCourseComparison(courseId);

const shownIds = (courseId: string) => {
  const records = comparatorsForCourse(courseId);
  return [...records.sriLanka, ...records.developingEmerging, ...records.developed].map((record) => record.record_id);
};

test("Step 33 courses load only their verified comparator records", () => {
  for (const [courseId, expected] of Object.entries(EXPECTED)) {
    assert.deepEqual(shownIds(courseId).sort(), [...expected].sort(), courseId);
  }
});

test("only Desktop Publisher has a competency matrix", () => {
  assert.equal(coverageForCourse("COURSE-062")!.state, "FULL_COMPARISON");
  const mapping = mappingForCourse("COURSE-062")!;
  assert.equal(mapping.competencies.length, 4);
  for (const row of mapping.competencies) {
    assert.equal(row.cells["IN-DGT-CTS-DTPO-V2"].coverage, "FULL");
  }
  for (const courseId of ["COURSE-002", "COURSE-043", "COURSE-073", "COURSE-076"]) {
    assert.equal(coverageForCourse(courseId)!.state, "COMPARATORS_ONLY", courseId);
    assert.equal(mappingForCourse(courseId), null, courseId);
  }
});

test("stored curricula expose the occupation-specific evidence used for links", () => {
  assert.ok(findBenchmarkRecord("IN-DGT-CTS-AIPA-V1")!.modules.some((unit) => /Python/i.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("IN-DGT-ATS-CADCAM-OPERATOR-PROGRAMMER")!.modules.some((unit) => /AutoCAD/i.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("IN-DGT-CTS-DTPO-V2")!.modules.some((unit) => /PageMaker/i.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("PH-TESDA-PROGRAMMING-JAVA-NC3-2021")!.modules.some((unit) => /Java/i.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("IN-DGT-ATS-MECHANIC-EMBEDDED-PLC")!.modules.some((unit) => /microcontroller/i.test(unit.title_verbatim)));
});
