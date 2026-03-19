import { useState, useCallback, useRef } from "react";
import { submitSARAnalysis, getSARJobStatus } from "@/api/sar";
import type { SARAnalyzeRequest, SARResult } from "@/types/sar";

const POLL_INTERVAL_MS = 2000;
const MAX_POLL_ATTEMPTS = 30;

/** Hook for SAR analysis with async polling. */
export function useSARAnalysis() {
  const [result, setResult] = useState<SARResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const cleanup = useCallback(() => {
    if (pollRef.current) {
      clearTimeout(pollRef.current);
      pollRef.current = null;
    }
  }, []);

  const analyze = useCallback(
    async (request: SARAnalyzeRequest) => {
      cleanup();
      setIsLoading(true);
      setError(null);
      setResult(null);

      try {
        const job = await submitSARAnalysis(request);
        setJobId(job.job_id);

        let attempts = 0;
        const poll = async (): Promise<void> => {
          attempts += 1;
          if (attempts > MAX_POLL_ATTEMPTS) {
            setError("Analysis timed out. Please try again.");
            setIsLoading(false);
            return;
          }

          try {
            const status = await getSARJobStatus(job.job_id);

            if (status.status === "completed" && status.result) {
              setResult(status.result);
              setIsLoading(false);
              return;
            }

            if (status.status === "failed") {
              setError(status.error ?? "Analysis failed");
              setIsLoading(false);
              return;
            }

            pollRef.current = setTimeout(poll, POLL_INTERVAL_MS);
          } catch {
            setError("Failed to check analysis status");
            setIsLoading(false);
          }
        };

        pollRef.current = setTimeout(poll, POLL_INTERVAL_MS);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to start SAR analysis";
        setError(message);
        setIsLoading(false);
      }
    },
    [cleanup],
  );

  const reset = useCallback(() => {
    cleanup();
    setResult(null);
    setError(null);
    setJobId(null);
    setIsLoading(false);
  }, [cleanup]);

  return { result, isLoading, error, jobId, analyze, reset };
}
