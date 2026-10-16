import { createContext, useContext } from "react";
import { createLocalizer, type Language, type Localizer } from "./localize.ts";

export const LANGUAGE_STORAGE_KEY = "nysc.officer.language";

export interface LanguageContextValue {
  localizer: Localizer;
  setLanguage: (language: Language) => void;
}

// Interface language lives here — never in IntakeState — so switching it
// re-renders text without touching answers, requests or results.
export const LanguageContext = createContext<LanguageContextValue>({
  localizer: createLocalizer("en"),
  setLanguage: () => {},
});

export function useLocalizer(): Localizer {
  return useContext(LanguageContext).localizer;
}

export function useSetLanguage() {
  return useContext(LanguageContext).setLanguage;
}

export function readStoredLanguage(): Language {
  try {
    return window.localStorage.getItem(LANGUAGE_STORAGE_KEY) === "si" ? "si" : "en";
  } catch {
    return "en";
  }
}

export function storeLanguage(language: Language) {
  try {
    window.localStorage.setItem(LANGUAGE_STORAGE_KEY, language);
  } catch {
    // Storage can be unavailable (private windows, blocked site data); the
    // switch still works for the current session.
  }
}
