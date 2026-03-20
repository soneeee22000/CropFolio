import { useState, useCallback } from "react";
import { generateAdvisory, queryAdvisory } from "@/api/advisory";
import type { AdvisoryResponse, QueryHistoryEntry } from "@/types/advisory";

/** Hook for generating full township advisories. */
export function useAdvisory() {
  const [advisory, setAdvisory] = useState<AdvisoryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generate = useCallback(
    async (townshipId: string, season: "monsoon" | "dry") => {
      setIsLoading(true);
      setError(null);
      setAdvisory(null);

      try {
        const result = await generateAdvisory({
          township_id: townshipId,
          season,
        });
        setAdvisory(result);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to generate advisory";
        setError(message);
      } finally {
        setIsLoading(false);
      }
    },
    [],
  );

  const reset = useCallback(() => {
    setAdvisory(null);
    setError(null);
    setIsLoading(false);
  }, []);

  return { advisory, isLoading, error, generate, reset };
}

/** Hook for advisory Q&A with conversation history. */
export function useAdvisoryQuery() {
  const [queries, setQueries] = useState<QueryHistoryEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ask = useCallback(
    async (townshipId: string, season: "monsoon" | "dry", question: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const result = await queryAdvisory({
          township_id: townshipId,
          season,
          question,
        });
        const entry: QueryHistoryEntry = {
          id: crypto.randomUUID(),
          question,
          result,
          timestamp: new Date(),
        };
        setQueries((prev) => [...prev, entry]);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to get answer";
        setError(message);
      } finally {
        setIsLoading(false);
      }
    },
    [],
  );

  const reset = useCallback(() => {
    setQueries([]);
    setError(null);
    setIsLoading(false);
  }, []);

  return { queries, isLoading, error, ask, reset };
}
