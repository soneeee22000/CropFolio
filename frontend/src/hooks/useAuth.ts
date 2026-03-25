/** Authentication hook managing JWT token, user profile, and auth state. */

import { useState, useCallback, useEffect } from "react";
import {
  requestOTP,
  verifyOTP,
  getProfile,
  storeToken,
  clearToken,
  hasToken,
} from "@/api/auth";
import type { UserProfile } from "@/types/auth";

interface AuthState {
  user: UserProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

/** Hook for farmer authentication (phone + OTP flow). */
export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: hasToken(),
    isLoading: false,
    error: null,
  });

  /** Load user profile if token exists. */
  useEffect(() => {
    if (hasToken() && !state.user) {
      setState((s) => ({ ...s, isLoading: true }));
      getProfile()
        .then((user) =>
          setState({
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          }),
        )
        .catch(() => {
          clearToken();
          setState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        });
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  /** Step 1: Request OTP. Returns dev OTP code. */
  const sendOTP = useCallback(async (phone: string) => {
    setState((s) => ({ ...s, isLoading: true, error: null }));
    try {
      const result = await requestOTP(phone);
      setState((s) => ({ ...s, isLoading: false }));
      return result.otp_dev_only;
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to send OTP";
      setState((s) => ({ ...s, isLoading: false, error: msg }));
      return null;
    }
  }, []);

  /** Step 2: Verify OTP. Stores token and loads profile. */
  const verifyCode = useCallback(
    async (phone: string, code: string, fullName?: string) => {
      setState((s) => ({ ...s, isLoading: true, error: null }));
      try {
        const tokenRes = await verifyOTP(phone, code, fullName);
        storeToken(tokenRes.access_token);
        const user = await getProfile();
        setState({
          user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
        return tokenRes;
      } catch (err) {
        const msg =
          err instanceof Error ? err.message : "OTP verification failed";
        setState((s) => ({ ...s, isLoading: false, error: msg }));
        return null;
      }
    },
    [],
  );

  /** Logout: clear token and state. */
  const logout = useCallback(() => {
    clearToken();
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  }, []);

  return {
    ...state,
    sendOTP,
    verifyCode,
    logout,
  };
}
