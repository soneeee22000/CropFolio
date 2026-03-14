"""WFP price correlation and statistics computation for Myanmar crops.

Loads monthly price CSVs from data/wfp_prices/, computes month-over-month
price returns, and derives pairwise Pearson correlations and per-crop
statistics (mean, std, CV).

Source: WFP VAM Food Prices Myanmar (data.humdata.org),
        WFP Market Price Bulletins 2022-2025.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "wfp_prices"

CROP_IDS = ("rice", "black_gram", "green_gram", "chickpea", "sesame", "groundnut")


def _load_prices(crop_id: str) -> NDArray[np.float64]:
    """Load monthly price series from CSV.

    Args:
        crop_id: Crop identifier matching the CSV filename.

    Returns:
        Array of monthly prices in MMK/kg.
    """
    csv_path = DATA_DIR / f"{crop_id}.csv"
    prices: list[float] = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prices.append(float(row["price_mmk_per_kg"]))
    return np.array(prices, dtype=np.float64)


def _compute_monthly_returns(prices: NDArray[np.float64]) -> NDArray[np.float64]:
    """Compute month-over-month percentage price changes.

    Args:
        prices: Array of monthly price values.

    Returns:
        Array of (n-1) return values.
    """
    return np.diff(prices) / prices[:-1]


def compute_price_correlations() -> dict[tuple[str, str], float]:
    """Compute pairwise Pearson correlations of monthly price returns.

    Returns:
        Dict mapping (crop_a, crop_b) -> correlation coefficient.
    """
    returns_map: dict[str, NDArray[np.float64]] = {}
    for crop_id in CROP_IDS:
        prices = _load_prices(crop_id)
        returns_map[crop_id] = _compute_monthly_returns(prices)

    correlations: dict[tuple[str, str], float] = {}
    for crop_a in CROP_IDS:
        for crop_b in CROP_IDS:
            ret_a = returns_map[crop_a]
            ret_b = returns_map[crop_b]

            min_len = min(len(ret_a), len(ret_b))
            aligned_a = ret_a[-min_len:]
            aligned_b = ret_b[-min_len:]

            corr_matrix = np.corrcoef(aligned_a, aligned_b)
            corr_val = float(corr_matrix[0, 1])
            corr_val = max(min(corr_val, 1.0), -1.0)

            correlations[(crop_a, crop_b)] = corr_val

    return correlations


def compute_price_statistics() -> dict[str, dict[str, float]]:
    """Compute summary statistics for each crop's price series.

    Returns:
        Dict mapping crop_id -> {mean, std, cv, min, max}.
    """
    stats: dict[str, dict[str, float]] = {}
    for crop_id in CROP_IDS:
        prices = _load_prices(crop_id)
        mean_val = float(np.mean(prices))
        std_val = float(np.std(prices, ddof=1))
        cv_val = std_val / mean_val if mean_val > 0 else 0.0

        stats[crop_id] = {
            "mean": round(mean_val, 2),
            "std": round(std_val, 2),
            "cv": round(cv_val, 4),
            "min": round(float(np.min(prices)), 2),
            "max": round(float(np.max(prices)), 2),
        }
    return stats


# Pre-computed at module load for use by the optimizer.
PRICE_CORRELATIONS: dict[tuple[str, str], float] = compute_price_correlations()
PRICE_STATISTICS: dict[str, dict[str, float]] = compute_price_statistics()
