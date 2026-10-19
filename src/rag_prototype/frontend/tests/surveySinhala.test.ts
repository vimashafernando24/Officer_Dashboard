import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

import { translateConclusionToSinhala } from "../src/i18n/conclusionSi.ts";

const readJson = (name: string) =>
  JSON.parse(fs.readFileSync(new URL(`../src/data/${name}`, import.meta.url), "utf8"));

const surveyMap = readJson("surveySinhalaMap.json");
const teachingLibrary = readJson("clusterResearchTeachingLibrary.json");

type Finding = {
  simple_conclusion: string;
  survey_question: { question_id: string | null; question_text: string | null };
  distribution: { kind: string; profiles: { answers: { answer: string }[] }[] };
};

const findings: Finding[] = teachingLibrary.models.flatMap((model: { profiles: { retained_findings: Finding[] }[] }) =>
  model.profiles.flatMap((profile) => profile.retained_findings),
);

const SINHALA = /[඀-෿]/;

test("every teaching-library question has the survey's Sinhala wording", () => {
  for (const finding of findings) {
    const id = finding.survey_question.question_id;
    if (!id) continue;
    const entry = surveyMap.questions_by_id[id];
    assert.ok(entry, `no survey entry for ${id}`);
    assert.equal(entry.en, finding.survey_question.question_text, `${id} English text differs from the survey`);
    assert.match(entry.si, SINHALA);
  }
});

test("every categorical answer shown in the teaching library has survey Sinhala", () => {
  for (const finding of findings) {
    if (finding.distribution.kind === "numeric_summary") continue;
    const id = finding.survey_question.question_id ?? "";
    for (const profile of finding.distribution.profiles) {
      for (const { answer } of profile.answers) {
        const sinhala = surveyMap.answers_by_question_id[id]?.[answer] ?? surveyMap.answers[answer];
        assert.ok(sinhala, `no Sinhala for “${answer}” (${id})`);
      }
    }
  }
});

test("answers use the wording of their own survey question", () => {
  // The survey translates "No" differently in different questions.
  assert.equal(surveyMap.answers_by_question_id.C2["No — not yet"], "නැහැ — තවම ආරම්භ කර නැත");
  assert.equal(surveyMap.answers_by_question_id.C2["Yes — I am already searching"], "ඔව් — දැනටමත් සොයමින්");
});

test("shortened motivation labels map to the survey option with the same code", () => {
  const sc1 = surveyMap.answers_by_question_id.SC1;
  assert.equal(sc1["Intrinsic: genuinely passionate about the subject"], sc1["I am genuinely passionate about this subject"]);
});

test("every conclusion sentence has a Sinhala form", () => {
  const translators = { answer: (a: string) => `<${a}>`, profileName: (p: string) => `[${p}]` };
  for (const finding of findings) {
    const sinhala = translateConclusionToSinhala(finding.simple_conclusion, translators);
    assert.ok(sinhala, `no template for: ${finding.simple_conclusion}`);
    assert.doesNotMatch(sinhala.replace(/<[^>]*>|\[[^\]]*\]/g, ""), /[A-Za-z]{3,}/, sinhala);
  }
});

test("conclusion keeps numbers, answer and profile names", () => {
  const text =
    "Only 1 of 29 members (3.4%) selected “Above LKR 200,000”. In the “Permanent work with stronger security” profile, 36.5% selected the same answer. This response was much less common in this historical profile.";
  const sinhala = translateConclusionToSinhala(text, {
    answer: () => "රු. 200,000 ට වැඩි",
    profileName: () => "ස්ථිර රැකියා",
  });
  assert.equal(
    sinhala,
    "සාමාජිකයින් 29 දෙනාගෙන් 1 දෙනෙකු පමණක් (3.4%) “රු. 200,000 ට වැඩි” තෝරා ඇත. “ස්ථිර රැකියා” කාණ්ඩයේ 36.5% ක් එම පිළිතුරම තෝරා ඇත. මෙම පිළිතුර මෙම ඓතිහාසික කාණ්ඩයේ බෙහෙවින් අඩුවෙන් දක්නට ලැබිණි.",
  );
});

test("unknown sentences fall back to English", () => {
  assert.equal(translateConclusionToSinhala("Something new.", { answer: (a) => a, profileName: (p) => p }), null);
});
