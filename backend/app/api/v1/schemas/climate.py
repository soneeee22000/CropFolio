"""Pydantic schemas for climate risk API."""

from __future__ import annotations

from pydantic import BaseModel


class ClimateRiskResponse(BaseModel):
    """Climate risk assessment response for a township."""

    township_id: str
    township_name: str
    season: str
    drought_probability: float
    flood_probability: float
    temp_anomaly_celsius: float
    rainfall_forecast_mm: float
    rainfall_historical_avg_mm: float
    risk_level: str
    confidence: float
    data_source: str
