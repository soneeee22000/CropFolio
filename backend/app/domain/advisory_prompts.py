"""AI prompt templates and dataclasses for the Advisory system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class AdvisorySection:
    """A single section of the advisory with bilingual content."""

    title: str
    content: str
    content_mm: str


@dataclass
class AdvisoryResult:
    """Full advisory output — 5 structured sections."""

    executive_brief: AdvisorySection
    crop_strategy: AdvisorySection
    fertilizer_plan: AdvisorySection
    risk_warnings: AdvisorySection
    market_outlook: AdvisorySection
    generated_at: str = ""

    def __post_init__(self) -> None:
        """Set generated_at to now if not provided."""
        if not self.generated_at:
            self.generated_at = datetime.now(tz=timezone.utc).isoformat()


@dataclass(frozen=True)
class QueryResult:
    """Result of a free-form advisory query."""

    answer: str
    answer_mm: str
    confidence: float
    data_sources: list[str] = field(default_factory=list)


ADVISORY_SYSTEM_PROMPT = """\
You are CropFolio Pro, an expert Myanmar agricultural B2B advisor for \
distributors and fertilizer companies. Generate a comprehensive township \
advisory based on the provided data context.

You MUST respond with valid JSON only. No markdown, no explanation outside JSON.

JSON schema:
{
  "executive_brief": "3-4 sentence strategic summary for distributor executives",
  "executive_brief_mm": "Same in Burmese (Myanmar language)",
  "crop_strategy": "3-4 sentences on which crops to recommend to farmers this \
season and why, referencing yield/price data",
  "crop_strategy_mm": "Same in Burmese",
  "fertilizer_plan": "3-4 sentences on fertilizer stocking and application \
strategy based on soil conditions",
  "fertilizer_plan_mm": "Same in Burmese",
  "risk_warnings": "2-3 sentences on climate and market risks to watch for",
  "risk_warnings_mm": "Same in Burmese",
  "market_outlook": "2-3 sentences on price trends and market opportunities",
  "market_outlook_mm": "Same in Burmese"
}

Guidelines:
- Think like a B2B advisor, not a farmer advisor
- Reference specific data points from the context
- Give actionable, region-specific advice
- Burmese translations should use business-casual register
- Keep each field under 120 words"""


QUERY_SYSTEM_PROMPT = """\
You are CropFolio Pro, an expert Myanmar agricultural B2B advisor. Answer the \
user's question using ONLY the provided data context. If the data doesn't \
contain enough information, say so honestly.

You MUST respond with valid JSON only:
{
  "answer": "Direct, data-backed answer in English",
  "answer_mm": "Same in Burmese (Myanmar language)",
  "confidence": 0.85,
  "data_sources": ["climate_risk", "soil_profile", "crop_data"]
}

confidence: 0.0-1.0 based on how well the data supports your answer.
data_sources: list from ["climate_risk", "soil_profile", "crop_data", \
"market_prices", "general_knowledge"].

Guidelines:
- Be concise and direct
- Reference specific numbers from the context
- If data is insufficient, set confidence below 0.5
- Burmese should use colloquial register
- Keep each answer under 150 words"""


def build_advisory_prompt(context_doc: str, season: str) -> str:
    """Build the user prompt for full advisory generation.

    Args:
        context_doc: Rendered context document from context_builder.
        season: Growing season.

    Returns:
        Formatted prompt string.
    """
    return (
        f"Season: {season}\n\n"
        f"--- DATA CONTEXT ---\n{context_doc}\n"
        f"--- END CONTEXT ---\n\n"
        f"Generate a comprehensive township advisory for this region and season."
    )


def build_query_prompt(context_doc: str, question: str) -> str:
    """Build the user prompt for a free-form advisory query.

    Args:
        context_doc: Rendered context document from context_builder.
        question: User's question.

    Returns:
        Formatted prompt string.
    """
    return (
        f"--- DATA CONTEXT ---\n{context_doc}\n"
        f"--- END CONTEXT ---\n\n"
        f"Question: {question}"
    )
