import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorCounts, comparatorsForCourse } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse, coveragePresentation } from "../src/programmeCoverage.ts";

// Only the data these courses need is loaded, as the dashboard would.
for (const courseId of ["COURSE-041", "COURSE-071", "COURSE-084", "COURSE-049"]) await loadCourseComparison(courseId);


test("Preschool Teacher and Human Resources Management show full comparisons", () => {
  for (const courseId of ["COURSE-041", "COURSE-071"]) {
    const coverage = coverageForCourse(courseId)!;
    assert.equal(coverage.state, "FULL_COMPARISON", courseId);
    assert.deepEqual(coveragePresentation(coverage.state), { showComparators: true, showMatrix: true, showAreas: true });
    assert.ok(mappingForCourse(courseId), courseId);
  }
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-041")), { sriLanka: 1, developingEmerging: 1, developed: 1 });
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-071")), { sriLanka: 2, developingEmerging: 0, developed: 1 });
  assert.deepEqual(investigationAreas(mappingForCourse("COURSE-071")!).map((a) => a.label), ["Workplace health and safety"]);
  assert.equal(investigationAreas(mappingForCourse("COURSE-041")!).length, 4);
});


test("Store Management shows comparators without a matrix; Business Management stays pending", () => {
  assert.equal(coverageForCourse("COURSE-084")!.state, "COMPARATORS_ONLY");
  assert.equal(mappingForCourse("COURSE-084"), null);
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-084")), { sriLanka: 1, developingEmerging: 1, developed: 1 });
  assert.equal(coverageForCourse("COURSE-049")!.state, "RESEARCH_PENDING");
});
