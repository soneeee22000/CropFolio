"""PDF report generation and AI analysis API routes."""

from fastapi import APIRouter, Body, Request
from fastapi.responses import Response

from app.api.v1.schemas.report import (
    AnalysisRequest,
    AnalysisResponse,
    ReportRequest,
)
from app.core.limiter import limiter
from app.services.ai_service import get_ai_service
from app.services.report_service import generate_report_pdf

router = APIRouter(prefix="/report", tags=["report"])



@router.post("/pdf")
@limiter.limit("10/minute")
async def generate_pdf_report(
    request: Request,
    body: ReportRequest = Body(...),  # noqa: B008
) -> Response:
    """Generate a printable PDF recommendation report."""
    if body.language == "mm":
        from app.services.burmese_report_service import generate_burmese_report_pdf

        pdf_bytes = generate_burmese_report_pdf(
            data=body,
            soil_data=body.soil_data,
            fertilizer_recs=body.fertilizer_recs,
            crop_confidence=body.crop_confidence,
        )
        filename = "cropfolio-report-mm.pdf"
    else:
        ai_service = get_ai_service()
        narrative = await ai_service.generate_report_narrative(
            township_name=body.township_name,
            season=body.season,
            allocations=[a.model_dump() for a in body.allocations],
            expected_income=body.expected_income,
            risk_reduction_pct=body.risk_reduction_pct,
            drought_probability=body.drought_probability,
            flood_probability=body.flood_probability,
            risk_level=body.climate_risk_level,
        )
        pdf_bytes = generate_report_pdf(body, narrative=narrative)
        filename = "cropfolio-report.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        },
    )


@router.post("/analyze")
@limiter.limit("10/minute")
async def analyze_portfolio(
    request: Request,
    body: AnalysisRequest = Body(...),  # noqa: B008
) -> AnalysisResponse:
    """Generate AI analysis of simulation results."""
    ai_service = get_ai_service()
    result = await ai_service.analyze_simulation(
        township_name=body.township_name,
        season=body.season,
        mean_income=body.mean_income,
        expected_income=body.expected_income,
        risk_reduction_pct=body.risk_reduction_pct,
        prob_catastrophic_loss_monocrop=body.prob_catastrophic_loss_monocrop,
        prob_catastrophic_loss_diversified=body.prob_catastrophic_loss_diversified,
        drought_probability=body.drought_probability,
        flood_probability=body.flood_probability,
    )
    if result:
        return AnalysisResponse(
            analysis=result["analysis"],
            analysis_mm=result["analysis_mm"],
            has_ai=True,
        )
    return AnalysisResponse(
        analysis=(
            f"Portfolio optimized for {body.township_name} "
            f"({body.season} season). "
            f"Expected income: {body.expected_income:,.0f} MMK/ha "
            f"with {body.risk_reduction_pct:.1f}% risk reduction "
            f"vs monocropping."
        ),
        analysis_mm="",
        has_ai=False,
    )
