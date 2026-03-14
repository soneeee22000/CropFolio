import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
} from "react";
import type { ReactNode } from "react";

type Theme = "dark" | "light";
const STORAGE_KEY = "cropfolio-theme";

interface ThemeContextType {
  /** Current active theme. */
  theme: Theme;
  /** Toggle between dark and light themes. */
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: "dark",
  toggleTheme: () => {},
});

/** Provider that manages theme state and syncs with DOM + localStorage. */
export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored === "light" ? "light" : "dark";
  });

  useEffect(() => {
    if (theme === "light") {
      document.documentElement.dataset.theme = "light";
    } else {
      delete document.documentElement.dataset.theme;
    }
    localStorage.setItem(STORAGE_KEY, theme);
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

/** Hook to access current theme and toggle function. */
export function useTheme() {
  return useContext(ThemeContext);
}
