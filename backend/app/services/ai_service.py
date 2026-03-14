"""AI service for Gemini-powered narrative generation."""

from __future__ import annotations

import asyncio
import json
import logging
from functools import lru_cache
from typing import Any

from app.core.config import settings
from app.domain.ai_prompts import (
    ANALYSIS_SYSTEM_PROMPT,
    REPORT_SYSTEM_PROMPT,
    AiNarrative,
    CropRecommendation,
    build_analysis_prompt,
    build_report_prompt,
)

logger = logging.getLogger(__name__)

GEMINI_TIMEOUT_SECONDS = 15
GEMINI_MODEL_NAME = "gemini-1.5-flash"


class AiService:
    """Gemini-powered AI narrative generation with graceful degradation."""

    def __init__(self) -> None:
        """Initialize Gemini client if API key is available."""
        self._model: Any = None
        if settings.gemini_api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=settings.gemini_api_key)
                self._model = genai.GenerativeModel(GEMINI_MODEL_NAME)
                logger.info("Gemini AI service initialized")
            except Exception:
                logger.warning("Failed to initialize Gemini", exc_info=True)
        else:
            logger.info("No GEMINI_API_KEY — AI features disabled")

    @property
    def is_available(self) -> bool:
        """Check if the AI model is configured and ready."""
        return self._model is not None

    async def generate_report_narrative(
        self,
        township_name: str,
        season: str,
        allocations: list[dict[str, object]],
        expected_income: float,
        risk_reduction_pct: float,
        drought_probability: float = 0.0,
        flood_probability: float = 0.0,
        risk_level: str = "moderate",
    ) -> AiNarrative | None:
        """Generate an AI narrative for a portfolio report.

        Returns None if AI is unavailable or on any error.
        """
        if self._model is None:
            return None

        prompt = build_report_prompt(
            township_name=township_name,
            season=season,
            allocations=allocations,
            expected_income=expected_income,
            risk_reduction_pct=risk_reduction_pct,
            drought_probability=drought_probability,
            flood_probability=flood_probability,
            risk_level=risk_level,
        )

        return await self._call_gemini_for_narrative(prompt)

    async def analyze_simulation(
        self,
        township_name: str,
        season: str,
        mean_income: float,
        expected_income: float,
        risk_reduction_pct: float,
        prob_catastrophic_loss_monocrop: float = 0.0,
        prob_catastrophic_loss_diversified: float = 0.0,
        drought_probability: float = 0.0,
        flood_probability: float = 0.0,
    ) -> dict[str, str] | None:
        """Generate AI analysis of simulation results.

        Returns dict with 'analysis' and 'analysis_mm' keys,
        or None if AI is unavailable or on any error.
        """
        if self._model is None:
            return None

        prompt = build_analysis_prompt(
            township_name=township_name,
            season=season,
            mean_income=mean_income,
            expected_income=expected_income,
            risk_reduction_pct=risk_reduction_pct,
            prob_catastrophic_loss_monocrop=prob_catastrophic_loss_monocrop,
            prob_catastrophic_loss_diversified=prob_catastrophic_loss_diversified,
            drought_probability=drought_probability,
            flood_probability=flood_probability,
        )

        return await self._call_gemini_for_analysis(prompt)

    async def _call_gemini_for_narrative(
        self, prompt: str
    ) -> AiNarrative | None:
        """Call Gemini and parse response into AiNarrative."""
        try:
            raw = await asyncio.wait_for(
                asyncio.to_thread(self._generate_content, prompt, REPORT_SYSTEM_PROMPT),
                timeout=GEMINI_TIMEOUT_SECONDS,
            )
            data = json.loads(raw)
            return _parse_narrative(data)
        except Exception:
            logger.warning("Gemini narrative generation failed", exc_info=True)
            return None

    async def _call_gemini_for_analysis(
        self, prompt: str
    ) -> dict[str, str] | None:
        """Call Gemini and parse response into analysis dict."""
        try:
            raw = await asyncio.wait_for(
                asyncio.to_thread(
                    self._generate_content, prompt, ANALYSIS_SYSTEM_PROMPT
                ),
                timeout=GEMINI_TIMEOUT_SECONDS,
            )
            data = json.loads(raw)
            return {
                "analysis": str(data.get("analysis", "")),
                "analysis_mm": str(data.get("analysis_mm", "")),
            }
        except Exception:
            logger.warning("Gemini analysis generation failed", exc_info=True)
            return None

    def _generate_content(self, prompt: str, system_prompt: str) -> str:
        """Synchronous Gemini API call (run in thread)."""
        response = self._model.generate_content(
            [system_prompt, prompt],
            generation_config={"response_mime_type": "application/json"},
        )
        return str(response.text)


def _parse_narrative(data: dict[str, Any]) -> AiNarrative:
    """Parse raw JSON dict into an AiNarrative dataclass."""
    crop_recs = [
        CropRecommendation(
            crop_name=str(c.get("crop_name", "")),
            recommendation=str(c.get("recommendation", "")),
            recommendation_mm=str(c.get("recommendation_mm", "")),
            planting_month=str(c.get("planting_month", "")),
            harvest_month=str(c.get("harvest_month", "")),
        )
        for c in data.get("crop_recommendations", [])
    ]
    return AiNarrative(
        executive_summary=str(data.get("executive_summary", "")),
        executive_summary_mm=str(data.get("executive_summary_mm", "")),
        risk_narrative=str(data.get("risk_narrative", "")),
        risk_narrative_mm=str(data.get("risk_narrative_mm", "")),
        crop_recommendations=crop_recs,
        seasonal_calendar_summary=str(
            data.get("seasonal_calendar_summary", "")
        ),
        seasonal_calendar_summary_mm=str(
            data.get("seasonal_calendar_summary_mm", "")
        ),
    )


@lru_cache(maxsize=1)
def get_ai_service() -> AiService:
    """Return singleton AiService instance."""
    return AiService()
