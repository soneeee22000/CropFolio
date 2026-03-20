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
import { BayesianDashboard } from "./components/bayesian/BayesianDashboard";
import { SARDashboard } from "./components/sar/SARDashboard";
import { FieldMonitorDashboard } from "./components/field-monitor/FieldMonitorDashboard";
import { AdvisoryPage } from "./components/advisory/AdvisoryPage";
import "./index.css";
import App from "./App.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <LanguageProvider>
        <BrowserRouter>
          <Routes>
            {/* Landing page */}
            <Route path="/" element={<LandingPage />} />

            {/* B2B Dashboard */}
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<DashboardOverview />} />
              <Route path="/recommend" element={<RecommendPage />} />
              <Route path="/demo-calculator" element={<DemoROICalculator />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/bayesian" element={<BayesianDashboard />} />
              <Route path="/sar" element={<SARDashboard />} />
              <Route
                path="/field-monitor"
                element={<FieldMonitorDashboard />}
              />
              <Route path="/advisory" element={<AdvisoryPage />} />
            </Route>

            {/* Legacy wizard */}
            <Route path="/app" element={<App />} />
            <Route path="/admin" element={<AdminPage />} />

            {/* Catch-all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </LanguageProvider>
    </ThemeProvider>
  </StrictMode>,
);
