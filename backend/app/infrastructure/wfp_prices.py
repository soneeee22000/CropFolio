"""WFP price data loader for Myanmar crop price histories."""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "wfp_prices"


@dataclass(frozen=True)
class PriceRecord:
    """A single price observation from WFP market data."""

    date: str
    price_mmk_per_kg: float
    market: str


def load_price_history(crop_id: str) -> list[PriceRecord] | None:
    """Load historical price data for a crop from CSV.

    Args:
        crop_id: Crop identifier matching CSV filename (e.g. 'rice').

    Returns:
        List of PriceRecord, or None if file not found.
    """
    csv_path = DATA_DIR / f"{crop_id}.csv"
    if not csv_path.exists():
        logger.warning("Price CSV not found: %s", csv_path)
        return None

    records: list[PriceRecord] = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(
                PriceRecord(
                    date=row["date"],
                    price_mmk_per_kg=float(row["price_mmk_per_kg"]),
                    market=row["market"],
                )
            )
    return records


def compute_price_statistics(records: list[PriceRecord]) -> dict[str, float]:
    """Compute summary statistics from price records.

    Args:
        records: Non-empty list of PriceRecord.

    Returns:
        Dict with mean, std, min, max, and cv (coefficient of variation).
    """
    prices = [r.price_mmk_per_kg for r in records]
    n = len(prices)
    mean = sum(prices) / n
    variance = sum((p - mean) ** 2 for p in prices) / n
    std = variance ** 0.5
    cv = std / mean if mean > 0 else 0.0

    return {
        "mean": round(mean, 2),
        "std": round(std, 2),
        "min": round(min(prices), 2),
        "max": round(max(prices), 2),
        "cv": round(cv, 4),
    }
