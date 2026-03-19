import { useState, useCallback } from "react";
import { optimizeBayesian } from "@/api/bayesian";
import type {
  OptimizeBayesianRequest,
  OptimizeBayesianResponse,
} from "@/types/bayesian";

/** Hook for Bayesian portfolio optimization with evidence. */
export function useBayesianOptimize() {
  const [result, setResult] = useState<OptimizeBayesianResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const optimize = useCallback(async (request: OptimizeBayesianRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await optimizeBayesian(request);
      setResult(data);
      return data;
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Bayesian optimization failed";
      setError(message);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return { result, isLoading, error, optimize, reset };
}
