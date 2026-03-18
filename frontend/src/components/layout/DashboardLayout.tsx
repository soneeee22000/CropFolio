import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { ErrorBoundary } from "@/components/common/ErrorBoundary";

/** Dashboard shell with sidebar navigation and router outlet. */
export function DashboardLayout() {
  return (
    <div className="flex min-h-screen bg-surface">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <div className="max-w-6xl mx-auto px-8 py-8">
          <ErrorBoundary>
            <Outlet />
          </ErrorBoundary>
        </div>
      </main>
    </div>
  );
}
