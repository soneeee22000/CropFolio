import { useState, useEffect } from "react";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { useBayesianOptimize } from "@/hooks/useBayesianOptimize";
import { fetchTownships } from "@/api/townships";
import { fetchCrops } from "@/api/crops";
import { useLanguage } from "@/i18n/LanguageContext";
import { formatMMKCompact, formatPercent } from "@/utils/formatters";
import { CROP_COLORS } from "@/constants";
import type { Township } from "@/types/township";
import type { EvidenceItem } from "@/types/bayesian";

interface CropOption {
  id: string;
  name_en: string;
}

const EVIDENCE_OPTIONS: Array<{
  variable: string;
  label: string;
  values: string[];
}> = [
  {
    variable: "rainfall",
    label: "Observed Rainfall",
    values: ["low", "normal", "high"],
  },
  { variable: "drought", label: "Drought Observed", values: ["yes", "no"] },
  { variable: "flood", label: "Flood Observed", values: ["yes", "no"] },
  {
    variable: "soil",
    label: "Soil Quality",
    values: ["poor", "moderate", "good"],
  },
];

/** Bayesian evidence panel + yield prediction dashboard. */
export function BayesianDashboard() {
  const { t } = useLanguage();
  const [townships, setTownships] = useState<Township[]>([]);
  const [crops, setCrops] = useState<CropOption[]>([]);
  const [selectedTownship, setSelectedTownship] = useState("");
  const [selectedCrops, setSelectedCrops] = useState<string[]>([]);
  const [season, setSeason] = useState<"monsoon" | "dry">("dry");
  const [evidence, setEvidence] = useState<Record<string, string>>({});
  const { result, isLoading, error, optimize } = useBayesianOptimize();

  useEffect(() => {
    async function load() {
      const [twpRes, cropRes] = await Promise.all([
        fetchTownships(),
        fetchCrops(),
      ]);
      setTownships(twpRes.townships);
      setCrops(
        cropRes.crops.map((c: { id: string; name_en: string }) => ({
          id: c.id,
          name_en: c.name_en,
        })),
      );
    }
    load();
  }, []);

  const toggleCrop = (id: string) => {
    setSelectedCrops((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id],
    );
  };

  const setEvidenceValue = (variable: string, value: string) => {
    setEvidence((prev) => {
      if (prev[variable] === value) {
        const next = { ...prev };
        delete next[variable];
        return next;
      }
      return { ...prev, [variable]: value };
    });
  };

  const handleOptimize = () => {
    const evidenceItems: EvidenceItem[] = Object.entries(evidence).map(
      ([variable, value]) => ({ variable, value }),
    );
    optimize({
      crop_ids: selectedCrops,
      township_id: selectedTownship,
      season,
      risk_tolerance: 0.5,
      evidence: evidenceItems,
    });
  };

  const canSubmit = selectedTownship && selectedCrops.length >= 2;

  return (
    <div className="space-y-8 animate-fade-in-up">
      <div>
        <h2 className="font-display text-3xl text-text-primary">
          {t("bayesian.title")}
        </h2>
        <p className="text-text-secondary mt-1">{t("bayesian.subtitle")}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Selection */}
        <Card title={t("bayesian.setup")}>
          <div className="space-y-4">
            <div>
              <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
                {t("township.overline")}
              </label>
              <select
                value={selectedTownship}
                onChange={(e) => setSelectedTownship(e.target.value)}
                className="w-full p-2 rounded-lg border border-border bg-surface-elevated text-text-primary text-sm"
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
                {t("recommend.selectCrops")}
              </label>
              <div className="flex flex-wrap gap-2">
                {crops.map((c) => {
                  const selected = selectedCrops.includes(c.id);
                  return (
                    <button
                      key={c.id}
                      onClick={() => toggleCrop(c.id)}
                      className={`px-3 py-1.5 rounded-lg text-sm border transition-colors ${
                        selected
                          ? "border-primary bg-primary/10 text-primary font-medium"
                          : "border-border text-text-secondary hover:border-text-tertiary"
                      }`}
                    >
                      {c.name_en}
                    </button>
                  );
                })}
              </div>
            </div>
            <div className="flex gap-2">
              {(["dry", "monsoon"] as const).map((s) => (
                <button
                  key={s}
                  onClick={() => setSeason(s)}
                  className={`px-4 py-2 rounded-lg text-sm border transition-colors ${
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
        </Card>

        {/* Evidence panel */}
        <Card title={t("bayesian.evidence")}>
          <p className="text-xs text-text-tertiary mb-4">
            {t("bayesian.evidenceDesc")}
          </p>
          <div className="space-y-4">
            {EVIDENCE_OPTIONS.map((opt) => (
              <div key={opt.variable}>
                <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
                  {opt.label}
                </label>
                <div className="flex gap-2">
                  {opt.values.map((val) => {
                    const active = evidence[opt.variable] === val;
                    return (
                      <button
                        key={val}
                        onClick={() => setEvidenceValue(opt.variable, val)}
                        className={`px-3 py-1.5 rounded-lg text-sm border transition-colors capitalize ${
                          active
                            ? "border-accent bg-accent/10 text-accent font-medium"
                            : "border-border text-text-secondary hover:border-text-tertiary"
                        }`}
                      >
                        {val}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Submit */}
      <div className="flex justify-center">
        <button
          onClick={handleOptimize}
          disabled={!canSubmit || isLoading}
          className="px-8 py-3 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? t("bayesian.running") : t("bayesian.run")}
        </button>
      </div>

      {isLoading && <LoadingSpinner message={t("bayesian.running")} />}
      {error && <ErrorAlert message={error} />}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <MetricCard
              value={formatMMKCompact(result.metrics.expected_income_per_ha)}
              label={t("recommend.expectedIncome")}
              highlight
            />
            <MetricCard
              value={formatPercent(result.metrics.risk_reduction_pct / 100)}
              label={t("recommend.riskReduction")}
            />
            <MetricCard
              value={result.metrics.sharpe_ratio.toFixed(2)}
              label="Sharpe Ratio"
            />
            <MetricCard value={result.model_type.toUpperCase()} label="Model" />
          </div>

          {/* Yield predictions */}
          <Card title={t("bayesian.predictions")}>
            <div className="space-y-4">
              {result.bayesian_predictions.map((pred) => {
                const color = CROP_COLORS[pred.crop_id] ?? "#666";
                return (
                  <div
                    key={pred.crop_id}
                    className="p-4 rounded-lg border border-border"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: color }}
                        />
                        <span className="text-sm font-medium text-text-primary capitalize">
                          {pred.crop_id.replace(/_/g, " ")}
                        </span>
                      </div>
                      <span className="font-data text-lg text-accent">
                        {pred.expected_yield_factor.toFixed(2)}x
                      </span>
                    </div>
                    {/* Yield probability bars */}
                    <div className="space-y-1.5">
                      {(["low", "medium", "high"] as const).map((cat) => {
                        const prob = pred.yield_probabilities[cat] ?? 0;
                        const barColor =
                          cat === "low"
                            ? "bg-danger"
                            : cat === "medium"
                              ? "bg-warning"
                              : "bg-primary";
                        return (
                          <div key={cat} className="flex items-center gap-2">
                            <span className="text-[10px] w-14 text-text-tertiary capitalize">
                              {cat}
                            </span>
                            <div className="flex-1 h-4 bg-surface-subtle rounded overflow-hidden">
                              <div
                                className={`h-full ${barColor} rounded transition-all`}
                                style={{ width: `${prob * 100}%` }}
                              />
                            </div>
                            <span className="text-[10px] w-10 text-right font-data text-text-secondary">
                              {(prob * 100).toFixed(0)}%
                            </span>
                          </div>
                        );
                      })}
                    </div>
                    {pred.evidence_used.length > 0 && (
                      <div className="mt-2 text-[10px] text-text-tertiary">
                        Evidence: {pred.evidence_used.join(", ")}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </Card>

          {/* Portfolio weights */}
          <Card title={t("bayesian.portfolioWeights")}>
            <div className="space-y-2">
              {result.weights
                .filter((w) => w.weight > 0.01)
                .sort((a, b) => b.weight - a.weight)
                .map((w) => {
                  const color = CROP_COLORS[w.crop_id] ?? "#666";
                  return (
                    <div
                      key={w.crop_id}
                      className="flex items-center gap-3 p-3 rounded-lg border border-border"
                    >
                      <div
                        className="w-3 h-3 rounded-full flex-shrink-0"
                        style={{ backgroundColor: color }}
                      />
                      <span className="text-sm text-text-primary flex-1">
                        {w.crop_name}
                      </span>
                      <span className="font-data text-lg text-text-primary">
                        {(w.weight * 100).toFixed(0)}%
                      </span>
                      <span className="font-data text-sm text-text-secondary">
                        {formatMMKCompact(w.expected_income_per_ha)}
                      </span>
                    </div>
                  );
                })}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
