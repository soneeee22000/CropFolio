/** Request body for portfolio optimization. */
export interface OptimizeRequest {
  crop_ids: string[];
  township_id: string;
  risk_tolerance?: number;
  season?: "monsoon" | "dry";
}

/** Single crop's allocation in optimized portfolio. */
export interface CropWeight {
  crop_id: string;
  crop_name: string;
  crop_name_mm: string;
  weight: number;
  expected_income_per_ha: number;
}

/** Climate risk summary embedded in optimization response. */
export interface ClimateRiskSummary {
  drought_probability: number;
  flood_probability: number;
  risk_level: string;
  data_source: string;
}

/** Aggregate portfolio performance metrics. */
export interface PortfolioMetrics {
  expected_income_per_ha: number;
  income_std_dev: number;
  sharpe_ratio: number;
  risk_reduction_pct: number;
}

/** Full optimization response. */
export interface OptimizeResponse {
  township_id: string;
  township_name: string;
  season: string;
  weights: CropWeight[];
  metrics: PortfolioMetrics;
  climate_risk: ClimateRiskSummary;
}
