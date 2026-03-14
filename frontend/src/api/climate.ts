import type { ClimateRiskResponse } from "@/types/climate";
import { apiGet } from "./client";

/** Fetch climate risk assessment for a township and season. */
export function fetchClimateRisk(
  townshipId: string,
  season: "monsoon" | "dry" = "monsoon",
): Promise<ClimateRiskResponse> {
  return apiGet<ClimateRiskResponse>(
    `/climate-risk/${townshipId}?season=${season}`,
  );
}
