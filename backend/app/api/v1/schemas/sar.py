"""Pydantic schemas for SAR analysis API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class SARAnalyzeRequest(BaseModel):
    """Request to trigger SAR analysis."""

    township_id: str
    season: Literal["monsoon", "dry"] = "monsoon"
    year: int = Field(default=2025, ge=2020, le=2030)


class SARJobResponse(BaseModel):
    """Response after submitting a SAR analysis job."""

    job_id: str
    township_id: str
    status: str
    message: str


class SARTimePointResponse(BaseModel):
    """A single SAR observation point."""

    date: str
    vh_db: float
    vv_db: float
    vh_vv_ratio: float


class PhenologySignalResponse(BaseModel):
    """A detected phenological signal."""

    signal_type: str
    detected: bool
    confidence: float
    date_range: str
    description: str


class SARResultResponse(BaseModel):
    """Complete SAR analysis result."""

    township_id: str
    analysis_date: str
    season: str
    time_series: list[SARTimePointResponse]
    phenology_signals: list[PhenologySignalResponse]
    rice_detected: bool
    rice_confidence: float
    estimated_area_pct: float
    summary: str


class SARJobStatusResponse(BaseModel):
    """Status of a SAR analysis job."""

    job_id: str
    township_id: str
    status: str
    created_at: str
    completed_at: str | None = None
    error: str | None = None
    result: SARResultResponse | None = None
