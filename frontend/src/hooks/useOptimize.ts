import { useState, useCallback } from "react";
import type { OptimizeRequest, OptimizeResponse } from "@/types/optimizer";
import { runOptimization } from "@/api/optimizer";

/** Callable hook for portfolio optimization. */
export function useOptimize() {
  const [result, setResult] = useState<OptimizeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const optimize = useCallback(async (request: OptimizeRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await runOptimization(request);
      setResult(data);
      return data;
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Optimization failed";
      setError(message);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { result, isLoading, error, optimize };
}
