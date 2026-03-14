"""AI prompt templates and narrative dataclasses for Gemini integration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CropRecommendation:
    """Single crop recommendation with bilingual text."""

    crop_name: str
    recommendation: str
    recommendation_mm: str
    planting_month: str
    harvest_month: str


@dataclass(frozen=True)
class AiNarrative:
    """AI-generated narrative for a crop portfolio report."""

    executive_summary: str
    executive_summary_mm: str
    risk_narrative: str
    risk_narrative_mm: str
    crop_recommendations: list[CropRecommendation]
    seasonal_calendar_summary: str
    seasonal_calendar_summary_mm: str


REPORT_SYSTEM_PROMPT = """You are an expert Myanmar agricultural advisor. \
Generate a crop portfolio recommendation report based on the provided \
optimization data.

You MUST respond with valid JSON only. No markdown, no explanation outside JSON.

JSON schema:
{
  "executive_summary": "2-3 sentence English summary of the recommendation \
and why",
  "executive_summary_mm": "Same in Burmese (Myanmar language)",
  "risk_narrative": "2-3 sentences explaining the climate risks this season \
in plain language",
  "risk_narrative_mm": "Same in Burmese",
  "crop_recommendations": [
    {
      "crop_name": "Rice",
      "recommendation": "1-2 sentences on why this crop is included and what \
to watch for",
      "recommendation_mm": "Same in Burmese",
      "planting_month": "May",
      "harvest_month": "October"
    }
  ],
  "seasonal_calendar_summary": "Brief overview of the planting/harvest \
timeline",
  "seasonal_calendar_summary_mm": "Same in Burmese"
}

Guidelines:
- Use simple language a farmer or extension worker can understand
- Reference specific climate risks (drought probability, flood probability)
- Give actionable advice, not generic statements
- Burmese translations should use colloquial register, not overly formal
- Keep each field under 100 words"""


ANALYSIS_SYSTEM_PROMPT = """You are an expert Myanmar agricultural advisor. \
Analyze the Monte Carlo simulation results and provide actionable insights.

You MUST respond with valid JSON only:
{
  "analysis": "3-5 sentence English analysis of portfolio performance",
  "analysis_mm": "Same in Burmese (Myanmar language)"
}

Guidelines:
- Reference specific numbers from the simulation
- Compare monocrop vs diversified risk
- Explain what the numbers mean for a farmer
- Use simple, actionable language
- Keep under 150 words per field"""


def build_report_prompt(
    township_name: str,
    season: str,
    allocations: list[dict[str, object]],
    expected_income: float,
    risk_reduction_pct: float,
    drought_probability: float = 0.0,
    flood_probability: float = 0.0,
    risk_level: str = "moderate",
) -> str:
    """Build the user prompt for report narrative generation.

    Args:
        township_name: Name of the target township.
        season: Growing season (monsoon/dry).
        allocations: List of crop allocation dicts with name and weight.
        expected_income: Expected income in MMK per hectare.
        risk_reduction_pct: Percentage risk reduction vs monocrop.
        drought_probability: Probability of drought (0-1).
        flood_probability: Probability of flood (0-1).
        risk_level: Climate risk level string.

    Returns:
        Formatted prompt string.
    """
    crops_text = "\n".join(
        f"- {a['crop_name']} ({a.get('crop_name_mm', '')}): "
        f"{float(str(a['weight_pct'])):.1f}% allocation"
        for a in allocations
    )
    return (
        f"Township: {township_name}\n"
        f"Season: {season}\n"
        f"Climate Risk Level: {risk_level}\n"
        f"Drought Probability: {drought_probability:.0%}\n"
        f"Flood Probability: {flood_probability:.0%}\n"
        f"\nOptimized Crop Portfolio:\n{crops_text}\n"
        f"\nExpected Income: {expected_income:,.0f} MMK per hectare\n"
        f"Risk Reduction vs Monocrop: {risk_reduction_pct:.1f}%\n"
        f"\nGenerate a recommendation report for this portfolio."
    )


def build_analysis_prompt(
    township_name: str,
    season: str,
    mean_income: float,
    expected_income: float,
    risk_reduction_pct: float,
    prob_catastrophic_loss_monocrop: float = 0.0,
    prob_catastrophic_loss_diversified: float = 0.0,
    drought_probability: float = 0.0,
    flood_probability: float = 0.0,
) -> str:
    """Build the user prompt for simulation analysis.

    Args:
        township_name: Name of the target township.
        season: Growing season.
        mean_income: Simulated mean income.
        expected_income: Expected income from optimization.
        risk_reduction_pct: Risk reduction percentage.
        prob_catastrophic_loss_monocrop: Monocrop catastrophic loss prob.
        prob_catastrophic_loss_diversified: Diversified catastrophic loss prob.
        drought_probability: Drought probability (0-1).
        flood_probability: Flood probability (0-1).

    Returns:
        Formatted prompt string.
    """
    return (
        f"Township: {township_name}\n"
        f"Season: {season}\n"
        f"Drought Probability: {drought_probability:.0%}\n"
        f"Flood Probability: {flood_probability:.0%}\n"
        f"\nSimulation Results:\n"
        f"- Mean simulated income: {mean_income:,.0f} MMK/ha\n"
        f"- Expected optimized income: {expected_income:,.0f} MMK/ha\n"
        f"- Risk reduction: {risk_reduction_pct:.1f}%\n"
        f"- Catastrophic loss (monocrop): "
        f"{prob_catastrophic_loss_monocrop:.1f}%\n"
        f"- Catastrophic loss (diversified): "
        f"{prob_catastrophic_loss_diversified:.1f}%\n"
        f"\nAnalyze the portfolio performance and give actionable insights."
    )
