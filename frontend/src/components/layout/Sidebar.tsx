import { useEffect } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { useTheme } from "@/hooks/useTheme";
import { useLanguage } from "@/i18n/LanguageContext";

const NAV_ITEMS = [
  {
    to: "/dashboard",
    labelKey: "nav.overview",
    icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6",
  },
  {
    to: "/recommend",
    labelKey: "nav.recommend",
    icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4",
  },
  {
    to: "/demo-calculator",
    labelKey: "nav.demoRoi",
    icon: "M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z",
  },
  {
    to: "/reports",
    labelKey: "nav.reports",
    icon: "M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
  },
  {
    to: "/bayesian",
    labelKey: "nav.bayesian",
    icon: "M13 10V3L4 14h7v7l9-11h-7z",
  },
  {
    to: "/sar",
    labelKey: "nav.sar",
    icon: "M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
  },
] as const;

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

/** Dashboard sidebar navigation — static on desktop, drawer on mobile. */
export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const { theme, toggleTheme } = useTheme();
  const { lang, toggleLang, t } = useLanguage();
  const location = useLocation();

  useEffect(() => {
    onClose();
  }, [location.pathname, onClose]);

  return (
    <>
      {/* Backdrop overlay — mobile only */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`
          fixed inset-y-0 left-0 z-50 w-64 bg-surface-elevated border-r border-border flex flex-col
          transform transition-transform duration-300 ease-in-out
          lg:static lg:translate-x-0
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        {/* Brand */}
        <div className="px-6 py-5 border-b border-border">
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
            <div>
              <h1 className="font-display text-xl text-text-primary tracking-tight">
                CropFolio
              </h1>
              <span className="text-[10px] uppercase tracking-widest text-accent font-medium">
                Pro
              </span>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1">
          <Link
            to="/"
            data-testid="nav-home"
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition-colors duration-200 mb-2 border-b border-border pb-3"
          >
            <svg
              className="w-5 h-5 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            {t("nav.backToHome")}
          </Link>
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              data-testid={`nav-${item.to.slice(1)}`}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors duration-200 ${
                  isActive
                    ? "bg-primary/10 text-primary font-medium"
                    : "text-text-secondary hover:text-text-primary hover:bg-surface-subtle"
                }`
              }
            >
              <svg
                className="w-5 h-5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d={item.icon} />
              </svg>
              {t(item.labelKey)}
            </NavLink>
          ))}
        </nav>

        {/* Bottom controls */}
        <div className="px-3 py-4 border-t border-border space-y-2">
          <button
            onClick={toggleLang}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition-colors"
          >
            <span className="w-5 text-center text-xs">
              {lang === "en" ? "MM" : "EN"}
            </span>
            {t("nav.language")}
          </button>
          <button
            onClick={toggleTheme}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition-colors"
            aria-label={
              theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
            }
          >
            <span className="w-5 text-center">
              {theme === "dark" ? "\u2600" : "\u263D"}
            </span>
            {theme === "dark" ? t("nav.lightMode") : t("nav.darkMode")}
          </button>
        </div>
      </aside>
    </>
  );
}
