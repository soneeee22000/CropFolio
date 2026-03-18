import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

/* eslint-disable no-console */
console.log("[CropFolio] API base URL:", API_BASE_URL);

/** Configured axios instance for CropFolio API. */
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

/** Typed GET request wrapper. */
export async function apiGet<T>(url: string): Promise<T> {
  try {
    const response = await apiClient.get<T>(url);
    return response.data;
  } catch (err) {
    console.error("[CropFolio] apiGet failed:", url, err);
    throw err;
  }
}

/** Typed POST request wrapper. */
export async function apiPost<T, D = unknown>(
  url: string,
  data: D,
): Promise<T> {
  const response = await apiClient.post<T>(url, data);
  return response.data;
}
