"""Open-Meteo API client for weather forecasts."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 15.0


class OpenMeteoClient:
    """Client for Open-Meteo API to fetch weather forecasts."""

    def __init__(self) -> None:
        """Initialize with base URL from settings."""
        self._base_url = settings.open_meteo_base_url

    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        forecast_days: int = 14,
    ) -> dict[str, float] | None:
        """Fetch weather forecast summary for a location.

        Args:
            latitude: Location latitude.
            longitude: Location longitude.
            forecast_days: Number of days to forecast.

        Returns:
            Dict with total_rainfall_mm and temp_anomaly_celsius,
            or None on failure.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "precipitation_sum,temperature_2m_mean",
            "forecast_days": forecast_days,
        }

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(CONNECT_TIMEOUT, read=READ_TIMEOUT)
            ) as client:
                url = f"{self._base_url}forecast"
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return _extract_forecast_summary(data)
        except (httpx.HTTPError, KeyError, ValueError) as e:
            logger.warning("Open-Meteo API request failed: %s", e)
            return None


def _extract_forecast_summary(data: dict[str, Any]) -> dict[str, float]:
    """Extract total rainfall and temperature anomaly from forecast."""
    daily = data["daily"]
    precipitation = daily["precipitation_sum"]
    temperatures = daily["temperature_2m_mean"]

    valid_precip = [p for p in precipitation if p is not None]
    valid_temps = [t for t in temperatures if t is not None]

    total_rainfall = sum(valid_precip)
    avg_temp = sum(valid_temps) / len(valid_temps) if valid_temps else 27.0

    myanmar_avg_temp = 27.0
    temp_anomaly = avg_temp - myanmar_avg_temp

    return {
        "total_rainfall_mm": round(total_rainfall, 1),
        "temp_anomaly_celsius": round(temp_anomaly, 2),
    }


_client: OpenMeteoClient | None = None


def get_open_meteo_client() -> OpenMeteoClient:
    """Return singleton OpenMeteoClient instance."""
    global _client
    if _client is None:
        _client = OpenMeteoClient()
    return _client
