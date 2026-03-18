/** Scored fertilizer recommendation for a crop-soil combination. */
export interface FertilizerRecommendation {
  fertilizer_id: string;
  fertilizer_name: string;
  formulation: string;
  score: number;
  crop_need_score: number;
  soil_deficiency_score: number;
  cost_efficiency_score: number;
  compatibility_score: number;
  recommended_rate_kg_per_ha: number;
  cost_per_ha_mmk: number;
  reasoning: string;
}

/** Crop + fertilizer pairing recommendation. */
export interface CropRecommendation {
  crop_id: string;
  crop_name: string;
  crop_name_mm: string;
  portfolio_weight: number;
  expected_income_per_ha: number;
  fertilizers: FertilizerRecommendation[];
}

/** Soil profile for a township. */
export interface SoilProfile {
  township_id: string;
  ph_h2o: number;
  nitrogen_g_per_kg: number;
  soc_g_per_kg: number;
  clay_pct: number;
  sand_pct: number;
  silt_pct: number;
  cec_cmol_per_kg: number;
  texture_class: string;
  fertility_rating: string;
}

/** Monte Carlo confidence metrics. */
export interface ConfidenceMetrics {
  num_simulations: number;
  mean_income: number;
  median_income: number;
  percentile_5: number;
  percentile_95: number;
  prob_catastrophic_loss: number;
  success_probability: number;
}

/** Full recommendation for a single township. */
export interface TownshipRecommendation {
  township_id: string;
  township_name: string;
  season: string;
  soil: SoilProfile | null;
  crops: CropRecommendation[];
  confidence: ConfidenceMetrics | null;
  expected_income_per_ha: number;
  risk_reduction_pct: number;
  ai_advisory: string | null;
  ai_advisory_mm: string | null;
}

/** Request body for recommendations. */
export interface RecommendRequest {
  township_ids: string[];
  crop_ids: string[];
  risk_tolerance?: number;
  season?: "monsoon" | "dry";
  top_fertilizers?: number;
}

/** Response with recommendations for one or more townships. */
export interface RecommendResponse {
  recommendations: TownshipRecommendation[];
  total_townships: number;
}

/** Request body for demo ROI calculation. */
export interface DemoROIRequest {
  township_id: string;
  crop_id: string;
  area_hectares?: number;
  season?: "monsoon" | "dry";
}

/** ROI calculation response for a demo crop scenario. */
export interface DemoROIResponse {
  township_id: string;
  township_name: string;
  crop_id: string;
  crop_name: string;
  area_hectares: number;
  season: string;
  fertilizer_cost_mmk: number;
  seed_cost_mmk: number;
  total_input_cost_mmk: number;
  expected_revenue_mmk: number;
  expected_profit_mmk: number;
  success_probability: number;
  catastrophic_loss_probability: number;
  reimbursement_exposure_mmk: number;
  recommended_fertilizer: FertilizerRecommendation | null;
  soil: SoilProfile | null;
}
