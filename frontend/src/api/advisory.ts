import { apiPost } from "./client";
import type {
  AdvisoryRequest,
  AdvisoryResponse,
  QueryRequest,
  QueryResponseData,
} from "@/types/advisory";

/** Generate a full AI advisory for a township. */
export function generateAdvisory(
  request: AdvisoryRequest,
): Promise<AdvisoryResponse> {
  return apiPost<AdvisoryResponse, AdvisoryRequest>(
    "/advisory/generate",
    request,
  );
}

/** Ask a free-form question about a township. */
export function queryAdvisory(
  request: QueryRequest,
): Promise<QueryResponseData> {
  return apiPost<QueryResponseData, QueryRequest>("/advisory/query", request);
}
