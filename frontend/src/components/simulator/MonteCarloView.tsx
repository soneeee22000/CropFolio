import { useState } from "react";
import { useSimulate } from "@/hooks/useSimulate";
import { useLanguage } from "@/i18n/LanguageContext";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { MonteCarloHistogram } from "./MonteCarloHistogram";
import { formatMMKCompact, formatPercent } from "@/utils/formatters";
import { DEFAULT_NUM_SIMULATIONS } from "@/constants";
import { apiClient } from "@/api/client";
import type { OptimizeResponse } from "@/types/optimizer";
import type { SimulateResponse } from "@/types/simulator";

interface MonteCarloViewProps {
  townshipId: string;
  season: "monsoon" | "dry";
  optimizeResult: OptimizeResponse;
}

/** Premium Monte Carlo simulation view. */
export function MonteCarloView({
  townshipId,
  season,
  optimizeResult,
}: MonteCarloViewProps) {
  const { result, isLoading, error, simulate } = useSimulate();
  const { result: monocropResult, simulate: simulateMonocrop } = useSimulate();
  useLanguage(); // connected for future i18n
  const [numSims, setNumSims] = useState(DEFAULT_NUM_SIMULATIONS);
  const [showComparison, setShowComparison] = useState(false);

  const handleRun = async () => {
    const weights: Record<string, number> = {};
    for (const w of optimizeResult.weights) {
      weights[w.crop_id] = w.weight;
    }
    const cropIds = optimizeResult.weights.map((w) => w.crop_id);

    await simulate({
      crop_ids: cropIds,
      weights,
      township_id: townshipId,
      num_simulations: numSims,
      season,
    });

    // Use the highest-weighted crop as the monocrop baseline
    const topCrop = optimizeResult.weights.reduce((a, b) =>
      a.weight > b.weight ? a : b,
    );
    const monocropWeights: Record<string, number> = {};
    for (const id of cropIds) {
      monocropWeights[id] = id === topCrop.crop_id ? 1.0 : 0.0;
    }
    const mono = await simulateMonocrop({
      crop_ids: cropIds,
      weights: monocropWeights,
      township_id: townshipId,
      num_simulations: numSims,
      season,
    });
    if (mono) setShowComparison(true);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <p className="text-[11px] uppercase tracking-[0.2em] text-text-tertiary mb-3">
          Simulation
        </p>
        <h2 className="font-display text-4xl text-text-primary">
          Monte Carlo Analysis
        </h2>
        <p className="text-text-secondary mt-3">
          Simulate {numSims.toLocaleString()} possible climate seasons
        </p>
      </div>

      <div className="flex items-center justify-center gap-4 mb-12">
        <select
          value={numSims}
          onChange={(e) => setNumSims(Number(e.target.value))}
          className="bg-transparent text-sm text-text-secondary border-b-2 border-border focus:border-primary py-2 pr-8 outline-none transition-colors cursor-pointer"
        >
          <option value={500}>500 simulations</option>
          <option value={1000}>1,000 simulations</option>
          <option value={5000}>5,000 simulations</option>
        </select>
        <button
          onClick={handleRun}
          disabled={isLoading}
          className="px-10 py-4 bg-primary text-white rounded-lg text-sm uppercase tracking-wide font-medium hover:bg-primary-dark transition-colors duration-200 disabled:opacity-40"
        >
          {isLoading ? "Simulating..." : "Run Simulation"}
        </button>
      </div>

      {isLoading && (
        <LoadingSpinner
          message={`Simulating ${numSims.toLocaleString()} seasons...`}
        />
      )}
      {error && <ErrorAlert message={error} />}

      {result && (
        <>
          <Card className="mb-8">
            <MonteCarloHistogram
              histogram={result.histogram}
              stats={result.stats}
              comparisonHistogram={
                showComparison ? monocropResult?.histogram : undefined
              }
            />
          </Card>

          <StatsComparison
            diversified={result}
            monocrop={showComparison ? monocropResult : null}
          />

          <div className="text-center mt-8">
            <button
              onClick={async () => {
                const reportData = {
                  township_name: result.township_name,
                  season: result.season,
                  allocations: optimizeResult.weights.map((w) => ({
                    crop_name: w.crop_name,
                    crop_name_mm: w.crop_name_mm,
                    weight_pct: w.weight * 100,
                  })),
                  expected_income:
                    optimizeResult.metrics.expected_income_per_ha,
                  risk_reduction_pct: optimizeResult.metrics.risk_reduction_pct,
                  prob_catastrophic_loss_monocrop:
                    (monocropResult?.stats.prob_catastrophic_loss ?? 0) * 100,
                  prob_catastrophic_loss_diversified:
                    result.stats.prob_catastrophic_loss * 100,
                };
                const res = await apiClient.post("/report/pdf", reportData, {
                  responseType: "blob",
                });
                const url = URL.createObjectURL(res.data as Blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "cropfolio-report.pdf";
                a.click();
                URL.revokeObjectURL(url);
              }}
              className="px-8 py-3 border border-border rounded-lg text-sm text-text-secondary hover:text-text-primary hover:border-text-tertiary transition-colors duration-200"
            >
              Download PDF Report
            </button>
          </div>
        </>
      )}
    </div>
  );
}

/** Side-by-side stats comparison. */
function StatsComparison({
  diversified,
  monocrop,
}: {
  diversified: SimulateResponse;
  monocrop: SimulateResponse | null;
}) {
  const d = diversified.stats;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          value={formatMMKCompact(d.mean_income)}
          label="Mean Income"
        />
        <MetricCard
          value={formatMMKCompact(d.percentile_5)}
          label="Worst Case (P5)"
        />
        <MetricCard
          value={formatMMKCompact(d.percentile_95)}
          label="Best Case (P95)"
        />
        <MetricCard
          value={formatPercent(d.prob_catastrophic_loss)}
          label="Catastrophic Loss"
          highlight={d.prob_catastrophic_loss < 0.1}
        />
      </div>

      {monocrop && (
        <Card className="text-center">
          <p className="text-sm text-text-secondary">
            Catastrophic loss probability:{" "}
            <span className="font-data font-medium text-danger">
              {formatPercent(monocrop.stats.prob_catastrophic_loss)}
            </span>
            {" (monocrop) vs "}
            <span className="font-data font-medium text-primary">
              {formatPercent(d.prob_catastrophic_loss)}
            </span>
            {" (diversified)"}
          </p>
        </Card>
      )}
    </div>
  );
}
