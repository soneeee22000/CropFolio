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


@router.get("/debug-models")
async def debug_models() -> dict:
    """Temporary: list available Gemini models."""
    from app.core.config import settings

    key = settings.gemini_api_key.strip()
    if not key:
        return {"error": "No API key", "key_length": 0}
    try:
        from google import genai

        client = genai.Client(api_key=key)
        models = [m.name for m in client.models.list() if "flash" in m.name.lower()]
        return {"key_length": len(key), "models": models}
    except Exception as e:
        return {"error": str(e), "key_length": len(key)}


@router.post("/pdf")
@limiter.limit("10/minute")
async def generate_pdf_report(
    request: Request,
    body: ReportRequest = Body(...),  # noqa: B008
) -> Response:
    """Generate a printable PDF recommendation report."""
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
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=cropfolio-report.pdf"
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
