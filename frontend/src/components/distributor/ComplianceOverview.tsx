/** Distributor compliance overview across all farmers. */

/** Compliance dashboard for distributors. */
export function ComplianceOverview() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-display text-text-primary">
        Compliance Overview
      </h1>
      <p className="text-text-secondary">
        Monitor farmer compliance scores across townships and plans.
      </p>
      <div className="rounded-xl bg-surface-elevated border border-border p-8 text-center">
        <p className="text-text-tertiary">
          Connect to PostgreSQL to see live compliance data.
          <br />
          API: GET /api/v2/compliance/farmer/&#123;farmer_id&#125;
        </p>
      </div>
    </div>
  );
}
