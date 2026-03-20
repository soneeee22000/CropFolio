"""Unit tests for advisory_prompts module."""

from app.domain.advisory_prompts import (
    ADVISORY_SYSTEM_PROMPT,
    QUERY_SYSTEM_PROMPT,
    AdvisoryResult,
    AdvisorySection,
    QueryResult,
    build_advisory_prompt,
    build_query_prompt,
)


class TestPromptBuilders:
    """Tests for prompt builder functions."""

    def test_build_advisory_prompt_non_empty(self) -> None:
        """Advisory prompt includes context and season."""
        prompt = build_advisory_prompt("Test context doc", "monsoon")
        assert "monsoon" in prompt
        assert "Test context doc" in prompt
        assert "DATA CONTEXT" in prompt
        assert len(prompt) > 50

    def test_build_query_prompt_non_empty(self) -> None:
        """Query prompt includes context and question."""
        prompt = build_query_prompt("Test context doc", "What crops?")
        assert "What crops?" in prompt
        assert "Test context doc" in prompt
        assert "DATA CONTEXT" in prompt

    def test_system_prompts_non_empty(self) -> None:
        """System prompts contain JSON schema instructions."""
        assert "JSON" in ADVISORY_SYSTEM_PROMPT
        assert "JSON" in QUERY_SYSTEM_PROMPT
        assert "executive_brief" in ADVISORY_SYSTEM_PROMPT
        assert "confidence" in QUERY_SYSTEM_PROMPT


class TestDataclasses:
    """Tests for advisory dataclasses."""

    def test_advisory_section_creation(self) -> None:
        """AdvisorySection can be constructed."""
        section = AdvisorySection(
            title="Test", content="English", content_mm="Burmese"
        )
        assert section.title == "Test"
        assert section.content == "English"
        assert section.content_mm == "Burmese"

    def test_advisory_result_creation(self) -> None:
        """AdvisoryResult sets generated_at automatically."""
        section = AdvisorySection(
            title="T", content="C", content_mm="M"
        )
        result = AdvisoryResult(
            executive_brief=section,
            crop_strategy=section,
            fertilizer_plan=section,
            risk_warnings=section,
            market_outlook=section,
        )
        assert result.generated_at != ""
        assert "T" in result.executive_brief.title

    def test_query_result_creation(self) -> None:
        """QueryResult can be constructed with defaults."""
        result = QueryResult(
            answer="Test answer",
            answer_mm="Test MM",
            confidence=0.8,
        )
        assert result.answer == "Test answer"
        assert result.confidence == 0.8
        assert result.data_sources == []
