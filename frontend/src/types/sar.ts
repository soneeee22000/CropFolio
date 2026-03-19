/** Request to trigger SAR analysis. */
export interface SARAnalyzeRequest {
  township_id: string;
  season?: "monsoon" | "dry";
  year?: number;
}

/** Response after submitting a SAR analysis job. */
export interface SARJobResponse {
  job_id: string;
  township_id: string;
  status: string;
  message: string;
}

/** A single SAR observation point. */
export interface SARTimePoint {
  date: string;
  vh_db: number;
  vv_db: number;
  vh_vv_ratio: number;
}

/** A detected phenological signal. */
export interface PhenologySignal {
  signal_type: string;
  detected: boolean;
  confidence: number;
  date_range: string;
  description: string;
}

/** Complete SAR analysis result. */
export interface SARResult {
  township_id: string;
  analysis_date: string;
  season: string;
  time_series: SARTimePoint[];
  phenology_signals: PhenologySignal[];
  rice_detected: boolean;
  rice_confidence: number;
  estimated_area_pct: number;
  summary: string;
}

/** Status of a SAR analysis job. */
export interface SARJobStatus {
  job_id: string;
  township_id: string;
  status: string;
  created_at: string;
  completed_at: string | null;
  error: string | null;
  result: SARResult | null;
}
