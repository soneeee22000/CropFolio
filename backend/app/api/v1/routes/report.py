"""PDF report generation API route."""

from fastapi import APIRouter, Body, Request
from fastapi.responses import Response

from app.api.v1.schemas.report import ReportRequest
from app.core.limiter import limiter
from app.services.report_service import generate_report_pdf

router = APIRouter(prefix="/report", tags=["report"])


@router.post("/pdf")
@limiter.limit("10/minute")
async def generate_pdf_report(
    request: Request,
    body: ReportRequest = Body(...),  # noqa: B008
) -> Response:
    """Generate a printable PDF recommendation report."""
    pdf_bytes = generate_report_pdf(body)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=cropfolio-report.pdf"
        },
    )
