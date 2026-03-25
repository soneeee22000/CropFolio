/** Types for farmer-facing features: farms, plots, plans, applications. */

export interface Plot {
  id: string;
  name: string | null;
  area_hectares: number;
  soil_type: string | null;
  latitude: number | null;
  longitude: number | null;
}

export interface Farm {
  id: string;
  name: string;
  name_mm: string | null;
  township_id: string;
  total_area_hectares: number;
  latitude: number | null;
  longitude: number | null;
  plots: Plot[];
}

export interface FertilizerApplicationItem {
  id: string;
  crop_id: string;
  fertilizer_id: string;
  fertilizer_name: string;
  stage: string;
  planned_rate_kg_per_ha: number;
  actual_rate_kg_per_ha: number | null;
  planned_day: number;
  actual_date: string | null;
  applied: boolean;
  notes: string | null;
}

export interface CropPlan {
  id: string;
  plot_id: string;
  season: "monsoon" | "dry";
  year: number;
  status: "draft" | "active" | "completed" | "abandoned";
  crop_ids: string[];
  risk_tolerance: number;
  portfolio_weights: Record<string, number> | null;
  optimizer_result: Record<string, number> | null;
  confidence_metrics: Record<string, number> | null;
  applications: FertilizerApplicationItem[];
}
