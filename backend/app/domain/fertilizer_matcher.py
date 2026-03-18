"""Fertilizer-crop matching algorithm based on soil analysis and crop needs."""

# Scoring formula:
#   score = crop_need_match * 0.4
#         + soil_deficiency_match * 0.3
#         + cost_efficiency * 0.2
#         + compatibility * 0.1
#
# Sources: FAO Fertilizer Best Practices, IRRI nutrient management

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.domain.fertilizers import (
    CropNutrientRequirement,
    FertilizerProfile,
    SoilProfile,
    get_crop_fertilizer_score,
)

logger = logging.getLogger(__name__)

# Scoring weights
WEIGHT_CROP_NEED = 0.4
WEIGHT_SOIL_DEFICIENCY = 0.3
WEIGHT_COST_EFFICIENCY = 0.2
WEIGHT_COMPATIBILITY = 0.1

# Soil nutrient thresholds (g/kg for N, cmol/kg for CEC)
LOW_NITROGEN_THRESHOLD = 1.0
LOW_SOC_THRESHOLD = 8.0
HIGH_PH_THRESHOLD = 7.5
LOW_PH_THRESHOLD = 5.5

# Cost normalization — most expensive fertilizer per ha application cost (MMK)
MAX_COST_PER_HA_MMK = 300000


@dataclass(frozen=True)
class FertilizerRecommendation:
    """A scored fertilizer recommendation for a specific crop-soil combination."""

    fertilizer_id: str
    fertilizer_name: str
    formulation: str
    score: float
    crop_need_score: float
    soil_deficiency_score: float
    cost_efficiency_score: float
    compatibility_score: float
    recommended_rate_kg_per_ha: int
    cost_per_ha_mmk: int
    reasoning: str


def _compute_crop_need_score(
    fertilizer: FertilizerProfile,
    requirement: CropNutrientRequirement,
) -> float:
    """Score how well a fertilizer matches the crop's primary nutrient need.

    Crops needing N prefer high-N fertilizers, P-needing crops prefer DAP/TSP, etc.
    """
    primary = requirement.primary_nutrient
    if primary == "nitrogen":
        return min(fertilizer.nitrogen_pct / 46.0, 1.0)
    if primary == "phosphorus":
        return min(fertilizer.phosphorus_pct / 46.0, 1.0)
    if primary == "potassium":
        return min(fertilizer.potassium_pct / 60.0, 1.0)
    return 0.5


def _compute_soil_deficiency_score(
    fertilizer: FertilizerProfile,
    soil: SoilProfile,
) -> float:
    """Score how well a fertilizer addresses soil deficiencies.

    Low soil N → prefer N fertilizers. High pH → prefer acidifying (AS).
    Low SOC → prefer balanced NPK or organic matter builders.
    """
    score = 0.5  # baseline

    # Nitrogen-deficient soils benefit from N fertilizers
    if soil.nitrogen_g_per_kg < LOW_NITROGEN_THRESHOLD:
        n_bonus = (fertilizer.nitrogen_pct / 46.0) * 0.3
        score += n_bonus

    # High pH soils benefit from acidifying fertilizers (AS, urea)
    if soil.ph_h2o > HIGH_PH_THRESHOLD:
        if fertilizer.sulfur_pct > 0:
            score += 0.15
        if fertilizer.id == "ammonium_sulfate":
            score += 0.1

    # Low pH soils should avoid further acidification
    if soil.ph_h2o < LOW_PH_THRESHOLD:
        if fertilizer.id == "ammonium_sulfate":
            score -= 0.2

    # Low organic carbon soils need more balanced nutrition
    if soil.soc_g_per_kg < LOW_SOC_THRESHOLD:
        if fertilizer.potassium_pct > 0 and fertilizer.nitrogen_pct > 0:
            score += 0.1

    return max(0.0, min(1.0, score))


def _compute_cost_efficiency(fertilizer: FertilizerProfile) -> float:
    """Score cost efficiency (cheaper per ha = higher score).

    Normalized against the maximum expected cost per ha.
    """
    cost_per_ha = (
        fertilizer.price_mmk_per_50kg
        * fertilizer.application_rate_kg_per_ha
        / 50
    )
    return max(0.0, 1.0 - (cost_per_ha / MAX_COST_PER_HA_MMK))


def _build_reasoning(
    fertilizer: FertilizerProfile,
    requirement: CropNutrientRequirement,
    soil: SoilProfile,
    score: float,
) -> str:
    """Build a plain-language reasoning string for the recommendation."""
    parts: list[str] = []

    if requirement.primary_nutrient == "nitrogen" and fertilizer.nitrogen_pct > 15:
        parts.append(
            f"{requirement.crop_id.replace('_', ' ').title()} has high N demand "
            f"({requirement.nitrogen_kg_per_ha} kg/ha)"
        )
    elif requirement.primary_nutrient == "phosphorus" and fertilizer.phosphorus_pct > 15:
        parts.append(
            f"{requirement.crop_id.replace('_', ' ').title()} needs P for "
            f"root/nodule development ({requirement.phosphorus_kg_per_ha} kg/ha)"
        )

    if soil.nitrogen_g_per_kg < LOW_NITROGEN_THRESHOLD:
        parts.append(f"soil N is low ({soil.nitrogen_g_per_kg} g/kg)")
    if soil.ph_h2o > HIGH_PH_THRESHOLD:
        parts.append(f"alkaline soil (pH {soil.ph_h2o})")
    if soil.ph_h2o < LOW_PH_THRESHOLD:
        parts.append(f"acidic soil (pH {soil.ph_h2o})")

    cost_per_ha = (
        fertilizer.price_mmk_per_50kg
        * fertilizer.application_rate_kg_per_ha
        / 50
    )
    parts.append(f"cost: {cost_per_ha:,.0f} MMK/ha")

    return "; ".join(parts) if parts else f"Score: {score:.2f}"


def match_fertilizers(
    crop_id: str,
    requirement: CropNutrientRequirement,
    soil: SoilProfile,
    fertilizers: list[FertilizerProfile],
    top_n: int = 3,
) -> list[FertilizerRecommendation]:
    """Rank fertilizers for a crop-soil combination.

    Args:
        crop_id: The crop being evaluated.
        requirement: Crop's NPK requirements.
        soil: Township soil profile.
        fertilizers: Available fertilizer products.
        top_n: Number of top recommendations to return.

    Returns:
        Sorted list of FertilizerRecommendation (highest score first).
    """
    recommendations: list[FertilizerRecommendation] = []

    for fert in fertilizers:
        crop_need = _compute_crop_need_score(fert, requirement)
        soil_def = _compute_soil_deficiency_score(fert, soil)
        cost_eff = _compute_cost_efficiency(fert)
        compat = get_crop_fertilizer_score(crop_id, fert.id)

        total = (
            WEIGHT_CROP_NEED * crop_need
            + WEIGHT_SOIL_DEFICIENCY * soil_def
            + WEIGHT_COST_EFFICIENCY * cost_eff
            + WEIGHT_COMPATIBILITY * compat
        )

        cost_per_ha = (
            fert.price_mmk_per_50kg * fert.application_rate_kg_per_ha // 50
        )

        reasoning = _build_reasoning(fert, requirement, soil, total)

        recommendations.append(
            FertilizerRecommendation(
                fertilizer_id=fert.id,
                fertilizer_name=fert.name_en,
                formulation=fert.formulation,
                score=round(total, 3),
                crop_need_score=round(crop_need, 3),
                soil_deficiency_score=round(soil_def, 3),
                cost_efficiency_score=round(cost_eff, 3),
                compatibility_score=round(compat, 3),
                recommended_rate_kg_per_ha=fert.application_rate_kg_per_ha,
                cost_per_ha_mmk=cost_per_ha,
                reasoning=reasoning,
            )
        )

    recommendations.sort(key=lambda r: r.score, reverse=True)
    return recommendations[:top_n]
