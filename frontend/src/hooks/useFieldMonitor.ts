import { useState, useCallback } from "react";
import { fetchFieldMonitor } from "@/api/field-monitor";
import type {
  FieldMonitorRequest,
  FieldMonitorSummary,
} from "@/types/field-monitor";

/** Hook for field monitoring — synchronous fetch, no polling. */
export function useFieldMonitor() {
  const [summary, setSummary] = useState<FieldMonitorSummary | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadMonitor = useCallback(async (request: FieldMonitorRequest) => {
    setIsLoading(true);
    setError(null);
    setSummary(null);

    try {
      const result = await fetchFieldMonitor(request);
      setSummary(result);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to load field monitor";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setSummary(null);
    setError(null);
    setIsLoading(false);
  }, []);

  return { summary, isLoading, error, loadMonitor, reset };
}
