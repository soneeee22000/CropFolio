import { RISK_LEVEL_BG } from "@/constants";

interface BadgeProps {
  label: string;
  variant?: "success" | "warning" | "danger" | "info";
  riskLevel?: string;
}

const VARIANT_CLASSES: Record<string, string> = {
  success: "border-primary/30 text-primary",
  warning: "border-warning/30 text-warning",
  danger: "border-danger/30 text-danger",
  info: "border-border text-text-secondary",
};

/** Minimal badge with border-only default style. */
export function Badge({ label, variant, riskLevel }: BadgeProps) {
  const classes = riskLevel
    ? (RISK_LEVEL_BG[riskLevel] ?? VARIANT_CLASSES.info)
    : VARIANT_CLASSES[variant ?? "info"];

  return (
    <span
      className={`inline-block px-2.5 py-0.5 rounded-full text-[11px] font-medium border ${classes}`}
    >
      {label}
    </span>
  );
}
