import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorCounts, comparatorsForCourse } from "../src/programmeBenchmarks.ts";
import { mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

const COMPARATORS: Record<string, { sriLanka: number; developingEmerging: number; developed: number }> = {
  "COURSE-031": { sriLanka: 1, developingEmerging: 1, developed: 1 },
  "COURSE-059": { sriLanka: 1, developingEmerging: 3, developed: 0 },
  "COURSE-028": { sriLanka: 1, developingEmerging: 0, developed: 0 },
  "COURSE-066": { sriLanka: 0, developingEmerging: 0, developed: 2 },
  "COURSE-004": { sriLanka: 0, developingEmerging: 0, developed: 2 },
};
const PENDING = ["COURSE-003", "COURSE-049", "COURSE-067", "COURSE-070", "COURSE-072", "COURSE-074", "COURSE-075", "COURSE-083", "COURSE-086"];

for (const courseId of [...Object.keys(COMPARATORS), ...PENDING]) await loadCourseComparison(courseId);


test("media, gem-cutting and Professional English courses show comparators without a matrix", () => {
  for (const [courseId, counts] of Object.entries(COMPARATORS)) {
    assert.equal(coverageForCourse(courseId)!.state, "COMPARATORS_ONLY", courseId);
    assert.equal(mappingForCourse(courseId), null, courseId);
    assert.deepEqual(comparatorCounts(comparatorsForCourse(courseId)), counts, courseId);
  }
});


test("unsupported courses remain research pending with no comparators", () => {
  for (const courseId of PENDING) {
    assert.equal(coverageForCourse(courseId)!.state, "RESEARCH_PENDING", courseId);
    assert.deepEqual(comparatorCounts(comparatorsForCourse(courseId)), { sriLanka: 0, developingEmerging: 0, developed: 0 }, courseId);
  }
});
