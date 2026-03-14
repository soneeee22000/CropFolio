"""Portfolio optimization and simulation service."""

from __future__ import annotations

import asyncio
import logging
from functools import lru_cache

import numpy as np

from app.domain.crops import CropProfile, get_crop_by_id
from app.domain.optimizer import compute_expected_returns, optimize_portfolio
from app.domain.results import (
    ClimateRiskSummaryResult,
    CropWeightResult,
    HistogramBinResult,
    PortfolioMetricsResult,
    PortfolioResult,
    SimStatsResult,
    SimulationServiceResult,
)
from app.domain.simulator import run_monte_carlo
from app.services.climate_service import ClimateService, get_climate_service
from app.services.township_service import TownshipService, get_township_service

logger = logging.getLogger(__name__)

HISTOGRAM_NUM_BINS = 25


class PortfolioService:
    """Orchestrates portfolio optimization and Monte Carlo simulation."""

    def __init__(
        self,
        climate_service: ClimateService | None = None,
        township_service: TownshipService | None = None,
    ) -> None:
        """Initialize with dependencies."""
        self._climate = climate_service or get_climate_service()
        self._townships = township_service or get_township_service()

    async def optimize(
        self,
        crop_ids: list[str],
        township_id: str,
        risk_tolerance: float,
        season: str,
    ) -> PortfolioResult | None:
        """Run portfolio optimization for given crops and township.

        Returns None if township not found.
        Raises ValueError if any crop_id is invalid.
        """
        crops = self._resolve_crops(crop_ids)
        township = self._townships.get_by_id(township_id)
        if township is None:
            return None

        climate_result = await self._climate.assess_risk(township_id, season)
        if climate_result is None:
            return None
        risk_profile, data_source = climate_result

        result = await asyncio.to_thread(
            optimize_portfolio,
            crops,
            risk_profile.drought_probability,
            risk_profile.flood_probability,
            risk_tolerance,
        )

        expected_returns = compute_expected_returns(
            crops,
            risk_profile.drought_probability,
            risk_profile.flood_probability,
        )

        crop_weights = [
            CropWeightResult(
                crop_id=crop.id,
                crop_name=crop.name_en,
                crop_name_mm=crop.name_mm,
                weight=result.weights[crop.id],
                expected_income_per_ha=round(
                    float(expected_returns[i]) * result.weights[crop.id], 2
                ),
            )
            for i, crop in enumerate(crops)
        ]

        return PortfolioResult(
            township_id=township_id,
            township_name=township["name"],
            season=season,
            crop_weights=crop_weights,
            metrics=PortfolioMetricsResult(
                expected_income_per_ha=result.expected_income_per_ha,
                income_std_dev=result.income_std_dev,
                sharpe_ratio=result.sharpe_ratio,
                risk_reduction_pct=result.risk_reduction_pct,
            ),
            climate_risk=ClimateRiskSummaryResult(
                drought_probability=risk_profile.drought_probability,
                flood_probability=risk_profile.flood_probability,
                risk_level=risk_profile.risk_level,
                data_source=data_source,
            ),
        )

    async def simulate(
        self,
        crop_ids: list[str],
        weights: dict[str, float],
        township_id: str,
        num_simulations: int,
        season: str,
    ) -> SimulationServiceResult | None:
        """Run Monte Carlo simulation for a crop portfolio.

        Returns None if township not found.
        Raises ValueError if any crop_id is invalid.
        """
        crops = self._resolve_crops(crop_ids)
        township = self._townships.get_by_id(township_id)
        if township is None:
            return None

        climate_result = await self._climate.assess_risk(township_id, season)
        if climate_result is None:
            return None
        risk_profile, _ = climate_result

        result = await asyncio.to_thread(
            run_monte_carlo,
            crops,
            weights,
            risk_profile.drought_probability,
            risk_profile.flood_probability,
            num_simulations,
        )

        histogram = _build_histogram(result.incomes, HISTOGRAM_NUM_BINS)

        return SimulationServiceResult(
            township_id=township_id,
            township_name=township["name"],
            season=season,
            num_simulations=num_simulations,
            stats=SimStatsResult(
                mean_income=result.mean_income,
                median_income=result.median_income,
                std_dev=result.std_dev,
                percentile_5=result.percentile_5,
                percentile_95=result.percentile_95,
                prob_catastrophic_loss=result.prob_catastrophic_loss,
                value_at_risk_95=result.value_at_risk_95,
            ),
            histogram=histogram,
        )

    async def compare_townships(
        self,
        township_ids: list[str],
        crop_ids: list[str],
        risk_tolerance: float,
        season: str,
    ) -> list[PortfolioResult | None]:
        """Run optimization for multiple townships concurrently.

        Args:
            township_ids: List of township IDs to compare.
            crop_ids: Crops to include in each optimization.
            risk_tolerance: Risk tolerance parameter (0-1).
            season: Growing season (monsoon/dry).

        Returns:
            List of optimization results (None for missing townships).
        """
        tasks = [
            self.optimize(crop_ids, tid, risk_tolerance, season)
            for tid in township_ids
        ]
        results: list[PortfolioResult | None] = await asyncio.gather(*tasks)
        return results

    def _resolve_crops(self, crop_ids: list[str]) -> list[CropProfile]:
        """Resolve crop IDs to CropProfile objects."""
        crops: list[CropProfile] = []
        for cid in crop_ids:
            crop = get_crop_by_id(cid)
            if crop is None:
                msg = f"Unknown crop: '{cid}'"
                raise ValueError(msg)
            crops.append(crop)
        return crops


def _build_histogram(
    incomes: list[float], num_bins: int
) -> list[HistogramBinResult]:
    """Bin income values into a histogram for chart rendering."""
    arr = np.array(incomes)
    counts, bin_edges = np.histogram(arr, bins=num_bins)
    total = len(incomes)

    return [
        HistogramBinResult(
            bin_start=round(float(bin_edges[i]), 2),
            bin_end=round(float(bin_edges[i + 1]), 2),
            count=int(counts[i]),
            frequency=round(int(counts[i]) / total, 4),
        )
        for i in range(num_bins)
    ]


@lru_cache(maxsize=1)
def get_portfolio_service() -> PortfolioService:
    """Return singleton PortfolioService instance."""
    return PortfolioService()
