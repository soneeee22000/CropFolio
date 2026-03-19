"""Integration tests for enhanced fertilizer plan fields on /recommend endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

AMARAPURA = "mdy_amarapura"
MEIKTILA = "mdy_meiktila"

VALID_REQUEST = {
    "township_ids": [AMARAPURA],
    "crop_ids": ["rice", "chickpea", "sesame"],
    "risk_tolerance": 0.5,
    "season": "monsoon",
}


class TestEnhancedFertilizerPlan:
    """Tests that POST /api/v1/recommend returns fertilizer_plan fields."""

    def test_fertilizer_plan_present_on_crop(self) -> None:
        """At least one crop in the recommendation should include a fertilizer_plan."""
        response = client.post("/api/v1/recommend", json=VALID_REQUEST)
        assert response.status_code == 200
        data = response.json()
        crops = data["recommendations"][0]["crops"]
        plans = [c["fertilizer_plan"] for c in crops if c["fertilizer_plan"] is not None]
        assert len(plans) >= 1

    def test_fertilizer_plan_structure(self) -> None:
        """fertilizer_plan must contain applications, nutrient_totals, micronutrient_flags, and roi_estimate."""
        response = client.post("/api/v1/recommend", json=VALID_REQUEST)
        assert response.status_code == 200
        data = response.json()
        crops = data["recommendations"][0]["crops"]
        plan = next(
            (c["fertilizer_plan"] for c in crops if c["fertilizer_plan"] is not None),
            None,
        )
        assert plan is not None, "Expected at least one crop to have a fertilizer_plan"
        assert "applications" in plan
        assert "nutrient_totals" in plan
        assert "micronutrient_flags" in plan
        assert "roi_estimate" in plan

    def test_roi_estimate_fields(self) -> None:
        """roi_estimate inside fertilizer_plan must have total_cost_mmk, expected_yield_increase_pct, return_ratio."""
        response = client.post("/api/v1/recommend", json=VALID_REQUEST)
        assert response.status_code == 200
        data = response.json()
        crops = data["recommendations"][0]["crops"]
        plan = next(
            (c["fertilizer_plan"] for c in crops if c["fertilizer_plan"] is not None),
            None,
        )
        assert plan is not None
        roi = plan["roi_estimate"]
        assert "total_cost_mmk" in roi
        assert "expected_yield_increase_pct" in roi
        assert "return_ratio" in roi
        assert roi["total_cost_mmk"] >= 0
        assert roi["return_ratio"] >= 0
