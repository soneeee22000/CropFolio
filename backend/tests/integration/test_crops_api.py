"""Integration tests for crop API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestListCrops:
    """Tests for GET /api/v1/crops/."""

    def test_returns_200(self) -> None:
        """Should return 200 OK."""
        response = client.get("/api/v1/crops/")
        assert response.status_code == 200

    def test_returns_all_crops(self) -> None:
        """Should return all 6 Myanmar crops."""
        response = client.get("/api/v1/crops/")
        data = response.json()
        assert data["count"] == 6
        assert len(data["crops"]) == 6

    def test_crop_has_required_fields(self) -> None:
        """Each crop should have all profile fields."""
        response = client.get("/api/v1/crops/")
        crop = response.json()["crops"][0]
        required_fields = [
            "id", "name_en", "name_mm", "category",
            "growing_season", "drought_tolerance", "flood_tolerance",
            "avg_yield_kg_per_ha", "yield_variance",
            "avg_price_mmk_per_kg", "price_variance",
        ]
        for field in required_fields:
            assert field in crop, f"Missing field: {field}"

    def test_includes_known_crops(self) -> None:
        """Should include rice, black gram, sesame."""
        response = client.get("/api/v1/crops/")
        crop_ids = [c["id"] for c in response.json()["crops"]]
        assert "rice" in crop_ids
        assert "black_gram" in crop_ids
        assert "sesame" in crop_ids


class TestGetCrop:
    """Tests for GET /api/v1/crops/{crop_id}."""

    def test_valid_id_returns_200(self) -> None:
        """Should return crop for valid ID."""
        response = client.get("/api/v1/crops/rice")
        assert response.status_code == 200
        data = response.json()
        assert data["name_en"] == "Rice (Paddy)"
        assert data["category"] == "cereal"

    def test_invalid_id_returns_404(self) -> None:
        """Should return 404 for unknown crop ID."""
        response = client.get("/api/v1/crops/banana")
        assert response.status_code == 404

    def test_drought_tolerance_in_range(self) -> None:
        """Crop tolerance values should be between 0 and 1."""
        response = client.get("/api/v1/crops/sesame")
        data = response.json()
        assert 0.0 <= data["drought_tolerance"] <= 1.0
        assert 0.0 <= data["flood_tolerance"] <= 1.0
