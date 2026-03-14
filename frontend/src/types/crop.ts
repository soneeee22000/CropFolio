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
}

/** API response for listing crops. */
export interface CropListResponse {
  count: number;
  crops: Crop[];
}
