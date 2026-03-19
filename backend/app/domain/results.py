"""Domain result types for portfolio optimization and simulation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CropWeightResult:
    """Single crop's allocation in the optimized portfolio."""

    crop_id: str
    crop_name: str
    crop_name_mm: str
    weight: float
    expected_income_per_ha: float


@dataclass(frozen=True)
class PortfolioMetricsResult:
    """Aggregate metrics for the optimized portfolio."""

    expected_income_per_ha: float
    income_std_dev: float
    sharpe_ratio: float
    risk_reduction_pct: float


@dataclass(frozen=True)
class ClimateRiskSummaryResult:
    """Summary of climate risk used in optimization."""

    drought_probability: float
    flood_probability: float
    risk_level: str
    data_source: str


@dataclass(frozen=True)
class PortfolioResult:
    """Full result from portfolio optimization."""

    township_id: str
    township_name: str
    season: str
    crop_weights: list[CropWeightResult]
    metrics: PortfolioMetricsResult
    climate_risk: ClimateRiskSummaryResult


@dataclass(frozen=True)
class HistogramBinResult:
    """Single bin in income distribution histogram."""

    bin_start: float
    bin_end: float
    count: int
    frequency: float


@dataclass(frozen=True)
class SimStatsResult:
    """Statistical summary of Monte Carlo simulation."""

    mean_income: float
    median_income: float
    std_dev: float
    percentile_5: float
    percentile_95: float
    prob_catastrophic_loss: float
    value_at_risk_95: float


@dataclass(frozen=True)
class SimulationServiceResult:
    """Full result from Monte Carlo simulation."""

    township_id: str
    township_name: str
    season: str
    num_simulations: int
    stats: SimStatsResult
    histogram: list[HistogramBinResult]
    distribution_model: str = "normal"
