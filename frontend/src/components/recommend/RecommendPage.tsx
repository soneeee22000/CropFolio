import { useState, useEffect } from "react";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { RecommendationCard } from "./RecommendationCard";
import { SoilProfileCard } from "./SoilProfileCard";
import { ConfidenceGauge } from "./ConfidenceGauge";
import { useRecommend } from "@/hooks/useRecommend";
import { fetchTownships } from "@/api/townships";
import { fetchCrops } from "@/api/crops";
import { useLanguage } from "@/i18n/LanguageContext";
import { formatMMKCompact, formatPercent } from "@/utils/formatters";
import type { Township } from "@/types/township";

interface CropOption {
  id: string;
  name_en: string;
}

/** Recommendation engine page: multi-township + crop selection -> results. */
export function RecommendPage() {
  const { t } = useLanguage();
  const [townships, setTownships] = useState<Township[]>([]);
  const [crops, setCrops] = useState<CropOption[]>([]);
  const [selectedTownships, setSelectedTownships] = useState<string[]>([]);
  const [selectedCrops, setSelectedCrops] = useState<string[]>([]);
  const [season, setSeason] = useState<"monsoon" | "dry">("dry");
  const [riskTolerance, setRiskTolerance] = useState(0.5);
  const [loadError, setLoadError] = useState<string | null>(null);
  const { result, isLoading, error, recommend } = useRecommend();

  useEffect(() => {
    async function loadOptions() {
      try {
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
      } catch {
        setLoadError("Failed to load townships and crops");
      }
    }
    loadOptions();
  }, []);

  const toggleTownship = (id: string) => {
    setSelectedTownships((prev) =>
      prev.includes(id) ? prev.filter((tw) => tw !== id) : [...prev, id],
    );
  };

  const toggleCrop = (id: string) => {
    setSelectedCrops((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id],
    );
  };

  const canSubmit = selectedTownships.length > 0 && selectedCrops.length >= 2;

  const handleSubmit = () => {
    recommend({
      township_ids: selectedTownships,
      crop_ids: selectedCrops,
      risk_tolerance: riskTolerance,
      season,
    });
  };

  const regions = [...new Set(townships.map((tw) => tw.region))];

  if (loadError) {
    return <ErrorAlert message={loadError} />;
  }

  return (
    <div className="space-y-8 animate-fade-in-up">
      <div>
        <h2 className="font-display text-3xl text-text-primary">
          {t("recommend.title")}
        </h2>
        <p className="text-text-secondary mt-1">{t("recommend.subtitle")}</p>
      </div>

      {/* Township selection */}
      <Card title={t("recommend.selectTownships")}>
        <div className="space-y-4">
          {regions.map((region) => (
            <div key={region}>
              <h5 className="text-xs uppercase tracking-wide text-text-tertiary mb-2">
                {region}
              </h5>
              <div className="flex flex-wrap gap-2">
                {townships
                  .filter((tw) => tw.region === region)
                  .map((tw) => {
                    const selected = selectedTownships.includes(tw.id);
                    return (
                      <button
                        key={tw.id}
                        onClick={() => toggleTownship(tw.id)}
                        className={`px-3 py-1.5 rounded-lg text-sm border transition-colors ${
                          selected
                            ? "border-primary bg-primary/10 text-primary font-medium"
                            : "border-border text-text-secondary hover:border-text-tertiary"
                        }`}
                      >
                        {tw.name}
                      </button>
                    );
                  })}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Crop selection + controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title={t("recommend.selectCrops")}>
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
        </Card>
        <Card title={t("recommend.parameters")}>
          <div className="space-y-4">
            <div>
              <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
                {t("recommend.season")}
              </label>
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
            <div>
              <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
                {t("recommend.riskTolerance")}:{" "}
                {(riskTolerance * 100).toFixed(0)}%
              </label>
              <input
                type="range"
                min={0}
                max={1}
                step={0.05}
                value={riskTolerance}
                onChange={(e) => setRiskTolerance(Number(e.target.value))}
                className="w-full accent-primary"
              />
              <div className="flex justify-between text-[10px] text-text-tertiary mt-1">
                <span>{t("recommend.conservative")}</span>
                <span>{t("recommend.aggressive")}</span>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Submit button */}
      <div className="flex justify-center">
        <button
          onClick={handleSubmit}
          disabled={!canSubmit || isLoading}
          className="px-8 py-3 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? t("recommend.generating") : t("recommend.generate")}
        </button>
      </div>

      {isLoading && <LoadingSpinner message={t("recommend.running")} />}
      {error && <ErrorAlert message={error} />}

      {/* Results */}
      {result &&
        result.recommendations.map((rec) => (
          <div key={rec.township_id} className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="font-display text-2xl text-text-primary">
                {rec.township_name}
                <span className="text-sm text-text-tertiary ml-2 capitalize">
                  {rec.season}
                </span>
              </h3>
              {rec.confidence && (
                <div className="relative">
                  <ConfidenceGauge value={rec.confidence.success_probability} />
                </div>
              )}
            </div>

            {/* Summary metrics */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <MetricCard
                value={formatMMKCompact(rec.expected_income_per_ha)}
                label={t("recommend.expectedIncome")}
                highlight
              />
              <MetricCard
                value={formatPercent(rec.risk_reduction_pct / 100)}
                label={t("recommend.riskReduction")}
                sublabel={t("recommend.vsMonocrop")}
              />
              {rec.confidence && (
                <>
                  <MetricCard
                    value={formatPercent(rec.confidence.success_probability)}
                    label={t("recommend.successProb")}
                  />
                  <MetricCard
                    value={formatMMKCompact(rec.confidence.percentile_5)}
                    label={t("recommend.worstCase")}
                  />
                </>
              )}
            </div>

            {/* Soil profile */}
            {rec.soil && <SoilProfileCard soil={rec.soil} />}

            {/* Crop-fertilizer cards */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {rec.crops.map((crop) => (
                <RecommendationCard key={crop.crop_id} recommendation={crop} />
              ))}
            </div>
          </div>
        ))}
    </div>
  );
}
