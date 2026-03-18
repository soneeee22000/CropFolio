import { Card } from "@/components/common/Card";

/** Reports page — AI-generated distributor advisory briefs. */
export function ReportsPage() {
  return (
    <div className="space-y-8 animate-fade-in-up">
      <div>
        <h2 className="font-display text-3xl text-text-primary">Reports</h2>
        <p className="text-text-secondary mt-1">
          AI-generated distributor advisory briefs and PDF reports
        </p>
      </div>

      <Card title="Advisory Report Generator">
        <p className="text-sm text-text-secondary mb-4">
          Generate recommendations first, then create distributor-ready PDF
          reports with AI-powered insights including inventory guidance, field
          agent notes, and risk warnings.
        </p>
        <div className="p-8 rounded-lg border-2 border-dashed border-border text-center">
          <p className="text-text-tertiary text-sm">
            Run a recommendation from the Recommend tab to generate a report
          </p>
        </div>
      </Card>

      <Card title="Recent Reports">
        <div className="p-8 rounded-lg border-2 border-dashed border-border text-center">
          <p className="text-text-tertiary text-sm">No reports generated yet</p>
        </div>
      </Card>
    </div>
  );
}
