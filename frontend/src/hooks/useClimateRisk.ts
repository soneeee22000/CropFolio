import { useEffect, useState } from "react";
import type { ClimateRiskResponse } from "@/types/climate";
import { fetchClimateRisk } from "@/api/climate";

/** Fetch climate risk for a township when ID changes. */
export function useClimateRisk(
  townshipId: string | null,
  season: "monsoon" | "dry",
) {
  const [climateRisk, setClimateRisk] = useState<ClimateRiskResponse | null>(
    null,
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!townshipId) return;

    setIsLoading(true);
    setError(null);

    fetchClimateRisk(townshipId, season)
      .then(setClimateRisk)
      .catch((err: Error) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, [townshipId, season]);

  return { climateRisk, isLoading, error };
}
