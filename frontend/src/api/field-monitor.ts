import { apiGet, apiPost } from "./client";
import type {
  FieldMonitorRequest,
  FieldMonitorSummary,
  MonitoredPlot,
  PlotAlert,
} from "@/types/field-monitor";

/** Fetch field monitoring summary for a township. */
export function fetchFieldMonitor(
  request: FieldMonitorRequest,
): Promise<FieldMonitorSummary> {
  return apiPost<FieldMonitorSummary, FieldMonitorRequest>(
    "/field-monitor/monitor",
    request,
  );
}

/** Fetch detailed data for a specific plot. */
export function fetchPlotDetail(
  townshipId: string,
  plotId: string,
): Promise<MonitoredPlot> {
  const path = `/field-monitor/plot/${encodeURIComponent(townshipId)}/${encodeURIComponent(plotId)}`;
  return apiGet<MonitoredPlot>(path);
}

/** Fetch alerts for a township, optionally filtered by severity. */
export function fetchAlerts(
  townshipId: string,
  severity?: string,
): Promise<PlotAlert[]> {
  const base = `/field-monitor/alerts/${encodeURIComponent(townshipId)}`;
  if (severity) {
    const params = new URLSearchParams({ severity });
    return apiGet<PlotAlert[]>(`${base}?${params.toString()}`);
  }
  return apiGet<PlotAlert[]>(base);
}
