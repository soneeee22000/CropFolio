"""Tests for Markowitz portfolio optimization engine."""

import pytest

from app.domain.crops import CropProfile
from app.domain.optimizer import (
    OptimizationResult,
    compute_covariance_matrix,
    compute_expected_returns,
    optimize_portfolio,
)


class TestComputeExpectedReturns:
    """Tests for climate-adjusted expected returns calculation."""

    def test_returns_positive_for_all_crops(
        self, all_crops: list[CropProfile]
    ) -> None:
        """All crops should have positive expected returns."""
        returns = compute_expected_returns(all_crops, drought_prob=0.2, flood_prob=0.1)
        assert all(r > 0 for r in returns)

    def test_drought_reduces_drought_sensitive_crops_more(
        self, rice: CropProfile, sesame: CropProfile
    ) -> None:
        """Drought hurts rice more than sesame."""
        no_drought = compute_expected_returns([rice, sesame], 0.0, 0.0)
        high_drought = compute_expected_returns([rice, sesame], 0.6, 0.0)

        rice_loss_pct = 1 - high_drought[0] / no_drought[0]
        sesame_loss_pct = 1 - high_drought[1] / no_drought[1]

        assert rice_loss_pct > sesame_loss_pct

    def test_flood_reduces_flood_sensitive_crops_more(
        self, rice: CropProfile, black_gram: CropProfile
    ) -> None:
        """Flood hurts black gram more than rice."""
        no_flood = compute_expected_returns([rice, black_gram], 0.0, 0.0)
        high_flood = compute_expected_returns([rice, black_gram], 0.0, 0.6)

        rice_loss_pct = 1 - high_flood[0] / no_flood[0]
        gram_loss_pct = 1 - high_flood[1] / no_flood[1]

        assert gram_loss_pct > rice_loss_pct

    def test_zero_climate_risk_returns_base_income(
        self, rice: CropProfile
    ) -> None:
        """With zero climate risk, returns should equal base yield * price."""
        returns = compute_expected_returns([rice], drought_prob=0.0, flood_prob=0.0)
        expected = rice.avg_yield_kg_per_ha * rice.avg_price_mmk_per_kg
        assert abs(returns[0] - expected) < 1.0


class TestCovarianceMatrix:
    """Tests for crop covariance matrix computation."""

    def test_matrix_is_square(self, three_crops: list[CropProfile]) -> None:
        """Covariance matrix should be n x n."""
        cov = compute_covariance_matrix(three_crops)
        assert cov.shape == (3, 3)

    def test_matrix_is_symmetric(self, three_crops: list[CropProfile]) -> None:
        """Covariance matrix must be symmetric."""
        cov = compute_covariance_matrix(three_crops)
        for i in range(3):
            for j in range(3):
                assert abs(cov[i][j] - cov[j][i]) < 1e-4

    def test_diagonal_is_positive(self, three_crops: list[CropProfile]) -> None:
        """Diagonal (variances) must be positive."""
        cov = compute_covariance_matrix(three_crops)
        for i in range(3):
            assert cov[i][i] > 0

    def test_rice_sesame_negative_correlation(
        self, rice: CropProfile, sesame: CropProfile
    ) -> None:
        """Rice and sesame have negative yield correlation per FAOSTAT data."""
        cov = compute_covariance_matrix([rice, sesame])
        assert cov[0][1] < 0, "Rice-sesame covariance should be negative (FAOSTAT r=-0.49)"


class TestOptimizePortfolio:
    """Tests for full portfolio optimization."""

    def test_weights_sum_to_one(self, three_crops: list[CropProfile]) -> None:
        """Optimized weights must sum to 1.0."""
        result = optimize_portfolio(three_crops, drought_prob=0.3, flood_prob=0.1)
        assert abs(sum(result.weights.values()) - 1.0) < 1e-4

    def test_all_weights_non_negative(
        self, three_crops: list[CropProfile]
    ) -> None:
        """No crop should have negative allocation."""
        result = optimize_portfolio(three_crops, drought_prob=0.3, flood_prob=0.1)
        for weight in result.weights.values():
            assert weight >= 0.0

    def test_returns_all_crop_ids(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Result should contain weights for all input crops."""
        result = optimize_portfolio(three_crops, drought_prob=0.3, flood_prob=0.1)
        for crop in three_crops:
            assert crop.id in result.weights

    def test_diversified_portfolio_reduces_risk(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Diversified portfolio should have lower risk than monocrop average."""
        result = optimize_portfolio(three_crops, drought_prob=0.3, flood_prob=0.1)
        assert result.risk_reduction_pct > 0

    def test_positive_expected_income(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Portfolio should have positive expected income."""
        result = optimize_portfolio(three_crops, drought_prob=0.3, flood_prob=0.1)
        assert result.expected_income_per_ha > 0

    def test_high_drought_shifts_away_from_rice(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Under high drought risk, rice weight should decrease."""
        low_drought = optimize_portfolio(three_crops, drought_prob=0.1, flood_prob=0.1)
        high_drought = optimize_portfolio(three_crops, drought_prob=0.7, flood_prob=0.1)

        assert high_drought.weights["rice"] < low_drought.weights["rice"]

    def test_result_type(self, three_crops: list[CropProfile]) -> None:
        """Optimization should return OptimizationResult."""
        result = optimize_portfolio(three_crops, drought_prob=0.3, flood_prob=0.1)
        assert isinstance(result, OptimizationResult)

    def test_sharpe_ratio_positive(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Sharpe ratio should be positive for a valid portfolio."""
        result = optimize_portfolio(three_crops, drought_prob=0.3, flood_prob=0.1)
        assert result.sharpe_ratio > 0


@pytest.fixture
def chickpea() -> CropProfile:
    """Chickpea crop profile fixture."""
    from app.domain.crops import MYANMAR_CROPS

    return MYANMAR_CROPS["chickpea"]
