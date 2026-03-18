import { Card } from "@/components/common/Card";
import { FertilizerBadge } from "./FertilizerBadge";
import { formatMMK } from "@/utils/formatters";
import { CROP_COLORS } from "@/constants";
import type { CropRecommendation } from "@/types/recommend";

interface RecommendationCardProps {
  recommendation: CropRecommendation;
}

/** Crop + fertilizer pairing card with confidence and cost data. */
export function RecommendationCard({
  recommendation,
}: RecommendationCardProps) {
  const {
    crop_id,
    crop_name,
    crop_name_mm,
    portfolio_weight,
    expected_income_per_ha,
    fertilizers,
  } = recommendation;
  const color = CROP_COLORS[crop_id] ?? "#666";

  return (
    <Card>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div
            className="w-3 h-3 rounded-full flex-shrink-0"
            style={{ backgroundColor: color }}
          />
          <div>
            <h4 className="font-display text-lg text-text-primary">
              {crop_name}
            </h4>
            <span className="text-xs text-text-tertiary">{crop_name_mm}</span>
          </div>
        </div>
        <div className="text-right">
          <div className="font-data text-2xl text-text-primary">
            {(portfolio_weight * 100).toFixed(0)}%
          </div>
          <div className="text-[10px] uppercase tracking-wide text-text-tertiary">
            Allocation
          </div>
        </div>
      </div>

      <div className="mb-4 p-3 rounded-lg bg-surface-subtle">
        <div className="text-xs text-text-tertiary mb-1">Expected Income</div>
        <div className="font-data text-lg text-accent">
          {formatMMK(expected_income_per_ha)}/ha
        </div>
      </div>

      {fertilizers.length > 0 && (
        <div>
          <h5 className="text-xs uppercase tracking-wide text-text-tertiary mb-3">
            Recommended Fertilizers
          </h5>
          <div className="space-y-3">
            {fertilizers.map((fert, idx) => (
              <div
                key={fert.fertilizer_id}
                className="flex items-start justify-between p-3 rounded-lg border border-border"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-medium text-text-tertiary">
                      #{idx + 1}
                    </span>
                    <FertilizerBadge
                      formulation={fert.formulation}
                      name={fert.fertilizer_name}
                      score={fert.score}
                    />
                  </div>
                  <div className="text-xs text-text-tertiary ml-5">
                    {fert.reasoning}
                  </div>
                </div>
                <div className="text-right flex-shrink-0 ml-4">
                  <div className="font-data text-sm text-text-primary">
                    {formatMMK(fert.cost_per_ha_mmk)}
                  </div>
                  <div className="text-[10px] text-text-tertiary">
                    {fert.recommended_rate_kg_per_ha} kg/ha
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}
