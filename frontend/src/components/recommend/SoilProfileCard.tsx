import { Card } from "@/components/common/Card";
import { Badge } from "@/components/common/Badge";
import type { SoilProfile } from "@/types/recommend";

interface SoilProfileCardProps {
  soil: SoilProfile;
}

const FERTILITY_VARIANT: Record<
  string,
  "success" | "warning" | "danger" | "info"
> = {
  high: "success",
  moderate_high: "success",
  moderate: "warning",
  low: "danger",
  very_low: "danger",
};

/** Compact soil profile summary card. */
export function SoilProfileCard({ soil }: SoilProfileCardProps) {
  const fertilityLabel = soil.fertility_rating.replace("_", " ");
  const textureLabel = soil.texture_class.replace(/_/g, " ");
  const variant = FERTILITY_VARIANT[soil.fertility_rating] ?? "info";

  return (
    <Card title="Soil Profile">
      <div className="flex items-center gap-2 mb-4">
        <Badge label={fertilityLabel} variant={variant} />
        <span className="text-xs text-text-tertiary capitalize">
          {textureLabel}
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <SoilMetric
          label="pH"
          value={soil.ph_h2o.toFixed(1)}
          warn={soil.ph_h2o > 7.5 || soil.ph_h2o < 5.5}
        />
        <SoilMetric
          label="Nitrogen"
          value={`${soil.nitrogen_g_per_kg} g/kg`}
          warn={soil.nitrogen_g_per_kg < 1.0}
        />
        <SoilMetric
          label="Org. Carbon"
          value={`${soil.soc_g_per_kg} g/kg`}
          warn={soil.soc_g_per_kg < 8.0}
        />
        <SoilMetric
          label="CEC"
          value={`${soil.cec_cmol_per_kg}`}
          warn={soil.cec_cmol_per_kg < 12.0}
        />
      </div>

      <div className="mt-3 flex gap-4 text-[11px] text-text-tertiary">
        <span>Clay: {soil.clay_pct}%</span>
        <span>Sand: {soil.sand_pct}%</span>
        <span>Silt: {soil.silt_pct}%</span>
      </div>
    </Card>
  );
}

function SoilMetric({
  label,
  value,
  warn,
}: {
  label: string;
  value: string;
  warn: boolean;
}) {
  return (
    <div className="text-center p-2 rounded-lg bg-surface-subtle">
      <div
        className={`font-data text-lg ${warn ? "text-warning" : "text-text-primary"}`}
      >
        {value}
      </div>
      <div className="text-[10px] uppercase tracking-wide text-text-tertiary mt-1">
        {label}
      </div>
    </div>
  );
}
