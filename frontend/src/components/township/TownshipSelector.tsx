import { useMemo, useState } from "react";
import { useTownships } from "@/hooks/useTownships";
import { useLanguage } from "@/i18n/LanguageContext";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import type { Township } from "@/types/township";

interface TownshipSelectorProps {
  onSelect: (townshipId: string, season: "monsoon" | "dry") => void;
}

/** Premium township selector with hero typography and refined list. */
export function TownshipSelector({ onSelect }: TownshipSelectorProps) {
  const { townships, isLoading } = useTownships();
  const { t } = useLanguage();
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
    <div className="max-w-2xl mx-auto pt-8">
      <div className="text-center mb-12">
        <p className="text-[11px] uppercase tracking-[0.2em] text-text-tertiary mb-3">
          {t("township.overline")}
        </p>
        <h2 className="font-display text-4xl text-text-primary">
          {t("township.heading")}
        </h2>
        <p className="text-text-secondary mt-3">{t("township.subtitle")}</p>
      </div>

      <div className="flex justify-center mb-10">
        <div className="inline-flex bg-surface-subtle rounded-full p-1">
          <button
            onClick={() => setSeason("monsoon")}
            className={`px-5 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
              season === "monsoon"
                ? "bg-primary text-white"
                : "text-text-secondary hover:text-text-primary"
            }`}
          >
            {t("season.monsoon")}
          </button>
          <button
            onClick={() => setSeason("dry")}
            className={`px-5 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
              season === "dry"
                ? "bg-primary text-white"
                : "text-text-secondary hover:text-text-primary"
            }`}
          >
            {t("season.dry")}
          </button>
        </div>
      </div>

      <div className="mb-8">
        <input
          type="text"
          placeholder={t("township.search")}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-transparent text-lg text-text-primary placeholder:text-text-tertiary border-b-2 border-border focus:border-primary pb-3 outline-none transition-colors duration-300"
        />
      </div>

      <div className="space-y-6 max-h-[32rem] overflow-y-auto pr-2">
        {Object.entries(grouped).map(([region, regionTownships]) => (
          <div key={region} className="animate-fade-in-up">
            <h4 className="text-[11px] uppercase tracking-[0.2em] text-text-tertiary mb-4">
              {region}
              <span className="ml-2 text-text-tertiary/60">
                ({regionTownships.length})
              </span>
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-1">
              {regionTownships.map((t) => (
                <button
                  key={t.id}
                  onClick={() => onSelect(t.id, season)}
                  className="text-left px-4 py-3 rounded-lg hover:bg-surface-subtle hover:border-l-2 hover:border-primary transition-all duration-200 group"
                >
                  <span className="font-medium text-sm text-text-primary group-hover:text-primary transition-colors">
                    {t.name}
                  </span>
                  <span className="font-myanmar text-xs text-text-tertiary block mt-0.5">
                    {t.name_mm}
                  </span>
                </button>
              ))}
            </div>
          </div>
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
