"""FAOSTAT historical yield data loader and covariance computation.

Loads Myanmar crop yield data (2010-2021) from FAOSTAT via data.un.org
and computes real yield return covariances for use in Markowitz optimization.

Source: FAOSTAT, element code 5419 (yield hg/ha), country code 28 (Myanmar).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "faostat_yields.json"

# Crop IDs in the optimizer mapped to FAOSTAT series names.
# black_gram and green_gram both use beans_dry as proxy.
CROP_TO_FAOSTAT: dict[str, str] = {
    "rice": "rice",
    "groundnut": "groundnut",
    "sesame": "sesame",
    "chickpea": "chickpea",
    "black_gram": "beans_dry",
    "green_gram": "beans_dry",
}

# beans_dry has a methodology break between 2013-2014.
# Use only 2014-2021 (index 4 onward) for that series.
BEANS_DRY_START_INDEX = 4


def _load_faostat_data() -> dict:
    """Load raw FAOSTAT yield data from JSON file.

    Returns:
        Parsed JSON dict with years and crop yield arrays.
    """
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _get_yield_series(crop_id: str, data: dict) -> NDArray[np.float64]:
    """Get the yield time series for a crop, handling beans_dry truncation.

    Args:
        crop_id: CropFolio crop identifier.
        data: Loaded FAOSTAT JSON data.

    Returns:
        Array of annual yields in tonnes/hectare.
    """
    faostat_name = CROP_TO_FAOSTAT.get(crop_id)
    if faostat_name is None:
        raise KeyError(f"No FAOSTAT mapping for crop: {crop_id}")

    series = np.array(data["crops"][faostat_name], dtype=np.float64)

    if faostat_name == "beans_dry":
        series = series[BEANS_DRY_START_INDEX:]

    return series


def _compute_yield_returns(series: NDArray[np.float64]) -> NDArray[np.float64]:
    """Compute year-over-year percentage changes in yield.

    Args:
        series: Array of annual yield values.

    Returns:
        Array of (n-1) yield return values.
    """
    return np.diff(series) / series[:-1]


def compute_yield_covariance() -> dict[tuple[str, str], float]:
    """Compute pairwise yield return covariances from FAOSTAT data.

    For black_gram and green_gram (both proxied by beans_dry), adds
    small independent noise to avoid a singular covariance matrix.

    Returns:
        Dict mapping (crop_id_a, crop_id_b) -> covariance of yield returns.
    """
    data = _load_faostat_data()
    crop_ids = list(CROP_TO_FAOSTAT.keys())

    # Compute yield returns for each crop
    returns_map: dict[str, NDArray[np.float64]] = {}
    for crop_id in crop_ids:
        series = _get_yield_series(crop_id, data)
        returns_map[crop_id] = _compute_yield_returns(series)

    # For beans_dry proxies, add small noise to differentiate them
    rng = np.random.default_rng(seed=42)
    noise_scale = 0.005
    for proxy_crop in ("black_gram", "green_gram"):
        if proxy_crop in returns_map:
            noise = rng.normal(0, noise_scale, size=returns_map[proxy_crop].shape)
            returns_map[proxy_crop] = returns_map[proxy_crop] + noise

    # Build pairwise covariance dict
    # For pairs involving beans_dry crops (shorter series), use the shorter length
    covariance: dict[tuple[str, str], float] = {}
    for crop_a in crop_ids:
        for crop_b in crop_ids:
            ret_a = returns_map[crop_a]
            ret_b = returns_map[crop_b]

            # Align to shortest series (beans_dry has fewer years)
            min_len = min(len(ret_a), len(ret_b))
            aligned_a = ret_a[-min_len:]
            aligned_b = ret_b[-min_len:]

            # Use numpy cov (ddof=1 for sample covariance)
            cov_val = float(np.cov(aligned_a, aligned_b, ddof=1)[0, 1])
            covariance[(crop_a, crop_b)] = cov_val

    return covariance


def compute_yield_correlation() -> dict[tuple[str, str], float]:
    """Compute pairwise yield return correlations from FAOSTAT data.

    Returns:
        Dict mapping (crop_id_a, crop_id_b) -> Pearson correlation of yield returns.
    """
    data = _load_faostat_data()
    crop_ids = list(CROP_TO_FAOSTAT.keys())

    returns_map: dict[str, NDArray[np.float64]] = {}
    for crop_id in crop_ids:
        series = _get_yield_series(crop_id, data)
        returns_map[crop_id] = _compute_yield_returns(series)

    # Add noise to beans_dry proxies
    rng = np.random.default_rng(seed=42)
    noise_scale = 0.005
    for proxy_crop in ("black_gram", "green_gram"):
        if proxy_crop in returns_map:
            noise = rng.normal(0, noise_scale, size=returns_map[proxy_crop].shape)
            returns_map[proxy_crop] = returns_map[proxy_crop] + noise

    correlation: dict[tuple[str, str], float] = {}
    for crop_a in crop_ids:
        for crop_b in crop_ids:
            ret_a = returns_map[crop_a]
            ret_b = returns_map[crop_b]

            min_len = min(len(ret_a), len(ret_b))
            aligned_a = ret_a[-min_len:]
            aligned_b = ret_b[-min_len:]

            corr_matrix = np.corrcoef(aligned_a, aligned_b)
            corr_val = float(corr_matrix[0, 1])

            # Clamp to valid range (numerical edge cases)
            corr_val = max(min(corr_val, 1.0), -1.0)
            correlation[(crop_a, crop_b)] = corr_val

    return correlation


def get_historical_yield_stats(crop_id: str) -> dict[str, float]:
    """Get summary statistics for a crop's historical yields.

    Args:
        crop_id: CropFolio crop identifier.

    Returns:
        Dict with mean_yield_t_per_ha, std_yield, cv (coefficient of variation),
        and n_years.
    """
    data = _load_faostat_data()
    series = _get_yield_series(crop_id, data)

    mean_val = float(np.mean(series))
    std_val = float(np.std(series, ddof=1))
    cv_val = std_val / mean_val if mean_val > 0 else 0.0

    return {
        "mean_yield_t_per_ha": round(mean_val, 4),
        "std_yield": round(std_val, 4),
        "cv": round(cv_val, 4),
        "n_years": len(series),
    }


# Pre-computed at module load for use by the optimizer.
# This runs once when the module is first imported.
FAOSTAT_YIELD_CORRELATIONS: dict[tuple[str, str], float] = compute_yield_correlation()
