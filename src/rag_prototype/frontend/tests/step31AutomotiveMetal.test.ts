import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorCounts, comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse, coveragePresentation } from "../src/programmeCoverage.ts";

const EXPECTED: Record<string, [string[], { sriLanka: number; developingEmerging: number; developed: number }]> = {
  "COURSE-038": [["IN-DGT-CTS-2W3W-V2"], { sriLanka: 0, developingEmerging: 1, developed: 0 }],
  "COURSE-017": [["IN-DGT-CTS-AGMACH-V2", "PH-TESDA-AGMACH-4WT-NC3", "AU-TGA-AUR30420"], { sriLanka: 0, developingEmerging: 2, developed: 1 }],
  "COURSE-045": [["LK-TVEC-NCS-WELDER-R3", "IN-DGT-CTS-WELDER-V2", "AU-TGA-MEM31925-WELDING"], { sriLanka: 1, developingEmerging: 1, developed: 1 }],
  "COURSE-044": [["LK-TVEC-NCS-MACHINIST-R2", "PH-TESDA-MACHINING-NC2", "AU-TGA-MEM30219-MACHINING"], { sriLanka: 1, developingEmerging: 1, developed: 1 }],
  "COURSE-018": [["LK-TVEC-NCS-ALUMINIUM-FABRICATOR-2022"], { sriLanka: 1, developingEmerging: 0, developed: 0 }],
};

for (const courseId of Object.keys(EXPECTED)) await loadCourseComparison(courseId);

const shownIds = (courseId: string) => {
  const records = comparatorsForCourse(courseId);
  return [...records.sriLanka, ...records.developingEmerging, ...records.developed].map((record) => record.record_id);
};

test("Step 31 courses render verified comparator-only coverage", () => {
  for (const [courseId, [expectedIds, counts]] of Object.entries(EXPECTED)) {
    assert.deepEqual(shownIds(courseId).sort(), [...expectedIds].sort(), courseId);
    assert.deepEqual(comparatorCounts(comparatorsForCourse(courseId)), counts, courseId);
    const coverage = coverageForCourse(courseId)!;
    assert.equal(coverage.state, "COMPARATORS_ONLY", courseId);
    assert.equal(coverage.evidenceAvailability, "NO_HEADINGS", courseId);
    assert.equal(coverage.hasMapping, false, courseId);
    assert.equal(mappingForCourse(courseId), null, courseId);
    assert.deepEqual(coveragePresentation(coverage.state), { showComparators: true, showMatrix: false, showAreas: false });
  }
});

test("specialist records expose the verified occupational content", () => {
  assert.ok(findBenchmarkRecord("IN-DGT-CTS-2W3W-V2")!.modules.some((unit) => /two and three wheelers/i.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("PH-TESDA-AGMACH-4WT-NC3")!.modules.every((unit) => /4-Wheel Tractor/.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("LK-TVEC-NCS-WELDER-R3")!.modules.some((unit) => unit.code === "D28S002U19"));
  assert.ok(findBenchmarkRecord("PH-TESDA-MACHINING-NC2")!.modules.some((unit) => unit.code === "MEE722303"));
  assert.equal(findBenchmarkRecord("LK-TVEC-NCS-ALUMINIUM-FABRICATOR-2022")!.modules.length, 14);
});
