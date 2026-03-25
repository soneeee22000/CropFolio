/** Distributor loan portfolio overview. */

/** Loan portfolio management for distributors. */
export function LoanPortfolio() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-display text-text-primary">
        Loan Portfolio
      </h1>
      <p className="text-text-secondary">
        Manage farmer loans, track disbursements and repayments.
      </p>
      <div className="rounded-xl bg-surface-elevated border border-border p-8 text-center">
        <p className="text-text-tertiary">
          Connect to PostgreSQL to see live loan data.
          <br />
          API: GET /api/v2/loans/
        </p>
      </div>
    </div>
  );
}
