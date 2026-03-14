import { useState, useCallback } from "react";
import type { SimulateRequest, SimulateResponse } from "@/types/simulator";
import { runSimulation } from "@/api/simulator";

/** Callable hook for Monte Carlo simulation. */
export function useSimulate() {
  const [result, setResult] = useState<SimulateResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const simulate = useCallback(async (request: SimulateRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await runSimulation(request);
      setResult(data);
      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Simulation failed";
      setError(message);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { result, isLoading, error, simulate };
}
