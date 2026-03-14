/** Format a number as Myanmar Kyat currency. */
export function formatMMK(value: number): string {
  return `${Math.round(value).toLocaleString()} MMK`;
}

/** Format a number as compact currency (e.g., 2.3M MMK). */
export function formatMMKCompact(value: number): string {
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(1)}M MMK`;
  }
  if (value >= 1_000) {
    return `${(value / 1_000).toFixed(0)}K MMK`;
  }
  return `${Math.round(value)} MMK`;
}

/** Format a decimal as percentage string. */
export function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

/** Format a number with specified decimal places. */
export function formatNumber(value: number, decimals: number = 0): string {
  return value.toLocaleString(undefined, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}
