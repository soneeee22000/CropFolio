"""Climate risk assessment service orchestrating API clients and domain engine."""

from __future__ import annotations

import logging

from app.core.constants import (
    DEFAULT_FORECAST_DAYS,
    DRY_SEASON_DAYS,
    MONSOON_SEASON_DAYS,
)
from app.domain.climate import ClimateRiskProfile, assess_climate_risk
from app.infrastructure.nasa_power import NasaPowerClient, get_nasa_power_client
from app.infrastructure.open_meteo import OpenMeteoClient, get_open_meteo_client
from app.services.township_service import TownshipService, get_township_service

logger = logging.getLogger(__name__)

# Regional rainfall averages (mm/year) as fallback data
# Source: Myanmar Meteorological Department historical averages
REGIONAL_RAINFALL_FALLBACK: dict[str, dict[str, float]] = {
    "Mandalay": {"monsoon": 800.0, "dry": 150.0},
    "Sagaing": {"monsoon": 900.0, "dry": 180.0},
    "Magway": {"monsoon": 700.0, "dry": 120.0},
    "Bago": {"monsoon": 2500.0, "dry": 200.0},
    "Ayeyarwady": {"monsoon": 2800.0, "dry": 180.0},
    "Yangon": {"monsoon": 2700.0, "dry": 150.0},
    "Nay Pyi Taw": {"monsoon": 1200.0, "dry": 160.0},
    "Shan": {"monsoon": 1500.0, "dry": 200.0},
}

DEFAULT_RAINFALL: dict[str, float] = {"monsoon": 1500.0, "dry": 170.0}


class ClimateService:
    """Orchestrates climate risk assessment using external APIs and domain logic."""

    def __init__(
        self,
        township_service: TownshipService | None = None,
        nasa_client: NasaPowerClient | None = None,
        meteo_client: OpenMeteoClient | None = None,
    ) -> None:
        """Initialize with dependencies."""
        self._townships = township_service or get_township_service()
        self._nasa = nasa_client or get_nasa_power_client()
        self._meteo = meteo_client or get_open_meteo_client()

    async def assess_risk(
        self,
        township_id: str,
        season: str = "monsoon",
    ) -> tuple[ClimateRiskProfile, str] | None:
        """Assess climate risk for a township.

        Args:
            township_id: Township identifier.
            season: 'monsoon' or 'dry'.

        Returns:
            Tuple of (ClimateRiskProfile, data_source) or None if township not found.
        """
        township = self._townships.get_by_id(township_id)
        if township is None:
            return None

        lat = township["latitude"]
        lon = township["longitude"]
        region = township["region"]

        historical, forecast, data_source = await self._fetch_climate_data(
            lat, lon, region, season
        )

        season_days = MONSOON_SEASON_DAYS if season == "monsoon" else DRY_SEASON_DAYS
        forecast_days = forecast.get("forecast_days", DEFAULT_FORECAST_DAYS)
        if forecast_days > 0 and forecast_days != season_days:
            forecast["total_rainfall_mm"] = (
                forecast["total_rainfall_mm"] * (season_days / forecast_days)
            )

        forecast_rainfall = forecast.get("total_rainfall_mm", 0.0)
        forecast_temp_anomaly = forecast.get("temp_anomaly_celsius", 0.0)

        profile = assess_climate_risk(
            township_id=township_id,
            township_name=township["name"],
            season=season,
            historical_rainfall=historical,
            forecast_rainfall_mm=forecast_rainfall,
            forecast_temp_anomaly=forecast_temp_anomaly,
        )

        return profile, data_source

    async def _fetch_climate_data(
        self,
        lat: float,
        lon: float,
        region: str,
        season: str,
    ) -> tuple[list[float], dict[str, float], str]:
        """Fetch climate data from APIs with fallback."""
        data_source = "live"

        historical = await self._nasa.get_historical_rainfall(lat, lon)
        forecast = await self._meteo.get_forecast(lat, lon)

        if historical is None:
            historical = self._get_fallback_historical(region, season)
            data_source = "fallback"

        if forecast is None:
            forecast = self._get_fallback_forecast(region, season)
            if data_source == "live":
                data_source = "partial"

        return historical, forecast, data_source

    def _get_fallback_historical(
        self, region: str, season: str
    ) -> list[float]:
        """Generate synthetic historical data from regional averages."""
        avg = REGIONAL_RAINFALL_FALLBACK.get(
            region, DEFAULT_RAINFALL
        ).get(season, DEFAULT_RAINFALL[season])

        import numpy as np
        rng = np.random.default_rng(hash(region) % 2**32)
        return [
            float(rng.normal(avg, avg * 0.2)) for _ in range(20)
        ]

    def _get_fallback_forecast(
        self, region: str, season: str
    ) -> dict[str, float]:
        """Generate fallback forecast from regional averages."""
        avg = REGIONAL_RAINFALL_FALLBACK.get(
            region, DEFAULT_RAINFALL
        ).get(season, DEFAULT_RAINFALL[season])

        season_days = MONSOON_SEASON_DAYS if season == "monsoon" else DRY_SEASON_DAYS
        return {
            "total_rainfall_mm": avg * 0.95,
            "temp_anomaly_celsius": 0.5,
            "forecast_days": season_days,
        }


_service: ClimateService | None = None


def get_climate_service() -> ClimateService:
    """Return singleton ClimateService instance."""
    global _service
    if _service is None:
        _service = ClimateService()
    return _service
