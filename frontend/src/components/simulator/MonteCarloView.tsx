import { useState } from "react";
import { useSimulate } from "@/hooks/useSimulate";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { ErrorAlert } from "@/components/common/ErrorAlert";
import { MonteCarloHistogram } from "./MonteCarloHistogram";
import { formatMMKCompact, formatPercent } from "@/utils/formatters";
import { DEFAULT_NUM_SIMULATIONS } from "@/constants";
import type { OptimizeResponse } from "@/types/optimizer";
import type { SimulateResponse } from "@/types/simulator";

interface MonteCarloViewProps {
  townshipId: string;
  season: "monsoon" | "dry";
  optimizeResult: OptimizeResponse;
}

/** Monte Carlo simulation view with animated histogram. */
export function MonteCarloView({
  townshipId,
  season,
  optimizeResult,
}: MonteCarloViewProps) {
  const { result, isLoading, error, simulate } = useSimulate();
  const { result: monocropResult, simulate: simulateMonocrop } = useSimulate();
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

    const monocropWeights: Record<string, number> = {};
    for (const id of cropIds) {
      monocropWeights[id] = id === "rice" ? 1.0 : 0.0;
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
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">
          Monte Carlo Simulation
        </h2>
        <p className="text-gray-500 mt-1">
          Simulate {numSims.toLocaleString()} possible climate seasons
        </p>
      </div>

      <Card className="flex items-center justify-center gap-4">
        <select
          value={numSims}
          onChange={(e) => setNumSims(Number(e.target.value))}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
        >
          <option value={500}>500 simulations</option>
          <option value={1000}>1,000 simulations</option>
          <option value={5000}>5,000 simulations</option>
        </select>
        <button
          onClick={handleRun}
          disabled={isLoading}
          className="px-8 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary-dark transition-colors disabled:opacity-50"
        >
          {isLoading ? "Simulating..." : "Run Simulation"}
        </button>
      </Card>

      {isLoading && (
        <LoadingSpinner
          message={`Simulating ${numSims.toLocaleString()} seasons...`}
        />
      )}
      {error && <ErrorAlert message={error} />}

      {result && (
        <>
          <Card>
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
    <div className="space-y-4">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <MetricCard
          value={formatMMKCompact(d.mean_income)}
          label="Mean Income/ha"
        />
        <MetricCard
          value={formatMMKCompact(d.percentile_5)}
          label="Worst Case (5th %ile)"
        />
        <MetricCard
          value={formatMMKCompact(d.percentile_95)}
          label="Best Case (95th %ile)"
        />
        <MetricCard
          value={formatPercent(d.prob_catastrophic_loss)}
          label="P(Catastrophic Loss)"
          highlight={d.prob_catastrophic_loss < 0.1}
        />
      </div>

      {monocrop && (
        <Card className="text-center">
          <p className="text-sm text-gray-600">
            Catastrophic loss probability:{" "}
            <span className="font-bold text-red-600">
              {formatPercent(monocrop.stats.prob_catastrophic_loss)}
            </span>
            {" (monocrop) vs "}
            <span className="font-bold text-green-700">
              {formatPercent(d.prob_catastrophic_loss)}
            </span>
            {" (diversified)"}
          </p>
        </Card>
      )}
    </div>
  );
}
