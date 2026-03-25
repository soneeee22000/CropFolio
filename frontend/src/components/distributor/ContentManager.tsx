/** Distributor content creation and management. */

/** Content management dashboard for distributors. */
export function ContentManager() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-display text-text-primary">
        Content Manager
      </h1>
      <p className="text-text-secondary">
        Create and publish weather alerts, farming tips, and fertilizer
        reminders for your farmers.
      </p>
      <div className="rounded-xl bg-surface-elevated border border-border p-8 text-center">
        <p className="text-text-tertiary">
          Connect to PostgreSQL to manage content.
          <br />
          API: POST /api/v2/content/
        </p>
      </div>
    </div>
  );
}
