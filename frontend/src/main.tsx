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
import { FarmerLayout } from "./components/farmer/FarmerLayout";
import { FarmerLogin } from "./components/farmer/FarmerLogin";
import { FarmerHome } from "./components/farmer/FarmerHome";
import { FarmerFarm } from "./components/farmer/FarmerFarm";
import { FarmerPlan } from "./components/farmer/FarmerPlan";
import { FarmerWeather } from "./components/farmer/FarmerWeather";
import { FarmerLoanStatus } from "./components/farmer/FarmerLoanStatus";
import { LoanPortfolio } from "./components/distributor/LoanPortfolio";
import { ComplianceOverview } from "./components/distributor/ComplianceOverview";
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
              <Route path="/loan-portfolio" element={<LoanPortfolio />} />
              <Route path="/compliance" element={<ComplianceOverview />} />
            </Route>

            {/* Farmer app (mobile-first, auth required) */}
            <Route path="/farmer/login" element={<FarmerLogin />} />
            <Route element={<FarmerLayout />}>
              <Route path="/farmer" element={<FarmerHome />} />
              <Route path="/farmer/farm" element={<FarmerFarm />} />
              <Route path="/farmer/plan" element={<FarmerPlan />} />
              <Route path="/farmer/weather" element={<FarmerWeather />} />
              <Route path="/farmer/loans" element={<FarmerLoanStatus />} />
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
