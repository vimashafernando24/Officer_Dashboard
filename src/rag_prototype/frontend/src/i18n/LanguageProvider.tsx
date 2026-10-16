import { useEffect, useMemo, useState, type ReactNode } from "react";
import { LanguageContext, readStoredLanguage, storeLanguage } from "./languageContext.ts";
import { createLocalizer, type Language } from "./localize.ts";

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>(readStoredLanguage);

  useEffect(() => {
    document.documentElement.lang = language;
    storeLanguage(language);
  }, [language]);

  const value = useMemo(
    () => ({ localizer: createLocalizer(language), setLanguage }),
    [language],
  );

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}
