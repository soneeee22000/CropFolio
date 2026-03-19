"""Integration tests for copula distribution mode on the simulate endpoint."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _mock_climate_risk():  # type: ignore[no-untyped-def]
    """Mock climate service to return deterministic risk profile."""
    from app.domain.climate import ClimateRiskProfile

    profile = ClimateRiskProfile(
        township_id="mdy_amarapura",
        township_name="Amarapura",
        season="monsoon",
        drought_probability=0.25,
        flood_probability=0.1,
        temp_anomaly_celsius=0.4,
        rainfall_forecast_mm=800.0,
        rainfall_historical_avg_mm=820.0,
        risk_level="low",
        data_quality_score=0.75,
    )
    return profile, "mock"


VALID_COPULA_REQUEST = {
    "crop_ids": ["rice", "chickpea", "sesame"],
    "weights": {"rice": 0.5, "chickpea": 0.3, "sesame": 0.2},
    "township_id": "mdy_amarapura",
    "num_simulations": 500,
    "season": "monsoon",
    "distribution_model": "copula",
}


class TestCopulaSimulation:
    """Tests for POST /api/v1/simulate/ with distribution_model='copula'."""

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_copula_request_returns_200(self, mock_climate: AsyncMock) -> None:
        """Should return 200 and valid SimulateResponse for copula mode."""
        response = client.post("/api/v1/simulate/", json=VALID_COPULA_REQUEST)
        assert response.status_code == 200
        data = response.json()
        assert data["num_simulations"] == 500
        assert data["township_id"] == "mdy_amarapura"

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_copula_response_reports_distribution_model(
        self, mock_climate: AsyncMock
    ) -> None:
        """Response distribution_model field must equal 'copula'."""
        response = client.post("/api/v1/simulate/", json=VALID_COPULA_REQUEST)
        assert response.status_code == 200
        data = response.json()
        assert data["distribution_model"] == "copula"
