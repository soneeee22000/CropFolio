import { CROP_COLORS, RISK_LEVEL_COLORS } from "@/constants";

/** Get the chart color for a crop by ID. */
export function getCropColor(cropId: string): string {
  return CROP_COLORS[cropId] ?? "#94a3b8";
}

/** Get the color for a risk level string. */
export function getRiskColor(riskLevel: string): string {
  return RISK_LEVEL_COLORS[riskLevel] ?? "#94a3b8";
}
