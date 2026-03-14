"""Integration tests for Monte Carlo simulation API endpoint."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _mock_climate_risk():  # type: ignore[no-untyped-def]
    """Mock climate service to return deterministic risk profile."""
    from app.domain.climate import ClimateRiskProfile

    profile = ClimateRiskProfile(
        township_id="mgw_magway",
        township_name="Magway",
        season="monsoon",
        drought_probability=0.3,
        flood_probability=0.15,
        temp_anomaly_celsius=0.5,
        rainfall_forecast_mm=750.0,
        rainfall_historical_avg_mm=800.0,
        risk_level="moderate",
        confidence=0.7,
    )
    return profile, "mock"


VALID_REQUEST = {
    "crop_ids": ["rice", "black_gram", "sesame"],
    "weights": {"rice": 0.6, "black_gram": 0.25, "sesame": 0.15},
    "township_id": "mgw_magway",
    "num_simulations": 500,
    "season": "monsoon",
}


class TestRunSimulation:
    """Tests for POST /api/v1/simulate/."""

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_valid_request_returns_200(self, mock_climate: AsyncMock) -> None:
        """Should return simulation results for valid input."""
        response = client.post("/api/v1/simulate/", json=VALID_REQUEST)
        assert response.status_code == 200
        data = response.json()
        assert data["township_name"] == "Magway"
        assert data["num_simulations"] == 500

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_stats_present(self, mock_climate: AsyncMock) -> None:
        """Response should include simulation statistics."""
        response = client.post("/api/v1/simulate/", json=VALID_REQUEST)
        stats = response.json()["stats"]
        assert "mean_income" in stats
        assert "median_income" in stats
        assert "std_dev" in stats
        assert "percentile_5" in stats
        assert "percentile_95" in stats
        assert "prob_catastrophic_loss" in stats
        assert "value_at_risk_95" in stats
        assert stats["mean_income"] > 0

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_histogram_present(self, mock_climate: AsyncMock) -> None:
        """Response should include histogram bins."""
        response = client.post("/api/v1/simulate/", json=VALID_REQUEST)
        histogram = response.json()["histogram"]
        assert len(histogram) == 25
        for hbin in histogram:
            assert "bin_start" in hbin
            assert "bin_end" in hbin
            assert "count" in hbin
            assert "frequency" in hbin

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_histogram_counts_match_simulations(
        self, mock_climate: AsyncMock
    ) -> None:
        """Sum of histogram counts should equal num_simulations."""
        response = client.post("/api/v1/simulate/", json=VALID_REQUEST)
        histogram = response.json()["histogram"]
        total_count = sum(b["count"] for b in histogram)
        assert total_count == 500

    def test_weights_not_summing_to_one_returns_422(self) -> None:
        """Should reject weights that don't sum to 1.0."""
        bad_request = {
            **VALID_REQUEST,
            "weights": {"rice": 0.5, "black_gram": 0.2, "sesame": 0.1},
        }
        response = client.post("/api/v1/simulate/", json=bad_request)
        assert response.status_code == 422

    def test_invalid_crop_returns_400(self) -> None:
        """Should return 400 for unknown crop IDs."""
        bad_request = {
            **VALID_REQUEST,
            "crop_ids": ["rice", "banana", "sesame"],
            "weights": {"rice": 0.5, "banana": 0.3, "sesame": 0.2},
        }
        response = client.post("/api/v1/simulate/", json=bad_request)
        assert response.status_code == 400

    def test_invalid_township_returns_404(self) -> None:
        """Should return 404 for unknown township."""
        bad_request = {**VALID_REQUEST, "township_id": "nonexistent"}
        response = client.post("/api/v1/simulate/", json=bad_request)
        assert response.status_code == 404
