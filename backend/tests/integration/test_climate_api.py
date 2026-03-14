"""Integration tests for climate risk API endpoint."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _mock_nasa_rainfall() -> list[float]:
    """Return synthetic historical rainfall values."""
    return [800.0 + i * 20 for i in range(20)]


def _mock_meteo_forecast() -> dict[str, float]:
    """Return synthetic 14-day weather forecast.

    70mm over 14 days scales to ~765mm over monsoon (153 days),
    close to original 750mm seasonal expectation.
    """
    return {"total_rainfall_mm": 70.0, "temp_anomaly_celsius": 0.8, "forecast_days": 14}


class TestGetClimateRisk:
    """Tests for GET /api/v1/climate-risk/{township_id}."""

    @patch(
        "app.services.climate_service.NasaPowerClient.get_historical_rainfall",
        new_callable=AsyncMock,
        return_value=_mock_nasa_rainfall(),
    )
    @patch(
        "app.services.climate_service.OpenMeteoClient.get_forecast",
        new_callable=AsyncMock,
        return_value=_mock_meteo_forecast(),
    )
    def test_valid_township_returns_200(
        self, mock_meteo: AsyncMock, mock_nasa: AsyncMock
    ) -> None:
        """Should return climate risk for valid township."""
        response = client.get("/api/v1/climate-risk/mgw_magway?season=monsoon")
        assert response.status_code == 200
        data = response.json()
        assert data["township_id"] == "mgw_magway"
        assert data["township_name"] == "Magway"
        assert data["season"] == "monsoon"
        assert "drought_probability" in data
        assert "flood_probability" in data
        assert "risk_level" in data
        assert "data_source" in data

    @patch(
        "app.services.climate_service.NasaPowerClient.get_historical_rainfall",
        new_callable=AsyncMock,
        return_value=_mock_nasa_rainfall(),
    )
    @patch(
        "app.services.climate_service.OpenMeteoClient.get_forecast",
        new_callable=AsyncMock,
        return_value=_mock_meteo_forecast(),
    )
    def test_probabilities_bounded(
        self, mock_meteo: AsyncMock, mock_nasa: AsyncMock
    ) -> None:
        """All probabilities should be between 0 and 1."""
        response = client.get("/api/v1/climate-risk/bgo_bago?season=monsoon")
        data = response.json()
        assert 0.0 <= data["drought_probability"] <= 1.0
        assert 0.0 <= data["flood_probability"] <= 1.0
        assert 0.0 <= data["confidence"] <= 1.0

    def test_invalid_township_returns_404(self) -> None:
        """Should return 404 for unknown township."""
        response = client.get("/api/v1/climate-risk/nonexistent")
        assert response.status_code == 404

    @patch(
        "app.services.climate_service.NasaPowerClient.get_historical_rainfall",
        new_callable=AsyncMock,
        return_value=None,
    )
    @patch(
        "app.services.climate_service.OpenMeteoClient.get_forecast",
        new_callable=AsyncMock,
        return_value=None,
    )
    def test_fallback_on_api_failure(
        self, mock_meteo: AsyncMock, mock_nasa: AsyncMock
    ) -> None:
        """Should use fallback data when external APIs fail."""
        response = client.get("/api/v1/climate-risk/mgw_magway?season=dry")
        assert response.status_code == 200
        data = response.json()
        assert data["data_source"] == "fallback"

    @patch(
        "app.services.climate_service.NasaPowerClient.get_historical_rainfall",
        new_callable=AsyncMock,
        return_value=_mock_nasa_rainfall(),
    )
    @patch(
        "app.services.climate_service.OpenMeteoClient.get_forecast",
        new_callable=AsyncMock,
        return_value=_mock_meteo_forecast(),
    )
    def test_dry_season_accepted(
        self, mock_meteo: AsyncMock, mock_nasa: AsyncMock
    ) -> None:
        """Should accept 'dry' as season parameter."""
        response = client.get("/api/v1/climate-risk/sgn_monywa?season=dry")
        assert response.status_code == 200
        assert response.json()["season"] == "dry"
