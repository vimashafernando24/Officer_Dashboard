import assert from "node:assert/strict";
import test from "node:test";

import comparatorLinks from "../../../../outputs/programme_benchmarking/course_comparator_links.json" with { type: "json" };
import { MAPPING_LOADERS, RECORD_DATASET_LOADERS, RECORD_DATASET_ORDER } from "../src/data/comparisonDataLoaders.ts";
import { courseNeedsData, loadAllComparisonData, loadCourseComparison } from "../src/comparisonData.ts";
import { BENCHMARK_RECORDS, comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { NYSC_COURSES } from "../src/programmeComparison.ts";
import { coverageForCourse, indexEntry } from "../src/programmeCoverage.ts";

// Each test file runs in its own process, so nothing is loaded when these tests start.
const ids = () => BENCHMARK_RECORDS.map((record) => record.record_id);
const shown = (courseId: string) => {
  const c = comparatorsForCourse(courseId);
  return [...c.sriLanka, ...c.developingEmerging, ...c.developed].map((record) => record.record_id);
};


test("coverage states for all 84 courses are available before any comparator data loads", () => {
  assert.equal(BENCHMARK_RECORDS.length, 0);
  assert.equal(mappingForCourse("COURSE-005"), null);
  const states: Record<string, number> = {};
  for (const course of NYSC_COURSES) {
    const coverage = coverageForCourse(course.course_id)!;
    states[coverage.state] = (states[coverage.state] ?? 0) + 1;
  }
  assert.deepEqual(states, { FULL_COMPARISON: 24, COMPARATORS_ONLY: 37, RESEARCH_PENDING: 23 });
});


test("courses without stored comparator data load nothing", async () => {
  assert.equal(courseNeedsData("COURSE-003"), false);
  await loadCourseComparison("COURSE-003");
  assert.equal(BENCHMARK_RECORDS.length, 0);
});


test("a course loads only its own datasets and mapping; variants share the same records", async () => {
  await loadCourseComparison("COURSE-005");
  assert.deepEqual(ids().sort(), [...indexEntry("COURSE-005")!.records].sort());
  assert.ok(mappingForCourse("COURSE-005"));
  assert.equal(mappingForCourse("COURSE-040"), null, "the other variant's mapping is not loaded yet");
  const shared = findBenchmarkRecord("LK-CGTTI-AUTO-TECH");

  await loadCourseComparison("COURSE-040");
  assert.equal(BENCHMARK_RECORDS.length, 5, "shared records are stored once");
  assert.equal(findBenchmarkRecord("LK-CGTTI-AUTO-TECH"), shared);
  assert.deepEqual(shown("COURSE-005"), shown("COURSE-040"));
  assert.ok(mappingForCourse("COURSE-040"));
  assert.equal(mappingForCourse("COURSE-025"), null);
});


test("loaded records keep the dataset order whatever order courses are viewed in", async () => {
  await loadCourseComparison("COURSE-012"); // RAC before Electrician
  await loadCourseComparison("COURSE-064");
  const expected: string[] = [];
  for (const key of RECORD_DATASET_ORDER.filter((k) => ["automotive", "electrical", "rac"].includes(k))) {
    const module = (await RECORD_DATASET_LOADERS[key]()).default as { records: { record_id: string }[] };
    expected.push(...module.records.map((record) => record.record_id));
  }
  assert.deepEqual(ids(), expected);
  assert.equal(BENCHMARK_RECORDS.length, 16);
});


test("the generated index and loaders agree with the stored links and mappings", async () => {
  await loadAllComparisonData();
  const links = new Map(comparatorLinks.links.map((link) => [link.nysc_course_id, link.record_ids]));
  for (const course of NYSC_COURSES) {
    const entry = indexEntry(course.course_id)!;
    assert.deepEqual(entry.records, links.get(course.course_id) ?? [], course.course_id);
    assert.equal(entry.mapping, course.course_id in MAPPING_LOADERS, course.course_id);
    assert.equal(entry.mapping, mappingForCourse(course.course_id) !== null, course.course_id);
    // Every linked record is displayable once its datasets are loaded, and nothing else is shown.
    assert.deepEqual(shown(course.course_id).sort(), [...entry.records].sort(), course.course_id);
  }
});


test("Areas counts are deterministic after on-demand loading", async () => {
  await loadAllComparisonData();
  const summary = (courseId: string) =>
    investigationAreas(mappingForCourse(courseId)!).map((a) => [a.competency_id, a.supporting_comparators.length, a.supporting_countries.length]);
  assert.deepEqual(summary("COURSE-005").map(([, n]) => n), [4, 4, 4, 3, 2]);
  assert.deepEqual(summary("COURSE-040").map(([, n]) => n), [4, 4, 4, 3, 3]);
  assert.deepEqual(summary("COURSE-025").map(([, n]) => n), [4, 2]);
  assert.deepEqual(summary("COURSE-064").map(([, n]) => n), [4, 2]);
  assert.deepEqual(summary("COURSE-034").map(([, n, c]) => [n, c]), [[5, 4], [5, 4], [5, 4], [3, 3], [2, 2], [2, 2]]);
  assert.deepEqual(summary("COURSE-012"), summary("COURSE-034"));
  assert.deepEqual(summary("COURSE-011"), summary("COURSE-047"));
  assert.deepEqual(summary("COURSE-011").map(([, n, c]) => [n, c]), [[3, 3], [3, 3], [3, 3], [2, 2], [2, 2]]);
  assert.deepEqual(summary("COURSE-007").map(([, n, c]) => [n, c]), [[4, 4], [3, 3], [3, 3]]);
});


test("unknown courses and datasets fail safely", async () => {
  assert.equal(coverageForCourse("COURSE-999"), null);
  assert.equal(courseNeedsData("COURSE-999"), false);
  await loadCourseComparison("COURSE-999");
});
