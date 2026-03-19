"""Copula-based tail risk engine for correlated crop failure modeling.

Models fat-tail climate risk using copula functions instead of naive
multivariate normal distributions. Captures tail dependence — the
tendency for multiple crops to fail simultaneously during drought events.

Key concepts:
- Marginals: KDE-fitted from FAOSTAT yield returns (captures skewness)
- Copula: Gaussian baseline + Clayton for lower tail dependence
- Clayton theta: Estimated from Kendall's tau, scaled by drought probability
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from app.core.constants import (
    CLAYTON_DROUGHT_SCALE_FACTOR,
    COPULA_MIN_OBSERVATIONS,
    DEFAULT_CLAYTON_THETA,
    GAUSSIAN_COPULA_REGULARIZATION,
)
from app.domain.crops import CropProfile
from app.infrastructure.faostat_yields import (
    CROP_TO_FAOSTAT,
    _compute_yield_returns,
    _get_yield_series,
    _load_faostat_data,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MarginalFit:
    """Fitted marginal distribution for a single crop's yield returns."""

    crop_id: str
    distribution_type: str
    mean: float
    std: float
    skewness: float
    kurtosis: float


@dataclass(frozen=True)
class CopulaConfig:
    """Configuration for copula dependence structure."""

    copula_type: str
    tail_dependence_lower: float
    tail_dependence_upper: float
    n_crops: int


@dataclass(frozen=True)
class TailRiskMetrics:
    """Tail risk metrics computed from copula-based simulation."""

    copula_type: str
    tail_dependence_lower: float
    joint_failure_prob: float
    conditional_var_95: float


def fit_marginals(
    crops: list[CropProfile],
) -> list[MarginalFit]:
    """Fit KDE-based marginal distributions from FAOSTAT yield returns.

    For each crop, computes year-over-year yield returns and fits
    distribution statistics. Uses KDE rather than parametric distributions
    to capture skewness and fat tails in historical data.

    Args:
        crops: List of crop profiles to fit marginals for.

    Returns:
        List of MarginalFit objects with distribution parameters.
    """
    data = _load_faostat_data()
    marginals: list[MarginalFit] = []

    for crop in crops:
        if crop.id not in CROP_TO_FAOSTAT:
            marginals.append(
                MarginalFit(
                    crop_id=crop.id,
                    distribution_type="normal_fallback",
                    mean=0.0,
                    std=float(np.sqrt(crop.yield_variance)),
                    skewness=0.0,
                    kurtosis=3.0,
                )
            )
            continue

        series = _get_yield_series(crop.id, data)
        returns = _compute_yield_returns(series)

        if len(returns) < COPULA_MIN_OBSERVATIONS:
            marginals.append(
                MarginalFit(
                    crop_id=crop.id,
                    distribution_type="normal_fallback",
                    mean=float(np.mean(returns)),
                    std=float(np.std(returns, ddof=1)),
                    skewness=0.0,
                    kurtosis=3.0,
                )
            )
            continue

        marginals.append(
            MarginalFit(
                crop_id=crop.id,
                distribution_type="kde",
                mean=float(np.mean(returns)),
                std=float(np.std(returns, ddof=1)),
                skewness=float(stats.skew(returns)),
                kurtosis=float(stats.kurtosis(returns, fisher=False)),
            )
        )

    return marginals


def estimate_kendall_tau(
    crops: list[CropProfile],
) -> NDArray[np.float64]:
    """Estimate Kendall's tau rank correlation matrix from yield returns.

    Kendall's tau is more robust to outliers than Pearson correlation
    and directly relates to copula parameters via the relationship:
    theta_clayton = 2 * tau / (1 - tau) for tau > 0.

    Args:
        crops: List of crop profiles.

    Returns:
        n x n matrix of pairwise Kendall's tau values.
    """
    data = _load_faostat_data()
    n = len(crops)
    tau_matrix = np.eye(n, dtype=np.float64)

    returns_list: list[NDArray[np.float64]] = []
    for crop in crops:
        if crop.id not in CROP_TO_FAOSTAT:
            returns_list.append(
                np.zeros(1, dtype=np.float64)
            )
            continue
        series = _get_yield_series(crop.id, data)
        returns_list.append(_compute_yield_returns(series))

    for i in range(n):
        for j in range(i + 1, n):
            ret_i = returns_list[i]
            ret_j = returns_list[j]

            too_few = (
                len(ret_i) < COPULA_MIN_OBSERVATIONS
                or len(ret_j) < COPULA_MIN_OBSERVATIONS
            )
            if too_few:
                tau_matrix[i, j] = 0.0
                tau_matrix[j, i] = 0.0
                continue

            min_len = min(len(ret_i), len(ret_j))
            aligned_i = ret_i[-min_len:]
            aligned_j = ret_j[-min_len:]

            tau, _ = stats.kendalltau(aligned_i, aligned_j)
            if np.isnan(tau):
                tau = 0.0

            tau_matrix[i, j] = tau
            tau_matrix[j, i] = tau

    return tau_matrix


def compute_clayton_theta(
    tau_matrix: NDArray[np.float64],
    drought_prob: float,
) -> float:
    """Compute Clayton copula theta from average Kendall's tau.

    The Clayton copula has lower tail dependence = 2^(-1/theta),
    making it ideal for modeling correlated crop failures during drought.

    Theta is scaled by drought probability: higher drought risk
    increases the tail dependence (crops fail together more under stress).

    Args:
        tau_matrix: n x n Kendall's tau matrix.
        drought_prob: Probability of drought (0-1).

    Returns:
        Clayton theta parameter (>= 0.01).
    """
    n = tau_matrix.shape[0]
    if n < 2:
        return DEFAULT_CLAYTON_THETA

    upper_triangle = tau_matrix[np.triu_indices(n, k=1)]
    avg_tau = float(np.mean(upper_triangle))

    avg_tau = max(avg_tau, 0.01)

    base_theta = 2.0 * avg_tau / (1.0 - avg_tau)

    drought_scale = 1.0 + drought_prob * CLAYTON_DROUGHT_SCALE_FACTOR
    theta = base_theta * drought_scale

    return max(theta, 0.01)


def _build_gaussian_copula_corr(
    tau_matrix: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Convert Kendall's tau matrix to Gaussian copula correlation matrix.

    Uses the relationship: rho = sin(pi/2 * tau) for the Gaussian copula.
    Ensures positive semi-definiteness via eigenvalue clamping.

    Args:
        tau_matrix: n x n Kendall's tau matrix.

    Returns:
        Positive semi-definite correlation matrix for the Gaussian copula.
    """
    n = tau_matrix.shape[0]
    rho = np.sin(np.pi / 2.0 * tau_matrix)

    np.fill_diagonal(rho, 1.0)

    rho += GAUSSIAN_COPULA_REGULARIZATION * np.eye(n)

    eigvals, eigvecs = np.linalg.eigh(rho)
    eigvals = np.maximum(eigvals, 1e-8)
    rho = eigvecs @ np.diag(eigvals) @ eigvecs.T

    d_inv = np.diag(1.0 / np.sqrt(np.diag(rho)))
    rho = d_inv @ rho @ d_inv

    return rho


def sample_correlated_scenarios(
    crops: list[CropProfile],
    expected_returns: NDArray[np.float64],
    cov_matrix: NDArray[np.float64],
    drought_prob: float,
    num_simulations: int,
    seed: int | None = None,
) -> NDArray[np.float64]:
    """Generate correlated crop income scenarios using copula-based sampling.

    Process:
    1. Fit marginals from FAOSTAT yield returns
    2. Estimate Kendall's tau rank correlations
    3. Sample from Gaussian copula (uniform marginals)
    4. Apply Clayton lower-tail adjustment for drought correlation
    5. Transform back to income space using fitted marginals

    Args:
        crops: List of crop profiles.
        expected_returns: Climate-adjusted expected incomes per crop.
        cov_matrix: Revenue covariance matrix (used for scale).
        drought_prob: Drought probability for Clayton scaling.
        num_simulations: Number of scenarios to generate.
        seed: Random seed for reproducibility.

    Returns:
        Array of shape (num_simulations, n_crops) with income scenarios.
    """
    rng = np.random.default_rng(seed)
    n = len(crops)

    marginals = fit_marginals(crops)

    tau_matrix = estimate_kendall_tau(crops)

    gauss_corr = _build_gaussian_copula_corr(tau_matrix)

    normal_samples = rng.multivariate_normal(
        np.zeros(n), gauss_corr, size=num_simulations
    )

    uniform_samples = stats.norm.cdf(normal_samples)

    theta = compute_clayton_theta(tau_matrix, drought_prob)
    tail_dep_lower = 2.0 ** (-1.0 / theta)

    uniform_samples = _apply_clayton_tail(
        uniform_samples, theta, rng
    )

    scenarios = np.zeros((num_simulations, n), dtype=np.float64)
    stds = np.sqrt(np.diag(cov_matrix))

    for j in range(n):
        marginal = marginals[j]

        if marginal.skewness != 0.0 and marginal.distribution_type == "kde":
            a = marginal.skewness
            loc = expected_returns[j]
            scale = stds[j]
            scenarios[:, j] = stats.skewnorm.ppf(
                uniform_samples[:, j], a, loc=loc, scale=scale
            )
        else:
            scenarios[:, j] = stats.norm.ppf(
                uniform_samples[:, j],
                loc=expected_returns[j],
                scale=stds[j],
            )

    scenarios = np.nan_to_num(scenarios, nan=0.0, posinf=0.0, neginf=0.0)

    tail_risk = TailRiskMetrics(
        copula_type="gaussian_clayton_hybrid",
        tail_dependence_lower=round(tail_dep_lower, 4),
        joint_failure_prob=_compute_joint_failure_prob(
            scenarios, expected_returns
        ),
        conditional_var_95=_compute_conditional_var(
            scenarios, expected_returns
        ),
    )

    logger.info(
        "Copula simulation: theta=%.3f, tail_dep=%.4f, joint_fail=%.4f",
        theta,
        tail_risk.tail_dependence_lower,
        tail_risk.joint_failure_prob,
    )

    return scenarios


def _apply_clayton_tail(
    uniform_samples: NDArray[np.float64],
    theta: float,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    """Apply Clayton copula lower-tail dependence adjustment.

    Shifts the lower quantiles of the uniform samples toward
    simultaneous low values, modeling correlated crop failures.

    Uses a mixing approach: with probability proportional to
    tail_dependence, replace samples with Clayton-correlated values.

    Args:
        uniform_samples: Array of shape (n_sims, n_crops) in [0, 1].
        theta: Clayton theta parameter.
        rng: Random number generator.

    Returns:
        Adjusted uniform samples with increased lower tail dependence.
    """
    n_sims, n_crops = uniform_samples.shape
    result = uniform_samples.copy()

    tail_dep = 2.0 ** (-1.0 / theta)
    mixing_prob = tail_dep * 0.5

    tail_mask = rng.random(n_sims) < mixing_prob

    if np.any(tail_mask):
        n_tail = int(np.sum(tail_mask))

        common_factor = rng.beta(1.0 / theta, 1.0, size=n_tail)

        for j in range(n_crops):
            idiosyncratic = rng.beta(1.0, theta, size=n_tail)
            result[tail_mask, j] = common_factor * idiosyncratic

    return np.clip(result, 1e-6, 1.0 - 1e-6)


def _compute_joint_failure_prob(
    scenarios: NDArray[np.float64],
    expected_returns: NDArray[np.float64],
) -> float:
    """Compute probability that ALL crops fall below 50% of expected returns."""
    threshold = expected_returns * 0.5
    below_threshold = scenarios < threshold
    all_fail = np.all(below_threshold, axis=1)
    return round(float(np.mean(all_fail)), 6)


def _compute_conditional_var(
    scenarios: NDArray[np.float64],
    expected_returns: NDArray[np.float64],
) -> float:
    """Compute Conditional VaR (Expected Shortfall) at 95% for portfolio.

    When the worst crop falls below its 5th percentile, what is the
    expected loss across all crops?
    """
    portfolio_incomes = np.sum(scenarios, axis=1)
    percentile_5 = np.percentile(portfolio_incomes, 5)
    tail_losses = portfolio_incomes[portfolio_incomes <= percentile_5]

    if len(tail_losses) == 0:
        return 0.0

    expected_total = float(np.sum(expected_returns))
    return round(expected_total - float(np.mean(tail_losses)), 2)
