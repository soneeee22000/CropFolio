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


DISTRIBUTOR_ADVISORY_SYSTEM_PROMPT = """You are a B2B agricultural business \
advisor for Myanmar distributors and fertilizer companies. Generate data-driven \
advisory briefs based on crop-fertilizer recommendation data.

You MUST respond with valid JSON only. No markdown, no explanation outside JSON.

JSON schema:
{
  "executive_brief": "3-4 sentence English brief for distributor executives — \
focus on ROI, risk reduction, and competitive advantage",
  "executive_brief_mm": "Same in Burmese (Myanmar language)",
  "inventory_guidance": "2-3 sentences on which fertilizers to stock for \
this region and why",
  "inventory_guidance_mm": "Same in Burmese",
  "field_agent_notes": "3-4 bullet points for field agents — simple, \
actionable fertilizer application advice",
  "field_agent_notes_mm": "Same in Burmese",
  "risk_warnings": "1-2 sentences on key risks and what to watch for",
  "risk_warnings_mm": "Same in Burmese",
  "demo_farm_advice": "2-3 sentences on whether a demo farm is recommended \
for this crop-region combination and expected outcomes",
  "demo_farm_advice_mm": "Same in Burmese"
}

Guidelines:
- Think like a business advisor, not a farmer advisor
- Reference specific numbers (cost, probability, expected yield)
- Inventory guidance should be practical — quantities for a typical township
- Field agent notes should be understandable by someone with no agronomic training
- Burmese translations should use business-casual register
- Keep each field under 120 words"""


FERTILIZER_EXPLANATION_SYSTEM_PROMPT = """You are a Myanmar agricultural advisor \
explaining a fertilizer recommendation in plain language.

You MUST respond with valid JSON only:
{
  "explanation": "3-4 sentence English explanation of why this fertilizer was \
recommended for this crop and soil",
  "explanation_mm": "Same in Burmese (Myanmar language)",
  "application_guide": "Step-by-step application instructions (3-4 steps)",
  "application_guide_mm": "Same in Burmese"
}

Guidelines:
- Explain the science simply — why this NPK ratio matches the crop's needs
- Reference soil conditions (pH, nitrogen level)
- Include timing (when to apply relative to planting)
- Keep language accessible for field agents with basic training
- Keep each field under 100 words"""


def build_distributor_advisory_prompt(
    township_name: str,
    season: str,
    crop_recommendations: list[dict[str, object]],
    soil_summary: dict[str, object],
    expected_income: float,
    risk_reduction_pct: float,
    success_probability: float,
) -> str:
    """Build the user prompt for distributor advisory generation.

    Args:
        township_name: Name of the target township.
        season: Growing season (monsoon/dry).
        crop_recommendations: List of crop + fertilizer recommendation dicts.
        soil_summary: Soil profile summary dict.
        expected_income: Expected income in MMK per hectare.
        risk_reduction_pct: Percentage risk reduction vs monocrop.
        success_probability: Overall success probability from Monte Carlo.

    Returns:
        Formatted prompt string.
    """
    crops_text = ""
    for rec in crop_recommendations:
        crops_text += (
            f"\n- {rec['crop_name']} ({rec.get('weight', 0):.0%} allocation)"
        )
        ferts = rec.get("fertilizers", [])
        if ferts:
            top = ferts[0] if isinstance(ferts[0], dict) else {}
            crops_text += (
                f"\n  Top fertilizer: {top.get('name', 'N/A')} "
                f"({top.get('formulation', 'N/A')}), "
                f"score {top.get('score', 0):.2f}, "
                f"cost {top.get('cost_per_ha', 0):,.0f} MMK/ha"
            )

    soil_text = (
        f"pH: {soil_summary.get('ph', 'N/A')}, "
        f"N: {soil_summary.get('nitrogen', 'N/A')} g/kg, "
        f"Texture: {soil_summary.get('texture', 'N/A')}, "
        f"Fertility: {soil_summary.get('fertility', 'N/A')}"
    )

    return (
        f"Township: {township_name}\n"
        f"Season: {season}\n"
        f"Soil Profile: {soil_text}\n"
        f"\nOptimized Recommendations:{crops_text}\n"
        f"\nPortfolio Expected Income: {expected_income:,.0f} MMK/ha\n"
        f"Risk Reduction vs Monocrop: {risk_reduction_pct:.1f}%\n"
        f"Success Probability: {success_probability:.0%}\n"
        f"\nGenerate a distributor advisory brief for this recommendation."
    )


def build_fertilizer_explanation_prompt(
    crop_name: str,
    fertilizer_name: str,
    formulation: str,
    soil_ph: float,
    soil_nitrogen: float,
    soil_texture: str,
    score: float,
    reasoning: str,
) -> str:
    """Build prompt for plain-language fertilizer explanation.

    Args:
        crop_name: Name of the crop.
        fertilizer_name: Name of the fertilizer.
        formulation: NPK formulation string.
        soil_ph: Soil pH value.
        soil_nitrogen: Soil nitrogen in g/kg.
        soil_texture: Soil texture class.
        score: Match score (0-1).
        reasoning: Algorithm reasoning string.

    Returns:
        Formatted prompt string.
    """
    return (
        f"Crop: {crop_name}\n"
        f"Recommended Fertilizer: {fertilizer_name} ({formulation})\n"
        f"Match Score: {score:.2f}\n"
        f"Algorithm Reasoning: {reasoning}\n"
        f"\nSoil Conditions:\n"
        f"- pH: {soil_ph}\n"
        f"- Nitrogen: {soil_nitrogen} g/kg\n"
        f"- Texture: {soil_texture}\n"
        f"\nExplain this recommendation in plain language."
    )


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
