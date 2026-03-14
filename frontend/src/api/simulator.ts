import type { SimulateRequest, SimulateResponse } from "@/types/simulator";
import { apiPost } from "./client";

/** Run Monte Carlo simulation for a crop portfolio. */
export function runSimulation(
  request: SimulateRequest,
): Promise<SimulateResponse> {
  return apiPost<SimulateResponse, SimulateRequest>("/simulate/", request);
}
