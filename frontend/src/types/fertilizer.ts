/** A fertilizer product available in Myanmar. */
export interface Fertilizer {
  id: string;
  name_en: string;
  name_mm: string;
  formulation: string;
  nitrogen_pct: number;
  phosphorus_pct: number;
  potassium_pct: number;
  sulfur_pct: number;
  price_mmk_per_50kg: number;
  application_rate_kg_per_ha: number;
  availability: string;
  notes: string;
}

/** API response for listing fertilizers. */
export interface FertilizerListResponse {
  count: number;
  fertilizers: Fertilizer[];
}
