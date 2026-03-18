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
import { formatMMKCompact, formatPercent } from "@/utils/formatters";
import type { Township } from "@/types/township";

interface CropOption {
  id: string;
  name_en: string;
}

/** Recommendation engine page: multi-township + crop selection -> results. */
export function RecommendPage() {
  const [townships, setTownships] = useState<Township[]>([]);
  const [crops, setCrops] = useState<CropOption[]>([]);
  const [selectedTownships, setSelectedTownships] = useState<string[]>([]);
  const [selectedCrops, setSelectedCrops] = useState<string[]>([]);
  const [season, setSeason] = useState<"monsoon" | "dry">("dry");
  const [riskTolerance, setRiskTolerance] = useState(0.5);
  const { result, isLoading, error, recommend } = useRecommend();

  useEffect(() => {
    async function loadOptions() {
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
    loadOptions();
  }, []);

  const toggleTownship = (id: string) => {
    setSelectedTownships((prev) =>
      prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id],
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

  const regions = [...new Set(townships.map((t) => t.region))];

  return (
    <div className="space-y-8 animate-fade-in-up">
      <div>
        <h2 className="font-display text-3xl text-text-primary">
          Recommendation Engine
        </h2>
        <p className="text-text-secondary mt-1">
          Select townships and crops to generate optimized crop-fertilizer
          recommendations
        </p>
      </div>

      {/* Township selection */}
      <Card title="Select Townships">
        <div className="space-y-4">
          {regions.map((region) => (
            <div key={region}>
              <h5 className="text-xs uppercase tracking-wide text-text-tertiary mb-2">
                {region}
              </h5>
              <div className="flex flex-wrap gap-2">
                {townships
                  .filter((t) => t.region === region)
                  .map((t) => {
                    const selected = selectedTownships.includes(t.id);
                    return (
                      <button
                        key={t.id}
                        onClick={() => toggleTownship(t.id)}
                        className={`px-3 py-1.5 rounded-lg text-sm border transition-colors ${
                          selected
                            ? "border-primary bg-primary/10 text-primary font-medium"
                            : "border-border text-text-secondary hover:border-text-tertiary"
                        }`}
                      >
                        {t.name}
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
        <Card title="Select Crops (min. 2)">
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
        <Card title="Parameters">
          <div className="space-y-4">
            <div>
              <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
                Season
              </label>
              <div className="flex gap-2">
                {(["dry", "monsoon"] as const).map((s) => (
                  <button
                    key={s}
                    onClick={() => setSeason(s)}
                    className={`px-4 py-2 rounded-lg text-sm border capitalize transition-colors ${
                      season === s
                        ? "border-primary bg-primary/10 text-primary font-medium"
                        : "border-border text-text-secondary"
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
                Risk Tolerance: {(riskTolerance * 100).toFixed(0)}%
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
                <span>Conservative</span>
                <span>Aggressive</span>
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
          {isLoading ? "Generating..." : "Generate Recommendations"}
        </button>
      </div>

      {isLoading && (
        <LoadingSpinner message="Running portfolio optimization + 1,000 Monte Carlo simulations..." />
      )}
      {error && <ErrorAlert message={error} />}

      {/* Results */}
      {result &&
        result.recommendations.map((rec) => (
          <div key={rec.township_id} className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="font-display text-2xl text-text-primary">
                {rec.township_name}
                <span className="text-sm text-text-tertiary ml-2 capitalize">
                  {rec.season} season
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
                label="Expected Income/ha"
                highlight
              />
              <MetricCard
                value={formatPercent(rec.risk_reduction_pct / 100)}
                label="Risk Reduction"
                sublabel="vs. monocrop"
              />
              {rec.confidence && (
                <>
                  <MetricCard
                    value={formatPercent(rec.confidence.success_probability)}
                    label="Success Probability"
                  />
                  <MetricCard
                    value={formatMMKCompact(rec.confidence.percentile_5)}
                    label="Worst Case (5th pctl)"
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
