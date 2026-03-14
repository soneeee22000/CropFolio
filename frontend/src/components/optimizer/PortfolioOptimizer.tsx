import { useState } from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { useCrops } from "@/hooks/useCrops";
import { useOptimize } from "@/hooks/useOptimize";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { Badge } from "@/components/common/Badge";
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

/** Portfolio optimization view with crop selection and results. */
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
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">
          Optimize Crop Portfolio
        </h2>
        <p className="text-gray-500 mt-1">
          Select crops and risk tolerance, then optimize
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Left: Controls */}
        <div className="space-y-4">
          <Card title="Select Crops (min. 2)">
            <div className="grid grid-cols-2 gap-2">
              {crops.map((crop) => (
                <button
                  key={crop.id}
                  onClick={() => toggleCrop(crop.id)}
                  className={`text-left p-3 rounded-lg border-2 transition-colors ${
                    selectedCrops.includes(crop.id)
                      ? "border-primary bg-green-50"
                      : "border-gray-200 hover:border-gray-300"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: CROP_COLORS[crop.id] }}
                    />
                    <span className="font-medium text-sm">{crop.name_en}</span>
                  </div>
                  <div className="flex items-center gap-1 mt-1">
                    <Badge label={crop.category} variant="info" />
                    <span className="font-myanmar text-xs text-gray-400">
                      {crop.name_mm}
                    </span>
                  </div>
                  <div className="mt-2 space-y-1">
                    <ToleranceBar
                      label="Drought"
                      value={crop.drought_tolerance}
                    />
                    <ToleranceBar label="Flood" value={crop.flood_tolerance} />
                  </div>
                </button>
              ))}
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
              className="w-full accent-primary"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
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
            className="w-full py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "Optimizing..." : "Optimize Portfolio"}
          </button>

          {error && <ErrorAlert message={error} />}
        </div>

        {/* Right: Results */}
        <div className="space-y-4">
          {result ? (
            <OptimizationResults result={result} />
          ) : (
            <Card className="flex items-center justify-center h-64 text-gray-400 text-sm">
              Select crops and click Optimize to see results
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

/** Display optimization results with pie charts and metrics. */
function OptimizationResults({ result }: { result: OptimizeResponse }) {
  const monocropData = [{ name: "Rice (100%)", value: 1, id: "rice" }];
  const optimizedData = result.weights
    .filter((w) => w.weight > 0.01)
    .map((w) => ({ name: w.crop_name, value: w.weight, id: w.crop_id }));

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <Card title="Monocrop (Rice Only)">
          <PieChartView data={monocropData} />
        </Card>
        <Card title="Optimized Portfolio">
          <PieChartView data={optimizedData} />
        </Card>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <MetricCard
          value={formatMMKCompact(result.metrics.expected_income_per_ha)}
          label="Expected Income/ha"
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
        <p className="text-sm text-gray-600">
          Diversification reduces risk by{" "}
          <span className="font-bold text-green-700">
            {result.metrics.risk_reduction_pct.toFixed(1)}%
          </span>{" "}
          compared to monocrop rice farming.
        </p>
      </Card>
    </div>
  );
}

/** Recharts pie chart for crop allocation. */
function PieChartView({
  data,
}: {
  data: { name: string; value: number; id: string }[];
}) {
  return (
    <ResponsiveContainer width="100%" height={180}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={70}
          dataKey="value"
          label={({ name, value }) => `${name} ${Math.round(value * 100)}%`}
          labelLine={false}
          animationDuration={800}
        >
          {data.map((entry) => (
            <Cell key={entry.id} fill={getCropColor(entry.id)} />
          ))}
        </Pie>
        <Tooltip formatter={(val) => `${(Number(val) * 100).toFixed(1)}%`} />
      </PieChart>
    </ResponsiveContainer>
  );
}

/** Tiny horizontal bar showing tolerance level. */
function ToleranceBar({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className="text-xs text-gray-400 w-12">{label}</span>
      <div className="flex-1 bg-gray-200 rounded-full h-1.5">
        <div
          className="h-1.5 rounded-full bg-primary"
          style={{ width: `${value * 100}%` }}
        />
      </div>
    </div>
  );
}
