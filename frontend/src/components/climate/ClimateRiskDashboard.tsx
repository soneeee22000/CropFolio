import { useClimateRisk } from "@/hooks/useClimateRisk";
import { Card } from "@/components/common/Card";
import { Badge } from "@/components/common/Badge";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { formatPercent, formatNumber } from "@/utils/formatters";
import { getRiskColor } from "@/utils/colors";

interface ClimateRiskDashboardProps {
  townshipId: string;
  season: "monsoon" | "dry";
  onContinue: () => void;
}

/** Climate risk assessment dashboard for a selected township. */
export function ClimateRiskDashboard({
  townshipId,
  season,
  onContinue,
}: ClimateRiskDashboardProps) {
  const { climateRisk, isLoading, error } = useClimateRisk(townshipId, season);

  if (isLoading) return <LoadingSpinner message="Analyzing climate risk..." />;
  if (error) return <ErrorAlert message={error} />;
  if (!climateRisk) return null;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">
          Climate Risk: {climateRisk.township_name}
        </h2>
        <p className="text-gray-500 mt-1">
          {season === "monsoon" ? "Monsoon" : "Dry"} season forecast
        </p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <RiskGauge
          label="Drought Risk"
          probability={climateRisk.drought_probability}
        />
        <RiskGauge
          label="Flood Risk"
          probability={climateRisk.flood_probability}
        />
        <MetricCard
          value={`${formatNumber(climateRisk.rainfall_forecast_mm, 0)} mm`}
          label="Forecast Rainfall"
          sublabel={`Avg: ${formatNumber(climateRisk.rainfall_historical_avg_mm, 0)} mm`}
        />
        <MetricCard
          value={`${climateRisk.temp_anomaly_celsius > 0 ? "+" : ""}${climateRisk.temp_anomaly_celsius.toFixed(1)}°C`}
          label="Temp Anomaly"
          sublabel="vs. historical average"
        />
      </div>

      <Card className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-600">Overall Risk Level:</span>
          <Badge
            label={climateRisk.risk_level.toUpperCase()}
            riskLevel={climateRisk.risk_level}
          />
        </div>
        <div className="text-xs text-gray-400">
          Source:{" "}
          {climateRisk.data_source === "live"
            ? "NASA POWER + Open-Meteo"
            : "Regional averages (fallback)"}
          {" · "}Confidence: {formatPercent(climateRisk.confidence)}
        </div>
      </Card>

      <div className="text-center">
        <button
          onClick={onContinue}
          className="px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark transition-colors"
        >
          Optimize Crop Portfolio
        </button>
      </div>
    </div>
  );
}

/** Semi-circular risk gauge rendered with SVG. */
function RiskGauge({
  label,
  probability,
}: {
  label: string;
  probability: number;
}) {
  const percentage = Math.round(probability * 100);
  const color = getRiskColor(
    probability >= 0.6 ? "high" : probability >= 0.3 ? "moderate" : "low",
  );
  const angle = probability * 180;
  const radians = (angle * Math.PI) / 180;
  const SIZE = 120;
  const RADIUS = 45;
  const cx = SIZE / 2;
  const cy = SIZE / 2 + 10;

  const endX = cx + RADIUS * Math.cos(Math.PI - radians);
  const endY = cy - RADIUS * Math.sin(Math.PI - radians);
  const largeArc = angle > 90 ? 1 : 0;

  return (
    <div className="bg-gray-50 rounded-lg p-4 text-center">
      <svg width={SIZE} height={SIZE / 2 + 20} className="mx-auto">
        <path
          d={`M ${cx - RADIUS} ${cy} A ${RADIUS} ${RADIUS} 0 0 1 ${cx + RADIUS} ${cy}`}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth="8"
          strokeLinecap="round"
        />
        {probability > 0 && (
          <path
            d={`M ${cx - RADIUS} ${cy} A ${RADIUS} ${RADIUS} 0 ${largeArc} 1 ${endX} ${endY}`}
            fill="none"
            stroke={color}
            strokeWidth="8"
            strokeLinecap="round"
          />
        )}
        <text
          x={cx}
          y={cy - 10}
          textAnchor="middle"
          className="text-lg font-bold fill-gray-900"
        >
          {percentage}%
        </text>
      </svg>
      <div className="text-sm text-gray-600 -mt-1">{label}</div>
    </div>
  );
}
