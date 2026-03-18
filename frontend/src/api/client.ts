import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

/** Configured axios instance for CropFolio API. */
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

/** Extract a human-readable error message from an Axios error. */
function extractErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      return detail.map((d: { msg?: string }) => d.msg ?? "").join(", ");
    }
    return err.message;
  }
  return err instanceof Error ? err.message : "Unknown error";
}

/** Typed GET request wrapper. */
export async function apiGet<T>(url: string): Promise<T> {
  const response = await apiClient.get<T>(url);
  return response.data;
}

/** Typed POST request wrapper. */
export async function apiPost<T, D = unknown>(
  url: string,
  data: D,
): Promise<T> {
  try {
    const response = await apiClient.post<T>(url, data);
    return response.data;
  } catch (err) {
    throw new Error(extractErrorMessage(err));
  }
}
