"""NASA POWER API client for historical climate data."""

from __future__ import annotations

import calendar
import logging
from functools import lru_cache
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 15.0


class NasaPowerClient:
    """Client for NASA POWER API to fetch historical climate data."""

    def __init__(self) -> None:
        """Initialize with base URL from settings."""
        self._base_url = settings.nasa_power_base_url

    async def get_historical_rainfall(
        self,
        latitude: float,
        longitude: float,
        start_year: int = 2015,
        end_year: int = 2024,
    ) -> list[float] | None:
        """Fetch historical annual rainfall data for a location.

        Args:
            latitude: Location latitude.
            longitude: Location longitude.
            start_year: Start year for data range.
            end_year: End year for data range.

        Returns:
            List of annual rainfall values (mm), or None on failure.
        """
        params = {
            "parameters": "PRECTOTCORR",
            "community": "AG",
            "longitude": longitude,
            "latitude": latitude,
            "start": f"{start_year}0101",
            "end": f"{end_year}1231",
            "format": "JSON",
        }

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(CONNECT_TIMEOUT, read=READ_TIMEOUT)
            ) as client:
                url = f"{self._base_url}monthly/point"
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return _extract_annual_rainfall(data)
        except (httpx.HTTPError, KeyError, ValueError) as e:
            logger.warning("NASA POWER API request failed: %s", e)
            return None


def _extract_annual_rainfall(data: dict[str, Any]) -> list[float]:
    """Extract annual rainfall totals from NASA POWER response.

    NASA POWER PRECTOTCORR monthly endpoint returns mm/day averages.
    We convert to mm/month by multiplying by days in each month.
    """
    monthly_data = data["properties"]["parameter"]["PRECTOTCORR"]
    annual_totals: dict[str, float] = {}

    for month_key, value in monthly_data.items():
        if value < 0:
            continue
        year_str = month_key[:4]
        month_str = month_key[4:6]
        days_in_month = calendar.monthrange(int(year_str), int(month_str))[1]
        monthly_mm = value * days_in_month
        annual_totals[year_str] = annual_totals.get(year_str, 0.0) + monthly_mm

    return list(annual_totals.values())


@lru_cache(maxsize=1)
def get_nasa_power_client() -> NasaPowerClient:
    """Return singleton NasaPowerClient instance."""
    return NasaPowerClient()
