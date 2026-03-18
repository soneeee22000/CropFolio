import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/common/Card";
import { MetricCard } from "@/components/common/MetricCard";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";
import { fetchTownships } from "@/api/townships";
import { fetchCrops } from "@/api/crops";
import { getFertilizers } from "@/api/fertilizers";
import type { Township } from "@/types/township";

/** Dashboard overview with KPI cards and quick actions. */
export function DashboardOverview() {
  const navigate = useNavigate();
  const [stats, setStats] = useState<{
    townships: number;
    crops: number;
    fertilizers: number;
  } | null>(null);
  const [townships, setTownships] = useState<Township[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const [twpRes, cropRes, fertRes] = await Promise.all([
          fetchTownships(),
          fetchCrops(),
          getFertilizers(),
        ]);
        setStats({
          townships: twpRes.count,
          crops: cropRes.count,
          fertilizers: fertRes.count,
        });
        setTownships(twpRes.townships);
        (window as Record<string, unknown>).__dashSuccess = {
          twp: twpRes.count,
          crops: cropRes.count,
          fert: fertRes.count,
        };
      } catch (err: unknown) {
        (window as Record<string, unknown>).__dashError = err;
        console.error("Dashboard loadStats failed:", err);
      } finally {
        setIsLoading(false);
      }
    }
    loadStats();
  }, []);

  if (isLoading) {
    return <LoadingSpinner message="Loading dashboard..." />;
  }

  const regions = [...new Set(townships.map((t) => t.region))];

  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* Page header */}
      <div>
        <h2 className="font-display text-3xl text-text-primary">
          CropFolio Pro
        </h2>
        <p className="text-text-secondary mt-1">
          Data-driven crop-fertilizer recommendations for distributors
        </p>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          value={String(stats?.townships ?? 0)}
          label="Townships"
          sublabel={`${regions.length} regions covered`}
        />
        <MetricCard
          value={String(stats?.crops ?? 0)}
          label="Crop Profiles"
          sublabel="FAOSTAT + WFP data"
        />
        <MetricCard
          value={String(stats?.fertilizers ?? 0)}
          label="Fertilizers"
          sublabel="NPK formulations"
        />
        <MetricCard
          value="1,000"
          label="Monte Carlo Sims"
          sublabel="Per recommendation"
          highlight
        />
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Generate Recommendations">
          <p className="text-sm text-text-secondary mb-6">
            Select townships and crops to get optimized crop-fertilizer pairings
            with confidence scores from 1,000 Monte Carlo simulations.
          </p>
          <button
            onClick={() => navigate("/recommend")}
            className="px-5 py-2.5 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors"
          >
            Start Recommendation
          </button>
        </Card>
        <Card title="Demo ROI Calculator">
          <p className="text-sm text-text-secondary mb-6">
            Before committing to a demo farm, calculate expected costs, revenue,
            and reimbursement risk for any crop-township combination.
          </p>
          <button
            onClick={() => navigate("/demo-calculator")}
            className="px-5 py-2.5 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary-dark transition-colors"
          >
            Calculate ROI
          </button>
        </Card>
      </div>

      {/* Coverage map placeholder */}
      <Card title="Coverage by Region">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {regions.map((region) => {
            const count = townships.filter((t) => t.region === region).length;
            return (
              <div
                key={region}
                className="p-3 rounded-lg bg-surface-subtle text-center"
              >
                <div className="font-data text-lg text-text-primary">
                  {count}
                </div>
                <div className="text-[11px] uppercase tracking-wide text-text-tertiary mt-1">
                  {region}
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
