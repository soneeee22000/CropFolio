/** Distributor analytics dashboard — loan metrics and compliance overview. */

import { useState, useEffect } from "react";
import { authClient } from "@/api/auth";

interface LoanSummary {
  total_loans: number;
  active_loans: number;
  total_disbursed_mmk: number;
  total_repaid_mmk: number;
  repayment_rate_pct: number;
  default_count: number;
  avg_compliance_score: number | null;
}

interface ComplianceItem {
  township_id: string;
  farmer_count: number;
  avg_compliance: number | null;
  compliant_count: number;
  warning_count: number;
  deviation_count: number;
}

/** Analytics dashboard for distributor decision-making. */
export function AnalyticsPage() {
  const [loanSummary, setLoanSummary] = useState<LoanSummary | null>(null);
  const [compliance, setCompliance] = useState<ComplianceItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      authClient.get<LoanSummary>("/distributor/loans/summary"),
      authClient.get<ComplianceItem[]>("/distributor/compliance/overview"),
    ])
      .then(([loanRes, compRes]) => {
        setLoanSummary(loanRes.data);
        setCompliance(compRes.data);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-text-tertiary text-center py-8">Loading...</p>;
  }

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-display text-text-primary">Analytics</h1>

      {/* Loan Portfolio KPIs */}
      {loanSummary && (
        <section>
          <h2 className="text-lg font-semibold text-text-primary mb-4">
            Loan Portfolio
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <MetricCard
              label="Total Disbursed"
              value={`${Math.round(loanSummary.total_disbursed_mmk / 1000).toLocaleString()}K`}
              unit="MMK"
            />
            <MetricCard
              label="Repayment Rate"
              value={`${loanSummary.repayment_rate_pct}%`}
              color={
                loanSummary.repayment_rate_pct >= 80
                  ? "text-primary"
                  : "text-warning"
              }
            />
            <MetricCard
              label="Active Loans"
              value={String(loanSummary.active_loans)}
              sub={`of ${loanSummary.total_loans} total`}
            />
            <MetricCard
              label="Avg Compliance"
              value={
                loanSummary.avg_compliance_score !== null
                  ? `${Math.round(loanSummary.avg_compliance_score * 100)}%`
                  : "--"
              }
              color={
                loanSummary.avg_compliance_score !== null &&
                loanSummary.avg_compliance_score >= 0.8
                  ? "text-primary"
                  : "text-warning"
              }
            />
          </div>
          {loanSummary.default_count > 0 && (
            <p className="mt-3 text-sm text-danger">
              {loanSummary.default_count} defaulted loan
              {loanSummary.default_count > 1 ? "s" : ""}
            </p>
          )}
        </section>
      )}

      {/* Compliance by Township */}
      <section>
        <h2 className="text-lg font-semibold text-text-primary mb-4">
          Compliance by Township
        </h2>
        {compliance.length === 0 ? (
          <div className="rounded-xl bg-surface-elevated border border-border p-8 text-center">
            <p className="text-text-tertiary">
              No compliance data yet. Enroll farmers and create loans to see
              township-level metrics.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-text-tertiary text-left">
                  <th className="pb-2 font-medium">Township</th>
                  <th className="pb-2 font-medium text-center">Farmers</th>
                  <th className="pb-2 font-medium text-center">Avg Score</th>
                  <th className="pb-2 font-medium text-center">Compliant</th>
                  <th className="pb-2 font-medium text-center">Warning</th>
                  <th className="pb-2 font-medium text-center">Deviation</th>
                </tr>
              </thead>
              <tbody>
                {compliance.map((item) => (
                  <tr
                    key={item.township_id}
                    className="border-b border-border-subtle"
                  >
                    <td className="py-2.5 text-text-primary font-medium">
                      {item.township_id}
                    </td>
                    <td className="py-2.5 text-center text-text-secondary">
                      {item.farmer_count}
                    </td>
                    <td className="py-2.5 text-center">
                      {item.avg_compliance !== null ? (
                        <span
                          className={`font-semibold ${
                            item.avg_compliance >= 0.8
                              ? "text-primary"
                              : item.avg_compliance >= 0.5
                                ? "text-warning"
                                : "text-danger"
                          }`}
                        >
                          {Math.round(item.avg_compliance * 100)}%
                        </span>
                      ) : (
                        <span className="text-text-tertiary">--</span>
                      )}
                    </td>
                    <td className="py-2.5 text-center text-primary">
                      {item.compliant_count}
                    </td>
                    <td className="py-2.5 text-center text-warning">
                      {item.warning_count}
                    </td>
                    <td className="py-2.5 text-center text-danger">
                      {item.deviation_count}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

function MetricCard({
  label,
  value,
  unit,
  sub,
  color = "text-text-primary",
}: {
  label: string;
  value: string;
  unit?: string;
  sub?: string;
  color?: string;
}) {
  return (
    <div className="rounded-xl bg-surface-elevated border border-border p-4">
      <p className="text-xs text-text-tertiary uppercase tracking-wider mb-1">
        {label}
      </p>
      <p className={`text-2xl font-semibold ${color}`}>
        {value}
        {unit && (
          <span className="text-sm text-text-tertiary ml-1">{unit}</span>
        )}
      </p>
      {sub && <p className="text-xs text-text-tertiary mt-0.5">{sub}</p>}
    </div>
  );
}
