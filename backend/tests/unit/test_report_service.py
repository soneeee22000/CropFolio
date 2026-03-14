"""Tests for PDF report generation service."""

from __future__ import annotations

from app.api.v1.schemas.report import CropAllocation, ReportRequest
from app.services.report_service import generate_report_pdf


def _make_report_request(
    allocations: list[CropAllocation] | None = None,
) -> ReportRequest:
    """Create a ReportRequest with sensible defaults."""
    if allocations is None:
        allocations = [
            CropAllocation(
                crop_name="Rice",
                crop_name_mm="\u1006\u1014\u103a",
                weight_pct=60.0,
            ),
            CropAllocation(
                crop_name="Sesame",
                crop_name_mm="\u1014\u1036\u1038",
                weight_pct=40.0,
            ),
        ]
    return ReportRequest(
        township_name="Magway",
        season="monsoon",
        allocations=allocations,
        expected_income=850000.0,
        risk_reduction_pct=23.5,
        prob_catastrophic_loss_monocrop=18.2,
        prob_catastrophic_loss_diversified=6.1,
    )


class TestGenerateReportPdf:
    """Tests for generate_report_pdf."""

    def test_generates_valid_pdf_bytes(self) -> None:
        """Output should start with PDF magic bytes."""
        request = _make_report_request()
        pdf = generate_report_pdf(request)
        assert isinstance(pdf, bytes)
        assert pdf[:5] == b"%PDF-"

    def test_with_burmese_crop_names(self) -> None:
        """Should handle Burmese Unicode characters."""
        allocations = [
            CropAllocation(
                crop_name="Black Gram",
                crop_name_mm="\u1019\u1010\u103a\u1015\u1032",
                weight_pct=55.0,
            ),
            CropAllocation(
                crop_name="Chickpea",
                crop_name_mm="\u1000\u101c\u102c\u1038\u1015\u1032",
                weight_pct=45.0,
            ),
        ]
        request = _make_report_request(allocations=allocations)
        pdf = generate_report_pdf(request)
        assert isinstance(pdf, bytes)
        assert pdf[:5] == b"%PDF-"

    def test_with_empty_allocations(self) -> None:
        """Should generate valid PDF even with no allocations."""
        request = _make_report_request(allocations=[])
        pdf = generate_report_pdf(request)
        assert isinstance(pdf, bytes)
        assert pdf[:5] == b"%PDF-"
