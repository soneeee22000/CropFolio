import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useSimulate } from "./useSimulate";
import type { SimulateResponse } from "@/types/simulator";

const MOCK_RESPONSE: SimulateResponse = {
  township_id: "mgw_magway",
  township_name: "Magway",
  season: "monsoon",
  num_simulations: 500,
  stats: {
    mean_income: 850000,
    median_income: 840000,
    std_dev: 120000,
    percentile_5: 650000,
    percentile_95: 1050000,
    prob_catastrophic_loss: 0.06,
    value_at_risk_95: 650000,
  },
  histogram: [
    { bin_start: 500000, bin_end: 600000, count: 25, frequency: 0.05 },
    { bin_start: 600000, bin_end: 700000, count: 75, frequency: 0.15 },
  ],
};

vi.mock("@/api/simulator", () => ({
  runSimulation: vi.fn(),
}));

describe("useSimulate", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should have correct initial state", () => {
    const { result } = renderHook(() => useSimulate());
    expect(result.current.result).toBeNull();
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it("should return data on success", async () => {
    const { runSimulation } = await import("@/api/simulator");
    vi.mocked(runSimulation).mockResolvedValueOnce(MOCK_RESPONSE);

    const { result } = renderHook(() => useSimulate());

    await act(async () => {
      await result.current.simulate({
        crop_ids: ["rice", "sesame"],
        weights: { rice: 0.6, sesame: 0.4 },
        township_id: "mgw_magway",
      });
    });

    expect(result.current.result).toEqual(MOCK_RESPONSE);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it("should set error on failure", async () => {
    const { runSimulation } = await import("@/api/simulator");
    vi.mocked(runSimulation).mockRejectedValueOnce(new Error("Server error"));

    const { result } = renderHook(() => useSimulate());

    await act(async () => {
      await result.current.simulate({
        crop_ids: ["rice", "sesame"],
        weights: { rice: 0.6, sesame: 0.4 },
        township_id: "mgw_magway",
      });
    });

    expect(result.current.result).toBeNull();
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe("Server error");
  });
});
