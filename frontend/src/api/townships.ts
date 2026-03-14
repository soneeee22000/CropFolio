import type { TownshipListResponse } from "@/types/township";
import { apiGet } from "./client";

/** Fetch all Myanmar townships. */
export function fetchTownships(): Promise<TownshipListResponse> {
  return apiGet<TownshipListResponse>("/townships/");
}
