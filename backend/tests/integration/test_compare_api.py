"""Integration tests for multi-township comparison API endpoint."""

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
        data_quality_score=0.7,
    )
    return profile, "mock"


class TestCompareTownships:
    """Tests for POST /api/v1/compare/."""

    @patch(
        "app.services.portfolio_service.ClimateService.assess_risk",
        new_callable=AsyncMock,
        return_value=_mock_climate_risk(),
    )
    def test_compare_two_townships_returns_200(
        self, mock_climate: AsyncMock
    ) -> None:
        """Should return 200 with results for two townships."""
        response = client.post(
            "/api/v1/compare/",
            json={
                "township_ids": ["mgw_magway", "bgo_bago"],
                "crop_ids": ["rice", "sesame", "black_gram"],
                "season": "monsoon",
                "risk_tolerance": 0.5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["season"] == "monsoon"
        assert len(data["townships"]) == 2

    def test_compare_single_township_returns_422(self) -> None:
        """Should return 422 when fewer than 2 townships provided."""
        response = client.post(
            "/api/v1/compare/",
            json={
                "township_ids": ["mgw_magway"],
                "crop_ids": ["rice", "sesame"],
                "season": "monsoon",
            },
        )
        assert response.status_code == 422

    def test_compare_invalid_township_returns_404(self) -> None:
        """Should return 404 for unknown township IDs."""
        response = client.post(
            "/api/v1/compare/",
            json={
                "township_ids": ["nonexistent_a", "nonexistent_b"],
                "crop_ids": ["rice", "sesame"],
                "season": "monsoon",
            },
        )
        assert response.status_code == 404
