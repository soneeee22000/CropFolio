/** Authentication API calls for farmer OTP and distributor login. */

import axios from "axios";
import type { TokenResponse, UserProfile } from "@/types/auth";

const API_V2_BASE =
  import.meta.env.VITE_API_BASE_URL?.replace("/v1", "/v2") ?? "/api/v2";

/** Axios instance for v2 authenticated endpoints. */
export const authClient = axios.create({
  baseURL: API_V2_BASE,
  timeout: 30000,
});

/** Attach JWT token to all v2 requests. */
authClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("cropfolio_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/** Request an OTP for farmer phone login. */
export async function requestOTP(
  phoneNumber: string,
): Promise<{ otp_dev_only: string }> {
  const res = await authClient.post<{ message: string; otp_dev_only: string }>(
    "/auth/farmer/request-otp",
    { phone_number: phoneNumber },
  );
  return res.data;
}

/** Verify OTP and get JWT token. */
export async function verifyOTP(
  phoneNumber: string,
  code: string,
  fullName?: string,
  fullNameMm?: string,
  townshipId?: string,
): Promise<TokenResponse> {
  const res = await authClient.post<TokenResponse>("/auth/farmer/verify-otp", {
    phone_number: phoneNumber,
    code,
    full_name: fullName,
    full_name_mm: fullNameMm,
    township_id: townshipId,
  });
  return res.data;
}

/** Get the authenticated user's profile. */
export async function getProfile(): Promise<UserProfile> {
  const res = await authClient.get<UserProfile>("/auth/me");
  return res.data;
}

/** Store JWT token after successful auth. */
export function storeToken(token: string): void {
  localStorage.setItem("cropfolio_token", token);
}

/** Clear JWT token on logout. */
export function clearToken(): void {
  localStorage.removeItem("cropfolio_token");
}

/** Check if a token exists. */
export function hasToken(): boolean {
  return localStorage.getItem("cropfolio_token") !== null;
}
