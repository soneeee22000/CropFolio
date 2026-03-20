"""Pydantic schemas for Field Monitor API."""

from typing import Literal

from pydantic import BaseModel, Field


class FieldMonitorRequest(BaseModel):
    """Request to monitor a township's plots."""

    township_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-z0-9_-]+$")
    season: Literal["monsoon", "dry"] = "monsoon"
    year: int = Field(default=2025, ge=2020, le=2030)


class PlotLocationResponse(BaseModel):
    """Geographic location of a plot."""

    latitude: float
    longitude: float


class PlotObservationResponse(BaseModel):
    """A single SAR observation for a plot."""

    date: str
    observed_vh_db: float
    expected_vh_db: float


class ComplianceInfoResponse(BaseModel):
    """Compliance scoring breakdown."""

    status: str
    score: float
    planting_detected: bool
    crop_match: bool
    phenology_match: float


class PlotAlertResponse(BaseModel):
    """An alert from a plot deviation."""

    alert_id: str
    plot_id: str
    farmer_name: str
    alert_type: str
    severity: str
    message: str
    created_date: str


class MonitoredPlotResponse(BaseModel):
    """A single monitored plot with full details."""

    plot_id: str
    farmer_name: str
    location: PlotLocationResponse
    area_ha: float
    recommended_crop: str
    compliance: ComplianceInfoResponse
    observations: list[PlotObservationResponse]
    alerts: list[PlotAlertResponse]


class FieldMonitorSummaryResponse(BaseModel):
    """Full monitoring summary for a township."""

    township_id: str
    season: str
    year: int
    total_plots: int
    compliant_count: int
    warning_count: int
    deviation_count: int
    compliance_rate: float
    total_area_ha: float
    active_alerts: int
    plots: list[MonitoredPlotResponse]
    alerts: list[PlotAlertResponse]
