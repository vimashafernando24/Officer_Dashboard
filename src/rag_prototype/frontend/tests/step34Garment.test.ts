import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse, coveragePresentation } from "../src/programmeCoverage.ts";

const COURSES = ["COURSE-037", "COURSE-063", "COURSE-085"];
const RECORD_IDS = [
  "LK-TVEC-NCS-TAILOR-R2-2017",
  "IN-DGT-CTS-SEWING-TECHNOLOGY-V2",
  "PH-TESDA-DRESSMAKING-NC2-2005",
];

for (const courseId of COURSES) await loadCourseComparison(courseId);

const ids = (courseId: string) => {
  const records = comparatorsForCourse(courseId);
  return [...records.sriLanka, ...records.developingEmerging, ...records.developed].map((record) => record.record_id);
};

test("Step 34 courses share the deduplicated garment records", () => {
  for (const courseId of COURSES) assert.deepEqual(ids(courseId), RECORD_IDS, courseId);
  assert.match(findBenchmarkRecord("PH-TESDA-DRESSMAKING-NC2-2005")!.notes.join(" "), /basic\/block patterns/i);
  assert.match(findBenchmarkRecord("LK-TVEC-NCS-TAILOR-R2-2017")!.notes.join(" "), /block templates/i);
});

test("only the two courses with governed headings render one-row matrices", () => {
  for (const courseId of ["COURSE-037", "COURSE-063"]) {
    const coverage = coverageForCourse(courseId)!;
    const mapping = mappingForCourse(courseId)!;
    assert.equal(coverage.state, "FULL_COMPARISON", courseId);
    assert.equal(mapping.competencies.length, 1, courseId);
    assert.equal(investigationAreas(mapping).length, 0, courseId);
    assert.deepEqual(coveragePresentation(coverage.state), { showComparators: true, showMatrix: true, showAreas: true });
  }
  const coverage = coverageForCourse("COURSE-085")!;
  assert.equal(coverage.state, "COMPARATORS_ONLY");
  assert.equal(mappingForCourse("COURSE-085"), null);
  assert.deepEqual(coveragePresentation(coverage.state), { showComparators: true, showMatrix: false, showAreas: false });
});

test("COURSE-063 keeps raw scheduling text but uses its approved content display", () => {
  const row = mappingForCourse("COURSE-063")!.competencies[0];
  const evidence = row.cells["NYSC-COURSE-063"].evidence[0];
  assert.equal(evidence.text, "Women and children clothing which will be held on weekends.");
  assert.equal(evidence.display_text, "Women and children clothing");
  assert.match(row.cells["LK-TVEC-NCS-TAILOR-R2-2017"].note!, /not method-equivalent/i);
});
