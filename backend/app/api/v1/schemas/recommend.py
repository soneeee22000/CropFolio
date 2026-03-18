"""Pydantic schemas for recommendation API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class FertilizerRecommendationResponse(BaseModel):
    """A scored fertilizer recommendation."""

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


class CropRecommendationResponse(BaseModel):
    """Crop + fertilizer pairing recommendation."""

    crop_id: str
    crop_name: str
    crop_name_mm: str
    portfolio_weight: float
    expected_income_per_ha: float
    fertilizers: list[FertilizerRecommendationResponse]


class SoilProfileResponse(BaseModel):
    """Soil profile for a township."""

    township_id: str
    ph_h2o: float
    nitrogen_g_per_kg: float
    soc_g_per_kg: float
    clay_pct: int
    sand_pct: int
    silt_pct: int
    cec_cmol_per_kg: float
    texture_class: str
    fertility_rating: str


class ConfidenceMetrics(BaseModel):
    """Monte Carlo confidence metrics for a recommendation."""

    num_simulations: int
    mean_income: float
    median_income: float
    percentile_5: float
    percentile_95: float
    prob_catastrophic_loss: float
    success_probability: float


class RecommendRequest(BaseModel):
    """Request for crop-fertilizer recommendations."""

    township_ids: list[str] = Field(min_length=1, max_length=10)
    crop_ids: list[str] = Field(min_length=2, max_length=10)
    risk_tolerance: float = Field(default=0.5, ge=0.0, le=1.0)
    season: Literal["monsoon", "dry"] = "dry"
    top_fertilizers: int = Field(default=3, ge=1, le=8)


class TownshipRecommendation(BaseModel):
    """Full recommendation for a single township."""

    township_id: str
    township_name: str
    season: str
    soil: SoilProfileResponse | None
    crops: list[CropRecommendationResponse]
    confidence: ConfidenceMetrics | None
    expected_income_per_ha: float
    risk_reduction_pct: float
    ai_advisory: str | None = None
    ai_advisory_mm: str | None = None


class RecommendResponse(BaseModel):
    """Response with recommendations for one or more townships."""

    recommendations: list[TownshipRecommendation]
    total_townships: int


class DemoROIRequest(BaseModel):
    """Request for demo crop ROI calculation."""

    township_id: str
    crop_id: str
    area_hectares: float = Field(default=1.0, ge=0.1, le=100.0)
    season: Literal["monsoon", "dry"] = "dry"


class DemoROIResponse(BaseModel):
    """ROI calculation for a demo crop scenario."""

    township_id: str
    township_name: str
    crop_id: str
    crop_name: str
    area_hectares: float
    season: str
    # Costs
    fertilizer_cost_mmk: int
    seed_cost_mmk: int
    total_input_cost_mmk: int
    # Returns
    expected_revenue_mmk: int
    expected_profit_mmk: int
    # Risk
    success_probability: float
    catastrophic_loss_probability: float
    reimbursement_exposure_mmk: int
    # Alternatives
    recommended_fertilizer: FertilizerRecommendationResponse | None
    soil: SoilProfileResponse | None
