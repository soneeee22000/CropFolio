"""Helper to compute price statistics from WFP price CSVs.

Usage:
    cd backend
    python -m scripts.update_crop_prices
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "wfp_prices"

MIN_DATA_POINTS = 3


def main() -> None:
    """Scan CSVs and print price statistics."""
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {DATA_DIR}")
        sys.exit(1)

    print(f"\n{'Crop':<15} {'Mean (MMK/kg)':>14} {'Std':>10} {'CV':>8} {'Points':>8}")
    print("-" * 60)

    for csv_path in csv_files:
        crop_id = csv_path.stem
        prices: list[float] = []
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                prices.append(float(row["price_mmk_per_kg"]))

        if len(prices) < MIN_DATA_POINTS:
            print(f"{crop_id:<15} {'INSUFFICIENT DATA':>14} {'':>10} {'':>8} {len(prices):>8}")
            continue

        arr = np.array(prices)
        mean_val = float(np.mean(arr))
        std_val = float(np.std(arr, ddof=1))
        cv_val = std_val / mean_val if mean_val > 0 else 0.0

        print(f"{crop_id:<15} {mean_val:>14,.2f} {std_val:>10,.2f} {cv_val:>8.4f} {len(prices):>8}")

    print("\n# Ready-to-paste for crops.py:")
    print("# avg_price_mmk_per_kg=<mean>, price_variance=<cv**2>,")
    print('# price_data_source="WFP VAM + Field collection March 2026"')
    print('# data_confidence="medium"')


if __name__ == "__main__":
    main()
