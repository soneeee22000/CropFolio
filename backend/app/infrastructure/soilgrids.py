"""ISRIC SoilGrids API client with static data fallback."""

# SoilGrids v2.0: https://rest.isric.org/soilgrids/v2.0/properties/query
# Provides global soil property predictions at 250m resolution.
# We use static fallback data for hackathon reliability.

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

import httpx

from app.domain.fertilizers import SoilProfile, get_soil_profile

logger = logging.getLogger(__name__)

SOILGRIDS_BASE_URL = "https://rest.isric.org/soilgrids/v2.0"
CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 15.0

# Properties we query from SoilGrids
SOIL_PROPERTIES = ["phh2o", "nitrogen", "soc", "clay", "sand", "silt", "cec"]
DEPTH_INTERVAL = "0-30cm"
VALUE_TYPE = "Q0.5"  # Median prediction


class SoilGridsClient:
    """Client for ISRIC SoilGrids REST API with static data fallback."""

    def __init__(self) -> None:
        """Initialize with base URL."""
        self._base_url = SOILGRIDS_BASE_URL

    async def get_soil_properties(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any] | None:
        """Fetch soil properties from SoilGrids API.

        Args:
            latitude: Location latitude.
            longitude: Location longitude.

        Returns:
            Dict of soil properties, or None on failure.
        """
        params = {
            "lon": longitude,
            "lat": latitude,
            "property": SOIL_PROPERTIES,
            "depth": DEPTH_INTERVAL,
            "value": VALUE_TYPE,
        }

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(CONNECT_TIMEOUT, read=READ_TIMEOUT)
            ) as client:
                url = f"{self._base_url}/properties/query"
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return _extract_soil_properties(data)
        except (httpx.HTTPError, KeyError, ValueError) as e:
            logger.warning("SoilGrids API request failed: %s", e)
            return None

    async def get_soil_profile_with_fallback(
        self,
        township_id: str,
        latitude: float,
        longitude: float,
    ) -> tuple[SoilProfile | None, str]:
        """Get soil profile, trying API first then static fallback.

        Args:
            township_id: Township identifier.
            latitude: Township latitude.
            longitude: Township longitude.

        Returns:
            Tuple of (SoilProfile, data_source) where data_source is
            "live" or "static".
        """
        # Try static data first for hackathon reliability
        static_profile = get_soil_profile(township_id)
        if static_profile is not None:
            return static_profile, "static"

        # Fall back to API if no static data
        api_data = await self.get_soil_properties(latitude, longitude)
        if api_data is not None:
            profile = SoilProfile(
                township_id=township_id,
                ph_h2o=api_data.get("ph_h2o", 6.5),
                nitrogen_g_per_kg=api_data.get("nitrogen_g_per_kg", 1.0),
                soc_g_per_kg=api_data.get("soc_g_per_kg", 10.0),
                clay_pct=int(api_data.get("clay_pct", 25)),
                sand_pct=int(api_data.get("sand_pct", 35)),
                silt_pct=int(api_data.get("silt_pct", 40)),
                cec_cmol_per_kg=api_data.get("cec_cmol_per_kg", 15.0),
                texture_class=_classify_texture(
                    int(api_data.get("clay_pct", 25)),
                    int(api_data.get("sand_pct", 35)),
                    int(api_data.get("silt_pct", 40)),
                ),
                fertility_rating=_rate_fertility(
                    api_data.get("nitrogen_g_per_kg", 1.0),
                    api_data.get("soc_g_per_kg", 10.0),
                    api_data.get("cec_cmol_per_kg", 15.0),
                ),
            )
            return profile, "live"

        logger.warning("No soil data for township %s", township_id)
        return None, "unavailable"


def _extract_soil_properties(data: dict[str, Any]) -> dict[str, float]:
    """Extract soil property values from SoilGrids API response."""
    properties = data.get("properties", {}).get("layers", [])
    result: dict[str, float] = {}

    for layer in properties:
        name = layer.get("name", "")
        depths = layer.get("depths", [])
        for depth in depths:
            if depth.get("label") == DEPTH_INTERVAL:
                values = depth.get("values", {})
                median = values.get(VALUE_TYPE)
                if median is not None:
                    result[name] = median

    # Convert SoilGrids units to our units
    # phh2o: stored as pH * 10 in SoilGrids
    if "phh2o" in result:
        result["ph_h2o"] = result.pop("phh2o") / 10.0
    # nitrogen: stored as cg/kg in SoilGrids → g/kg
    if "nitrogen" in result:
        result["nitrogen_g_per_kg"] = result.pop("nitrogen") / 100.0
    # soc: stored as dg/kg in SoilGrids → g/kg
    if "soc" in result:
        result["soc_g_per_kg"] = result.pop("soc") / 10.0
    # clay, sand, silt: stored as g/kg → %
    for prop in ["clay", "sand", "silt"]:
        if prop in result:
            result[f"{prop}_pct"] = result.pop(prop) / 10.0
    # cec: stored as mmol(c)/kg → cmol(+)/kg
    if "cec" in result:
        result["cec_cmol_per_kg"] = result.pop("cec") / 10.0

    return result


def _classify_texture(clay_pct: int, sand_pct: int, silt_pct: int) -> str:
    """Classify soil texture using USDA texture triangle (simplified)."""
    if clay_pct >= 40:
        return "clay"
    if clay_pct >= 35 and sand_pct < 45:
        return "silty_clay" if silt_pct >= 40 else "clay"
    if clay_pct >= 27:
        if silt_pct >= 40:
            return "silty_clay_loam"
        return "clay_loam"
    if sand_pct >= 70:
        return "sandy_loam" if clay_pct >= 10 else "sand"
    if silt_pct >= 50:
        return "silt_loam"
    return "loam"


def _rate_fertility(
    nitrogen: float, soc: float, cec: float
) -> str:
    """Rate overall soil fertility from key indicators."""
    score = 0
    if nitrogen >= 1.5:
        score += 2
    elif nitrogen >= 1.0:
        score += 1
    if soc >= 15.0:
        score += 2
    elif soc >= 8.0:
        score += 1
    if cec >= 20.0:
        score += 2
    elif cec >= 12.0:
        score += 1

    if score >= 5:
        return "high"
    if score >= 4:
        return "moderate_high"
    if score >= 2:
        return "moderate"
    if score >= 1:
        return "low"
    return "very_low"


@lru_cache(maxsize=1)
def get_soilgrids_client() -> SoilGridsClient:
    """Return singleton SoilGridsClient instance."""
    return SoilGridsClient()
