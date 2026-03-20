/** A single advisory section with bilingual content. */
export interface AdvisorySectionData {
  title: string;
  content: string;
  content_mm: string;
}

/** Full advisory response from the API. */
export interface AdvisoryResponse {
  township_id: string;
  township_name: string;
  season: string;
  executive_brief: AdvisorySectionData;
  crop_strategy: AdvisorySectionData;
  fertilizer_plan: AdvisorySectionData;
  risk_warnings: AdvisorySectionData;
  market_outlook: AdvisorySectionData;
  generated_at: string;
  has_ai: boolean;
}

/** Request to generate a full advisory. */
export interface AdvisoryRequest {
  township_id: string;
  season: "monsoon" | "dry";
}

/** Request to ask a question about a township. */
export interface QueryRequest {
  township_id: string;
  season: "monsoon" | "dry";
  question: string;
}

/** Response to a free-form advisory query. */
export interface QueryResponseData {
  answer: string;
  answer_mm: string;
  confidence: number;
  data_sources: string[];
  has_ai: boolean;
}

/** A query history entry for conversation display. */
export interface QueryHistoryEntry {
  id: string;
  question: string;
  result: QueryResponseData;
  timestamp: Date;
}
