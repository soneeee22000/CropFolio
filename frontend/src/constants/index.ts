/** Crop-specific colors for charts. */
export const CROP_COLORS: Record<string, string> = {
  rice: "#22c55e",
  black_gram: "#f59e0b",
  green_gram: "#06b6d4",
  chickpea: "#8b5cf6",
  sesame: "#ef4444",
  groundnut: "#ec4899",
};

/** Risk level color mapping. */
export const RISK_LEVEL_COLORS: Record<string, string> = {
  low: "#22c55e",
  moderate: "#f59e0b",
  high: "#ef4444",
  critical: "#991b1b",
};

/** Risk level background colors for badges. */
export const RISK_LEVEL_BG: Record<string, string> = {
  low: "bg-green-100 text-green-800",
  moderate: "bg-yellow-100 text-yellow-800",
  high: "bg-red-100 text-red-800",
  critical: "bg-red-200 text-red-900",
};

/** Chart animation durations in milliseconds. */
export const ANIMATION_DURATION_MS = 800;
export const STAGGER_DELAY_MS = 20;

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
  "Select Township",
  "Climate Risk",
  "Optimize Portfolio",
  "Monte Carlo",
] as const;
