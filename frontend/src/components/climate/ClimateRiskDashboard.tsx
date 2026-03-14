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

/** Premium climate risk assessment dashboard. */
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
    <div className="max-w-5xl mx-auto">
      <div className="text-center mb-12">
        <p className="text-[11px] uppercase tracking-[0.2em] text-text-tertiary mb-3">
          {season === "monsoon" ? "Monsoon" : "Dry"} Season Forecast
        </p>
        <h2 className="font-display text-4xl text-text-primary">
          {climateRisk.township_name}
        </h2>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
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
          value={`${climateRisk.temp_anomaly_celsius > 0 ? "+" : ""}${climateRisk.temp_anomaly_celsius.toFixed(1)}\u00B0C`}
          label="Temp Anomaly"
          sublabel="vs. historical average"
        />
      </div>

      <Card className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-12">
        <div className="flex items-center gap-3">
          <span className="text-sm text-text-secondary">Overall Risk:</span>
          <Badge
            label={climateRisk.risk_level.toUpperCase()}
            riskLevel={climateRisk.risk_level}
          />
        </div>
        <p className="text-xs text-text-tertiary">
          {climateRisk.data_source === "live"
            ? "NASA POWER + Open-Meteo"
            : "Regional averages (fallback)"}
          {" \u00B7 "}
          Confidence: {formatPercent(climateRisk.confidence)}
        </p>
      </Card>

      <div className="text-center">
        <button
          onClick={onContinue}
          className="px-8 py-4 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors duration-200"
        >
          Optimize Crop Portfolio
        </button>
      </div>
    </div>
  );
}

/** SVG risk gauge with draw-on animation. */
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
  const SIZE = 160;
  const RADIUS = 55;
  const cx = SIZE / 2;
  const cy = SIZE / 2 + 10;

  const endX = cx + RADIUS * Math.cos(Math.PI - radians);
  const endY = cy - RADIUS * Math.sin(Math.PI - radians);
  const largeArc = angle > 90 ? 1 : 0;

  const arcLength = (angle / 180) * Math.PI * RADIUS;

  return (
    <div className="bg-surface-subtle rounded-xl p-6 text-center">
      <svg width={SIZE} height={SIZE / 2 + 24} className="mx-auto">
        <path
          d={`M ${cx - RADIUS} ${cy} A ${RADIUS} ${RADIUS} 0 0 1 ${cx + RADIUS} ${cy}`}
          fill="none"
          stroke="var(--color-border)"
          strokeWidth="10"
          strokeLinecap="round"
        />
        {probability > 0 && (
          <path
            d={`M ${cx - RADIUS} ${cy} A ${RADIUS} ${RADIUS} 0 ${largeArc} 1 ${endX} ${endY}`}
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={arcLength}
            strokeDashoffset={arcLength}
            style={{
              animation: `drawArc 800ms var(--ease-out) 200ms forwards`,
            }}
          />
        )}
        <text
          x={cx}
          y={cy - 12}
          textAnchor="middle"
          className="font-data text-xl font-medium"
          fill="var(--color-text-primary)"
        >
          {percentage}%
        </text>
      </svg>
      <div className="text-[11px] uppercase tracking-[0.1em] text-text-tertiary -mt-1">
        {label}
      </div>
      <style>{`
        @keyframes drawArc {
          to { stroke-dashoffset: 0; }
        }
      `}</style>
    </div>
  );
}
