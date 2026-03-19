import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { useLanguage } from "@/i18n/LanguageContext";
import type { Township } from "@/types/township";

const API = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

/** Dashboard overview with KPI cards and quick actions. */
export function DashboardOverview() {
  const navigate = useNavigate();
  const { t } = useLanguage();
  const [stats, setStats] = useState<{
    townships: number;
    crops: number;
    fertilizers: number;
  } | null>(null);
  const [townships, setTownships] = useState<Township[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const [twpRes, cropRes, fertRes] = await Promise.all([
          fetch(`${API}/townships/`).then((r) => r.json()),
          fetch(`${API}/crops/`).then((r) => r.json()),
          fetch(`${API}/fertilizers/`).then((r) => r.json()),
        ]);
        setStats({
          townships: twpRes.count,
          crops: cropRes.count,
          fertilizers: fertRes.count,
        });
        setTownships(twpRes.townships);
      } catch {
        /* graceful degradation — show zeros */
      } finally {
        setIsLoading(false);
      }
    }
    loadStats();
  }, []);

  if (isLoading) {
    return <LoadingSpinner message={t("common.loading")} />;
  }

  const regions = [...new Set(townships.map((tw) => tw.region))];

  return (
    <div
      className="space-y-8 animate-fade-in-up"
      data-testid="dashboard-overview"
    >
      {/* Page header */}
      <div>
        <h2 className="font-display text-3xl text-text-primary">
          {t("dashboard.title")}
        </h2>
        <p className="text-text-secondary mt-1">{t("dashboard.subtitle")}</p>
      </div>

      {/* KPI cards */}
      <div
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
        data-testid="kpi-cards"
      >
        <MetricCard
          value={String(stats?.townships ?? 0)}
          label={t("dashboard.townships")}
          sublabel={t("dashboard.regionsFormat").replace(
            "{count}",
            String(regions.length),
          )}
        />
        <MetricCard
          value={String(stats?.crops ?? 0)}
          label={t("dashboard.cropProfiles")}
          sublabel={t("dashboard.faostatWfp")}
        />
        <MetricCard
          value={String(stats?.fertilizers ?? 0)}
          label={t("dashboard.fertilizers")}
          sublabel={t("dashboard.npkFormulations")}
        />
        <MetricCard
          value="1,000"
          label={t("dashboard.monteCarloSims")}
          sublabel={t("dashboard.perRecommendation")}
          highlight
        />
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title={t("dashboard.generateRec")}>
          <p className="text-sm text-text-secondary mb-6">
            {t("dashboard.generateRecDesc")}
          </p>
          <button
            onClick={() => navigate("/recommend")}
            data-testid="btn-generate-rec"
            className="px-5 py-2.5 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors"
          >
            {t("dashboard.startRec")}
          </button>
        </Card>
        <Card title={t("dashboard.demoCalc")}>
          <p className="text-sm text-text-secondary mb-6">
            {t("dashboard.demoCalcDesc")}
          </p>
          <button
            onClick={() => navigate("/demo-calculator")}
            data-testid="btn-demo-roi"
            className="px-5 py-2.5 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors"
          >
            {t("dashboard.calcRoi")}
          </button>
        </Card>
      </div>

      {/* Coverage by region */}
      <Card title={t("dashboard.coverageByRegion")}>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {regions.map((region) => {
            const count = townships.filter((tw) => tw.region === region).length;
            return (
              <div
                key={region}
                className="p-3 rounded-lg bg-surface-subtle text-center"
              >
                <div className="font-data text-lg text-text-primary">
                  {count}
                </div>
                <div className="text-[11px] uppercase tracking-wide text-text-tertiary mt-1">
                  {region}
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
