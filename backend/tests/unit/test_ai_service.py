"""Unit tests for AI service and prompt utilities."""

from __future__ import annotations

import pytest

from app.domain.ai_prompts import (
    AiNarrative,
    CropRecommendation,
    build_report_prompt,
)


class TestAiServiceNoKey:
    """Tests for AiService without API key configured."""

    @pytest.mark.asyncio
    async def test_returns_none_when_no_api_key(self) -> None:
        """Service should return None when no Gemini key is set."""
        from unittest.mock import patch

        with patch("app.services.ai_service.settings") as mock_settings:
            mock_settings.gemini_api_key = ""
            # Re-import to get fresh instance
            from app.services.ai_service import AiService

            service = AiService()
            result = await service.generate_report_narrative(
                township_name="Magway",
                season="monsoon",
                allocations=[],
                expected_income=100000,
                risk_reduction_pct=20.0,
            )
            assert result is None


class TestNarrativeDataclass:
    """Tests for AI narrative dataclass construction."""

    def test_narrative_dataclass_construction(self) -> None:
        """AiNarrative should be constructable with all fields."""
        rec = CropRecommendation(
            crop_name="Rice",
            recommendation="Good choice for monsoon.",
            recommendation_mm="မိုးရာသီအတွက် ကောင်းပါတယ်။",
            planting_month="May",
            harvest_month="October",
        )
        narrative = AiNarrative(
            executive_summary="Diversify with rice and sesame.",
            executive_summary_mm="ဆန်နှင့် နှမ်းဖြင့် မျိုးစုံစိုက်ပါ။",
            risk_narrative="Moderate drought risk this season.",
            risk_narrative_mm="ဤရာသီတွင် မိုးခေါင်မှု အလယ်အလတ်ရှိသည်။",
            crop_recommendations=[rec],
            seasonal_calendar_summary="Plant in May, harvest in October.",
            seasonal_calendar_summary_mm="မေလတွင် စိုက်ပျိုးပြီး အောက်တိုဘာတွင် ရိတ်သိမ်းပါ။",
        )
        assert narrative.executive_summary.startswith("Diversify")
        assert len(narrative.crop_recommendations) == 1
        assert narrative.crop_recommendations[0].crop_name == "Rice"


class TestBuildReportPrompt:
    """Tests for prompt builder function."""

    def test_build_report_prompt_contains_township(self) -> None:
        """Generated prompt should contain the township name."""
        prompt = build_report_prompt(
            township_name="Magway",
            season="monsoon",
            allocations=[
                {
                    "crop_name": "Rice",
                    "crop_name_mm": "ဆန်",
                    "weight_pct": 60.0,
                },
            ],
            expected_income=850000.0,
            risk_reduction_pct=23.5,
            drought_probability=0.3,
            flood_probability=0.15,
            risk_level="moderate",
        )
        assert "Magway" in prompt
        assert "monsoon" in prompt
        assert "Rice" in prompt
        assert "30%" in prompt  # drought probability formatted
