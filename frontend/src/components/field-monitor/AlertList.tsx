import { useLanguage } from "@/i18n/LanguageContext";
import type { PlotAlert, AlertSeverity } from "@/types/field-monitor";

const SEVERITY_STYLES: Record<AlertSeverity, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300",
  medium:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  low: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
};

interface AlertListProps {
  alerts: PlotAlert[];
  onSelectPlot?: (plotId: string) => void;
  selectedSeverity: string;
  onSeverityChange: (severity: string) => void;
}

/** Scrollable alert list with severity badges. */
export function AlertList({
  alerts,
  onSelectPlot,
  selectedSeverity,
  onSeverityChange,
}: AlertListProps) {
  const { t } = useLanguage();

  const filtered =
    selectedSeverity === "all"
      ? alerts
      : alerts.filter((a) => a.severity === selectedSeverity);

  return (
    <div>
      <div className="flex gap-2 mb-4 flex-wrap">
        {["all", "critical", "high", "medium", "low"].map((sev) => (
          <button
            key={sev}
            onClick={() => onSeverityChange(sev)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
              selectedSeverity === sev
                ? "border-primary bg-primary/10 text-primary"
                : "border-border text-text-secondary hover:text-text-primary"
            }`}
          >
            {sev === "all" ? t("fieldMonitor.allAlerts") : sev}
          </button>
        ))}
      </div>

      <div className="max-h-80 overflow-y-auto space-y-2 pr-1">
        {filtered.length === 0 && (
          <p className="text-sm text-text-tertiary text-center py-6">
            {t("fieldMonitor.noAlerts")}
          </p>
        )}
        {filtered.map((alert) => (
          <button
            key={alert.alert_id}
            onClick={() => onSelectPlot?.(alert.plot_id)}
            className="w-full text-left p-3 rounded-lg border border-border hover:bg-surface-subtle transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-medium text-text-primary">
                {alert.farmer_name}
              </span>
              <span
                className={`text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium ${
                  SEVERITY_STYLES[alert.severity]
                }`}
              >
                {alert.severity}
              </span>
            </div>
            <p className="text-xs text-text-secondary">{alert.message}</p>
            <div className="text-[10px] text-text-tertiary mt-1">
              {alert.plot_id} &middot; {alert.created_date}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
