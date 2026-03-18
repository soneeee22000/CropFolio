import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { LanguageProvider } from "./i18n/LanguageContext";
import { ThemeProvider } from "./hooks/useTheme";
import { LandingPage } from "./components/landing/LandingPage";
import { AdminPage } from "./components/admin/AdminPage";
import { DashboardLayout } from "./components/layout/DashboardLayout";
import { DashboardOverview } from "./components/dashboard/DashboardOverview";
import { RecommendPage } from "./components/recommend/RecommendPage";
import { DemoROICalculator } from "./components/demo/DemoROICalculator";
import { ReportsPage } from "./components/reports/ReportsPage";
import "./index.css";
import App from "./App.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <LanguageProvider>
        <BrowserRouter>
          <Routes>
            {/* Landing */}
            <Route path="/" element={<LandingPage />} />

            {/* Legacy wizard (kept for backwards compat) */}
            <Route path="/app" element={<App />} />
            <Route path="/admin" element={<AdminPage />} />

            {/* B2B Dashboard */}
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<DashboardOverview />} />
              <Route path="/recommend" element={<RecommendPage />} />
              <Route path="/demo-calculator" element={<DemoROICalculator />} />
              <Route path="/reports" element={<ReportsPage />} />
            </Route>

            {/* Catch-all redirect to dashboard */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </BrowserRouter>
      </LanguageProvider>
    </ThemeProvider>
  </StrictMode>,
);
