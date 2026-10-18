import assert from "node:assert/strict";
import test from "node:test";

import {
  BENCHMARK_RECORDS,
  MODULE_PREVIEW_LIMIT,
  coreCompetencyGroup,
  durationDisplay,
  groupModules,
  moduleDisclosure,
  modulePreview,
  qualificationDisplay,
} from "../src/programmeBenchmarks.ts";
import { loadAllComparisonData } from "../src/comparisonData.ts";

// Comparator data is loaded on demand in the dashboard; tests load all of it first.
await loadAllComparisonData();

const TESDA_IDS = [
  "PH-TESDA-ASER-NC2",
  "PH-TESDA-EIM-NC2",
  "PH-TESDA-EIM-NC3",
  "PH-TESDA-DOMRAC-NC2",
  "PH-TESDA-CAC-NC3",
  "PH-TESDA-CSS-NC2",
  "PH-TESDA-PRO-COOKERY-NC3",
  "PH-TESDA-WEBDEV-NC3",
  "PH-TESDA-MOTORCYCLE-NC2",
  "PH-TESDA-ASER-ELEC-NC2",
  "PH-TESDA-MOBILE-NC3",
  "PH-TESDA-VGD-NC3",
  "PH-TESDA-AGRI-CROPS-NC3",
  "PH-TESDA-LANDSCAPE-NC2",
  "PH-TESDA-HORTICULTURE-NC3",
  "PH-TESDA-FILM-VIDEO-POSTPRODUCTION-NC3",
  "PH-TESDA-3D-ANIMATION-NC3",
];

const byId = new Map(BENCHMARK_RECORDS.map((record) => [record.record_id, record]));
const record = (id: string) => byId.get(id)!;


test("Show all reveals every stored item in published order, with nothing omitted", () => {
  for (const item of BENCHMARK_RECORDS) {
    const all = modulePreview(item.modules, true);
    assert.equal(all.mode, "full", item.record_id);
    assert.deepEqual(all.modules, item.modules);
    assert.deepEqual(
      groupModules(all.modules).map(({ group }) => group),
      groupModules(item.modules).map(({ group }) => group),
    );
  }
});


test("programmes without Basic/Common/Core groups keep the first-five preview", () => {
  for (const item of BENCHMARK_RECORDS.filter((r) => !TESDA_IDS.includes(r.record_id))) {
    assert.equal(coreCompetencyGroup(item.modules), null, item.record_id);
    const preview = modulePreview(item.modules, false);
    // Records with five or fewer items show them all; longer ones show the first five.
    assert.equal(preview.mode, item.modules.length > MODULE_PREVIEW_LIMIT ? "first-items" : "full", item.record_id);
    assert.deepEqual(preview.modules, item.modules.slice(0, MODULE_PREVIEW_LIMIT));
  }
});


test("TESDA previews show their core competencies in published order", () => {
  const expected: Record<string, [string, string[]]> = {
    "PH-TESDA-ASER-NC2": ["Core Competencies", [
      "Diagnose and repair engine cooling and lubrication system",
      "Diagnose and repair intake and exhaust system",
      "Diagnose and overhaul engine mechanical system",
    ]],
    "PH-TESDA-EIM-NC2": ["Core Competencies", ["ELC741301", "ELC741302", "ELC741303"]],
    "PH-TESDA-EIM-NC3": ["Core Units of Competency", ["ELC741304", "ELC741305", "ELC741306"]],
    "PH-TESDA-PRO-COOKERY-NC3": ["Core Competencies", [
      "TRS512301",
      "TRS512302",
      "TRS512303",
      "TRS512304",
      "TRS512305",
    ]],
  };
  for (const [id, [group, items]] of Object.entries(expected)) {
    const item = record(id);
    assert.equal(coreCompetencyGroup(item.modules), group, id);
    const preview = modulePreview(item.modules, false);
    assert.equal(preview.mode, "core-preview", id);
    assert.ok(preview.modules.every((module) => module.group === group), id);
    // Codes where published, otherwise exact titles; order follows the source.
    assert.deepEqual(preview.modules.map((module) => module.code ?? module.title_verbatim), items, id);
    assert.deepEqual(preview.modules, item.modules.filter((module) => module.group === group).slice(0, MODULE_PREVIEW_LIMIT));
    // The preview is never the complete qualification, so the full list must stay reachable.
    assert.ok(preview.modules.length < item.modules.length);
    assert.equal(moduleDisclosure(item.modules.length, false)?.label, `Show all ${item.modules.length} modules / competencies`);
  }
});


test("Show fewer returns to the same core preview", () => {
  const nc3 = record("PH-TESDA-EIM-NC3");
  const first = modulePreview(nc3.modules, false);
  modulePreview(nc3.modules, true);
  assert.deepEqual(modulePreview(nc3.modules, false), first);
});


test("the preview keeps published grouping", () => {
  const ite = record("SG-ITE-HNITEC-AUTO-2Y");
  assert.deepEqual(
    groupModules(modulePreview(ite.modules, false).modules).map(({ group, modules }) => [group, modules.length]),
    [["Sector Foundation Modules", 2], ["Specialisation Modules", 3]],
  );
  const cgtti = record("LK-CGTTI-AUTO-TECH");
  assert.deepEqual(
    groupModules(modulePreview(cgtti.modules, false).modules).map(({ group, modules }) => [group, modules.length]),
    [["First Year", 1], ["Second Year", 4]],
  );
});


test("the show-all control exposes its expanded state, and is absent for five or fewer items", () => {
  assert.deepEqual(moduleDisclosure(28, false), { label: "Show all 28 modules / competencies", ariaExpanded: false });
  assert.deepEqual(moduleDisclosure(28, true), { label: "Show fewer", ariaExpanded: true });
  assert.equal(moduleDisclosure(5, false), null);
  assert.equal(moduleDisclosure(0, false), null);
  // Cards with more than five items offer the control; shorter ones (e.g. the 4-module Indian web qualification) do not.
  for (const item of BENCHMARK_RECORDS) {
    assert.equal(Boolean(moduleDisclosure(item.modules.length, false)), item.modules.length > 5, item.record_id);
  }
  assert.ok(BENCHMARK_RECORDS.some((item) => item.modules.length <= 5));
});


test("disclosure is a pure function of each card's own state", () => {
  // Expanding one card's list never changes another card's preview.
  const dgt = record("IN-DGT-CTS-MMV-V2");
  const tafe = record("AU-TAFENSW-AUR30620");
  modulePreview(dgt.modules, true);
  assert.equal(modulePreview(tafe.modules, false).modules.length, MODULE_PREVIEW_LIMIT);
});


test("duration summaries restate only published periods and totals", () => {
  const expected: Record<string, [string, boolean]> = {
    "LK-CGTTI-AUTO-TECH": ["4 years (full-time)", false],
    "LK-CGTTI-POWER-ELEC": ["42 months (full-time)", false],
    "IN-DGT-CTS-MMV-V2": ["2 years", true],
    "IN-DGT-CTS-ELEC-V3": ["2 years", false],
    "PH-TESDA-ASER-NC2": ["465 total hours (including supervised industry learning)", true],
    "PH-TESDA-EIM-NC2": ["196 nominal training hours", true],
    "PH-TESDA-EIM-NC3": ["160 nominal training hours", true],
    "SG-ITE-HNITEC-AUTO-2Y": ["2 years", true],
    "SG-ITE-HNITEC-ELEC-2Y": ["2 years", true],
    "AU-TAFENSW-AUR30620": ["Not stated", false],
    "AU-TAFENSW-UEE30820": ["Not stated", false],
  };
  for (const [id, [summary, hasDetails]] of Object.entries(expected)) {
    const display = durationDisplay(record(id).duration_as_published);
    assert.equal(display.summary, summary, id);
    // Details, when present, are the original published wording, unchanged.
    assert.equal(display.details, hasDetails ? record(id).duration_as_published : null, id);
  }
});


test("unrecognised durations are shown exactly as published, never summarised", () => {
  assert.deepEqual(durationDisplay("Approximately 300 hours over flexible blocks"), {
    summary: "Approximately 300 hours over flexible blocks",
    details: null,
  });
  assert.deepEqual(durationDisplay(null), { summary: "Not stated", details: null });
  assert.deepEqual(durationDisplay("  "), { summary: "Not stated", details: null });
});


test("qualifications keep their national framework and are never equated", () => {
  assert.deepEqual(qualificationDisplay(record("IN-DGT-CTS-MMV-V2")), { label: "NSQF Level 4", framework: "NSQF (India)", code: null });
  assert.deepEqual(qualificationDisplay(record("PH-TESDA-EIM-NC3")), { label: "NC III", framework: "Philippine TVET Qualification (NC)", code: null });
  assert.deepEqual(qualificationDisplay(record("SG-ITE-HNITEC-ELEC-2Y")), { label: "Higher Nitec", framework: "ITE Nitec / Higher Nitec (Singapore)", code: null });
  assert.deepEqual(qualificationDisplay(record("AU-TAFENSW-UEE30820")), { label: "Certificate III", framework: "AQF (Australia)", code: "UEE30820" });
  // CGTTI states no level, so no framework is implied either.
  assert.deepEqual(qualificationDisplay(record("LK-CGTTI-POWER-ELEC")), { label: "Not stated", framework: null, code: null });
});


test("formatting never alters the stored evidence", () => {
  const before = JSON.stringify(BENCHMARK_RECORDS);
  for (const item of BENCHMARK_RECORDS) {
    durationDisplay(item.duration_as_published);
    qualificationDisplay(item);
    groupModules(modulePreview(item.modules, false).modules);
    modulePreview(item.modules, true);
  }
  assert.equal(JSON.stringify(BENCHMARK_RECORDS), before);
  assert.equal(record("PH-TESDA-ASER-NC2").level_as_published, "NC II");
  assert.equal(record("IN-DGT-CTS-MMV-V2").level_as_published, "NSQF LEVEL - 4");
});
