"""Advisory service orchestrating context building and AI generation."""

from __future__ import annotations

import json
import logging
from functools import lru_cache

from app.domain.advisory_prompts import (
    ADVISORY_SYSTEM_PROMPT,
    QUERY_SYSTEM_PROMPT,
    AdvisoryResult,
    AdvisorySection,
    QueryResult,
    build_advisory_prompt,
    build_query_prompt,
)
from app.domain.context_builder import (
    build_township_context,
    render_context_document,
)
from app.services.ai_service import AiService, get_ai_service
from app.services.climate_service import ClimateService, get_climate_service
from app.services.township_service import TownshipService, get_township_service

logger = logging.getLogger(__name__)


class AdvisoryService:
    """Orchestrates context assembly + Gemini for advisory generation."""

    def __init__(
        self,
        township_service: TownshipService | None = None,
        climate_service: ClimateService | None = None,
        ai_service: AiService | None = None,
    ) -> None:
        """Initialize with dependencies."""
        self._townships = township_service or get_township_service()
        self._climate = climate_service or get_climate_service()
        self._ai = ai_service or get_ai_service()

    async def generate_advisory(
        self, township_id: str, season: str
    ) -> AdvisoryResult | None:
        """Generate a full advisory for a township.

        Args:
            township_id: Township identifier.
            season: Growing season (monsoon/dry).

        Returns:
            AdvisoryResult with 5 sections, or None if AI unavailable.
        """
        context_doc = await self._build_context(township_id, season)
        if context_doc is None:
            return None

        prompt = build_advisory_prompt(context_doc, season)
        raw = await self._ai.generate_content(
            ADVISORY_SYSTEM_PROMPT, prompt
        )
        if raw is None:
            return None

        return _parse_advisory_result(raw)

    async def answer_query(
        self, township_id: str, season: str, question: str
    ) -> QueryResult | None:
        """Answer a free-form question about a township.

        Args:
            township_id: Township identifier.
            season: Growing season.
            question: User's question text.

        Returns:
            QueryResult or None if AI unavailable.
        """
        context_doc = await self._build_context(township_id, season)
        if context_doc is None:
            return None

        prompt = build_query_prompt(context_doc, question)
        raw = await self._ai.generate_content(QUERY_SYSTEM_PROMPT, prompt)
        if raw is None:
            return None

        return _parse_query_result(raw)

    async def _build_context(
        self, township_id: str, season: str
    ) -> str | None:
        """Build the context document for a township."""
        township = self._townships.get_by_id(township_id)
        if township is None:
            return None

        climate_risk = await self._fetch_climate_data(township_id, season)

        ctx = build_township_context(
            township_id=township_id,
            season=season,
            township=township,
            climate_risk=climate_risk,
        )
        return render_context_document(ctx)

    async def _fetch_climate_data(
        self, township_id: str, season: str
    ) -> dict[str, float | str] | None:
        """Fetch climate risk data, returning None on failure."""
        try:
            result = await self._climate.assess_risk(township_id, season)
            if result is None:
                return None
            risk_profile, _ = result
            return {
                "drought_probability": risk_profile.drought_probability,
                "flood_probability": risk_profile.flood_probability,
                "risk_level": risk_profile.risk_level,
                "rainfall_mm": risk_profile.rainfall_forecast_mm,
            }
        except Exception:
            logger.warning(
                "Climate fetch failed for %s", township_id, exc_info=True
            )
            return None


def _parse_advisory_result(raw: str) -> AdvisoryResult | None:
    """Parse JSON string into AdvisoryResult."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Failed to parse advisory JSON")
        return None

    return AdvisoryResult(
        executive_brief=AdvisorySection(
            title="Executive Brief",
            content=str(data.get("executive_brief", "")),
            content_mm=str(data.get("executive_brief_mm", "")),
        ),
        crop_strategy=AdvisorySection(
            title="Crop Strategy",
            content=str(data.get("crop_strategy", "")),
            content_mm=str(data.get("crop_strategy_mm", "")),
        ),
        fertilizer_plan=AdvisorySection(
            title="Fertilizer Plan",
            content=str(data.get("fertilizer_plan", "")),
            content_mm=str(data.get("fertilizer_plan_mm", "")),
        ),
        risk_warnings=AdvisorySection(
            title="Risk Warnings",
            content=str(data.get("risk_warnings", "")),
            content_mm=str(data.get("risk_warnings_mm", "")),
        ),
        market_outlook=AdvisorySection(
            title="Market Outlook",
            content=str(data.get("market_outlook", "")),
            content_mm=str(data.get("market_outlook_mm", "")),
        ),
    )


def _parse_query_result(raw: str) -> QueryResult | None:
    """Parse JSON string into QueryResult."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Failed to parse query JSON")
        return None

    confidence = data.get("confidence", 0.5)
    if not isinstance(confidence, int | float):
        confidence = 0.5

    return QueryResult(
        answer=str(data.get("answer", "")),
        answer_mm=str(data.get("answer_mm", "")),
        confidence=min(max(float(confidence), 0.0), 1.0),
        data_sources=_sanitize_sources(data.get("data_sources", [])),
    )


def _sanitize_sources(raw: object) -> list[str]:
    """Validate and sanitize data_sources from AI response."""
    if not isinstance(raw, list):
        return []
    return [str(s) for s in raw if isinstance(s, str)]


@lru_cache(maxsize=1)
def get_advisory_service() -> AdvisoryService:
    """Return singleton AdvisoryService instance."""
    return AdvisoryService()
