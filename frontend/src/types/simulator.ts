/** Request body for Monte Carlo simulation. */
export interface SimulateRequest {
  crop_ids: string[];
  weights: Record<string, number>;
  township_id: string;
  num_simulations?: number;
  season?: "monsoon" | "dry";
}

/** Single histogram bin for income distribution chart. */
export interface HistogramBin {
  bin_start: number;
  bin_end: number;
  count: number;
  frequency: number;
}

/** Statistical summary of simulation results. */
export interface SimulationStats {
  mean_income: number;
  median_income: number;
  std_dev: number;
  percentile_5: number;
  percentile_95: number;
  prob_catastrophic_loss: number;
  value_at_risk_95: number;
}

/** Full simulation response. */
export interface SimulateResponse {
  township_id: string;
  township_name: string;
  season: string;
  num_simulations: number;
  stats: SimulationStats;
  histogram: HistogramBin[];
}
