"""Integration tests for SAR (Synthetic Aperture Radar) analysis API endpoints."""

from __future__ import annotations

import asyncio

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

AMARAPURA = "mdy_amarapura"


class TestSARAnalyze:
    """Tests for POST /api/v1/sar/analyze."""

    def test_valid_submit_returns_200_with_job_id(self) -> None:
        """Valid township submit should return 200 and a non-empty job_id."""
        response = client.post(
            "/api/v1/sar/analyze",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert len(data["job_id"]) > 0

    def test_submit_response_contains_pending_status(self) -> None:
        """Newly submitted job should have status='pending'."""
        response = client.post(
            "/api/v1/sar/analyze",
            json={"township_id": AMARAPURA, "season": "dry", "year": 2025},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"
        assert data["township_id"] == AMARAPURA

    def test_invalid_township_returns_400(self) -> None:
        """Unknown township must return 400."""
        response = client.post(
            "/api/v1/sar/analyze",
            json={"township_id": "nonexistent_twp", "season": "monsoon", "year": 2025},
        )
        assert response.status_code == 400


class TestSARResults:
    """Tests for GET /api/v1/sar/results/{job_id}."""

    def test_unknown_job_id_returns_404(self) -> None:
        """Polling a job ID that was never submitted must return 404."""
        response = client.get("/api/v1/sar/results/00000000")
        assert response.status_code == 404

    def test_known_job_id_returns_status(self) -> None:
        """After submitting, polling the returned job_id should return a valid status."""
        submit = client.post(
            "/api/v1/sar/analyze",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        assert submit.status_code == 200
        job_id = submit.json()["job_id"]

        poll = client.get(f"/api/v1/sar/results/{job_id}")
        assert poll.status_code == 200
        data = poll.json()
        assert data["job_id"] == job_id
        assert data["status"] in ("pending", "running", "completed", "failed")
        assert data["township_id"] == AMARAPURA


class TestSARCoverage:
    """Tests for GET /api/v1/sar/coverage/{township_id}."""

    def test_no_prior_coverage_returns_404(self) -> None:
        """Township with no SAR jobs must return 404.

        Uses a township ID that is never submitted anywhere in
        the test suite, so the singleton cache has no results.
        """
        response = client.get("/api/v1/sar/coverage/npt_tatkon")
        assert response.status_code == 404
