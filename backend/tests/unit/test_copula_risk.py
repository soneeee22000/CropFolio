"""Unit tests for the copula tail risk engine."""

from __future__ import annotations

import numpy as np
import pytest

from app.domain.copula_risk import (
    compute_clayton_theta,
    estimate_kendall_tau,
    fit_marginals,
    sample_correlated_scenarios,
)
from app.domain.crops import get_crop_by_id
from app.domain.optimizer import compute_covariance_matrix, compute_expected_returns


@pytest.fixture()
def rice_sesame_crops():
    """Two crops with contrasting drought tolerance."""
    rice = get_crop_by_id("rice")
    sesame = get_crop_by_id("sesame")
    assert rice is not None and sesame is not None
    return [rice, sesame]


@pytest.fixture()
def three_crops():
    """Three crops spanning categories."""
    crops = [get_crop_by_id(cid) for cid in ["rice", "chickpea", "groundnut"]]
    assert all(c is not None for c in crops)
    return crops


class TestFitMarginals:
    """Tests for marginal distribution fitting."""

    def test_returns_one_per_crop(self, rice_sesame_crops):
        """Each crop gets exactly one MarginalFit."""
        result = fit_marginals(rice_sesame_crops)
        assert len(result) == 2

    def test_marginal_has_nonzero_std(self, rice_sesame_crops):
        """Fitted marginals should have positive std dev."""
        result = fit_marginals(rice_sesame_crops)
        for m in result:
            assert m.std > 0

    def test_kde_marginals_have_skewness(self, rice_sesame_crops):
        """KDE-fitted marginals capture skewness from FAOSTAT data."""
        result = fit_marginals(rice_sesame_crops)
        kde_fits = [m for m in result if m.distribution_type == "kde"]
        assert len(kde_fits) > 0


class TestKendallTau:
    """Tests for rank correlation estimation."""

    def test_tau_matrix_shape(self, three_crops):
        """Tau matrix should be n x n."""
        tau = estimate_kendall_tau(three_crops)
        assert tau.shape == (3, 3)

    def test_tau_diagonal_is_one(self, three_crops):
        """Self-correlation should be 1.0."""
        tau = estimate_kendall_tau(three_crops)
        np.testing.assert_array_almost_equal(np.diag(tau), 1.0)

    def test_tau_is_symmetric(self, three_crops):
        """Kendall's tau matrix should be symmetric."""
        tau = estimate_kendall_tau(three_crops)
        np.testing.assert_array_almost_equal(tau, tau.T)


class TestClaytonTheta:
    """Tests for Clayton copula parameter estimation."""

    def test_theta_positive(self, three_crops):
        """Clayton theta should always be positive."""
        tau = estimate_kendall_tau(three_crops)
        theta = compute_clayton_theta(tau, drought_prob=0.3)
        assert theta > 0

    def test_theta_increases_with_drought(self, three_crops):
        """Higher drought probability should increase theta."""
        tau = estimate_kendall_tau(three_crops)
        theta_low = compute_clayton_theta(tau, drought_prob=0.1)
        theta_high = compute_clayton_theta(tau, drought_prob=0.7)
        assert theta_high > theta_low


class TestSampleCorrelatedScenarios:
    """Tests for copula-based scenario generation."""

    def test_output_shape(self, rice_sesame_crops):
        """Output should be (n_simulations, n_crops)."""
        expected = compute_expected_returns(rice_sesame_crops, 0.2, 0.1)
        cov = compute_covariance_matrix(rice_sesame_crops)

        scenarios = sample_correlated_scenarios(
            rice_sesame_crops, expected, cov,
            drought_prob=0.2, num_simulations=500, seed=42,
        )
        assert scenarios.shape == (500, 2)

    def test_scenarios_nonnegative_after_floor(self, rice_sesame_crops):
        """Scenarios should be non-negative (floored at 0)."""
        expected = compute_expected_returns(rice_sesame_crops, 0.2, 0.1)
        cov = compute_covariance_matrix(rice_sesame_crops)

        scenarios = sample_correlated_scenarios(
            rice_sesame_crops, expected, cov,
            drought_prob=0.2, num_simulations=500, seed=42,
        )
        assert np.all(np.isfinite(scenarios))

    def test_reproducibility_with_seed(self, rice_sesame_crops):
        """Same seed should produce same scenarios."""
        expected = compute_expected_returns(rice_sesame_crops, 0.2, 0.1)
        cov = compute_covariance_matrix(rice_sesame_crops)

        s1 = sample_correlated_scenarios(
            rice_sesame_crops, expected, cov,
            drought_prob=0.2, num_simulations=100, seed=123,
        )
        s2 = sample_correlated_scenarios(
            rice_sesame_crops, expected, cov,
            drought_prob=0.2, num_simulations=100, seed=123,
        )
        np.testing.assert_array_equal(s1, s2)
