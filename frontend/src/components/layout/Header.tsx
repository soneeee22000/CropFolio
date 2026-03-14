import { Link } from "react-router-dom";
import { STEP_LABELS } from "@/constants";
import { useLanguage } from "@/i18n/LanguageContext";
import { useTheme } from "@/hooks/useTheme";

interface HeaderProps {
  currentStep: number;
}

/** Premium sticky header with language toggle, theme toggle, and step indicator. */
export function Header({ currentStep }: HeaderProps) {
  const { lang, toggleLang } = useLanguage();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-50 bg-surface-elevated/80 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2.5">
            <svg width="22" height="22" viewBox="0 0 32 32" fill="none">
              <rect
                width="32"
                height="32"
                rx="8"
                fill="#1B7A4A"
                fillOpacity="0.1"
              />
              <rect x="6" y="20" width="5" height="6" rx="1" fill="#3A8F5C" />
              <rect
                x="13.5"
                y="14"
                width="5"
                height="12"
                rx="1"
                fill="#1B7A4A"
              />
              <rect x="21" y="8" width="5" height="18" rx="1" fill="#B8860B" />
              <path
                d="M25.5 7C25.5 7 23 4 20 5.5C21.5 6 23.5 6 25.5 7Z"
                fill="#3A8F5C"
                opacity="0.8"
              />
            </svg>
            <h1 className="font-display text-2xl text-text-primary tracking-tight">
              CropFolio
            </h1>
          </div>
          <button
            onClick={toggleLang}
            className="px-3 py-1 text-[11px] uppercase tracking-wide border border-border rounded-full text-text-secondary hover:text-text-primary hover:border-text-tertiary transition-colors duration-200"
          >
            {lang === "en" ? "MM" : "EN"}
          </button>
          <button
            onClick={toggleTheme}
            className="px-3 py-1 text-[11px] border border-border rounded-full text-text-secondary hover:text-text-primary hover:border-text-tertiary transition-colors duration-200"
            aria-label={
              theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
            }
          >
            {theme === "dark" ? "\u2600" : "\u263D"}
          </button>
        </div>
        <div className="flex items-center gap-6">
          <nav className="hidden sm:flex items-center gap-1">
            {STEP_LABELS.map((label, i) => (
              <div key={label} className="flex items-center">
                <div className="flex flex-col items-center gap-1">
                  <div
                    className={`w-2 h-2 rounded-full transition-all duration-300 ${
                      i === currentStep
                        ? "bg-primary scale-125"
                        : i < currentStep
                          ? "bg-primary/40"
                          : "bg-border"
                    }`}
                  />
                  <span
                    className={`text-[11px] tracking-wide transition-colors duration-300 ${
                      i === currentStep
                        ? "text-text-primary font-medium"
                        : "text-text-tertiary"
                    }`}
                  >
                    {label}
                  </span>
                </div>
                {i < STEP_LABELS.length - 1 && (
                  <div
                    className={`w-12 h-px mx-2 mt-[-14px] transition-colors duration-300 ${
                      i < currentStep ? "bg-primary/30" : "bg-border"
                    }`}
                  />
                )}
              </div>
            ))}
          </nav>
          <Link
            to="/"
            className="text-sm text-text-secondary hover:text-text-primary transition-colors"
          >
            Home
          </Link>
        </div>
      </div>
    </header>
  );
}
