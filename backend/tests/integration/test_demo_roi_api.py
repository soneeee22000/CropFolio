"""Integration tests for demo ROI API endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestDemoROIEndpoint:
    """Tests for POST /api/v1/recommend/demo-roi."""

    def test_happy_path_rice_meiktila(self) -> None:
        """Rice in Meiktila should return valid ROI data."""
        response = client.post(
            "/api/v1/recommend/demo-roi",
            json={
                "township_id": "mdy_meiktila",
                "crop_id": "rice",
                "area_hectares": 2.0,
                "season": "dry",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["township_id"] == "mdy_meiktila"
        assert data["crop_id"] == "rice"
        assert data["area_hectares"] == 2.0
        assert data["total_input_cost_mmk"] > 0
        assert data["expected_revenue_mmk"] > 0
        assert 0.0 <= data["success_probability"] <= 1.0
        assert 0.0 <= data["catastrophic_loss_probability"] <= 1.0

    def test_costs_scale_with_area(self) -> None:
        """Costs and revenue should scale linearly with area."""
        resp_1 = client.post(
            "/api/v1/recommend/demo-roi",
            json={
                "township_id": "mdy_meiktila",
                "crop_id": "rice",
                "area_hectares": 1.0,
                "season": "dry",
            },
        )
        resp_2 = client.post(
            "/api/v1/recommend/demo-roi",
            json={
                "township_id": "mdy_meiktila",
                "crop_id": "rice",
                "area_hectares": 2.0,
                "season": "dry",
            },
        )
        data_1 = resp_1.json()
        data_2 = resp_2.json()
        # Revenue should roughly double (integer rounding may differ slightly)
        ratio = data_2["expected_revenue_mmk"] / data_1["expected_revenue_mmk"]
        assert 1.9 <= ratio <= 2.1

    def test_crop_with_zero_price(self) -> None:
        """Crop with price=0.0 should still return valid structure."""
        response = client.post(
            "/api/v1/recommend/demo-roi",
            json={
                "township_id": "mdy_meiktila",
                "crop_id": "maize",
                "area_hectares": 1.0,
                "season": "dry",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["expected_revenue_mmk"] == 0
        assert data["total_input_cost_mmk"] >= 0

    def test_invalid_township_returns_400(self) -> None:
        """Unknown township should return 400."""
        response = client.post(
            "/api/v1/recommend/demo-roi",
            json={
                "township_id": "fake_township",
                "crop_id": "rice",
                "area_hectares": 1.0,
                "season": "dry",
            },
        )
        assert response.status_code == 400

    def test_invalid_crop_returns_400(self) -> None:
        """Unknown crop should return 400."""
        response = client.post(
            "/api/v1/recommend/demo-roi",
            json={
                "township_id": "mdy_meiktila",
                "crop_id": "fake_crop",
                "area_hectares": 1.0,
                "season": "dry",
            },
        )
        assert response.status_code == 400

    def test_includes_soil_and_fertilizer(self) -> None:
        """Should include soil profile and fertilizer recommendation."""
        response = client.post(
            "/api/v1/recommend/demo-roi",
            json={
                "township_id": "mdy_meiktila",
                "crop_id": "rice",
                "area_hectares": 1.0,
                "season": "dry",
            },
        )
        data = response.json()
        assert data["soil"] is not None
        assert data["recommended_fertilizer"] is not None
