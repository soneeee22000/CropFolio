import { createContext, useContext, useState, useCallback } from "react";
import type { ReactNode } from "react";
import { t as translate } from "./strings";
import type { Lang } from "./strings";

interface LanguageContextType {
  lang: Lang;
  toggleLang: () => void;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType>({
  lang: "en",
  toggleLang: () => {},
  t: (key: string) => key,
});

/** Language provider wrapping the app. */
export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Lang>("en");

  const toggleLang = useCallback(() => {
    setLang((prev) => (prev === "en" ? "mm" : "en"));
  }, []);

  const t = useCallback((key: string) => translate(key, lang), [lang]);

  return (
    <LanguageContext.Provider value={{ lang, toggleLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

/** Hook to access language and translation function. */
export function useLanguage() {
  return useContext(LanguageContext);
}
