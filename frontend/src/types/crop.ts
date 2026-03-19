/** A Myanmar crop profile with agronomic and economic data. */
export interface Crop {
  id: string;
  name_en: string;
  name_mm: string;
  category: string;
  growing_season: string;
  drought_tolerance: number;
  flood_tolerance: number;
  avg_yield_kg_per_ha: number;
  yield_variance: number;
  avg_price_mmk_per_kg: number;
  price_variance: number;
  nitrogen_requirement: number;
  phosphorus_requirement: number;
  potassium_requirement: number;
  yield_data_source: string;
  price_data_source: string;
  data_confidence: "high" | "medium" | "low";
}

/** API response for listing crops. */
export interface CropListResponse {
  count: number;
  crops: Crop[];
}
