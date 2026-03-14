import { RISK_LEVEL_BG } from "@/constants";

interface BadgeProps {
  label: string;
  variant?: "success" | "warning" | "danger" | "info";
  /** Use risk level string to auto-select variant. */
  riskLevel?: string;
}

const VARIANT_CLASSES: Record<string, string> = {
  success: "bg-green-100 text-green-800",
  warning: "bg-yellow-100 text-yellow-800",
  danger: "bg-red-100 text-red-800",
  info: "bg-blue-100 text-blue-800",
};

/** Small colored tag for status labels. */
export function Badge({ label, variant, riskLevel }: BadgeProps) {
  const classes = riskLevel
    ? (RISK_LEVEL_BG[riskLevel] ?? VARIANT_CLASSES.info)
    : VARIANT_CLASSES[variant ?? "info"];

  return (
    <span
      className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-medium ${classes}`}
    >
      {label}
    </span>
  );
}
