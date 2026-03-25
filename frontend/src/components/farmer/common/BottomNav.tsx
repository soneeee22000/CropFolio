/** Bottom tab navigation for the farmer mobile app. */

import { NavLink } from "react-router-dom";

const TABS = [
  {
    to: "/farmer",
    label: "ပင်မ",
    labelEn: "Home",
    icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6",
  },
  {
    to: "/farmer/farm",
    label: "လယ်",
    labelEn: "Farm",
    icon: "M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064",
  },
  {
    to: "/farmer/plan",
    label: "အစီအစဉ်",
    labelEn: "Plan",
    icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01",
  },
  {
    to: "/farmer/weather",
    label: "ရာသီဥတု",
    labelEn: "Weather",
    icon: "M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z",
  },
] as const;

/** Fixed bottom navigation bar with 4 tabs. */
export function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 h-16 bg-surface-elevated border-t border-border safe-area-bottom">
      <div className="flex h-full max-w-lg mx-auto">
        {TABS.map((tab) => (
          <NavLink
            key={tab.to}
            to={tab.to}
            end={tab.to === "/farmer"}
            className={({ isActive }) =>
              `flex-1 flex flex-col items-center justify-center gap-0.5 transition-colors min-h-[44px] ${
                isActive
                  ? "text-primary"
                  : "text-text-tertiary hover:text-text-secondary"
              }`
            }
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d={tab.icon} />
            </svg>
            <span className="text-xs font-myanmar leading-tight">
              {tab.label}
            </span>
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
