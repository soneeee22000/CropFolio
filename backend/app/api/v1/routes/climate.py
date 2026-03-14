"""Climate risk API routes."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.climate import ClimateRiskResponse
from app.services.climate_service import ClimateService, get_climate_service

router = APIRouter(prefix="/climate-risk", tags=["climate"])


@router.get("/{township_id}", response_model=ClimateRiskResponse)
async def get_climate_risk(
    township_id: str,
    season: Literal["monsoon", "dry"] = "monsoon",
    service: ClimateService = Depends(get_climate_service),
) -> ClimateRiskResponse:
    """Get climate risk assessment for a township."""
    result = await service.assess_risk(township_id, season)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Township '{township_id}' not found",
        )
    profile, data_source = result
    return ClimateRiskResponse(
        township_id=profile.township_id,
        township_name=profile.township_name,
        season=profile.season,
        drought_probability=profile.drought_probability,
        flood_probability=profile.flood_probability,
        temp_anomaly_celsius=profile.temp_anomaly_celsius,
        rainfall_forecast_mm=profile.rainfall_forecast_mm,
        rainfall_historical_avg_mm=profile.rainfall_historical_avg_mm,
        risk_level=profile.risk_level,
        confidence=profile.confidence,
        data_source=data_source,
    )
