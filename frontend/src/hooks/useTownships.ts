import { useEffect, useRef, useState } from "react";
import type { Township } from "@/types/township";
import { fetchTownships } from "@/api/townships";

/** Fetch and cache all Myanmar townships. */
export function useTownships() {
  const [townships, setTownships] = useState<Township[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const cached = useRef(false);

  useEffect(() => {
    if (cached.current) return;
    cached.current = true;

    fetchTownships()
      .then((data) => setTownships(data.townships))
      .catch((err: Error) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);

  return { townships, isLoading, error };
}
