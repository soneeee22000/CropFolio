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
    DISTRIBUTOR_ADVISORY_SYSTEM_PROMPT,
    FERTILIZER_EXPLANATION_SYSTEM_PROMPT,
    REPORT_SYSTEM_PROMPT,
    AiNarrative,
    CropRecommendation,
    build_analysis_prompt,
    build_distributor_advisory_prompt,
    build_fertilizer_explanation_prompt,
    build_report_prompt,
)

logger = logging.getLogger(__name__)

GEMINI_TIMEOUT_SECONDS = 15
GEMINI_MODEL_NAME = "gemini-2.5-flash"


class AiService:
    """Gemini-powered AI narrative generation with graceful degradation."""

    def __init__(self) -> None:
        """Initialize Gemini client if API key is available."""
        self._client: Any = None
        key = settings.gemini_api_key.strip()
        logger.info(
            "Gemini init: key length=%d, model=%s", len(key), GEMINI_MODEL_NAME
        )
        if key:
            try:
                from google import genai

                self._client = genai.Client(api_key=key)
                logger.info("Gemini AI service initialized successfully")
            except Exception:
                logger.warning("Failed to initialize Gemini", exc_info=True)
        else:
            logger.info("No GEMINI_API_KEY — AI features disabled")

    @property
    def is_available(self) -> bool:
        """Check if the AI client is configured and ready."""
        return self._client is not None

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
        """Generate an AI narrative for a portfolio report."""
        if self._client is None:
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
        """Generate AI analysis of simulation results."""
        if self._client is None:
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

    async def generate_distributor_advisory(
        self,
        township_name: str,
        season: str,
        crop_recommendations: list[dict[str, object]],
        soil_summary: dict[str, object],
        expected_income: float,
        risk_reduction_pct: float,
        success_probability: float,
    ) -> dict[str, str] | None:
        """Generate a distributor-oriented advisory brief."""
        if self._client is None:
            return None

        prompt = build_distributor_advisory_prompt(
            township_name=township_name,
            season=season,
            crop_recommendations=crop_recommendations,
            soil_summary=soil_summary,
            expected_income=expected_income,
            risk_reduction_pct=risk_reduction_pct,
            success_probability=success_probability,
        )

        try:
            raw = await asyncio.wait_for(
                asyncio.to_thread(
                    self._generate,
                    DISTRIBUTOR_ADVISORY_SYSTEM_PROMPT + "\n\n" + prompt,
                ),
                timeout=GEMINI_TIMEOUT_SECONDS,
            )
            return json.loads(raw)
        except Exception:
            logger.warning("Gemini distributor advisory failed", exc_info=True)
            return None

    async def explain_fertilizer_recommendation(
        self,
        crop_name: str,
        fertilizer_name: str,
        formulation: str,
        soil_ph: float,
        soil_nitrogen: float,
        soil_texture: str,
        score: float,
        reasoning: str,
    ) -> dict[str, str] | None:
        """Generate plain-language fertilizer recommendation explanation."""
        if self._client is None:
            return None

        prompt = build_fertilizer_explanation_prompt(
            crop_name=crop_name,
            fertilizer_name=fertilizer_name,
            formulation=formulation,
            soil_ph=soil_ph,
            soil_nitrogen=soil_nitrogen,
            soil_texture=soil_texture,
            score=score,
            reasoning=reasoning,
        )

        try:
            raw = await asyncio.wait_for(
                asyncio.to_thread(
                    self._generate,
                    FERTILIZER_EXPLANATION_SYSTEM_PROMPT + "\n\n" + prompt,
                ),
                timeout=GEMINI_TIMEOUT_SECONDS,
            )
            return json.loads(raw)
        except Exception:
            logger.warning("Gemini fertilizer explanation failed", exc_info=True)
            return None

    async def _call_gemini_for_narrative(
        self, prompt: str
    ) -> AiNarrative | None:
        """Call Gemini and parse response into AiNarrative."""
        try:
            raw = await asyncio.wait_for(
                asyncio.to_thread(
                    self._generate, REPORT_SYSTEM_PROMPT + "\n\n" + prompt
                ),
                timeout=GEMINI_TIMEOUT_SECONDS,
            )
            data = json.loads(raw)
            return _parse_narrative(data)
        except Exception:
            logger.warning("Gemini narrative failed", exc_info=True)
            return None

    async def _call_gemini_for_analysis(
        self, prompt: str
    ) -> dict[str, str] | None:
        """Call Gemini and parse response into analysis dict."""
        try:
            raw = await asyncio.wait_for(
                asyncio.to_thread(
                    self._generate, ANALYSIS_SYSTEM_PROMPT + "\n\n" + prompt
                ),
                timeout=GEMINI_TIMEOUT_SECONDS,
            )
            data = json.loads(raw)
            return {
                "analysis": str(data.get("analysis", "")),
                "analysis_mm": str(data.get("analysis_mm", "")),
            }
        except Exception:
            logger.warning("Gemini analysis failed", exc_info=True)
            return None

    async def generate_content(
        self, system_prompt: str, user_prompt: str
    ) -> str | None:
        """Generate content with system + user prompt separation.

        Args:
            system_prompt: System instructions for the model.
            user_prompt: User-facing prompt with context and request.

        Returns:
            Raw response text, or None if unavailable/failed.
        """
        if self._client is None:
            return None

        combined = system_prompt + "\n\n" + user_prompt
        try:
            raw = await asyncio.wait_for(
                asyncio.to_thread(self._generate, combined),
                timeout=GEMINI_TIMEOUT_SECONDS,
            )
            return raw
        except Exception:
            logger.warning("Gemini generate_content failed", exc_info=True)
            return None

    def _generate(self, prompt: str) -> str:
        """Synchronous Gemini API call (run in thread)."""
        from google.genai import types

        response = self._client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
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
