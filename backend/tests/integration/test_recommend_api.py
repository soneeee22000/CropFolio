"""Integration tests for recommendation API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PRICED_CROPS = ["rice", "black_gram", "green_gram"]
MEIKTILA = "mdy_meiktila"
MAGWAY = "mgw_magway"


class TestRecommendEndpoint:
    """Tests for POST /api/v1/recommend."""

    def test_happy_path_single_township(self) -> None:
        """Should return recommendations for a single township."""
        response = client.post(
            "/api/v1/recommend",
            json={
                "township_ids": [MEIKTILA],
                "crop_ids": PRICED_CROPS,
                "risk_tolerance": 0.5,
                "season": "dry",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_townships"] == 1
        rec = data["recommendations"][0]
        assert rec["township_id"] == MEIKTILA
        assert rec["season"] == "dry"
        assert len(rec["crops"]) >= 1
        # Portfolio weights should sum close to 1.0
        total_weight = sum(c["portfolio_weight"] for c in rec["crops"])
        assert 0.9 <= total_weight <= 1.01

    def test_happy_path_with_fertilizers(self) -> None:
        """Should include fertilizer recommendations when soil data exists."""
        response = client.post(
            "/api/v1/recommend",
            json={
                "township_ids": [MEIKTILA],
                "crop_ids": PRICED_CROPS,
                "season": "dry",
            },
        )
        assert response.status_code == 200
        data = response.json()
        rec = data["recommendations"][0]
        assert rec["soil"] is not None
        # At least one crop should have fertilizers
        has_fert = any(len(c["fertilizers"]) > 0 for c in rec["crops"])
        assert has_fert

    def test_multiple_townships(self) -> None:
        """Should return results for multiple townships."""
        response = client.post(
            "/api/v1/recommend",
            json={
                "township_ids": [MEIKTILA, MAGWAY],
                "crop_ids": PRICED_CROPS,
                "season": "dry",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_townships"] == 2
        ids = {r["township_id"] for r in data["recommendations"]}
        assert ids == {MEIKTILA, MAGWAY}

    def test_includes_confidence_metrics(self) -> None:
        """Should include Monte Carlo confidence metrics."""
        response = client.post(
            "/api/v1/recommend",
            json={
                "township_ids": [MEIKTILA],
                "crop_ids": PRICED_CROPS,
                "season": "dry",
            },
        )
        data = response.json()
        conf = data["recommendations"][0]["confidence"]
        assert conf is not None
        assert conf["num_simulations"] > 0
        assert 0.0 <= conf["success_probability"] <= 1.0

    def test_crops_with_zero_price(self) -> None:
        """Crops with price=0.0 should not crash the optimizer."""
        response = client.post(
            "/api/v1/recommend",
            json={
                "township_ids": [MEIKTILA],
                "crop_ids": ["rice", "maize"],
                "season": "dry",
            },
        )
        assert response.status_code == 200

    def test_invalid_township_returns_400(self) -> None:
        """Unknown township should return 400."""
        response = client.post(
            "/api/v1/recommend",
            json={
                "township_ids": ["invalid_township"],
                "crop_ids": PRICED_CROPS,
                "season": "dry",
            },
        )
        assert response.status_code == 400

    def test_too_few_crops_returns_422(self) -> None:
        """Fewer than 2 crops should fail validation (422)."""
        response = client.post(
            "/api/v1/recommend",
            json={
                "township_ids": [MEIKTILA],
                "crop_ids": ["rice"],
                "season": "dry",
            },
        )
        assert response.status_code == 422


class TestSoilEndpoint:
    """Tests for GET /api/v1/recommend/soil/{township_id}."""

    def test_existing_soil_profile(self) -> None:
        """Should return soil data for a township with coverage."""
        response = client.get(f"/api/v1/recommend/soil/{MEIKTILA}")
        assert response.status_code == 200
        data = response.json()
        assert data["township_id"] == MEIKTILA
        assert "ph_h2o" in data
        assert "texture_class" in data

    def test_missing_soil_returns_404(self) -> None:
        """Township without soil data should 404."""
        response = client.get("/api/v1/recommend/soil/nonexistent_township")
        assert response.status_code == 404
