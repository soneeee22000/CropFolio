/** Compliance status of a monitored plot. */
export type ComplianceStatus = "compliant" | "warning" | "deviation";

/** Alert severity level. */
export type AlertSeverity = "low" | "medium" | "high" | "critical";

/** Geographic location of a plot. */
export interface PlotLocation {
  latitude: number;
  longitude: number;
}

/** A single SAR observation for a plot. */
export interface PlotObservation {
  date: string;
  observed_vh_db: number;
  expected_vh_db: number;
}

/** Compliance scoring breakdown. */
export interface ComplianceInfo {
  status: ComplianceStatus;
  score: number;
  planting_detected: boolean;
  crop_match: boolean;
  phenology_match: number;
}

/** An alert from a plot deviation. */
export interface PlotAlert {
  alert_id: string;
  plot_id: string;
  farmer_name: string;
  alert_type: string;
  severity: AlertSeverity;
  message: string;
  created_date: string;
}

/** A single monitored plot with full details. */
export interface MonitoredPlot {
  plot_id: string;
  farmer_name: string;
  location: PlotLocation;
  area_ha: number;
  recommended_crop: string;
  compliance: ComplianceInfo;
  observations: PlotObservation[];
  alerts: PlotAlert[];
}

/** Full monitoring summary for a township. */
export interface FieldMonitorSummary {
  township_id: string;
  season: string;
  year: number;
  total_plots: number;
  compliant_count: number;
  warning_count: number;
  deviation_count: number;
  compliance_rate: number;
  total_area_ha: number;
  active_alerts: number;
  plots: MonitoredPlot[];
  alerts: PlotAlert[];
}

/** Request to monitor a township. */
export interface FieldMonitorRequest {
  township_id: string;
  season?: "monsoon" | "dry";
  year?: number;
}
