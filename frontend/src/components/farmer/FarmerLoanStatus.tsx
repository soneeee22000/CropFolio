/** Farmer loan and compliance overview screen. */

import { useState, useEffect } from "react";
import { authClient } from "@/api/auth";

interface LoanItem {
  id: string;
  principal_mmk: number;
  total_repaid_mmk: number;
  status: string;
  compliance_score: number | null;
  credit_score: number | null;
  due_date: string | null;
}

const STATUS_LABELS: Record<string, string> = {
  pending: "စောင့်ဆိုင်း",
  active: "အသက်ဝင်",
  repaid: "ပြန်ဆပ်ပြီ",
  defaulted: "ပျက်ကွက်",
};

const STATUS_COLORS: Record<string, string> = {
  pending: "text-warning",
  active: "text-primary",
  repaid: "text-primary",
  defaulted: "text-danger",
};

/** Loan balance, compliance score, and credit trend for a farmer. */
export function FarmerLoanStatus() {
  const [loans, setLoans] = useState<LoanItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    authClient
      .get<LoanItem[]>("/loans/")
      .then((r) => setLoans(r.data))
      .catch(() => setLoans([]))
      .finally(() => setLoading(false));
  }, []);

  const activeLoans = loans.filter((l) => l.status === "active");
  const totalOwed = activeLoans.reduce(
    (sum, l) => sum + (l.principal_mmk - l.total_repaid_mmk),
    0,
  );
  const latestCompliance = activeLoans.find((l) => l.compliance_score !== null);
  const latestCredit = activeLoans.find((l) => l.credit_score !== null);

  return (
    <div className="space-y-6 max-w-lg mx-auto">
      <h1 className="text-xl font-display text-text-primary font-myanmar">
        ချေးငွေ နှင့် လိုက်နာမှု
      </h1>

      {loading ? (
        <p className="text-text-tertiary text-center py-8">Loading...</p>
      ) : (
        <>
          {/* Summary cards */}
          <div className="grid grid-cols-3 gap-3">
            <div className="rounded-xl bg-surface-elevated border border-border p-3 text-center">
              <p className="text-xl font-semibold text-accent">
                {totalOwed > 0 ? `${Math.round(totalOwed / 1000)}K` : "0"}
              </p>
              <p className="text-xs text-text-tertiary mt-1 font-myanmar">
                ကျန်ငွေ (MMK)
              </p>
            </div>
            <div className="rounded-xl bg-surface-elevated border border-border p-3 text-center">
              <p className="text-xl font-semibold text-primary">
                {latestCompliance?.compliance_score !== null &&
                latestCompliance?.compliance_score !== undefined
                  ? `${Math.round(latestCompliance.compliance_score * 100)}%`
                  : "--"}
              </p>
              <p className="text-xs text-text-tertiary mt-1 font-myanmar">
                လိုက်နာမှု
              </p>
            </div>
            <div className="rounded-xl bg-surface-elevated border border-border p-3 text-center">
              <p className="text-xl font-semibold text-primary">
                {latestCredit?.credit_score !== null &&
                latestCredit?.credit_score !== undefined
                  ? `${Math.round(latestCredit.credit_score * 100)}`
                  : "--"}
              </p>
              <p className="text-xs text-text-tertiary mt-1 font-myanmar">
                ခရက်ဒစ်
              </p>
            </div>
          </div>

          {/* Loan list */}
          {loans.length === 0 ? (
            <div className="rounded-xl bg-surface-elevated border border-border p-6 text-center">
              <p className="text-text-secondary font-myanmar">
                ချေးငွေ မရှိသေးပါ
              </p>
              <p className="text-text-tertiary text-sm mt-1">No loans yet</p>
            </div>
          ) : (
            <div className="space-y-3">
              {loans.map((loan) => {
                const remaining = loan.principal_mmk - loan.total_repaid_mmk;
                const paidPct =
                  loan.principal_mmk > 0
                    ? (loan.total_repaid_mmk / loan.principal_mmk) * 100
                    : 0;

                return (
                  <div
                    key={loan.id}
                    className="rounded-xl bg-surface-elevated border border-border p-4"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="font-semibold text-text-primary">
                          {loan.principal_mmk.toLocaleString()} MMK
                        </p>
                        {loan.due_date && (
                          <p className="text-xs text-text-tertiary mt-0.5">
                            Due: {loan.due_date}
                          </p>
                        )}
                      </div>
                      <span
                        className={`text-xs font-semibold ${STATUS_COLORS[loan.status] ?? "text-text-tertiary"}`}
                      >
                        {STATUS_LABELS[loan.status] ?? loan.status}
                      </span>
                    </div>

                    {/* Progress bar */}
                    <div className="mt-3">
                      <div className="flex justify-between text-xs text-text-tertiary mb-1">
                        <span>ပြန်ဆပ်ပြီး</span>
                        <span>{Math.round(paidPct)}%</span>
                      </div>
                      <div className="h-2 rounded-full bg-surface overflow-hidden">
                        <div
                          className="h-full rounded-full bg-primary transition-all"
                          style={{ width: `${Math.min(paidPct, 100)}%` }}
                        />
                      </div>
                      <p className="text-xs text-text-secondary mt-1">
                        ကျန် {remaining.toLocaleString()} MMK
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}
    </div>
  );
}
