import { useState, useEffect } from "react";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { SARMapView } from "./SARMapView";
import { useSARAnalysis } from "@/hooks/useSARAnalysis";
import { fetchTownships } from "@/api/townships";
import { useLanguage } from "@/i18n/LanguageContext";
import { formatPercent } from "@/utils/formatters";
import type { Township } from "@/types/township";

/** SAR planting verification dashboard. */
export function SARDashboard() {
  const { t } = useLanguage();
  const [townships, setTownships] = useState<Township[]>([]);
  const [selectedTownship, setSelectedTownship] = useState("");
  const [season, setSeason] = useState<"monsoon" | "dry">("monsoon");
  const { result, isLoading, error, analyze } = useSARAnalysis();

  const [loadError, setLoadError] = useState<string | null>(null);

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

  const handleAnalyze = () => {
    if (selectedTownship) {
      analyze({ township_id: selectedTownship, season, year: 2025 });
    }
  };

  const activeTownship = townships.find((tw) => tw.id === selectedTownship);

  return (
    <div className="space-y-8 animate-fade-in-up">
      <div>
        <div className="flex items-center gap-3">
          <h2 className="font-display text-3xl text-text-primary">
            {t("sar.title")}
          </h2>
          <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-accent/10 text-accent font-medium">
            Beta
          </span>
        </div>
        <p className="text-text-secondary mt-1">{t("sar.subtitle")}</p>
      </div>

      {/* Controls */}
      <Card title={t("sar.selectArea")}>
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
              onClick={handleAnalyze}
              disabled={!selectedTownship || isLoading}
              className="w-full px-6 py-2.5 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? t("sar.analyzing") : t("sar.analyze")}
            </button>
          </div>
        </div>
      </Card>

      {/* Map — shown when a township is selected */}
      {activeTownship && (
        <Card title={t("sar.analysisArea")}>
          <SARMapView
            latitude={activeTownship.latitude}
            longitude={activeTownship.longitude}
            townshipName={activeTownship.name}
          />
        </Card>
      )}

      {loadError && <ErrorAlert message={loadError} />}
      {isLoading && <LoadingSpinner message={t("sar.analyzing")} />}
      {error && <ErrorAlert message={error} />}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Summary metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <MetricCard
              value={result.rice_detected ? "Detected" : "Not Detected"}
              label={t("sar.riceStatus")}
              highlight={result.rice_detected}
            />
            <MetricCard
              value={formatPercent(result.rice_confidence)}
              label={t("sar.confidence")}
            />
            <MetricCard
              value={`${result.estimated_area_pct.toFixed(1)}%`}
              label={t("sar.estimatedArea")}
            />
            <MetricCard
              value={result.analysis_date}
              label={t("sar.analysisDate")}
            />
          </div>

          {/* Summary text */}
          <Card>
            <p className="text-sm text-text-secondary leading-relaxed">
              {result.summary}
            </p>
          </Card>

          {/* Phenology signals */}
          <Card title={t("sar.phenologySignals")}>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {result.phenology_signals.map((signal) => (
                <div
                  key={signal.signal_type}
                  className={`p-4 rounded-lg border ${
                    signal.detected
                      ? "border-primary/30 bg-primary/5"
                      : "border-border bg-surface-subtle"
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-text-primary capitalize">
                      {signal.signal_type}
                    </span>
                    <span
                      className={`text-[10px] uppercase tracking-wide px-2 py-0.5 rounded ${
                        signal.detected
                          ? "bg-primary/10 text-primary"
                          : "bg-surface-subtle text-text-tertiary"
                      }`}
                    >
                      {signal.detected ? "Detected" : "Not detected"}
                    </span>
                  </div>
                  <div className="text-xs text-text-tertiary mb-1">
                    {signal.date_range}
                  </div>
                  <div className="text-xs text-text-secondary">
                    {signal.description}
                  </div>
                  <div className="mt-2 flex items-center gap-2">
                    <div className="flex-1 h-1.5 bg-surface-subtle rounded overflow-hidden">
                      <div
                        className={`h-full rounded ${
                          signal.detected ? "bg-primary" : "bg-text-tertiary"
                        }`}
                        style={{ width: `${signal.confidence * 100}%` }}
                      />
                    </div>
                    <span className="text-[10px] font-data text-text-tertiary">
                      {(signal.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* VH Time Series */}
          <Card title={t("sar.backscatterTimeSeries")}>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-[10px] uppercase tracking-wide text-text-tertiary border-b border-border">
                    <th className="pb-2 pr-4">Date</th>
                    <th className="pb-2 pr-4">VH (dB)</th>
                    <th className="pb-2 pr-4">VV (dB)</th>
                    <th className="pb-2">VH/VV</th>
                  </tr>
                </thead>
                <tbody>
                  {result.time_series.map((point) => (
                    <tr key={point.date} className="border-b border-border/50">
                      <td className="py-2 pr-4 text-text-secondary">
                        {point.date}
                      </td>
                      <td className="py-2 pr-4 font-data text-text-primary">
                        {point.vh_db.toFixed(1)}
                      </td>
                      <td className="py-2 pr-4 font-data text-text-primary">
                        {point.vv_db.toFixed(1)}
                      </td>
                      <td className="py-2 font-data text-text-tertiary">
                        {point.vh_vv_ratio.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
