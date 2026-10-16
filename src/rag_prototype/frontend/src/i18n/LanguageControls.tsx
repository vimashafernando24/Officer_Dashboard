import type { ReactNode } from "react";
import { useLocalizer, useSetLanguage } from "./languageContext.ts";
import type { Language } from "./localize.ts";
import "./i18n.css";

const OPTIONS: { language: Language; label: string; htmlLang: string }[] = [
  { language: "en", label: "English", htmlLang: "en" },
  { language: "si", label: "සිංහල", htmlLang: "si" },
];

export function LanguageSwitch() {
  const localizer = useLocalizer();
  const setLanguage = useSetLanguage();
  return (
    <div className="language-switch" role="group" aria-label={localizer.t("lang.groupLabel")}>
      {OPTIONS.map((option) => (
        <button
          key={option.language}
          type="button"
          lang={option.htmlLang}
          className={`language-switch-button${localizer.language === option.language ? " is-active" : ""}`}
          aria-pressed={localizer.language === option.language}
          onClick={() => setLanguage(option.language)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

// Shown only in Sinhala, wherever substantive content remains English-only.
export function EnglishOnlyNotice({ children }: { children?: ReactNode }) {
  const localizer = useLocalizer();
  if (!localizer.isSinhala) return null;
  return (
    <p className="english-only-notice" role="note">
      <span aria-hidden="true">EN</span>
      {children ?? localizer.t("notice.englishOnly")}
    </p>
  );
}

// Sinhala text followed by the English source, for content where the
// English wording is authoritative (validated questions, reliability notes).
export function EnglishOriginal({ text }: { text: string }) {
  const localizer = useLocalizer();
  if (!localizer.isSinhala) return null;
  return (
    <span className="english-original" lang="en">
      {text}
    </span>
  );
}
