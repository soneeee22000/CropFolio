/** Farmer-specific API calls: farms, plots, plans, applications. */

import { authClient } from "./auth";
import type {
  CropPlan,
  Farm,
  FertilizerApplicationItem,
  Plot,
} from "@/types/farmer";

/** List all farms for the authenticated farmer. */
export async function listFarms(): Promise<Farm[]> {
  const res = await authClient.get<Farm[]>("/farms/");
  return res.data;
}

/** Create a new farm. */
export async function createFarm(data: {
  name: string;
  name_mm?: string;
  township_id: string;
  total_area_hectares: number;
  latitude?: number;
  longitude?: number;
}): Promise<Farm> {
  const res = await authClient.post<Farm>("/farms/", data);
  return res.data;
}

/** Get a specific farm with plots. */
export async function getFarm(farmId: string): Promise<Farm> {
  const res = await authClient.get<Farm>(`/farms/${farmId}`);
  return res.data;
}

/** Add a plot to a farm. */
export async function createPlot(
  farmId: string,
  data: { name?: string; area_hectares: number; soil_type?: string },
): Promise<Plot> {
  const res = await authClient.post<Plot>(`/farms/${farmId}/plots`, data);
  return res.data;
}

/** Generate a new crop plan. */
export async function generatePlan(data: {
  plot_id: string;
  crop_ids: string[];
  season: string;
  year: number;
  risk_tolerance?: number;
}): Promise<CropPlan> {
  const res = await authClient.post<CropPlan>("/plans/generate", data);
  return res.data;
}

/** List all plans for the farmer. */
export async function listPlans(): Promise<CropPlan[]> {
  const res = await authClient.get<CropPlan[]>("/plans/");
  return res.data;
}

/** Get today's pending tasks. */
export async function getTodayTasks(): Promise<FertilizerApplicationItem[]> {
  const res = await authClient.get<FertilizerApplicationItem[]>("/plans/today");
  return res.data;
}

/** Get a specific plan detail. */
export async function getPlan(planId: string): Promise<CropPlan> {
  const res = await authClient.get<CropPlan>(`/plans/${planId}`);
  return res.data;
}

/** Accept a draft plan. */
export async function acceptPlan(planId: string): Promise<CropPlan> {
  const res = await authClient.post<CropPlan>(`/plans/${planId}/accept`);
  return res.data;
}

/** Reject a draft plan. */
export async function rejectPlan(planId: string): Promise<CropPlan> {
  const res = await authClient.post<CropPlan>(`/plans/${planId}/reject`);
  return res.data;
}

/** Report a fertilizer application as completed. */
export async function reportApplication(
  applicationId: string,
  data: { actual_rate_kg_per_ha: number; actual_date: string; notes?: string },
): Promise<FertilizerApplicationItem> {
  const res = await authClient.post<FertilizerApplicationItem>(
    `/plans/applications/${applicationId}/report`,
    data,
  );
  return res.data;
}
