"""Unit tests for the SAR service."""

from __future__ import annotations

import asyncio

import pytest

from app.services.sar_service import JobStatus, SARService


@pytest.fixture()
def sar_service():
    """SAR service with mock pipeline."""
    return SARService(use_mock=True)


class TestSARService:
    """Tests for SAR job management."""

    @pytest.mark.asyncio()
    async def test_submit_returns_job_id(self, sar_service):
        """Submitting analysis should return a job ID."""
        job_id = await sar_service.submit_analysis(
            township_id="mdy_amarapura", season="monsoon", year=2025,
        )
        assert isinstance(job_id, str)
        assert len(job_id) > 0

    @pytest.mark.asyncio()
    async def test_job_completes(self, sar_service):
        """Job should complete after submission."""
        job_id = await sar_service.submit_analysis(
            township_id="mdy_amarapura", season="monsoon", year=2025,
        )

        await asyncio.sleep(2)

        job = sar_service.get_job(job_id)
        assert job is not None
        assert job.status in (JobStatus.COMPLETED, JobStatus.RUNNING)

    @pytest.mark.asyncio()
    async def test_invalid_township_raises(self, sar_service):
        """Unknown township should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown township"):
            await sar_service.submit_analysis(
                township_id="nonexistent_township",
            )

    @pytest.mark.asyncio()
    async def test_get_nonexistent_job(self, sar_service):
        """Getting a non-existent job should return None."""
        job = sar_service.get_job("nonexistent")
        assert job is None
