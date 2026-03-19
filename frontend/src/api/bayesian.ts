import { apiPost } from "./client";
import type {
  OptimizeBayesianRequest,
  OptimizeBayesianResponse,
} from "@/types/bayesian";

/** Run Bayesian portfolio optimization with evidence. */
export function optimizeBayesian(
  request: OptimizeBayesianRequest,
): Promise<OptimizeBayesianResponse> {
  return apiPost<OptimizeBayesianResponse, OptimizeBayesianRequest>(
    "/optimize/bayesian",
    request,
  );
}
