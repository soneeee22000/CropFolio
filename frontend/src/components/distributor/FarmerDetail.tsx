/** Single farmer detail view for distributors. */

import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { authClient } from "@/api/auth";

interface FarmerData {
  id: string;
  full_name: string;
  full_name_mm: string | null;
  phone_number: string | null;
  township_id: string | null;
  farms: Array<{
    id: string;
    name: string;
    township_id: string;
    area_ha: number;
    plot_count: number;
  }>;
  plans: Array<{
    id: string;
    season: string;
    year: number;
    status: string;
    crop_ids: string[];
  }>;
  loans: Array<{
    id: string;
    principal_mmk: number;
    status: string;
    total_repaid_mmk: number;
    compliance_score: number | null;
    credit_score: number | null;
  }>;
}

const STATUS_COLORS: Record<string, string> = {
  draft: "text-warning",
  active: "text-primary",
  completed: "text-primary",
  abandoned: "text-danger",
  pending: "text-warning",
  repaid: "text-primary",
  defaulted: "text-danger",
};

/** Detailed farmer view for distributor dashboard. */
export function FarmerDetail() {
  const { farmerId } = useParams<{ farmerId: string }>();
  const [data, setData] = useState<FarmerData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!farmerId) return;
    authClient
      .get<FarmerData>(`/distributor/farmers/${farmerId}`)
      .then((r) => setData(r.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [farmerId]);

  if (loading) {
    return <p className="text-text-tertiary text-center py-8">Loading...</p>;
  }

  if (!data) {
    return <p className="text-danger text-center py-8">Farmer not found</p>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-display text-text-primary">
          {data.full_name}
        </h1>
        {data.full_name_mm && (
          <p className="text-text-secondary font-myanmar">
            {data.full_name_mm}
          </p>
        )}
        <p className="text-sm text-text-tertiary mt-1">
          {data.phone_number ?? "No phone"} |{" "}
          {data.township_id ?? "No township"}
        </p>
      </div>

      {/* Farms */}
      <section>
        <h2 className="text-lg font-semibold text-text-primary mb-3">
          Farms ({data.farms.length})
        </h2>
        <div className="grid gap-3 md:grid-cols-2">
          {data.farms.map((farm) => (
            <div
              key={farm.id}
              className="rounded-xl bg-surface-elevated border border-border p-4"
            >
              <p className="font-semibold text-text-primary">{farm.name}</p>
              <p className="text-sm text-text-secondary">
                {farm.township_id} | {farm.area_ha} ha | {farm.plot_count} plots
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Plans */}
      <section>
        <h2 className="text-lg font-semibold text-text-primary mb-3">
          Crop Plans ({data.plans.length})
        </h2>
        <div className="space-y-2">
          {data.plans.map((plan) => (
            <div
              key={plan.id}
              className="rounded-lg bg-surface-elevated border border-border px-4 py-3 flex justify-between items-center"
            >
              <div>
                <p className="text-text-primary font-semibold">
                  {plan.crop_ids.join(", ")}
                </p>
                <p className="text-xs text-text-tertiary">
                  {plan.season} {plan.year}
                </p>
              </div>
              <span
                className={`text-xs font-semibold ${STATUS_COLORS[plan.status] ?? "text-text-tertiary"}`}
              >
                {plan.status}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Loans */}
      <section>
        <h2 className="text-lg font-semibold text-text-primary mb-3">
          Loans ({data.loans.length})
        </h2>
        <div className="space-y-2">
          {data.loans.map((loan) => (
            <div
              key={loan.id}
              className="rounded-lg bg-surface-elevated border border-border px-4 py-3"
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-text-primary font-semibold">
                    {loan.principal_mmk.toLocaleString()} MMK
                  </p>
                  <p className="text-xs text-text-tertiary">
                    Repaid: {loan.total_repaid_mmk.toLocaleString()} MMK
                  </p>
                </div>
                <span
                  className={`text-xs font-semibold ${STATUS_COLORS[loan.status] ?? "text-text-tertiary"}`}
                >
                  {loan.status}
                </span>
              </div>
              {(loan.compliance_score !== null ||
                loan.credit_score !== null) && (
                <div className="flex gap-4 mt-2 text-xs text-text-secondary">
                  {loan.compliance_score !== null && (
                    <span>
                      Compliance: {Math.round(loan.compliance_score * 100)}%
                    </span>
                  )}
                  {loan.credit_score !== null && (
                    <span>Credit: {Math.round(loan.credit_score * 100)}</span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
