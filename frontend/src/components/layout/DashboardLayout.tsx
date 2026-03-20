import { useState, useCallback } from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { ErrorBoundary } from "@/components/common/ErrorBoundary";

/** Dashboard shell with responsive sidebar and router outlet. */
export function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const closeSidebar = useCallback(() => setSidebarOpen(false), []);

  return (
    <div className="flex min-h-screen bg-surface">
      <Sidebar isOpen={sidebarOpen} onClose={closeSidebar} />

      {/* Mobile top bar */}
      <div className="fixed top-0 left-0 right-0 z-30 h-14 bg-surface-elevated/80 backdrop-blur-md border-b border-border flex items-center px-4 lg:hidden">
        <button
          onClick={() => setSidebarOpen(true)}
          className="p-2 -ml-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition-colors"
          aria-label="Open navigation"
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
            <path d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <div className="flex-1 flex justify-center">
          <span className="font-display text-lg text-text-primary tracking-tight">
            CropFolio
          </span>
        </div>
        <div className="w-10" />
      </div>

      <main className="flex-1 overflow-auto">
        <div className="max-w-6xl mx-auto px-4 py-4 sm:px-6 sm:py-6 lg:px-8 lg:py-8 pt-18 lg:pt-4">
          <ErrorBoundary>
            <Outlet />
          </ErrorBoundary>
        </div>
      </main>
    </div>
  );
}
