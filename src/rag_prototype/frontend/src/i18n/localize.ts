// Pure, display-only lookups. Every function takes the canonical English text
// (and, where one exists, the canonical identifier) and returns the text to
// show. In English, or when no Sinhala entry exists, the English text is
// returned unchanged. These functions never produce values for the backend.

import { en, si, type MessageKey } from "./messages.ts";
import {
  SI_ANSWERS,
  SI_BRANCH_LABELS,
  SI_BRANCH_OPTIONS,
  SI_EVIDENCE_TEXT,
  SI_FINDING_TITLES,
  SI_LANGUAGE_NAMES,
  SI_MODEL_DESCRIPTIONS,
  SI_MODEL_JUDGMENTS,
  SI_MODEL_LABELS,
  SI_PROFILES,
  SI_PROGRAMME_OPTIONS,
  SI_QUESTIONS,
  SI_SECTORS,
  SI_SERVICE_MESSAGES,
  SI_SKILL_AREAS,
  SI_SKILLS,
  SI_VARIABLES,
} from "./siDomain.ts";

export type Language = "en" | "si";

export type MessageVars = Record<string, string | number>;

export function interpolate(template: string, vars?: MessageVars): string {
  if (!vars) return template;
  return template.replace(/\{(\w+)\}/g, (match, name: string) =>
    name in vars ? String(vars[name]) : match,
  );
}

export function translateMessage(language: Language, key: MessageKey, vars?: MessageVars): string {
  const template = (language === "si" && si[key]) || en[key];
  return interpolate(template, vars);
}

function lookup(language: Language, table: Record<string, string>, key: string | null | undefined, fallback: string) {
  if (language !== "si" || !key) return fallback;
  return Object.hasOwn(table, key) && table[key] ? table[key] : fallback;
}

function translateMismatch(language: Language, text: string): string {
  if (language !== "si") return text;
  const schedule = text.match(/^Schedule mismatch: the catalogue lists (.+)\.$/);
  if (schedule) {
    return `කාලසටහන නොගැළපේ (Schedule mismatch): පාඨමාලා නාමාවලියේ සඳහන් වන්නේ “${schedule[1]}” ලෙසයි.`;
  }
  const languageMismatch = text.match(/^Language mismatch: the member prefers (.+?), but the catalogue lists (.+)\.$/);
  if (languageMismatch) {
    const preferred = lookup(language, SI_PROGRAMME_OPTIONS, languageMismatch[1], languageMismatch[1]);
    const listed = languageMismatch[2]
      .split(" / ")
      .map((name) => lookup(language, SI_LANGUAGE_NAMES, name.trim().toLowerCase(), name))
      .join(" / ");
    return `භාෂාව නොගැළපේ (Language mismatch): සාමාජිකයා ${preferred} භාෂාවට කැමති වුවද, පාඨමාලා නාමාවලියේ සඳහන් වන්නේ ${listed} ය.`;
  }
  if (text === "Qualification to confirm: the catalogue does not state an NVQ or other formal qualification for this course.") {
    return "සුදුසුකම තහවුරු කළ යුතුය (Qualification to confirm): මෙම පාඨමාලාව සඳහා NVQ හෝ වෙනත් නිල සුදුසුකමක් ලැබෙන බව පාඨමාලා නාමාවලියේ සඳහන් නොවේ.";
  }
  return text;
}

export function createLocalizer(language: Language) {
  return {
    language,
    isSinhala: language === "si",
    t: (key: MessageKey, vars?: MessageVars) => translateMessage(language, key, vars),
    branchOption: (branchId: string, english: string) => lookup(language, SI_BRANCH_OPTIONS, branchId, english),
    branchLabel: (branchId: string, english: string) => lookup(language, SI_BRANCH_LABELS, branchId, english),
    modelLabel: (modelId: string, english: string) => lookup(language, SI_MODEL_LABELS, modelId, english),
    modelDescription: (modelId: string, english: string) => lookup(language, SI_MODEL_DESCRIPTIONS, modelId, english),
    profileName: (profileKey: string | null | undefined, english: string) =>
      language === "si" && profileKey && SI_PROFILES[profileKey] ? SI_PROFILES[profileKey].name : english,
    profileSummary: (profileKey: string | null | undefined, english: string) =>
      language === "si" && profileKey && SI_PROFILES[profileKey] ? SI_PROFILES[profileKey].summary : english,
    question: (variable: string, english: string) => lookup(language, SI_QUESTIONS, variable, english),
    variableName: (variable: string, english: string) => lookup(language, SI_VARIABLES, variable, english),
    answer: (english: string) => lookup(language, SI_ANSWERS, english, english),
    sector: (code: string, english: string) => lookup(language, SI_SECTORS, code, english),
    skillArea: (english: string) => lookup(language, SI_SKILL_AREAS, english, english),
    // Skill names are official catalogue titles, so a Sinhala name is always
    // shown together with the English one.
    skill: (english: string) => {
      const translated = lookup(language, SI_SKILLS, english, "");
      return translated && translated !== english ? `${translated} (${english})` : english;
    },
    programmeOption: (english: string) => lookup(language, SI_PROGRAMME_OPTIONS, english, english),
    findingTitle: (english: string) => lookup(language, SI_FINDING_TITLES, english, english),
    evidenceText: (english: string) => lookup(language, SI_EVIDENCE_TEXT, english, english),
    modelJudgment: (english: string) => lookup(language, SI_MODEL_JUDGMENTS, english, english),
    serviceMessage: (english: string) => lookup(language, SI_SERVICE_MESSAGES, english, english),
    mismatch: (english: string) => translateMismatch(language, english),
  };
}

export type Localizer = ReturnType<typeof createLocalizer>;
