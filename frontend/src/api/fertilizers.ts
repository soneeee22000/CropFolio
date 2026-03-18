import { apiGet } from "./client";
import type { FertilizerListResponse } from "@/types/fertilizer";

/** Fetch all available fertilizer products. */
export async function getFertilizers(): Promise<FertilizerListResponse> {
  return apiGet<FertilizerListResponse>("/fertilizers");
}
