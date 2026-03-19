"""Pydantic schemas for PDF report generation."""

from __future__ import annotations

from pydantic import BaseModel


class CropAllocation(BaseModel):
    """Single crop allocation for the report."""

    crop_name: str
    crop_name_mm: str
    weight_pct: float


class ReportRequest(BaseModel):
    """Request body for PDF report generation."""

    township_name: str
    season: str
    allocations: list[CropAllocation]
    expected_income: float
    risk_reduction_pct: float
    prob_catastrophic_loss_monocrop: float
    prob_catastrophic_loss_diversified: float
    climate_risk_level: str = ""
    drought_probability: float = 0.0
    flood_probability: float = 0.0
    language: str = "en"
    soil_data: dict | None = None
    fertilizer_recs: list[dict] | None = None
    crop_confidence: dict[str, str] | None = None


class AnalysisRequest(BaseModel):
    """Request body for AI portfolio analysis."""

    township_name: str
    season: str
    allocations: list[CropAllocation]
    expected_income: float
    risk_reduction_pct: float
    drought_probability: float = 0.0
    flood_probability: float = 0.0
    mean_income: float = 0.0
    prob_catastrophic_loss_monocrop: float = 0.0
    prob_catastrophic_loss_diversified: float = 0.0


class AnalysisResponse(BaseModel):
    """Response from AI portfolio analysis."""

    analysis: str
    analysis_mm: str
    has_ai: bool
