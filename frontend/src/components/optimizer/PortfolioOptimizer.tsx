import { useState } from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Label } from "recharts";
import { useCrops } from "@/hooks/useCrops";
import { useOptimize } from "@/hooks/useOptimize";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { formatMMKCompact } from "@/utils/formatters";
import { getCropColor } from "@/utils/colors";
import {
  CROP_COLORS,
  DEFAULT_RISK_TOLERANCE,
  MIN_CROPS_FOR_OPTIMIZATION,
} from "@/constants";
import type { OptimizeResponse } from "@/types/optimizer";

interface PortfolioOptimizerProps {
  townshipId: string;
  season: "monsoon" | "dry";
  onComplete: (result: OptimizeResponse) => void;
}

/** Premium portfolio optimization view. */
export function PortfolioOptimizer({
  townshipId,
  season,
  onComplete,
}: PortfolioOptimizerProps) {
  const { crops, isLoading: cropsLoading } = useCrops();
  const { result, isLoading, error, optimize } = useOptimize();
  const [selectedCrops, setSelectedCrops] = useState<string[]>([]);
  const [riskTolerance, setRiskTolerance] = useState(DEFAULT_RISK_TOLERANCE);

  const toggleCrop = (cropId: string) => {
    setSelectedCrops((prev) =>
      prev.includes(cropId)
        ? prev.filter((c) => c !== cropId)
        : [...prev, cropId],
    );
  };

  const handleOptimize = async () => {
    const res = await optimize({
      crop_ids: selectedCrops,
      township_id: townshipId,
      risk_tolerance: riskTolerance,
      season,
    });
    if (res) onComplete(res);
  };

  if (cropsLoading) return <LoadingSpinner message="Loading crops..." />;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <p className="text-[11px] uppercase tracking-[0.2em] text-text-tertiary mb-3">
          Portfolio
        </p>
        <h2 className="font-display text-4xl text-text-primary">
          Optimize Crop Allocation
        </h2>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <Card title="Select Crops">
            <p className="text-sm text-text-tertiary mb-4">
              Choose at least 2 crops to diversify
            </p>
            <div className="grid grid-cols-2 gap-3">
              {crops.map((crop) => {
                const selected = selectedCrops.includes(crop.id);
                return (
                  <button
                    key={crop.id}
                    onClick={() => toggleCrop(crop.id)}
                    className={`text-left p-4 rounded-xl border transition-all duration-200 relative ${
                      selected
                        ? "border-primary bg-primary-subtle"
                        : "border-border hover:border-text-tertiary"
                    }`}
                  >
                    {selected && (
                      <div className="absolute top-3 right-3 w-5 h-5 bg-primary rounded-full flex items-center justify-center">
                        <svg
                          width="10"
                          height="8"
                          viewBox="0 0 10 8"
                          fill="none"
                        >
                          <path
                            d="M1 4L3.5 6.5L9 1"
                            stroke="white"
                            strokeWidth="1.5"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />
                        </svg>
                      </div>
                    )}
                    <div className="flex items-center gap-2.5 mb-1">
                      <div
                        className={`w-4 h-4 rounded-full transition-shadow ${selected ? "ring-2 ring-primary/30" : ""}`}
                        style={{ backgroundColor: CROP_COLORS[crop.id] }}
                      />
                      <span className="font-medium text-sm text-text-primary">
                        {crop.name_en}
                      </span>
                    </div>
                    <span className="font-myanmar text-xs text-text-tertiary block mb-2">
                      {crop.name_mm}
                    </span>
                    <div className="space-y-1.5">
                      <ToleranceBar
                        label="Drought"
                        value={crop.drought_tolerance}
                        color="var(--color-warning)"
                      />
                      <ToleranceBar
                        label="Flood"
                        value={crop.flood_tolerance}
                        color="#4A8B9E"
                      />
                    </div>
                  </button>
                );
              })}
            </div>
          </Card>

          <Card title="Risk Tolerance">
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={riskTolerance}
              onChange={(e) => setRiskTolerance(Number(e.target.value))}
            />
            <div className="flex justify-between text-[11px] uppercase tracking-wide text-text-tertiary mt-2">
              <span>Conservative</span>
              <span>Balanced</span>
              <span>Aggressive</span>
            </div>
          </Card>

          <button
            onClick={handleOptimize}
            disabled={
              selectedCrops.length < MIN_CROPS_FOR_OPTIMIZATION || isLoading
            }
            className="w-full py-4 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors duration-200 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {isLoading ? "Optimizing..." : "Optimize Portfolio"}
          </button>

          {error && <ErrorAlert message={error} />}
        </div>

        <div className="space-y-6">
          {result ? (
            <OptimizationResults result={result} />
          ) : (
            <Card className="flex items-center justify-center h-72 text-text-tertiary text-sm">
              Select crops and click Optimize to see results
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

/** Optimization results with donut charts and metrics. */
function OptimizationResults({ result }: { result: OptimizeResponse }) {
  const monocropData = [{ name: "Rice (100%)", value: 1, id: "rice" }];
  const optimizedData = result.weights
    .filter((w) => w.weight > 0.01)
    .map((w) => ({ name: w.crop_name, value: w.weight, id: w.crop_id }));

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-6">
        <Card>
          <p className="text-[11px] uppercase tracking-[0.15em] text-text-tertiary mb-2">
            Monocrop
          </p>
          <DonutChart data={monocropData} centerLabel="1 crop" />
        </Card>
        <Card>
          <p className="text-[11px] uppercase tracking-[0.15em] text-text-tertiary mb-2">
            Optimized
          </p>
          <DonutChart
            data={optimizedData}
            centerLabel={`${optimizedData.length} crops`}
          />
        </Card>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <MetricCard
          value={formatMMKCompact(result.metrics.expected_income_per_ha)}
          label="Expected Income"
        />
        <MetricCard
          value={formatMMKCompact(result.metrics.income_std_dev)}
          label="Risk (Std Dev)"
        />
        <MetricCard
          value={result.metrics.sharpe_ratio.toFixed(2)}
          label="Sharpe Ratio"
        />
        <MetricCard
          value={`${result.metrics.risk_reduction_pct.toFixed(1)}%`}
          label="Risk Reduction"
          highlight
        />
      </div>

      <Card className="text-center">
        <p className="text-sm text-text-secondary">
          Diversification reduces risk by{" "}
          <span className="font-data font-medium text-accent">
            {result.metrics.risk_reduction_pct.toFixed(1)}%
          </span>{" "}
          compared to monocrop farming.
        </p>
      </Card>
    </div>
  );
}

/** Donut chart with centered label. */
function DonutChart({
  data,
  centerLabel,
}: {
  data: { name: string; value: number; id: string }[];
  centerLabel: string;
}) {
  return (
    <div>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={85}
            innerRadius={55}
            dataKey="value"
            animationDuration={800}
            stroke="none"
          >
            {data.map((entry) => (
              <Cell key={entry.id} fill={getCropColor(entry.id)} />
            ))}
            <Label
              value={centerLabel}
              position="center"
              className="font-display text-lg"
              fill="var(--color-text-primary)"
            />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="space-y-1 mt-2">
        {data.map((entry) => (
          <div key={entry.id} className="flex items-center gap-2 text-xs">
            <div
              className="w-2.5 h-2.5 rounded-full"
              style={{ backgroundColor: getCropColor(entry.id) }}
            />
            <span className="text-text-secondary">{entry.name}</span>
            <span className="font-data text-text-tertiary ml-auto">
              {Math.round(entry.value * 100)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

/** Tolerance bar with custom color. */
function ToleranceBar({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-[11px] text-text-tertiary w-12">{label}</span>
      <div className="flex-1 bg-border rounded-full h-2">
        <div
          className="h-2 rounded-full transition-all duration-500"
          style={{ width: `${value * 100}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}
