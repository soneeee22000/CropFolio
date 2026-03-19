import { apiGet, apiPost } from "./client";
import type {
  SARAnalyzeRequest,
  SARJobResponse,
  SARJobStatus,
  SARResult,
} from "@/types/sar";

/** Submit a SAR analysis job. */
export function submitSARAnalysis(
  request: SARAnalyzeRequest,
): Promise<SARJobResponse> {
  return apiPost<SARJobResponse, SARAnalyzeRequest>("/sar/analyze", request);
}

/** Poll for SAR job status and results. */
export function getSARJobStatus(jobId: string): Promise<SARJobStatus> {
  return apiGet<SARJobStatus>(`/sar/results/${jobId}`);
}

/** Get latest SAR coverage for a township. */
export function getSARCoverage(townshipId: string): Promise<SARResult> {
  return apiGet<SARResult>(`/sar/coverage/${townshipId}`);
}
