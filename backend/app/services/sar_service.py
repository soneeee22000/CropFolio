"""SAR analysis service with async job management.

Runs SAR analysis asynchronously and stores results for polling.
Supports both mock (development) and real (GEE) pipelines.
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.infrastructure.sar_pipeline import (
    BaseSARPipeline,
    MockSARPipeline,
    SARAnalysisResult,
    SARPipeline,
)
from app.services.township_service import TownshipService, get_township_service

logger = logging.getLogger(__name__)

RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "sar_results"


class JobStatus(str, Enum):
    """SAR job status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SARJob:
    """Tracks a single SAR analysis job."""

    def __init__(
        self,
        job_id: str,
        township_id: str,
        season: str,
        year: int,
    ) -> None:
        """Initialize job tracking."""
        self.job_id = job_id
        self.township_id = township_id
        self.season = season
        self.year = year
        self.status = JobStatus.PENDING
        self.created_at = datetime.utcnow().isoformat()
        self.completed_at: str | None = None
        self.error: str | None = None
        self.result: SARAnalysisResult | None = None


class SARService:
    """Manages SAR analysis jobs with async execution."""

    def __init__(
        self,
        use_mock: bool = True,
        township_service: TownshipService | None = None,
    ) -> None:
        """Initialize with pipeline selection."""
        self._township_service = township_service or get_township_service()
        self._jobs: dict[str, SARJob] = {}
        self._use_mock = use_mock

        self._pipeline: BaseSARPipeline
        if use_mock:
            self._pipeline = MockSARPipeline()
        else:
            try:
                self._pipeline = SARPipeline()
            except RuntimeError:
                logger.warning("GEE unavailable, falling back to mock")
                self._pipeline = MockSARPipeline()
                self._use_mock = True

        RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    async def submit_analysis(
        self,
        township_id: str,
        season: str = "monsoon",
        year: int = 2025,
    ) -> str:
        """Submit a SAR analysis job.

        Args:
            township_id: Township to analyze.
            season: Growing season.
            year: Analysis year.

        Returns:
            Job ID for polling.

        Raises:
            ValueError: If township not found.
        """
        township = self._township_service.get_by_id(township_id)
        if township is None:
            msg = f"Unknown township: '{township_id}'"
            raise ValueError(msg)

        job_id = str(uuid.uuid4())[:8]
        job = SARJob(
            job_id=job_id,
            township_id=township_id,
            season=season,
            year=year,
        )
        self._jobs[job_id] = job

        task = asyncio.create_task(
            self._run_analysis(job, township)
        )
        self._jobs[job_id]._task = task  # type: ignore[attr-defined]

        logger.info("SAR job %s submitted for %s", job_id, township_id)
        return job_id

    async def _run_analysis(
        self,
        job: SARJob,
        township: dict[str, Any],
    ) -> None:
        """Execute SAR analysis in background."""
        job.status = JobStatus.RUNNING

        try:
            result = await asyncio.to_thread(
                self._pipeline.analyze,
                job.township_id,
                township["latitude"],
                township["longitude"],
                job.season,
                job.year,
            )

            job.result = result
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow().isoformat()

            self._save_result(job.job_id, result)

            logger.info(
                "SAR job %s completed: rice=%s confidence=%.2f",
                job.job_id,
                result.rice_detected,
                result.rice_confidence,
            )

        except Exception as exc:
            job.status = JobStatus.FAILED
            job.error = str(exc)
            job.completed_at = datetime.utcnow().isoformat()
            logger.error("SAR job %s failed: %s", job.job_id, exc)

    def get_job(self, job_id: str) -> SARJob | None:
        """Get job by ID."""
        return self._jobs.get(job_id)

    def get_result(self, job_id: str) -> SARAnalysisResult | None:
        """Get completed result by job ID."""
        job = self._jobs.get(job_id)
        if job is not None and job.result is not None:
            return job.result

        return self._load_result(job_id)

    def get_latest_coverage(
        self, township_id: str,
    ) -> SARAnalysisResult | None:
        """Get the latest completed analysis for a township."""
        latest: SARJob | None = None
        for job in self._jobs.values():
            is_match = (
                job.township_id == township_id
                and job.status == JobStatus.COMPLETED
                and job.result is not None
            )
            if not is_match:
                continue
            is_newer = (
                latest is None
                or (job.completed_at or "") > (latest.completed_at or "")
            )
            if is_newer:
                latest = job

        if latest is not None and latest.result is not None:
            return latest.result

        return None

    def _save_result(
        self, job_id: str, result: SARAnalysisResult,
    ) -> None:
        """Persist result to JSON file."""
        path = RESULTS_DIR / f"{job_id}.json"
        data = asdict(result)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def _load_result(self, job_id: str) -> SARAnalysisResult | None:
        """Load result from JSON file."""
        path = RESULTS_DIR / f"{job_id}.json"
        if not path.exists():
            return None

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        from app.infrastructure.sar_pipeline import (
            PhenologySignal,
            SARTimePoint,
        )

        return SARAnalysisResult(
            township_id=data["township_id"],
            analysis_date=data["analysis_date"],
            season=data["season"],
            time_series=[
                SARTimePoint(**tp) for tp in data["time_series"]
            ],
            phenology_signals=[
                PhenologySignal(**ps)
                for ps in data["phenology_signals"]
            ],
            rice_detected=data["rice_detected"],
            rice_confidence=data["rice_confidence"],
            estimated_area_pct=data["estimated_area_pct"],
            summary=data["summary"],
        )


@lru_cache(maxsize=1)
def get_sar_service() -> SARService:
    """Return singleton SARService instance (mock mode by default)."""
    return SARService(use_mock=True)
