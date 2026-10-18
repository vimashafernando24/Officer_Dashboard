import assert from "node:assert/strict";
import test from "node:test";

import coverageRegister from "../../../../outputs/programme_benchmarking/coverage_register.json" with { type: "json" };
import { NYSC_COURSES } from "../src/programmeComparison.ts";
import { comparatorsForCourse } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import {
  EVIDENCE_REVIEW_NOTICE,
  MISSING_COMPARISON_CAUTION,
  areasUnavailableMessage,
  coverageForCourse,
  coverageNote,
  coveragePresentation,
  deriveCoverageState,
  headingsMessage,
  registerCurrentMode,
  researchMessage,
} from "../src/programmeCoverage.ts";
import type { CourseCoverage } from "../src/programmeCoverage.ts";
import { loadAllComparisonData } from "../src/comparisonData.ts";

// Comparator data is loaded on demand in the dashboard; tests load all of it first.
await loadAllComparisonData();

const COMPLETE = ["COURSE-005", "COURSE-006", "COURSE-007", "COURSE-008", "COURSE-009", "COURSE-010", "COURSE-011", "COURSE-012", "COURSE-014", "COURSE-025", "COURSE-034", "COURSE-035", "COURSE-037", "COURSE-040", "COURSE-041", "COURSE-046", "COURSE-047", "COURSE-050", "COURSE-053", "COURSE-055", "COURSE-058", "COURSE-062", "COURSE-063", "COURSE-064", "COURSE-071", "COURSE-081", "COURSE-082", "COURSE-087"];
const COMPARATORS_ONLY = ["COURSE-001", "COURSE-002", "COURSE-004", "COURSE-013", "COURSE-016", "COURSE-017", "COURSE-018", "COURSE-019", "COURSE-020", "COURSE-021", "COURSE-022", "COURSE-023", "COURSE-024", "COURSE-026", "COURSE-028", "COURSE-029", "COURSE-030", "COURSE-031", "COURSE-032", "COURSE-033", "COURSE-036", "COURSE-038", "COURSE-042", "COURSE-043", "COURSE-044", "COURSE-045", "COURSE-048", "COURSE-051", "COURSE-052", "COURSE-054", "COURSE-056", "COURSE-057", "COURSE-059", "COURSE-060", "COURSE-061", "COURSE-065", "COURSE-066", "COURSE-068", "COURSE-069", "COURSE-073", "COURSE-076", "COURSE-077", "COURSE-078", "COURSE-079", "COURSE-080", "COURSE-084", "COURSE-085"];
const ALL_IDS = NYSC_COURSES.map((course) => course.course_id);
const registerById = new Map(coverageRegister.courses.map((entry) => [entry.course_id, entry]));
const shownRecords = (courseId: string) => {
  const c = comparatorsForCourse(courseId);
  return [...c.sriLanka, ...c.developingEmerging, ...c.developed];
};


test("every one of the 84 governed courses has a coverage state that matches the register", () => {
  assert.equal(ALL_IDS.length, 84);
  assert.equal(new Set(ALL_IDS).size, 84);
  for (const courseId of ALL_IDS) {
    const coverage = coverageForCourse(courseId);
    assert.ok(coverage, courseId);
    // The dashboard derives its state from verified evidence; the register records the same state.
    assert.equal(coverage.state, registerCurrentMode(courseId), courseId);
  }
});


test("the 28 mapped courses keep their full comparison", () => {
  for (const courseId of COMPLETE) {
    const coverage = coverageForCourse(courseId)!;
    assert.equal(coverage.state, "FULL_COMPARISON", courseId);
    assert.deepEqual(coveragePresentation(coverage.state), { showComparators: true, showMatrix: true, showAreas: true });
    assert.ok(mappingForCourse(courseId), courseId);
    if (["COURSE-037", "COURSE-062", "COURSE-063"].includes(courseId)) {
      assert.equal(investigationAreas(mappingForCourse(courseId)!).length, 0, courseId);
    } else {
      assert.ok(investigationAreas(mappingForCourse(courseId)!).length > 0, courseId);
    }
  }
});


test("all 9 researched-but-unresolved courses show RESEARCH_PENDING with their documented reason", () => {
  const pending = ALL_IDS.filter((id) => !COMPLETE.includes(id) && !COMPARATORS_ONLY.includes(id));
  assert.equal(pending.length, 9);
  for (const courseId of pending) {
    const coverage = coverageForCourse(courseId)!;
    const entry = registerById.get(courseId)!;
    assert.equal(entry.research_status, "NO_DEFENSIBLE_COMPARATOR", courseId);
    assert.equal(coverage.state, "RESEARCH_PENDING", courseId);
    assert.deepEqual(coveragePresentation(coverage.state), { showComparators: false, showMatrix: false, showAreas: false });
    assert.equal(shownRecords(courseId).length, 0, courseId);
    const note = coverageNote(coverage);
    assert.equal(note.title, "No defensible comparison found");
    assert.match(note.lines[0], /research was carried out/);
    assert.ok(note.lines.includes(MISSING_COMPARISON_CAUTION), courseId);
    assert.ok(note.lines.includes(`Research note: ${entry.notes[0]}`), courseId);
    assert.match(areasUnavailableMessage(coverage), /no defensible comparator/);
  }
});


test("a genuinely unresearched course keeps the not-yet-completed wording", () => {
  const coverage = { ...coverageForCourse("COURSE-049")!, researchStatus: "NOT_RESEARCHED" as const, researchNote: null };
  const note = coverageNote(coverage);
  assert.equal(note.title, "Comparison research not yet completed");
  assert.match(note.lines[0], /comparison research has not yet been completed/);
  assert.match(areasUnavailableMessage(coverage), /once comparison research is completed/);
});


test("the dashboard review notice never implies human verification", () => {
  assert.match(EVIDENCE_REVIEW_NOTICE, /not yet been independently reviewed/);
  assert.match(EVIDENCE_REVIEW_NOTICE, /provisional/);
  assert.doesNotMatch(EVIDENCE_REVIEW_NOTICE, /\bverified\b|\bapproved\b|\bconfirmed\b/i);
});


test("no course displays unverified comparator data", () => {
  for (const courseId of ALL_IDS) {
    const records = shownRecords(courseId);
    // Only records linked in the register (and so verified and stored) are shown.
    assert.deepEqual(
      records.map((record) => record.record_id).sort(),
      [...registerById.get(courseId)!.comparator_record_ids].sort(),
      courseId,
    );
    for (const record of records) {
      assert.ok(
        ["source_inspected_pending_human_review", "human_verified"].includes(record.verification.status),
        `${courseId} ${record.record_id}`,
      );
      assert.notEqual(record.content_fidelity, "paraphrased_needs_manual_copy");
    }
    // A proposed future mode never turns into displayed coverage.
    if (coverageForCourse(courseId)!.state === "RESEARCH_PENDING") {
      assert.equal(records.length, 0, courseId);
    }
  }
});


test("missing NYSC headings and missing external evidence are explained separately", () => {
  const byAvailability: Record<string, string[]> = {};
  for (const courseId of ALL_IDS) {
    const coverage = coverageForCourse(courseId)!;
    (byAvailability[coverage.evidenceAvailability] ??= []).push(courseId);
    const heading = headingsMessage(coverage);
    const research = researchMessage(coverage);
    assert.match(heading, /^NYSC module headings:/, courseId);
    assert.match(research, /^Comparator programmes:/, courseId);
    // Neither message speaks for the other kind of evidence.
    assert.doesNotMatch(heading, /comparator|research/i, courseId);
    assert.doesNotMatch(research, /NYSC module heading/i, courseId);
  }
  assert.equal(byAvailability.HEADINGS_AVAILABLE.length, 29);
  assert.equal(byAvailability.NO_HEADINGS.length, 52);
  assert.deepEqual(byAvailability.HEADINGS_UNUSABLE, ["COURSE-072", "COURSE-074", "COURSE-086"]);

  assert.equal(headingsMessage(coverageForCourse("COURSE-001")!), "NYSC module headings: none published for this course, so a competency matrix cannot be assessed from the governed catalogue.");
  assert.equal(headingsMessage(coverageForCourse("COURSE-007")!), "NYSC module headings: 6 usable headings published for this course.");
  assert.equal(headingsMessage(coverageForCourse("COURSE-009")!), "NYSC module headings: 9 usable headings published for this course.");
  assert.match(headingsMessage(coverageForCourse("COURSE-072")!), /names no curriculum content/);
  // A course with headings but no research is still pending: headings are not comparator evidence.
  assert.equal(coverageForCourse("COURSE-075")!.state, "RESEARCH_PENDING");
});


test("COURSE-056 shows its verified comparators without a competency matrix", () => {
  const coverage = coverageForCourse("COURSE-056")!;
  assert.equal(coverage.state, "COMPARATORS_ONLY");
  assert.equal(coverage.evidenceAvailability, "NO_HEADINGS");
  assert.equal(coverage.hasMapping, false);
  assert.equal(mappingForCourse("COURSE-056"), null);
  assert.deepEqual(coveragePresentation(coverage.state), { showComparators: true, showMatrix: false, showAreas: false });
  assert.deepEqual(shownRecords("COURSE-056"), shownRecords("COURSE-008"));
  assert.equal(shownRecords("COURSE-056").length, 3);
  assert.match(researchMessage(coverage), /without a competency matrix, because no defensible NYSC mapping is available/);
  assert.match(headingsMessage(coverage), /none published/);
  assert.match(areasUnavailableMessage(coverage), /not available for this course/);
});


test("future comparator-only records are shown without a competency matrix", () => {
  const future: CourseCoverage = {
    courseId: "COURSE-X",
    state: deriveCoverageState({ comparatorCount: 3, hasMapping: false, researchStatus: "COMPLETE" }),
    researchStatus: "COMPLETE",
    evidenceAvailability: "NO_HEADINGS",
    verifiedHeadingCount: 0,
    comparatorCount: 3,
    hasMapping: false,
    blockingEvidence: null,
  };
  assert.equal(future.state, "COMPARATORS_ONLY");
  assert.deepEqual(coveragePresentation(future.state), { showComparators: true, showMatrix: false, showAreas: false });
  assert.equal(coverageNote(future).title, "Comparator programmes only");
  assert.match(researchMessage(future), /without a competency matrix/);
  assert.ok(!coverageNote(future).lines.includes(MISSING_COMPARISON_CAUTION));
  assert.match(areasUnavailableMessage(future), /not available for this course/);
  // With usable headings, comparator-only means the mapping is still to do.
  assert.match(researchMessage({ ...future, evidenceAvailability: "HEADINGS_AVAILABLE" }), /mapping has not been completed yet/);
});


test("evidence is unavailable only when documented research was blocked", () => {
  assert.equal(deriveCoverageState({ comparatorCount: 0, hasMapping: false, researchStatus: "BLOCKED" }), "EVIDENCE_UNAVAILABLE");
  assert.equal(deriveCoverageState({ comparatorCount: 0, hasMapping: false, researchStatus: "NOT_RESEARCHED" }), "RESEARCH_PENDING");
  assert.equal(deriveCoverageState({ comparatorCount: 0, hasMapping: false, researchStatus: "IN_PROGRESS" }), "RESEARCH_PENDING");
  assert.equal(deriveCoverageState({ comparatorCount: 0, hasMapping: false, researchStatus: "COMPLETE" }), "RESEARCH_PENDING");
  const blocked: CourseCoverage = {
    courseId: "COURSE-Y", state: "EVIDENCE_UNAVAILABLE", researchStatus: "BLOCKED",
    evidenceAvailability: "NO_HEADINGS", verifiedHeadingCount: 0, comparatorCount: 0, hasMapping: false,
    blockingEvidence: "the official curriculum is available only on request",
  };
  assert.equal(coverageNote(blocked).title, "Comparison evidence insufficient");
  assert.match(researchMessage(blocked), /research was attempted, but the documented evidence is insufficient: the official curriculum/);
  assert.ok(coverageNote(blocked).lines.includes(MISSING_COMPARISON_CAUTION));
  // No current course is blocked.
  assert.ok(ALL_IDS.every((id) => coverageForCourse(id)!.state !== "EVIDENCE_UNAVAILABLE"));
});
