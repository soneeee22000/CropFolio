"""Tests for Monte Carlo simulation engine."""

import pytest

from app.domain.crops import CropProfile
from app.domain.simulator import SimulationResult, run_monte_carlo


class TestMonteCarlo:
    """Tests for Monte Carlo simulation."""

    def test_returns_correct_number_of_simulations(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Should return exactly num_simulations income values."""
        weights = {"rice": 0.6, "black_gram": 0.25, "sesame": 0.15}
        result = run_monte_carlo(
            three_crops, weights, drought_prob=0.3, flood_prob=0.1,
            num_simulations=500, seed=42,
        )
        assert len(result.incomes) == 500

    def test_result_type(self, three_crops: list[CropProfile]) -> None:
        """Should return SimulationResult."""
        weights = {"rice": 0.6, "black_gram": 0.25, "sesame": 0.15}
        result = run_monte_carlo(
            three_crops, weights, drought_prob=0.3, flood_prob=0.1,
            num_simulations=100, seed=42,
        )
        assert isinstance(result, SimulationResult)

    def test_mean_near_expected(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Mean simulated income should be near expected income."""
        weights = {"rice": 0.6, "black_gram": 0.25, "sesame": 0.15}
        result = run_monte_carlo(
            three_crops, weights, drought_prob=0.2, flood_prob=0.1,
            num_simulations=5000, seed=42,
        )
        from app.domain.optimizer import compute_expected_returns
        import numpy as np

        expected_returns = compute_expected_returns(
            three_crops, drought_prob=0.2, flood_prob=0.1
        )
        weight_array = np.array([weights[c.id] for c in three_crops])
        expected_income = float(np.dot(weight_array, expected_returns))

        assert abs(result.mean_income - expected_income) / expected_income < 0.1

    def test_percentile_ordering(
        self, three_crops: list[CropProfile]
    ) -> None:
        """5th percentile should be less than 95th percentile."""
        weights = {"rice": 0.6, "black_gram": 0.25, "sesame": 0.15}
        result = run_monte_carlo(
            three_crops, weights, drought_prob=0.3, flood_prob=0.1,
            num_simulations=1000, seed=42,
        )
        assert result.percentile_5 < result.percentile_95

    def test_all_incomes_non_negative(
        self, three_crops: list[CropProfile]
    ) -> None:
        """No simulated income should be negative."""
        weights = {"rice": 0.6, "black_gram": 0.25, "sesame": 0.15}
        result = run_monte_carlo(
            three_crops, weights, drought_prob=0.3, flood_prob=0.1,
            num_simulations=1000, seed=42,
        )
        assert all(income >= 0 for income in result.incomes)

    def test_catastrophic_loss_probability_bounded(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Catastrophic loss probability should be between 0 and 1."""
        weights = {"rice": 0.6, "black_gram": 0.25, "sesame": 0.15}
        result = run_monte_carlo(
            three_crops, weights, drought_prob=0.3, flood_prob=0.1,
            num_simulations=1000, seed=42,
        )
        assert 0.0 <= result.prob_catastrophic_loss <= 1.0

    def test_reproducible_with_seed(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Same seed should produce identical results."""
        weights = {"rice": 0.6, "black_gram": 0.25, "sesame": 0.15}
        kwargs = {
            "crops": three_crops,
            "weights": weights,
            "drought_prob": 0.3,
            "flood_prob": 0.1,
            "num_simulations": 100,
            "seed": 42,
        }
        result1 = run_monte_carlo(**kwargs)
        result2 = run_monte_carlo(**kwargs)
        assert result1.incomes == result2.incomes

    def test_diversified_lower_catastrophic_risk(
        self, three_crops: list[CropProfile]
    ) -> None:
        """Diversified portfolio should have lower catastrophic loss risk than monocrop."""
        monocrop_weights = {"rice": 1.0, "black_gram": 0.0, "sesame": 0.0}
        diversified_weights = {"rice": 0.5, "black_gram": 0.3, "sesame": 0.2}

        mono_result = run_monte_carlo(
            three_crops, monocrop_weights, drought_prob=0.4, flood_prob=0.1,
            num_simulations=5000, seed=42,
        )
        div_result = run_monte_carlo(
            three_crops, diversified_weights, drought_prob=0.4, flood_prob=0.1,
            num_simulations=5000, seed=42,
        )

        assert div_result.prob_catastrophic_loss <= mono_result.prob_catastrophic_loss
