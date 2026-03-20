import { useState, useEffect } from "react";
import { Card } from "@/components/common/Card";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { AdvisorySection } from "./AdvisorySection";
import { QueryInput } from "./QueryInput";
import { QueryResult } from "./QueryResult";
import { useAdvisory, useAdvisoryQuery } from "@/hooks/useAdvisory";
import { fetchTownships } from "@/api/townships";
import { useLanguage } from "@/i18n/LanguageContext";
import type { Township } from "@/types/township";

const SECTION_ICONS = {
  executive_brief:
    "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
  crop_strategy:
    "M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064",
  fertilizer_plan:
    "M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 2v4m8-4v4m-9 4h10M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z",
  risk_warnings:
    "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z",
  market_outlook: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
};

/** Advisory page — AI-powered township intelligence with Q&A. */
export function AdvisoryPage() {
  const { t } = useLanguage();
  const [townships, setTownships] = useState<Township[]>([]);
  const [selectedTownship, setSelectedTownship] = useState("");
  const [season, setSeason] = useState<"monsoon" | "dry">("monsoon");
  const [loadError, setLoadError] = useState<string | null>(null);

  const {
    advisory,
    isLoading: advisoryLoading,
    error: advisoryError,
    generate,
    reset: resetAdvisory,
  } = useAdvisory();

  const {
    queries,
    isLoading: queryLoading,
    error: queryError,
    ask,
    reset: resetQueries,
  } = useAdvisoryQuery();

  useEffect(() => {
    async function load() {
      try {
        const res = await fetchTownships();
        setTownships(res.townships);
      } catch {
        setLoadError("Failed to load townships");
      }
    }
    load();
  }, []);

  const handleGenerate = () => {
    if (selectedTownship) {
      generate(selectedTownship, season);
    }
  };

  const handleAsk = (question: string) => {
    if (selectedTownship) {
      ask(selectedTownship, season, question);
    }
  };

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <h2
            className="font-display text-3xl text-text-primary"
            data-testid="advisory-title"
          >
            {t("advisory.title")}
          </h2>
          <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-primary/10 text-primary font-medium">
            AI
          </span>
        </div>
        <p className="text-text-secondary mt-1">{t("advisory.subtitle")}</p>
      </div>

      {/* Controls */}
      <Card title={t("advisory.selectArea")}>
        {loadError && <ErrorAlert message={loadError} />}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
              {t("township.overline")}
            </label>
            <select
              value={selectedTownship}
              onChange={(e) => {
                setSelectedTownship(e.target.value);
                resetAdvisory();
                resetQueries();
              }}
              className="w-full p-3 rounded-lg border border-border bg-surface-elevated text-text-primary text-base"
              data-testid="advisory-township-select"
            >
              <option value="">Select township...</option>
              {townships.map((tw) => (
                <option key={tw.id} value={tw.id}>
                  {tw.name} ({tw.region})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-xs uppercase tracking-wide text-text-tertiary block mb-2">
              {t("recommend.season")}
            </label>
            <select
              value={season}
              onChange={(e) => setSeason(e.target.value as "monsoon" | "dry")}
              className="w-full p-3 rounded-lg border border-border bg-surface-elevated text-text-primary text-base"
            >
              <option value="monsoon">{t("recommend.monsoon")}</option>
              <option value="dry">{t("recommend.dry")}</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleGenerate}
              disabled={!selectedTownship || advisoryLoading}
              data-testid="advisory-generate-btn"
              className="w-full p-3 rounded-lg bg-primary text-white font-medium text-sm hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {advisoryLoading
                ? t("advisory.generating")
                : t("advisory.generate")}
            </button>
          </div>
        </div>
      </Card>

      {/* Loading */}
      {advisoryLoading && (
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner />
          <span className="ml-3 text-text-secondary">
            {t("advisory.generating")}
          </span>
        </div>
      )}

      {/* Error */}
      {advisoryError && <ErrorAlert message={advisoryError} />}

      {/* Advisory sections */}
      {advisory && (
        <div className="space-y-4">
          {!advisory.has_ai && (
            <div className="px-4 py-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-700 text-sm">
              {t("advisory.noAiFallback")}
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="lg:col-span-2">
              <AdvisorySection
                section={advisory.executive_brief}
                icon={SECTION_ICONS.executive_brief}
              />
            </div>
            <AdvisorySection
              section={advisory.crop_strategy}
              icon={SECTION_ICONS.crop_strategy}
            />
            <AdvisorySection
              section={advisory.fertilizer_plan}
              icon={SECTION_ICONS.fertilizer_plan}
            />
            <AdvisorySection
              section={advisory.risk_warnings}
              icon={SECTION_ICONS.risk_warnings}
            />
            <AdvisorySection
              section={advisory.market_outlook}
              icon={SECTION_ICONS.market_outlook}
            />
          </div>
        </div>
      )}

      {/* Q&A section */}
      <Card title={t("advisory.askTitle")}>
        <div className="space-y-4">
          <QueryInput
            onSubmit={handleAsk}
            isLoading={queryLoading}
            disabled={!selectedTownship}
          />

          {queryError && <ErrorAlert message={queryError} />}

          {queries.length > 0 && (
            <div className="space-y-3 mt-4">
              {queries.map((entry) => (
                <QueryResult key={entry.id} entry={entry} />
              ))}
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
