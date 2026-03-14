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
