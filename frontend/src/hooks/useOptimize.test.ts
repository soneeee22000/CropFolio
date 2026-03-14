import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useOptimize } from "./useOptimize";
import type { OptimizeResponse } from "@/types/optimizer";

const MOCK_RESPONSE: OptimizeResponse = {
  township_id: "mgw_magway",
  township_name: "Magway",
  season: "monsoon",
  weights: [
    {
      crop_id: "rice",
      crop_name: "Rice",
      crop_name_mm: "\u1006\u1014\u103a",
      weight: 0.6,
      expected_income_per_ha: 510000,
    },
    {
      crop_id: "sesame",
      crop_name: "Sesame",
      crop_name_mm: "\u1014\u1036\u1038",
      weight: 0.4,
      expected_income_per_ha: 340000,
    },
  ],
  metrics: {
    expected_income_per_ha: 850000,
    income_std_dev: 120000,
    sharpe_ratio: 1.2,
    risk_reduction_pct: 23.5,
  },
  climate_risk: {
    drought_probability: 0.3,
    flood_probability: 0.15,
    risk_level: "moderate",
    data_source: "live",
  },
};

vi.mock("@/api/optimizer", () => ({
  runOptimization: vi.fn(),
}));

describe("useOptimize", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should have correct initial state", () => {
    const { result } = renderHook(() => useOptimize());
    expect(result.current.result).toBeNull();
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it("should return data on success", async () => {
    const { runOptimization } = await import("@/api/optimizer");
    vi.mocked(runOptimization).mockResolvedValueOnce(MOCK_RESPONSE);

    const { result } = renderHook(() => useOptimize());

    await act(async () => {
      await result.current.optimize({
        crop_ids: ["rice", "sesame"],
        township_id: "mgw_magway",
      });
    });

    expect(result.current.result).toEqual(MOCK_RESPONSE);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it("should set error on failure", async () => {
    const { runOptimization } = await import("@/api/optimizer");
    vi.mocked(runOptimization).mockRejectedValueOnce(
      new Error("Network error"),
    );

    const { result } = renderHook(() => useOptimize());

    await act(async () => {
      await result.current.optimize({
        crop_ids: ["rice", "sesame"],
        township_id: "mgw_magway",
      });
    });

    expect(result.current.result).toBeNull();
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe("Network error");
  });
});
