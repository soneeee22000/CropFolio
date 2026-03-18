import { apiGet, apiPost } from "./client";
import type {
  RecommendRequest,
  RecommendResponse,
  DemoROIRequest,
  DemoROIResponse,
  SoilProfile,
} from "@/types/recommend";

/** Generate crop + fertilizer recommendations for townships. */
export async function getRecommendations(
  request: RecommendRequest,
): Promise<RecommendResponse> {
  return apiPost<RecommendResponse, RecommendRequest>("/recommend", request);
}

/** Calculate ROI for a demo crop scenario. */
export async function calculateDemoROI(
  request: DemoROIRequest,
): Promise<DemoROIResponse> {
  return apiPost<DemoROIResponse, DemoROIRequest>(
    "/recommend/demo-roi",
    request,
  );
}

/** Fetch soil profile for a township. */
export async function getSoilProfile(townshipId: string): Promise<SoilProfile> {
  return apiGet<SoilProfile>(`/recommend/soil/${townshipId}`);
}
