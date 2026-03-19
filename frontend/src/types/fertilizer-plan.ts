/** A single fertilizer application at a growth stage. */
export interface StageApplication {
  stage: string;
  day: number;
  fertilizer_id: string;
  fertilizer_name: string;
  rate_kg_per_ha: number;
  cost_mmk: number;
}

/** A micronutrient deficiency warning. */
export interface MicronutrientFlag {
  nutrient: string;
  severity: string;
  recommendation: string;
}

/** A nutrient ratio imbalance warning. */
export interface NutrientInteractionFlag {
  ratio_name: string;
  actual_ratio: number;
  optimal_range: string;
  recommendation: string;
}

/** Return on investment estimate for the fertilizer plan. */
export interface ROIEstimate {
  total_cost_mmk: number;
  expected_yield_increase_pct: number;
  return_ratio: number;
}

/** Complete optimized fertilizer application plan. */
export interface FertilizerPlan {
  crop_id: string;
  applications: StageApplication[];
  nutrient_totals: Record<string, number>;
  micronutrient_flags: MicronutrientFlag[];
  interaction_flags: NutrientInteractionFlag[];
  roi_estimate: ROIEstimate;
  lp_feasible: boolean;
}
