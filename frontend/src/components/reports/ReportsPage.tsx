import { useState } from "react";
import { Card } from "@/components/common/Card";
import { apiClient } from "@/api/client";

/** Language option for PDF generation. */
type PdfLanguage = "en" | "mm";

/** Reports page — advisory briefs and PDF reports with language toggle. */
export function ReportsPage() {
  const [language, setLanguage] = useState<PdfLanguage>("mm");
  const [downloading, setDownloading] = useState(false);

  /** Download a sample PDF report in the selected language. */
  async function handleDownloadSample() {
    setDownloading(true);
    try {
      const response = await apiClient.post(
        "/report/pdf",
        {
          township_name: "Meiktila",
          season: "dry",
          language,
          allocations: [
            { crop_name: "Rice", crop_name_mm: "စပါး", weight_pct: 35.0 },
            {
              crop_name: "Chickpea",
              crop_name_mm: "ကုလားပဲ",
              weight_pct: 25.0,
            },
            { crop_name: "Sesame", crop_name_mm: "နှမ်း", weight_pct: 20.0 },
            { crop_name: "Groundnut", crop_name_mm: "မြေပဲ", weight_pct: 20.0 },
          ],
          expected_income: 1850000,
          risk_reduction_pct: 34.2,
          prob_catastrophic_loss_monocrop: 18.5,
          prob_catastrophic_loss_diversified: 4.2,
          crop_confidence: {
            Rice: "high",
            Chickpea: "high",
            Sesame: "low",
            Groundnut: "high",
          },
        },
        { responseType: "blob" },
      );

      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download =
        language === "mm" ? "cropfolio-report-mm.pdf" : "cropfolio-report.pdf";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      // Silently handle — user can retry
    } finally {
      setDownloading(false);
    }
  }

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

        {/* Language Toggle */}
        <div className="flex items-center gap-3 mb-4">
          <span className="text-sm text-text-secondary">PDF Language:</span>
          <button
            type="button"
            onClick={() => setLanguage("en")}
            className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
              language === "en"
                ? "bg-primary text-white"
                : "bg-surface-secondary text-text-secondary hover:bg-surface-tertiary"
            }`}
          >
            English
          </button>
          <button
            type="button"
            onClick={() => setLanguage("mm")}
            className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
              language === "mm"
                ? "bg-primary text-white"
                : "bg-surface-secondary text-text-secondary hover:bg-surface-tertiary"
            }`}
          >
            မြန်မာ (Burmese)
          </button>
        </div>

        <button
          type="button"
          onClick={handleDownloadSample}
          disabled={downloading}
          className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 disabled:opacity-50 transition-colors"
        >
          {downloading
            ? "Generating..."
            : language === "mm"
              ? "Download Burmese PDF"
              : "Download English PDF"}
        </button>

        <div className="mt-4 p-6 rounded-lg border-2 border-dashed border-border text-center">
          <p className="text-text-tertiary text-sm">
            Run a recommendation from the Recommend tab to generate a custom
            report
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
