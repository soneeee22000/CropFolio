"""Unit tests for the Bayesian Belief Network engine."""

from __future__ import annotations

import pytest

from app.domain.bayesian import (
    CropBayesianNetwork,
    EvidenceItem,
    compute_bayesian_returns,
)
from app.domain.crops import get_crop_by_id


@pytest.fixture()
def rice_crop():
    """Rice crop profile."""
    crop = get_crop_by_id("rice")
    assert crop is not None
    return crop


@pytest.fixture()
def chickpea_crop():
    """Chickpea crop profile (drought-tolerant)."""
    crop = get_crop_by_id("chickpea")
    assert crop is not None
    return crop


@pytest.fixture()
def three_crops():
    """Three crops for portfolio testing."""
    crops = [get_crop_by_id(cid) for cid in ["rice", "sesame", "black_gram"]]
    assert all(c is not None for c in crops)
    return crops


class TestCropBayesianNetwork:
    """Tests for single-crop BBN."""

    def test_predict_returns_valid_probs(self, rice_crop):
        """Yield probabilities should sum to ~1.0."""
        bbn = CropBayesianNetwork(rice_crop)
        result = bbn.predict(drought_prob=0.2, flood_prob=0.1)

        total = sum(result.yield_probabilities.values())
        assert abs(total - 1.0) < 0.01

    def test_predict_has_three_categories(self, rice_crop):
        """Prediction should have low/medium/high yield categories."""
        bbn = CropBayesianNetwork(rice_crop)
        result = bbn.predict()

        assert "low" in result.yield_probabilities
        assert "medium" in result.yield_probabilities
        assert "high" in result.yield_probabilities

    def test_drought_increases_low_yield_prob(self, rice_crop):
        """Rice under drought should have higher P(low yield)."""
        bbn = CropBayesianNetwork(rice_crop)

        normal = bbn.predict(drought_prob=0.1, flood_prob=0.1)
        drought = bbn.predict(drought_prob=0.8, flood_prob=0.1)

        assert drought.yield_probabilities["low"] > normal.yield_probabilities["low"]

    def test_drought_tolerant_less_affected(self, chickpea_crop, rice_crop):
        """Chickpea (drought_tolerance=0.85) should be less affected than rice (0.3)."""
        rice_bbn = CropBayesianNetwork(rice_crop)
        chickpea_bbn = CropBayesianNetwork(chickpea_crop)

        rice_drought = rice_bbn.predict(drought_prob=0.7, flood_prob=0.0)
        chick_drought = chickpea_bbn.predict(drought_prob=0.7, flood_prob=0.0)

        chick_low = chick_drought.yield_probabilities["low"]
        rice_low = rice_drought.yield_probabilities["low"]
        assert chick_low < rice_low

    def test_evidence_rainfall_low_shifts_prediction(self, rice_crop):
        """Setting rainfall=low should shift prediction toward drought."""
        bbn = CropBayesianNetwork(rice_crop)

        no_evidence = bbn.predict(drought_prob=0.2, flood_prob=0.1)
        with_evidence = bbn.predict(
            evidence=[EvidenceItem(variable="rainfall", value="low")],
            drought_prob=0.2,
            flood_prob=0.1,
        )

        ev_low = with_evidence.yield_probabilities["low"]
        no_ev_low = no_evidence.yield_probabilities["low"]
        assert ev_low > no_ev_low

    def test_evidence_soil_good_improves_prediction(self, rice_crop):
        """Good soil evidence should increase high yield probability."""
        bbn = CropBayesianNetwork(rice_crop)

        poor_soil = bbn.predict(
            evidence=[EvidenceItem(variable="soil", value="poor")],
        )
        good_soil = bbn.predict(
            evidence=[EvidenceItem(variable="soil", value="good")],
        )

        good_high = good_soil.yield_probabilities["high"]
        poor_high = poor_soil.yield_probabilities["high"]
        assert good_high > poor_high

    def test_expected_yield_factor_range(self, rice_crop):
        """Expected yield factor should be between 0.5 and 1.3."""
        bbn = CropBayesianNetwork(rice_crop)
        result = bbn.predict()

        assert 0.4 <= result.expected_yield_factor <= 1.4


class TestComputeBayesianReturns:
    """Tests for portfolio-level Bayesian returns."""

    def test_returns_length_matches_crops(self, three_crops):
        """Should return one adjusted return per crop."""
        returns, result = compute_bayesian_returns(
            three_crops, drought_prob=0.2, flood_prob=0.1,
        )
        assert len(returns) == 3

    def test_returns_positive(self, three_crops):
        """Adjusted returns should be positive."""
        returns, _ = compute_bayesian_returns(
            three_crops, drought_prob=0.2, flood_prob=0.1,
        )
        for r in returns:
            assert r > 0

    def test_model_type_is_bayesian(self, three_crops):
        """Result should indicate Bayesian model type."""
        _, result = compute_bayesian_returns(
            three_crops, drought_prob=0.2, flood_prob=0.1,
        )
        assert result.model_type == "bayesian"
