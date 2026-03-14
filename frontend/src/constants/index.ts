/** Crop-specific colors — muted, same saturation band. */
export const CROP_COLORS: Record<string, string> = {
  rice: "#3A8F5C",
  black_gram: "#C4923A",
  green_gram: "#4A8B9E",
  chickpea: "#7B6BA5",
  sesame: "#B85A5A",
  groundnut: "#A67B5B",
};

/** Risk level color mapping. */
export const RISK_LEVEL_COLORS: Record<string, string> = {
  low: "#1B7A4A",
  moderate: "#D4940A",
  high: "#C43B3B",
  critical: "#8B1A1A",
};

/** Risk level background colors for badges. */
export const RISK_LEVEL_BG: Record<string, string> = {
  low: "bg-primary-subtle text-primary-dark",
  moderate: "bg-amber-50 text-amber-800",
  high: "bg-danger-subtle text-danger",
  critical: "bg-red-100 text-red-900",
};

/** Chart animation durations in milliseconds. */
export const ANIMATION_DURATION_MS = 1000;
export const STAGGER_DELAY_MS = 30;

/** Monte Carlo defaults. */
export const DEFAULT_NUM_SIMULATIONS = 1000;
export const MIN_SIMULATIONS = 500;
export const MAX_SIMULATIONS = 5000;

/** Portfolio optimization defaults. */
export const DEFAULT_RISK_TOLERANCE = 0.5;
export const MIN_CROPS_FOR_OPTIMIZATION = 2;

/** Histogram bins (matches backend). */
export const HISTOGRAM_NUM_BINS = 25;

/** Step labels for the wizard. */
export const STEP_LABELS = [
  "Township",
  "Climate Risk",
  "Portfolio",
  "Simulation",
] as const;
