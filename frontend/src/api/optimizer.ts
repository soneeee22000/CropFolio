import type { OptimizeRequest, OptimizeResponse } from "@/types/optimizer";
import { apiPost } from "./client";

/** Run Markowitz portfolio optimization. */
export function runOptimization(
  request: OptimizeRequest,
): Promise<OptimizeResponse> {
  return apiPost<OptimizeResponse, OptimizeRequest>("/optimize/", request);
}
