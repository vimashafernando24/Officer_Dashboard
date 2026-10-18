import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorCounts, comparatorsForCourse, coreCompetencyGroup, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

for (const courseId of ["COURSE-020", "COURSE-026", "COURSE-032"]) await loadCourseComparison(courseId);


test("the three agriculture courses show comparators without a matrix", () => {
  const expected: Record<string, { sriLanka: number; developingEmerging: number; developed: number }> = {
    "COURSE-020": { sriLanka: 1, developingEmerging: 2, developed: 1 },
    "COURSE-026": { sriLanka: 1, developingEmerging: 2, developed: 0 },
    "COURSE-032": { sriLanka: 1, developingEmerging: 2, developed: 1 },
  };
  for (const [courseId, counts] of Object.entries(expected)) {
    assert.equal(coverageForCourse(courseId)!.state, "COMPARATORS_ONLY", courseId);
    assert.equal(mappingForCourse(courseId), null, courseId);
    assert.deepEqual(comparatorCounts(comparatorsForCourse(courseId)), counts, courseId);
  }
});


test("new TESDA agriculture cards preview their core competencies", () => {
  for (const id of ["PH-TESDA-LANDSCAPE-NC2", "PH-TESDA-AGRI-CROPS-NC3", "PH-TESDA-HORTICULTURE-NC3"]) {
    assert.equal(coreCompetencyGroup(findBenchmarkRecord(id)!.modules), "Core Competencies", id);
  }
});
