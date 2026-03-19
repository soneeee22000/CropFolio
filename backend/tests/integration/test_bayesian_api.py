"""Integration tests for Bayesian portfolio optimization endpoint."""

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


VALID_BAYESIAN_REQUEST = {
    "crop_ids": ["rice", "chickpea", "sesame"],
    "township_id": "mdy_amarapura",
    "risk_tolerance": 0.5,
    "season": "monsoon",
    "evidence": [
        {"variable": "rainfall", "value": "normal"},
        {"variable": "soil", "value": "moderate"},
    ],
}


class TestOptimizeBayesian:
    """Tests for POST /api/v1/optimize/bayesian."""

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_valid_request_returns_200(self, mock_climate: AsyncMock) -> None:
        """Should return 200 for a valid bayesian optimization request."""
        response = client.post("/api/v1/optimize/bayesian", json=VALID_BAYESIAN_REQUEST)
        assert response.status_code == 200
        data = response.json()
        assert data["township_id"] == "mdy_amarapura"
        assert data["model_type"] == "bayesian"

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_response_contains_bayesian_predictions(
        self, mock_climate: AsyncMock
    ) -> None:
        """Response must include bayesian_predictions for each requested crop."""
        response = client.post("/api/v1/optimize/bayesian", json=VALID_BAYESIAN_REQUEST)
        assert response.status_code == 200
        data = response.json()
        predictions = data["bayesian_predictions"]
        assert len(predictions) == len(VALID_BAYESIAN_REQUEST["crop_ids"])
        for pred in predictions:
            assert "crop_id" in pred
            assert "yield_probabilities" in pred
            assert "expected_yield_factor" in pred
            assert "evidence_used" in pred

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_empty_evidence_list_is_accepted(self, mock_climate: AsyncMock) -> None:
        """Bayesian endpoint must work with zero evidence items (prior only)."""
        request_no_evidence = {
            **VALID_BAYESIAN_REQUEST,
            "evidence": [],
        }
        response = client.post("/api/v1/optimize/bayesian", json=request_no_evidence)
        assert response.status_code == 200
        data = response.json()
        assert len(data["bayesian_predictions"]) > 0

    def test_invalid_township_returns_404(self) -> None:
        """Unknown township should return 404."""
        response = client.post(
            "/api/v1/optimize/bayesian",
            json={
                **VALID_BAYESIAN_REQUEST,
                "township_id": "nonexistent_township",
            },
        )
        assert response.status_code == 404

    def test_single_crop_returns_422(self) -> None:
        """Fewer than 2 crops must be rejected with 422."""
        response = client.post(
            "/api/v1/optimize/bayesian",
            json={
                **VALID_BAYESIAN_REQUEST,
                "crop_ids": ["rice"],
            },
        )
        assert response.status_code == 422
