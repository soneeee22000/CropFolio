"""Integration tests for PDF report generation API endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "township_name": "Magway",
    "season": "monsoon",
    "allocations": [
        {
            "crop_name": "Rice",
            "crop_name_mm": "\u1006\u1014\u103a",
            "weight_pct": 60.0,
        },
        {
            "crop_name": "Sesame",
            "crop_name_mm": "\u1014\u1036\u1038",
            "weight_pct": 40.0,
        },
    ],
    "expected_income": 850000.0,
    "risk_reduction_pct": 23.5,
    "prob_catastrophic_loss_monocrop": 18.2,
    "prob_catastrophic_loss_diversified": 6.1,
}


class TestGeneratePdfReport:
    """Tests for POST /api/v1/report/pdf."""

    def test_valid_payload_returns_200_pdf(self) -> None:
        """Should return 200 with application/pdf content type."""
        response = client.post("/api/v1/report/pdf", json=VALID_PAYLOAD)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content[:5] == b"%PDF-"

    def test_invalid_payload_returns_422(self) -> None:
        """Should return 422 for missing required fields."""
        response = client.post(
            "/api/v1/report/pdf",
            json={"township_name": "Magway"},
        )
        assert response.status_code == 422
