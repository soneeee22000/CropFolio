"""Markowitz portfolio optimization engine for crop allocation.

Applies Modern Portfolio Theory to find the optimal crop mix that
maximizes expected income while minimizing climate-adjusted risk.

LIMITATION: The covariance matrix is estimated from heuristic crop
tolerance profiles, not actual historical return data. This is a
proof-of-concept implementation. Production use requires real
FAO/WFP time series data for correlation estimation.
"""

import logging
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

from app.core.constants import (
    MAX_CROP_WEIGHT,
    MIN_CROP_WEIGHT,
    RISK_FREE_RATE,
)
from app.domain.crops import CropProfile

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OptimizationResult:
    """Result of portfolio optimization."""

    weights: dict[str, float]
    expected_income_per_ha: float
    income_std_dev: float
    sharpe_ratio: float
    risk_reduction_pct: float


def compute_expected_returns(
    crops: list[CropProfile],
    drought_prob: float,
    flood_prob: float,
) -> NDArray[np.float64]:
    """Compute climate-adjusted expected returns (income/ha) for each crop.

    Adjusts raw expected income based on climate risk probabilities
    and each crop's tolerance levels.
    """
    returns = []
    for crop in crops:
        base_income = crop.avg_yield_kg_per_ha * crop.avg_price_mmk_per_kg

        drought_loss = drought_prob * (1 - crop.drought_tolerance)
        flood_loss = flood_prob * (1 - crop.flood_tolerance)
        climate_adjustment = 1 - drought_loss - flood_loss

        adjusted_income = base_income * max(climate_adjustment, 0.1)
        returns.append(adjusted_income)

    return np.array(returns, dtype=np.float64)


def compute_covariance_matrix(
    crops: list[CropProfile],
) -> NDArray[np.float64]:
    """Build covariance matrix from crop yield and price variances.

    LIMITATION: This uses heuristic correlations estimated from drought/flood
    tolerance profiles, NOT actual historical return data. The variance formula
    assumes yield and price are independent (drops the Var(Y)*Var(P) cross term).
    Risk estimates are directionally correct but systematically overstated.
    A production version should use actual FAO/WFP time series data.
    """
    n = len(crops)
    cov_matrix = np.zeros((n, n), dtype=np.float64)

    for i, crop_i in enumerate(crops):
        income_i = crop_i.avg_yield_kg_per_ha * crop_i.avg_price_mmk_per_kg
        var_i = (crop_i.yield_variance + crop_i.price_variance) * income_i**2

        for j, crop_j in enumerate(crops):
            income_j = crop_j.avg_yield_kg_per_ha * crop_j.avg_price_mmk_per_kg
            var_j = (crop_j.yield_variance + crop_j.price_variance) * income_j**2

            if i == j:
                cov_matrix[i][j] = var_i
            else:
                correlation = _estimate_correlation(crop_i, crop_j)
                cov_matrix[i][j] = correlation * np.sqrt(var_i * var_j)

    # Ensure positive semi-definiteness (heuristic correlations can violate this)
    eigvals = np.linalg.eigvalsh(cov_matrix)
    if eigvals.min() < 0:
        cov_matrix += (-eigvals.min() + 1e-8) * np.eye(n)

    return cov_matrix


def _estimate_correlation(crop_a: CropProfile, crop_b: CropProfile) -> float:
    """Estimate correlation between two crops based on climate tolerance profiles.

    Crops with opposite climate tolerances (one drought-tolerant, one flood-tolerant)
    tend to have negatively correlated yields under climate stress.
    """
    drought_diff = abs(crop_a.drought_tolerance - crop_b.drought_tolerance)
    flood_diff = abs(crop_a.flood_tolerance - crop_b.flood_tolerance)

    same_category = crop_a.category == crop_b.category
    same_season = crop_a.growing_season == crop_b.growing_season

    base_correlation = 0.3 if same_category else 0.1
    if same_season:
        base_correlation += 0.1

    tolerance_divergence = (drought_diff + flood_diff) / 2
    correlation = base_correlation - tolerance_divergence * 0.8

    return max(min(correlation, 0.9), -0.7)


def optimize_portfolio(
    crops: list[CropProfile],
    drought_prob: float,
    flood_prob: float,
    risk_tolerance: float = 0.5,
) -> OptimizationResult:
    """Find the optimal crop allocation using Markowitz optimization.

    Args:
        crops: List of crop profiles to optimize across.
        drought_prob: Probability of drought (0-1).
        flood_prob: Probability of flood (0-1).
        risk_tolerance: 0 = minimum risk, 1 = maximum return.

    Returns:
        OptimizationResult with optimal weights and metrics.
    """
    n = len(crops)
    expected_returns = compute_expected_returns(crops, drought_prob, flood_prob)
    cov_matrix = compute_covariance_matrix(crops)

    def objective(weights: NDArray[np.float64]) -> float:
        """Minimize negative risk-adjusted return."""
        portfolio_return = float(np.dot(weights, expected_returns))
        portfolio_variance = float(weights @ cov_matrix @ weights)
        portfolio_std = np.sqrt(portfolio_variance)

        risk_weight = 1 - risk_tolerance
        return_weight = risk_tolerance

        return -(return_weight * portfolio_return - risk_weight * portfolio_std)

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
    bounds = [(MIN_CROP_WEIGHT, MAX_CROP_WEIGHT)] * n
    initial_weights = np.ones(n) / n

    result = minimize(
        objective,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000, "ftol": 1e-10},
    )

    if not result.success:
        logger.warning("Optimizer did not converge: %s", result.message)

    optimal_weights = result.x
    optimal_weights = np.maximum(optimal_weights, 0)
    optimal_weights /= optimal_weights.sum()

    portfolio_return = float(np.dot(optimal_weights, expected_returns))
    portfolio_std = float(
        np.sqrt(optimal_weights @ cov_matrix @ optimal_weights)
    )
    sharpe = (
        (portfolio_return - RISK_FREE_RATE) / portfolio_std
        if portfolio_std > 0
        else 0.0
    )

    monocrop_stds = [
        float(np.sqrt(cov_matrix[i][i])) for i in range(n)
    ]
    monocrop_avg_std = float(np.mean(monocrop_stds))
    risk_reduction = (
        (monocrop_avg_std - portfolio_std) / monocrop_avg_std * 100
        if monocrop_avg_std > 0
        else 0.0
    )

    raw_weights = {
        crop.id: round(float(w), 4)
        for crop, w in zip(crops, optimal_weights, strict=False)
    }

    # Adjust largest weight to ensure exact sum of 1.0 after rounding
    weight_sum = sum(raw_weights.values())
    max_crop = max(raw_weights, key=raw_weights.get)  # type: ignore[arg-type]
    raw_weights[max_crop] += round(1.0 - weight_sum, 4)
    weights_dict = raw_weights

    return OptimizationResult(
        weights=weights_dict,
        expected_income_per_ha=round(portfolio_return, 2),
        income_std_dev=round(portfolio_std, 2),
        sharpe_ratio=round(sharpe, 4),
        risk_reduction_pct=round(risk_reduction, 2),
    )
