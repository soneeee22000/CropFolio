import { useLanguage } from "@/i18n/LanguageContext";
import { COMPLIANCE_COLORS } from "@/constants/map";
import { PhenologyComparisonChart } from "./PhenologyComparisonChart";
import type { MonitoredPlot } from "@/types/field-monitor";

interface PlotDetailDrawerProps {
  plot: MonitoredPlot | null;
  onClose: () => void;
}

/** Side panel showing farmer info, compliance badge, and SAR comparison chart. */
export function PlotDetailDrawer({ plot, onClose }: PlotDetailDrawerProps) {
  const { t } = useLanguage();

  if (!plot) return null;

  const statusColor = COMPLIANCE_COLORS[plot.compliance.status] ?? "#888";

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div
        className="absolute inset-0 bg-black/40"
        onClick={onClose}
        aria-hidden="true"
      />
      <div className="relative w-full max-w-md bg-surface-elevated border-l border-border overflow-y-auto animate-slide-in-right">
        <div className="p-6 space-y-6">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div>
              <h3 className="font-display text-xl text-text-primary">
                {plot.farmer_name}
              </h3>
              <p className="text-xs text-text-tertiary mt-1">
                {plot.plot_id} &middot; {plot.area_ha} ha
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-surface-subtle text-text-tertiary"
              aria-label="Close"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          {/* Compliance badge */}
          <div className="flex items-center gap-3 p-4 rounded-lg border border-border">
            <div
              className="w-3 h-3 rounded-full flex-shrink-0"
              style={{ backgroundColor: statusColor }}
            />
            <div className="flex-1">
              <div className="text-sm font-medium text-text-primary capitalize">
                {t(`fieldMonitor.${plot.compliance.status}`)}
              </div>
              <div className="text-xs text-text-tertiary">
                {t("fieldMonitor.score")}:{" "}
                {(plot.compliance.score * 100).toFixed(0)}%
              </div>
            </div>
          </div>

          {/* Details grid */}
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 bg-surface-subtle rounded-lg">
              <div className="text-[10px] uppercase tracking-wide text-text-tertiary">
                {t("fieldMonitor.recommendedCrop")}
              </div>
              <div className="text-sm text-text-primary mt-1 capitalize">
                {plot.recommended_crop.replace("_", " ")}
              </div>
            </div>
            <div className="p-3 bg-surface-subtle rounded-lg">
              <div className="text-[10px] uppercase tracking-wide text-text-tertiary">
                {t("fieldMonitor.plantingDetected")}
              </div>
              <div className="text-sm text-text-primary mt-1">
                {plot.compliance.planting_detected ? "Yes" : "No"}
              </div>
            </div>
            <div className="p-3 bg-surface-subtle rounded-lg">
              <div className="text-[10px] uppercase tracking-wide text-text-tertiary">
                {t("fieldMonitor.cropMatch")}
              </div>
              <div className="text-sm text-text-primary mt-1">
                {plot.compliance.crop_match ? "Yes" : "No"}
              </div>
            </div>
            <div className="p-3 bg-surface-subtle rounded-lg">
              <div className="text-[10px] uppercase tracking-wide text-text-tertiary">
                {t("fieldMonitor.phenologyMatch")}
              </div>
              <div className="text-sm text-text-primary mt-1">
                {(plot.compliance.phenology_match * 100).toFixed(0)}%
              </div>
            </div>
          </div>

          {/* SAR vs expected chart */}
          <div>
            <h4 className="text-sm font-medium text-text-primary mb-3">
              {t("fieldMonitor.sarComparison")}
            </h4>
            <PhenologyComparisonChart observations={plot.observations} />
          </div>

          {/* Alerts for this plot */}
          {plot.alerts.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-text-primary mb-3">
                {t("fieldMonitor.plotAlerts")} ({plot.alerts.length})
              </h4>
              <div className="space-y-2">
                {plot.alerts.map((alert) => (
                  <div
                    key={alert.alert_id}
                    className="p-3 rounded-lg border border-border text-xs"
                  >
                    <span className="font-medium text-text-primary capitalize">
                      {alert.alert_type.replace("_", " ")}
                    </span>
                    <span className="text-text-tertiary ml-2">
                      {alert.severity}
                    </span>
                    <p className="text-text-secondary mt-1">{alert.message}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
