import { useEffect, useRef, useState } from "react";
import type { Crop } from "@/types/crop";
import { fetchCrops } from "@/api/crops";

/** Fetch and cache all Myanmar crop profiles. */
export function useCrops() {
  const [crops, setCrops] = useState<Crop[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const cached = useRef(false);

  useEffect(() => {
    if (cached.current) return;
    cached.current = true;

    fetchCrops()
      .then((data) => setCrops(data.crops))
      .catch((err: Error) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);

  return { crops, isLoading, error };
}
