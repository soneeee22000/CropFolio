"""Pydantic schemas for portfolio optimization API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class OptimizeRequest(BaseModel):
    """Request body for portfolio optimization."""

    crop_ids: list[str] = Field(min_length=2, max_length=10)
    township_id: str
    risk_tolerance: float = Field(default=0.5, ge=0.0, le=1.0)
    season: Literal["monsoon", "dry"] = "monsoon"


class CropWeight(BaseModel):
    """Single crop's allocation in the optimized portfolio."""

    crop_id: str
    crop_name: str
    crop_name_mm: str
    weight: float
    expected_income_per_ha: float


class ClimateRiskSummary(BaseModel):
    """Summary of climate risk used in optimization."""

    drought_probability: float
    flood_probability: float
    risk_level: str
    data_source: str


class PortfolioMetrics(BaseModel):
    """Aggregate metrics for the optimized portfolio."""

    expected_income_per_ha: float
    income_std_dev: float
    sharpe_ratio: float
    risk_reduction_pct: float


class OptimizeResponse(BaseModel):
    """Response from portfolio optimization."""

    township_id: str
    township_name: str
    season: str
    weights: list[CropWeight]
    metrics: PortfolioMetrics
    climate_risk: ClimateRiskSummary
