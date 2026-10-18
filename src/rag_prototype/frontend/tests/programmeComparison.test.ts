import assert from "node:assert/strict";
import test from "node:test";

import {
  COMPARISON_TABS,
  NYSC_COURSES,
  courseOptionLabel,
  coursesInSector,
  displayModules,
  findCourse,
  listSectors,
  sectorLabel,
} from "../src/programmeComparison.ts";


test("dropdowns are backed by the full governed catalogue snapshot", () => {
  assert.equal(NYSC_COURSES.length, 84);
  assert.equal(new Set(NYSC_COURSES.map((course) => course.course_id)).size, 84);
});


test("every course is reachable through exactly one sector", () => {
  const reachable = listSectors().flatMap((sector) => coursesInSector(sector));
  assert.equal(reachable.length, NYSC_COURSES.length);
  assert.equal(new Set(reachable.map((course) => course.course_id)).size, NYSC_COURSES.length);
});


test("an unstated sector is labelled plainly and listed last", () => {
  const sectors = listSectors();
  assert.equal(sectors.at(-1), "NOT_STATED");
  assert.equal(sectorLabel("NOT_STATED"), "Sector not stated");
  assert.equal(sectorLabel("ICT & Computing"), "ICT & Computing");
});


test("course labels distinguish courses that share a published title", () => {
  const electricians = coursesInSector("Electrical & Electronics")
    .filter((course) => course.course_name === "Electrician");
  assert.ok(electricians.length > 1);
  const labels = electricians.map(courseOptionLabel);
  assert.equal(new Set(labels).size, labels.length);
  assert.ok(labels.every((label) => label.includes("Electrician")));
});


test("course lookup returns the governed record or null", () => {
  assert.equal(findCourse("COURSE-005")?.course_name, "Automobile Mechanic");
  assert.equal(findCourse("COURSE-999"), null);
});


test("the dashboard exposes exactly the three approved tabs", () => {
  assert.deepEqual(
    COMPARISON_TABS.map(({ label }) => label),
    ["Overview", "Sri Lankan Programmes", "International Programmes"],
  );
});


test("display corrections keep the governed heading as the original", () => {
  const electrician = findCourse("COURSE-025");
  assert.ok(electrician);
  const modules = displayModules(electrician);
  assert.equal(modules.length, electrician.modules.length);
  assert.equal(modules[1].text, "Industrial Electrical Installation (Motor Controlling System)");
  assert.equal(modules[1].original, electrician.modules[1]);
  assert.equal(modules[0].original, null);
  assert.equal(modules[0].text, electrician.modules[0]);
});


test("unverifiable contamination is shown unchanged and flagged for review", () => {
  const course = findCourse("COURSE-009");
  assert.ok(course);
  const flagged = displayModules(course)[9];
  assert.equal(flagged.text, course.modules[9]);
  assert.equal(flagged.original, null);
  assert.equal(flagged.verifiedAgainst, null);
  assert.ok(flagged.reviewReason);
});


test("COURSE-012 heading 4 is corrected from its own source screenshot, keeping the governed text", () => {
  const refrigeration = findCourse("COURSE-012");
  assert.ok(refrigeration);
  const modules = displayModules(refrigeration);
  assert.equal(modules[3].text, "Operate and Maintain Central A/C System");
  assert.equal(modules[3].original, "Operate and Maintain Central A/C system gentle attitudes within a dis Screenshot unment.");
  assert.equal(modules[3].original, refrigeration.modules[3]);
  assert.equal(modules[3].verifiedAgainst, "CoursesSS/Screenshot 2026-04-12 at 22.26.56.png");
  assert.equal(modules[3].reviewReason, null);
  // The earlier heading 2 correction is unchanged and was not screenshot-based.
  assert.equal(modules[1].text, "Prepare Estimates");
  assert.equal(modules[1].verifiedAgainst, null);
});


test("courses without contamination display their governed headings exactly", () => {
  const mechanic = findCourse("COURSE-005");
  assert.ok(mechanic);
  assert.deepEqual(displayModules(mechanic).map((module) => module.text), mechanic.modules);
});
