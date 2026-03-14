"""Integration tests for township API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestListTownships:
    """Tests for GET /api/v1/townships/."""

    def test_returns_200(self) -> None:
        """Should return 200 OK."""
        response = client.get("/api/v1/townships/")
        assert response.status_code == 200

    def test_returns_all_townships(self) -> None:
        """Should return 25 townships."""
        response = client.get("/api/v1/townships/")
        data = response.json()
        assert data["count"] == 25
        assert len(data["townships"]) == 25

    def test_township_has_required_fields(self) -> None:
        """Each township should have id, name, name_mm, region, lat, lon."""
        response = client.get("/api/v1/townships/")
        township = response.json()["townships"][0]
        assert "id" in township
        assert "name" in township
        assert "name_mm" in township
        assert "region" in township
        assert "latitude" in township
        assert "longitude" in township


class TestGetTownship:
    """Tests for GET /api/v1/townships/{township_id}."""

    def test_valid_id_returns_200(self) -> None:
        """Should return township for valid ID."""
        response = client.get("/api/v1/townships/mgw_magway")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Magway"
        assert data["region"] == "Magway"

    def test_invalid_id_returns_404(self) -> None:
        """Should return 404 for unknown township ID."""
        response = client.get("/api/v1/townships/nonexistent")
        assert response.status_code == 404
