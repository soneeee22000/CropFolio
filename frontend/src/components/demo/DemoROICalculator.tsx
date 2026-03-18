import { useState, useEffect } from "react";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { FertilizerBadge } from "@/components/recommend/FertilizerBadge";
import { SoilProfileCard } from "@/components/recommend/SoilProfileCard";
import { fetchTownships } from "@/api/townships";
import { fetchCrops } from "@/api/crops";
import { calculateDemoROI } from "@/api/recommend";
import { formatMMK, formatPercent } from "@/utils/formatters";
import type { Township } from "@/types/township";
import type { DemoROIResponse } from "@/types/recommend";

interface CropOption {
  id: string;
  name_en: string;
}

/** Demo crop ROI calculator for distributors. */
export function DemoROICalculator() {
  const [townships, setTownships] = useState<Township[]>([]);
  const [crops, setCrops] = useState<CropOption[]>([]);
  const [townshipId, setTownshipId] = useState("");
  const [cropId, setCropId] = useState("");
  const [area, setArea] = useState(1.0);
  const [season, setSeason] = useState<"monsoon" | "dry">("dry");
  const [result, setResult] = useState<DemoROIResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

  const handleCalculate = async () => {
    if (!townshipId || !cropId) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await calculateDemoROI({
        township_id: townshipId,
        crop_id: cropId,
        area_hectares: area,
        season,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Calculation failed");
    } finally {
      setIsLoading(false);
    }
  };

  const isProfitable = result ? result.expected_profit_mmk > 0 : false;

  return (
    <div className="space-y-8 animate-fade-in-up">
      <div>
        <h2 className="font-display text-3xl text-text-primary">
          Demo ROI Calculator
        </h2>
        <p className="text-text-secondary mt-1">
          Calculate costs, expected returns, and reimbursement risk before
          committing to a demo farm
        </p>
      </div>

      {/* Input form */}
      <Card title="Scenario">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
              Township
            </label>
            <select
              value={townshipId}
              onChange={(e) => setTownshipId(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-border bg-surface text-text-primary text-sm"
            >
              <option value="">Select...</option>
              {townships.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name} ({t.region})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
              Crop
            </label>
            <select
              value={cropId}
              onChange={(e) => setCropId(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-border bg-surface text-text-primary text-sm"
            >
              <option value="">Select...</option>
              {crops.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name_en}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
              Area (hectares)
            </label>
            <input
              type="number"
              min={0.1}
              max={100}
              step={0.5}
              value={area}
              onChange={(e) => setArea(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-lg border border-border bg-surface text-text-primary text-sm"
            />
          </div>
          <div>
            <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
              Season
            </label>
            <div className="flex gap-2">
              {(["dry", "monsoon"] as const).map((s) => (
                <button
                  key={s}
                  onClick={() => setSeason(s)}
                  className={`flex-1 px-3 py-2 rounded-lg text-sm border capitalize transition-colors ${
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
        </div>
        <div className="mt-6 flex justify-center">
          <button
            onClick={handleCalculate}
            disabled={!townshipId || !cropId || isLoading}
            className="px-8 py-3 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "Calculating..." : "Calculate ROI"}
          </button>
        </div>
      </Card>

      {isLoading && <LoadingSpinner message="Running climate simulation..." />}
      {error && <ErrorAlert message={error} />}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          <h3 className="font-display text-2xl text-text-primary">
            {result.crop_name} in {result.township_name}
            <span className="text-sm text-text-tertiary ml-2">
              {result.area_hectares} ha, {result.season} season
            </span>
          </h3>

          {/* Financial summary */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <MetricCard
              value={formatMMK(result.total_input_cost_mmk)}
              label="Total Input Cost"
              sublabel={`Seed: ${formatMMK(result.seed_cost_mmk)} + Fert: ${formatMMK(result.fertilizer_cost_mmk)}`}
            />
            <MetricCard
              value={formatMMK(result.expected_revenue_mmk)}
              label="Expected Revenue"
              highlight={isProfitable}
            />
            <MetricCard
              value={formatMMK(result.expected_profit_mmk)}
              label="Expected Profit"
              highlight={isProfitable}
            />
            <MetricCard
              value={formatMMK(result.reimbursement_exposure_mmk)}
              label="Reimbursement Risk"
              sublabel="Expected payout if demo fails"
            />
          </div>

          {/* Risk metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card title="Risk Assessment">
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-4 rounded-lg bg-surface-subtle">
                  <div
                    className={`font-data text-3xl ${result.success_probability >= 0.7 ? "text-primary" : result.success_probability >= 0.4 ? "text-warning" : "text-danger"}`}
                  >
                    {formatPercent(result.success_probability)}
                  </div>
                  <div className="text-[10px] uppercase tracking-wide text-text-tertiary mt-2">
                    Success Probability
                  </div>
                </div>
                <div className="text-center p-4 rounded-lg bg-surface-subtle">
                  <div
                    className={`font-data text-3xl ${result.catastrophic_loss_probability <= 0.1 ? "text-primary" : result.catastrophic_loss_probability <= 0.3 ? "text-warning" : "text-danger"}`}
                  >
                    {formatPercent(result.catastrophic_loss_probability)}
                  </div>
                  <div className="text-[10px] uppercase tracking-wide text-text-tertiary mt-2">
                    Catastrophic Loss Risk
                  </div>
                </div>
              </div>
            </Card>

            {result.recommended_fertilizer && (
              <Card title="Recommended Fertilizer">
                <div className="space-y-3">
                  <FertilizerBadge
                    formulation={result.recommended_fertilizer.formulation}
                    name={result.recommended_fertilizer.fertilizer_name}
                    score={result.recommended_fertilizer.score}
                  />
                  <div className="text-sm text-text-secondary">
                    {result.recommended_fertilizer.reasoning}
                  </div>
                  <div className="flex gap-4 text-xs text-text-tertiary">
                    <span>
                      Rate:{" "}
                      {result.recommended_fertilizer.recommended_rate_kg_per_ha}{" "}
                      kg/ha
                    </span>
                    <span>
                      Cost:{" "}
                      {formatMMK(result.recommended_fertilizer.cost_per_ha_mmk)}
                      /ha
                    </span>
                  </div>
                </div>
              </Card>
            )}
          </div>

          {result.soil && <SoilProfileCard soil={result.soil} />}
        </div>
      )}
    </div>
  );
}
