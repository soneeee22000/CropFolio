"""SAR analysis API routes — Sentinel-1 rice detection and planting verification."""


from fastapi import APIRouter, Body, Depends, HTTPException, Request

from app.api.v1.schemas.sar import (
    PhenologySignalResponse,
    SARAnalyzeRequest,
    SARJobResponse,
    SARJobStatusResponse,
    SARResultResponse,
    SARTimePointResponse,
)
from app.core.limiter import limiter
from app.infrastructure.sar_pipeline import SARAnalysisResult
from app.services.sar_service import SARService, get_sar_service

router = APIRouter(prefix="/sar", tags=["sar"])


def _to_result_response(result: SARAnalysisResult) -> SARResultResponse:
    """Map domain SARAnalysisResult to API response."""
    return SARResultResponse(
        township_id=result.township_id,
        analysis_date=result.analysis_date,
        season=result.season,
        time_series=[
            SARTimePointResponse(
                date=tp.date,
                vh_db=tp.vh_db,
                vv_db=tp.vv_db,
                vh_vv_ratio=tp.vh_vv_ratio,
            )
            for tp in result.time_series
        ],
        phenology_signals=[
            PhenologySignalResponse(
                signal_type=ps.signal_type,
                detected=ps.detected,
                confidence=ps.confidence,
                date_range=ps.date_range,
                description=ps.description,
            )
            for ps in result.phenology_signals
        ],
        rice_detected=result.rice_detected,
        rice_confidence=result.rice_confidence,
        estimated_area_pct=result.estimated_area_pct,
        summary=result.summary,
    )


@router.post("/analyze", response_model=SARJobResponse)
@limiter.limit("5/minute")
async def submit_sar_analysis(
    request: Request,
    body: SARAnalyzeRequest = Body(...),  # noqa: B008
    service: SARService = Depends(get_sar_service),  # noqa: B008
) -> SARJobResponse:
    """Submit a SAR analysis job (async). Poll /results/{job_id} for status."""
    try:
        job_id = await service.submit_analysis(
            township_id=body.township_id,
            season=body.season,
            year=body.year,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return SARJobResponse(
        job_id=job_id,
        township_id=body.township_id,
        status="pending",
        message=f"SAR analysis submitted. Poll GET /sar/results/{job_id} for status.",
    )


@router.get("/results/{job_id}", response_model=SARJobStatusResponse)
@limiter.limit("30/minute")
async def get_sar_results(
    request: Request,
    job_id: str,
    service: SARService = Depends(get_sar_service),  # noqa: B008
) -> SARJobStatusResponse:
    """Get status and results of a SAR analysis job."""
    job = service.get_job(job_id)
    if job is None:
        raise HTTPException(
            status_code=404,
            detail=f"Job '{job_id}' not found",
        )

    result_resp = None
    if job.result is not None:
        result_resp = _to_result_response(job.result)

    return SARJobStatusResponse(
        job_id=job.job_id,
        township_id=job.township_id,
        status=job.status.value,
        created_at=job.created_at,
        completed_at=job.completed_at,
        error=job.error,
        result=result_resp,
    )


@router.get("/coverage/{township_id}", response_model=SARResultResponse)
@limiter.limit("30/minute")
async def get_sar_coverage(
    request: Request,
    township_id: str,
    service: SARService = Depends(get_sar_service),  # noqa: B008
) -> SARResultResponse:
    """Get latest SAR planting verification for a township."""
    result = service.get_latest_coverage(township_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No SAR coverage for township '{township_id}'",
        )
    return _to_result_response(result)
