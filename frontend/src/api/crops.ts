import type { CropListResponse } from "@/types/crop";
import { apiGet } from "./client";

/** Fetch all available Myanmar crop profiles. */
export function fetchCrops(): Promise<CropListResponse> {
  return apiGet<CropListResponse>("/crops/");
}
