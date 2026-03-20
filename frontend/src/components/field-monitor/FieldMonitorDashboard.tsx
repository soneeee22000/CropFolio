import { useState, useEffect } from "react";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { FieldMonitorMap } from "./FieldMonitorMap";
import { CompliancePieChart } from "./CompliancePieChart";
import { AlertList } from "./AlertList";
import { PlotDetailDrawer } from "./PlotDetailDrawer";
import { useFieldMonitor } from "@/hooks/useFieldMonitor";
import { fetchTownships } from "@/api/townships";
import { useLanguage } from "@/i18n/LanguageContext";
import { formatPercent } from "@/utils/formatters";
import type { Township } from "@/types/township";

/** Field Monitor Dashboard — multi-plot compliance monitoring from space. */
export function FieldMonitorDashboard() {
  const { t } = useLanguage();
  const [townships, setTownships] = useState<Township[]>([]);
  const [selectedTownship, setSelectedTownship] = useState("");
  const [season, setSeason] = useState<"monsoon" | "dry">("monsoon");
  const [selectedPlotId, setSelectedPlotId] = useState<string | null>(null);
  const [alertSeverity, setAlertSeverity] = useState("all");
  const [loadError, setLoadError] = useState<string | null>(null);

  const { summary, isLoading, error, loadMonitor } = useFieldMonitor();

  useEffect(() => {
    async function load() {
      try {
        const res = await fetchTownships();
        setTownships(res.townships);
      } catch {
        setLoadError("Failed to load townships");
      }
    }
    load();
  }, []);

  const handleMonitor = () => {
    if (selectedTownship) {
      setSelectedPlotId(null);
      loadMonitor({ township_id: selectedTownship, season, year: 2025 });
    }
  };

  const activeTownship = townships.find((tw) => tw.id === selectedTownship);
  const selectedPlot =
    summary?.plots.find((p) => p.plot_id === selectedPlotId) ?? null;

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <h2 className="font-display text-3xl text-text-primary">
            {t("fieldMonitor.title")}
          </h2>
          <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-accent/10 text-accent font-medium">
            Moat
          </span>
        </div>
        <p className="text-text-secondary mt-1">{t("fieldMonitor.subtitle")}</p>
      </div>

      {/* Controls */}
      <Card title={t("fieldMonitor.selectArea")}>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
              {t("township.overline")}
            </label>
            <select
              value={selectedTownship}
              onChange={(e) => setSelectedTownship(e.target.value)}
              className="w-full p-3 rounded-lg border border-border bg-surface-elevated text-text-primary text-base"
            >
              <option value="">Select township...</option>
              {townships.map((tw) => (
                <option key={tw.id} value={tw.id}>
                  {tw.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
              {t("recommend.season")}
            </label>
            <div className="flex gap-2">
              {(["monsoon", "dry"] as const).map((s) => (
                <button
                  key={s}
                  onClick={() => setSeason(s)}
                  className={`px-4 py-2.5 rounded-lg text-sm border transition-colors ${
                    season === s
                      ? "border-primary bg-primary/10 text-primary font-medium"
                      : "border-border text-text-secondary"
                  }`}
                >
                  {t(`recommend.${s}`)}
                </button>
              ))}
            </div>
          </div>
          <div className="flex items-end">
            <button
              onClick={handleMonitor}
              disabled={!selectedTownship || isLoading}
              className="w-full px-6 py-2.5 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading
                ? t("fieldMonitor.monitoring")
                : t("fieldMonitor.monitor")}
            </button>
          </div>
        </div>
      </Card>

      {loadError && <ErrorAlert message={loadError} />}
      {isLoading && <LoadingSpinner message={t("fieldMonitor.monitoring")} />}
      {error && <ErrorAlert message={error} />}

      {/* Results */}
      {summary && (
        <div className="space-y-6">
          {/* KPI Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <MetricCard
              value={String(summary.total_plots)}
              label={t("fieldMonitor.totalPlots")}
            />
            <MetricCard
              value={formatPercent(summary.compliance_rate)}
              label={t("fieldMonitor.complianceRate")}
              highlight={summary.compliance_rate >= 0.8}
            />
            <MetricCard
              value={String(summary.active_alerts)}
              label={t("fieldMonitor.activeAlerts")}
              highlight={summary.active_alerts > 0}
            />
            <MetricCard
              value={`${summary.total_area_ha} ha`}
              label={t("fieldMonitor.verifiedArea")}
            />
          </div>

          {/* Map + Pie side by side */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Card title={t("fieldMonitor.plotMap")}>
                {activeTownship && (
                  <FieldMonitorMap
                    plots={summary.plots}
                    centerLat={activeTownship.latitude}
                    centerLon={activeTownship.longitude}
                    onSelectPlot={setSelectedPlotId}
                    selectedPlotId={selectedPlotId}
                  />
                )}
              </Card>
            </div>
            <div>
              <Card title={t("fieldMonitor.complianceBreakdown")}>
                <CompliancePieChart
                  compliant={summary.compliant_count}
                  warning={summary.warning_count}
                  deviation={summary.deviation_count}
                />
              </Card>
            </div>
          </div>

          {/* Alerts */}
          <Card
            title={`${t("fieldMonitor.alerts")} (${summary.active_alerts})`}
          >
            <AlertList
              alerts={summary.alerts}
              onSelectPlot={setSelectedPlotId}
              selectedSeverity={alertSeverity}
              onSeverityChange={setAlertSeverity}
            />
          </Card>
        </div>
      )}

      {/* Plot detail drawer */}
      <PlotDetailDrawer
        plot={selectedPlot}
        onClose={() => setSelectedPlotId(null)}
      />
    </div>
  );
}
