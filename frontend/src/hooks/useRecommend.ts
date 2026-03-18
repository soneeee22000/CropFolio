import { useState, useCallback } from "react";
import { getRecommendations } from "@/api/recommend";
import type { RecommendRequest, RecommendResponse } from "@/types/recommend";

/** Hook for generating crop-fertilizer recommendations. */
export function useRecommend() {
  const [result, setResult] = useState<RecommendResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const recommend = useCallback(async (request: RecommendRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getRecommendations(request);
      setResult(data);
      return data;
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Recommendation failed";
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

  return { result, isLoading, error, recommend, reset };
}
