"""Monte Carlo simulation engine for crop portfolio risk analysis.

Simulates thousands of possible climate scenarios to show the
income distribution for a given crop portfolio allocation.

Supports two distribution models:
- "normal": Classic multivariate normal (fast, textbook)
- "copula": Copula-based with fat-tail dependence (production-grade)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from app.core.constants import (
    CATASTROPHIC_LOSS_THRESHOLD,
    DEFAULT_NUM_SIMULATIONS,
    STANDARD_DEVIATION_CAP,
)
from app.domain.crops import CropProfile
from app.domain.optimizer import compute_covariance_matrix, compute_expected_returns

logger = logging.getLogger(__name__)

DistributionModel = Literal["normal", "copula"]


@dataclass(frozen=True)
class SimulationResult:
    """Result of Monte Carlo simulation for a portfolio."""

    incomes: list[float]
    mean_income: float
    median_income: float
    std_dev: float
    percentile_5: float
    percentile_95: float
    prob_catastrophic_loss: float
    value_at_risk_95: float
    distribution_model: str = "normal"


def run_monte_carlo(
    crops: list[CropProfile],
    weights: dict[str, float],
    drought_prob: float,
    flood_prob: float,
    num_simulations: int = DEFAULT_NUM_SIMULATIONS,
    seed: int | None = None,
    distribution_model: DistributionModel = "normal",
) -> SimulationResult:
    """Run Monte Carlo simulation for a crop portfolio.

    Generates num_simulations climate scenarios using either multivariate
    normal or copula-based distribution, then computes portfolio income
    for each scenario.

    Args:
        crops: List of crop profiles in the portfolio.
        weights: Dict mapping crop_id to allocation weight (0-1).
        drought_prob: Probability of drought for the region.
        flood_prob: Probability of flood for the region.
        num_simulations: Number of scenarios to simulate.
        seed: Random seed for reproducibility.
        distribution_model: "normal" for classic MVN, "copula" for tail risk.

    Returns:
        SimulationResult with income distribution statistics.
    """
    rng = np.random.default_rng(seed)

    weight_array = np.array(
        [weights.get(crop.id, 0.0) for crop in crops],
        dtype=np.float64,
    )

    expected_returns = compute_expected_returns(crops, drought_prob, flood_prob)
    cov_matrix = compute_covariance_matrix(crops)

    if distribution_model == "copula":
        from app.domain.copula_risk import sample_correlated_scenarios

        raw_scenarios = sample_correlated_scenarios(
            crops=crops,
            expected_returns=expected_returns,
            cov_matrix=cov_matrix,
            drought_prob=drought_prob,
            num_simulations=num_simulations,
            seed=seed,
        )
        logger.info("Copula simulation completed: %d scenarios", num_simulations)
    else:
        raw_scenarios = rng.multivariate_normal(
            expected_returns, cov_matrix, size=num_simulations
        )
        raw_scenarios = _cap_outliers(raw_scenarios, expected_returns, cov_matrix)

    raw_scenarios = np.maximum(raw_scenarios, 0)

    portfolio_incomes: NDArray[np.float64] = raw_scenarios @ weight_array

    mean_income = float(np.mean(portfolio_incomes))
    expected_income = float(np.dot(weight_array, expected_returns))
    loss_threshold = expected_income * (1 - CATASTROPHIC_LOSS_THRESHOLD)
    prob_catastrophic = float(
        np.mean(portfolio_incomes < loss_threshold)
    )

    percentile_5 = float(np.percentile(portfolio_incomes, 5))
    value_at_risk = expected_income - percentile_5

    return SimulationResult(
        incomes=portfolio_incomes.tolist(),
        mean_income=round(mean_income, 2),
        median_income=round(float(np.median(portfolio_incomes)), 2),
        std_dev=round(float(np.std(portfolio_incomes)), 2),
        percentile_5=round(percentile_5, 2),
        percentile_95=round(float(np.percentile(portfolio_incomes, 95)), 2),
        prob_catastrophic_loss=round(prob_catastrophic, 4),
        value_at_risk_95=round(value_at_risk, 2),
        distribution_model=distribution_model,
    )


def _cap_outliers(
    scenarios: NDArray[np.float64],
    means: NDArray[np.float64],
    cov_matrix: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Cap simulation outliers at ±N standard deviations."""
    stds = np.sqrt(np.diag(cov_matrix))

    lower = means - STANDARD_DEVIATION_CAP * stds
    upper = means + STANDARD_DEVIATION_CAP * stds

    return np.clip(scenarios, lower, upper)
