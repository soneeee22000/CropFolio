"""Field Monitor API routes — multi-plot compliance monitoring and alerts."""

from typing import Literal

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Request

from app.api.v1.schemas.field_monitor import (
    ComplianceInfoResponse,
    FieldMonitorRequest,
    FieldMonitorSummaryResponse,
    MonitoredPlotResponse,
    PlotAlertResponse,
    PlotLocationResponse,
    PlotObservationResponse,
)
from app.core.limiter import limiter
from app.domain.field_monitor import MonitoredPlot, PlotAlert
from app.services.field_monitor_service import (
    FieldMonitorService,
    get_field_monitor_service,
)

router = APIRouter(prefix="/field-monitor", tags=["field-monitor"])

TOWNSHIP_PATH = Path(min_length=1, max_length=64, pattern=r"^[a-z0-9_-]+$")
PLOT_PATH = Path(min_length=1, max_length=128, pattern=r"^[a-z0-9_-]+$")


def _to_plot_response(plot: MonitoredPlot) -> MonitoredPlotResponse:
    """Map domain MonitoredPlot to API response."""
    return MonitoredPlotResponse(
        plot_id=plot.plot_id,
        farmer_name=plot.farmer_name,
        location=PlotLocationResponse(
            latitude=plot.location.latitude,
            longitude=plot.location.longitude,
        ),
        area_ha=plot.area_ha,
        recommended_crop=plot.recommended_crop,
        compliance=ComplianceInfoResponse(
            status=plot.compliance.status.value,
            score=plot.compliance.score,
            planting_detected=plot.compliance.planting_detected,
            crop_match=plot.compliance.crop_match,
            phenology_match=plot.compliance.phenology_match,
        ),
        observations=[
            PlotObservationResponse(
                date=obs.date,
                observed_vh_db=obs.observed_vh_db,
                expected_vh_db=obs.expected_vh_db,
            )
            for obs in plot.observations
        ],
        alerts=[_to_alert_response(a) for a in plot.alerts],
    )


def _to_alert_response(alert: PlotAlert) -> PlotAlertResponse:
    """Map domain PlotAlert to API response."""
    return PlotAlertResponse(
        alert_id=alert.alert_id,
        plot_id=alert.plot_id,
        farmer_name=alert.farmer_name,
        alert_type=alert.alert_type,
        severity=alert.severity.value,
        message=alert.message,
        created_date=alert.created_date,
    )


@router.post("/monitor", response_model=FieldMonitorSummaryResponse)
@limiter.limit("10/minute")
async def monitor_township(
    request: Request,
    body: FieldMonitorRequest = Body(...),  # noqa: B008
    service: FieldMonitorService = Depends(get_field_monitor_service),  # noqa: B008
) -> FieldMonitorSummaryResponse:
    """Get field monitoring summary for a township."""
    try:
        summary = service.get_township_monitor(
            township_id=body.township_id,
            season=body.season,
            year=body.year,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return FieldMonitorSummaryResponse(
        township_id=summary.township_id,
        season=summary.season,
        year=summary.year,
        total_plots=summary.total_plots,
        compliant_count=summary.compliant_count,
        warning_count=summary.warning_count,
        deviation_count=summary.deviation_count,
        compliance_rate=summary.compliance_rate,
        total_area_ha=summary.total_area_ha,
        active_alerts=summary.active_alerts,
        plots=[_to_plot_response(p) for p in summary.plots],
        alerts=[_to_alert_response(a) for a in summary.alerts],
    )


@router.get(
    "/plot/{township_id}/{plot_id}",
    response_model=MonitoredPlotResponse,
)
@limiter.limit("30/minute")
async def get_plot_detail(
    request: Request,
    township_id: str = TOWNSHIP_PATH,
    plot_id: str = PLOT_PATH,
    service: FieldMonitorService = Depends(get_field_monitor_service),  # noqa: B008
) -> MonitoredPlotResponse:
    """Get detailed monitoring data for a specific plot."""
    plot = service.get_plot_detail(township_id, plot_id)
    if plot is None:
        raise HTTPException(
            status_code=404,
            detail="Plot not found",
        )
    return _to_plot_response(plot)


@router.get(
    "/alerts/{township_id}",
    response_model=list[PlotAlertResponse],
)
@limiter.limit("30/minute")
async def get_alerts(
    request: Request,
    township_id: str = TOWNSHIP_PATH,
    severity: Literal["low", "medium", "high", "critical"] | None = Query(
        default=None,
    ),
    service: FieldMonitorService = Depends(get_field_monitor_service),  # noqa: B008
) -> list[PlotAlertResponse]:
    """Get alerts for a township, optionally filtered by severity."""
    alerts = service.get_alerts(township_id, severity)
    return [_to_alert_response(a) for a in alerts]
