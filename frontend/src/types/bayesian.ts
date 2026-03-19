/** A single piece of evidence for Bayesian updating. */
export interface EvidenceItem {
  variable: string;
  value: string;
}

/** Bayesian prediction for a single crop. */
export interface BayesianCropPrediction {
  crop_id: string;
  yield_probabilities: Record<string, number>;
  expected_yield_factor: number;
  evidence_used: string[];
}

/** Request body for Bayesian portfolio optimization. */
export interface OptimizeBayesianRequest {
  crop_ids: string[];
  township_id: string;
  risk_tolerance?: number;
  season?: "monsoon" | "dry";
  evidence?: EvidenceItem[];
}

/** Response from Bayesian portfolio optimization. */
export interface OptimizeBayesianResponse {
  township_id: string;
  township_name: string;
  season: string;
  model_type: string;
  weights: Array<{
    crop_id: string;
    crop_name: string;
    crop_name_mm: string;
    weight: number;
    expected_income_per_ha: number;
  }>;
  metrics: {
    expected_income_per_ha: number;
    income_std_dev: number;
    sharpe_ratio: number;
    risk_reduction_pct: number;
  };
  climate_risk: {
    drought_probability: number;
    flood_probability: number;
    risk_level: string;
    data_source: string;
  };
  bayesian_predictions: BayesianCropPrediction[];
}
