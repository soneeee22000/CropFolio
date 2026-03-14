"""Integration tests for portfolio optimization API endpoint."""

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


class TestOptimizePortfolio:
    """Tests for POST /api/v1/optimize/."""

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_valid_request_returns_200(self, mock_climate: AsyncMock) -> None:
        """Should return optimized portfolio for valid input."""
        response = client.post(
            "/api/v1/optimize/",
            json={
                "crop_ids": ["rice", "black_gram", "sesame"],
                "township_id": "mgw_magway",
                "risk_tolerance": 0.5,
                "season": "monsoon",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["township_name"] == "Magway"
        assert len(data["weights"]) == 3

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_weights_sum_to_one(self, mock_climate: AsyncMock) -> None:
        """Optimized weights must sum to 1.0."""
        response = client.post(
            "/api/v1/optimize/",
            json={
                "crop_ids": ["rice", "black_gram", "sesame"],
                "township_id": "mgw_magway",
            },
        )
        data = response.json()
        total_weight = sum(w["weight"] for w in data["weights"])
        assert abs(total_weight - 1.0) < 0.01

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_metrics_present(self, mock_climate: AsyncMock) -> None:
        """Response should include portfolio metrics."""
        response = client.post(
            "/api/v1/optimize/",
            json={
                "crop_ids": ["rice", "chickpea"],
                "township_id": "mgw_magway",
            },
        )
        metrics = response.json()["metrics"]
        assert "expected_income_per_ha" in metrics
        assert "income_std_dev" in metrics
        assert "sharpe_ratio" in metrics
        assert "risk_reduction_pct" in metrics
        assert metrics["expected_income_per_ha"] > 0

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_climate_risk_summary_present(
        self, mock_climate: AsyncMock
    ) -> None:
        """Response should include climate risk summary."""
        response = client.post(
            "/api/v1/optimize/",
            json={
                "crop_ids": ["rice", "sesame"],
                "township_id": "mgw_magway",
            },
        )
        climate = response.json()["climate_risk"]
        assert "drought_probability" in climate
        assert "flood_probability" in climate
        assert "risk_level" in climate
        assert "data_source" in climate

    def test_invalid_crop_returns_400(self) -> None:
        """Should return 400 for unknown crop IDs."""
        response = client.post(
            "/api/v1/optimize/",
            json={
                "crop_ids": ["rice", "banana"],
                "township_id": "mgw_magway",
            },
        )
        assert response.status_code == 400

    def test_invalid_township_returns_404(self) -> None:
        """Should return 404 for unknown township."""
        response = client.post(
            "/api/v1/optimize/",
            json={
                "crop_ids": ["rice", "sesame"],
                "township_id": "nonexistent",
            },
        )
        assert response.status_code == 404

    def test_single_crop_returns_422(self) -> None:
        """Should reject request with fewer than 2 crops."""
        response = client.post(
            "/api/v1/optimize/",
            json={
                "crop_ids": ["rice"],
                "township_id": "mgw_magway",
            },
        )
        assert response.status_code == 422
