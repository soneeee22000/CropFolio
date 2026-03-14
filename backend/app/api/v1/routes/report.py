"""PDF report generation API route."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from app.api.v1.schemas.report import ReportRequest
from app.services.report_service import generate_report_pdf

router = APIRouter(prefix="/report", tags=["report"])


@router.post("/pdf")
async def generate_pdf_report(request: ReportRequest) -> Response:
    """Generate a printable PDF recommendation report."""
    pdf_bytes = generate_report_pdf(request)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=cropfolio-report.pdf"
        },
    )
