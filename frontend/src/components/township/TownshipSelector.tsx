import { useMemo, useState } from "react";
import { useTownships } from "@/hooks/useTownships";
import { Card } from "@/components/common/Card";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import type { Township } from "@/types/township";

interface TownshipSelectorProps {
  onSelect: (townshipId: string, season: "monsoon" | "dry") => void;
}

/** Searchable township selector grouped by region. */
export function TownshipSelector({ onSelect }: TownshipSelectorProps) {
  const { townships, isLoading } = useTownships();
  const [search, setSearch] = useState("");
  const [season, setSeason] = useState<"monsoon" | "dry">("monsoon");

  const grouped = useMemo(() => {
    const filtered = townships.filter((t) =>
      t.name.toLowerCase().includes(search.toLowerCase()),
    );
    return groupByRegion(filtered);
  }, [townships, search]);

  if (isLoading) return <LoadingSpinner message="Loading townships..." />;

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">Select a Township</h2>
        <p className="text-gray-500 mt-1">
          Choose an agricultural township in Myanmar to analyze
        </p>
      </div>

      <div className="flex gap-3 justify-center">
        <button
          onClick={() => setSeason("monsoon")}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            season === "monsoon"
              ? "bg-primary text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          Monsoon Season
        </button>
        <button
          onClick={() => setSeason("dry")}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            season === "dry"
              ? "bg-primary text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          Dry Season
        </button>
      </div>

      <input
        type="text"
        placeholder="Search townships..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
      />

      <div className="space-y-4 max-h-96 overflow-y-auto">
        {Object.entries(grouped).map(([region, regionTownships]) => (
          <Card key={region} className="p-4">
            <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
              {region}
              <span className="ml-2 text-gray-400 font-normal">
                ({regionTownships.length})
              </span>
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {regionTownships.map((t) => (
                <button
                  key={t.id}
                  onClick={() => onSelect(t.id, season)}
                  className="text-left px-3 py-2 rounded-md hover:bg-green-50 hover:text-green-700 transition-colors text-sm"
                >
                  <span className="font-medium">{t.name}</span>
                  <span className="font-myanmar text-xs text-gray-400 ml-1">
                    {t.name_mm}
                  </span>
                </button>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

/** Group townships by region for display. */
function groupByRegion(townships: Township[]): Record<string, Township[]> {
  const groups: Record<string, Township[]> = {};
  for (const t of townships) {
    if (!groups[t.region]) groups[t.region] = [];
    groups[t.region].push(t);
  }
  return groups;
}
