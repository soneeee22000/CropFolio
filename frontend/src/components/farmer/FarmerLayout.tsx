/** Farmer app shell with bottom tab navigation. */

import { Outlet, Navigate } from "react-router-dom";
import { BottomNav } from "./common/BottomNav";
import { hasToken } from "@/api/auth";

/** Layout wrapper for farmer app — requires authentication. */
export function FarmerLayout() {
  if (!hasToken()) {
    return <Navigate to="/farmer/login" replace />;
  }

  return (
    <div className="min-h-screen bg-surface pb-20">
      {/* Top header */}
      <header className="sticky top-0 z-30 h-14 bg-surface-elevated/90 backdrop-blur-md border-b border-border flex items-center px-4">
        <div className="flex-1">
          <span className="font-display text-lg text-primary tracking-tight">
            CropFolio
          </span>
        </div>
      </header>

      {/* Page content */}
      <main className="px-4 pt-4">
        <Outlet />
      </main>

      <BottomNav />
    </div>
  );
}
