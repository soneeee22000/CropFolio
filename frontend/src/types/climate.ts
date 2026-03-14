/** Climate risk assessment for a township. */
export interface ClimateRiskResponse {
  township_id: string;
  township_name: string;
  season: string;
  drought_probability: number;
  flood_probability: number;
  temp_anomaly_celsius: number;
  rainfall_forecast_mm: number;
  rainfall_historical_avg_mm: number;
  risk_level: string;
  data_quality_score: number;
  data_source: string;
}
