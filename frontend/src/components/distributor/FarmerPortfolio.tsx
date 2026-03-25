/** Distributor view of all enrolled farmers with search and metrics. */

import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { authClient } from "@/api/auth";

interface FarmerItem {
  id: string;
  full_name: string;
  full_name_mm: string | null;
  phone_number: string | null;
  township_id: string | null;
  farm_count: number;
  active_plan_count: number;
  active_loan_count: number;
  compliance_score: number | null;
  credit_score: number | null;
}

/** Enrolled farmer portfolio for distributors. */
export function FarmerPortfolio() {
  const [farmers, setFarmers] = useState<FarmerItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    authClient
      .get<FarmerItem[]>("/distributor/farmers")
      .then((r) => setFarmers(r.data))
      .catch(() => setFarmers([]))
      .finally(() => setLoading(false));
  }, []);

  const filtered = farmers.filter(
    (f) =>
      f.full_name.toLowerCase().includes(search.toLowerCase()) ||
      (f.township_id?.toLowerCase().includes(search.toLowerCase()) ?? false),
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display text-text-primary">
          Farmer Portfolio
        </h1>
        <span className="text-text-tertiary text-sm">
          {farmers.length} farmers enrolled
        </span>
      </div>

      <input
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search by name or township..."
        className="w-full rounded-lg bg-surface-elevated border border-border px-4 py-2.5 text-text-primary focus:border-primary focus:outline-none"
      />

      {loading ? (
        <p className="text-text-tertiary text-center py-8">Loading...</p>
      ) : filtered.length === 0 ? (
        <div className="rounded-xl bg-surface-elevated border border-border p-8 text-center">
          <p className="text-text-secondary">No farmers found</p>
          <p className="text-text-tertiary text-sm mt-1">
            Create loans for farmers to see them here
          </p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((farmer) => (
            <Link
              key={farmer.id}
              to={`/farmer-detail/${farmer.id}`}
              className="block rounded-xl bg-surface-elevated border border-border p-4 hover:border-primary/50 transition-colors"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="font-semibold text-text-primary">
                    {farmer.full_name}
                  </p>
                  {farmer.full_name_mm && (
                    <p className="text-sm text-text-secondary font-myanmar">
                      {farmer.full_name_mm}
                    </p>
                  )}
                  <p className="text-xs text-text-tertiary mt-0.5">
                    {farmer.township_id ?? "No township"}
                  </p>
                </div>
                {farmer.compliance_score !== null && (
                  <span
                    className={`text-sm font-semibold ${
                      farmer.compliance_score >= 0.8
                        ? "text-primary"
                        : farmer.compliance_score >= 0.5
                          ? "text-warning"
                          : "text-danger"
                    }`}
                  >
                    {Math.round(farmer.compliance_score * 100)}%
                  </span>
                )}
              </div>

              <div className="grid grid-cols-3 gap-2 text-center">
                <div>
                  <p className="text-lg font-semibold text-text-primary">
                    {farmer.farm_count}
                  </p>
                  <p className="text-xs text-text-tertiary">Farms</p>
                </div>
                <div>
                  <p className="text-lg font-semibold text-text-primary">
                    {farmer.active_plan_count}
                  </p>
                  <p className="text-xs text-text-tertiary">Plans</p>
                </div>
                <div>
                  <p className="text-lg font-semibold text-text-primary">
                    {farmer.active_loan_count}
                  </p>
                  <p className="text-xs text-text-tertiary">Loans</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
