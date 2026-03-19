"""Recommendation service orchestrating optimize → soil → fertilizer → Monte Carlo."""

from __future__ import annotations

import asyncio
import logging
from functools import lru_cache

from app.core.constants import DEFAULT_NUM_SIMULATIONS
from app.domain.crops import CropProfile, get_crop_by_id
from app.domain.fertilizer_matcher import (
    FertilizerRecommendation,
    match_fertilizers,
)
from app.domain.fertilizers import (
    SoilProfile,
    get_all_fertilizers,
    get_nutrient_requirement,
    get_soil_profile,
)
from app.domain.optimizer import compute_expected_returns, optimize_portfolio
from app.domain.simulator import run_monte_carlo
from app.services.climate_service import ClimateService, get_climate_service
from app.services.township_service import TownshipService, get_township_service

logger = logging.getLogger(__name__)

# Seed cost estimates in MMK/ha (Myanmar DoA averages)
SEED_COST_MMK_PER_HA: dict[str, int] = {
    "rice": 120000,
    "black_gram": 45000,
    "green_gram": 40000,
    "chickpea": 55000,
    "sesame": 25000,
    "groundnut": 180000,
    "maize": 80000,
    "sugarcane": 200000,
    "potato": 350000,
    "onion": 100000,
    "chili": 60000,
}
DEFAULT_SEED_COST = 50000


class CropFertilizerResult:
    """Intermediate result for a single crop's fertilizer matching."""

    def __init__(
        self,
        crop: CropProfile,
        weight: float,
        expected_income: float,
        fertilizers: list[FertilizerRecommendation],
    ) -> None:
        """Initialize with crop, weight, and matched fertilizers."""
        self.crop = crop
        self.weight = weight
        self.expected_income = expected_income
        self.fertilizers = fertilizers


class TownshipRecommendationResult:
    """Full recommendation result for a single township."""

    def __init__(
        self,
        township_id: str,
        township_name: str,
        season: str,
        soil: SoilProfile | None,
        crop_results: list[CropFertilizerResult],
        expected_income: float,
        risk_reduction_pct: float,
        confidence: dict | None = None,
        ai_advisory: str | None = None,
        ai_advisory_mm: str | None = None,
    ) -> None:
        """Initialize with all recommendation data."""
        self.township_id = township_id
        self.township_name = township_name
        self.season = season
        self.soil = soil
        self.crop_results = crop_results
        self.expected_income = expected_income
        self.risk_reduction_pct = risk_reduction_pct
        self.confidence = confidence
        self.ai_advisory = ai_advisory
        self.ai_advisory_mm = ai_advisory_mm


class RecommendationService:
    """Orchestrates the full recommendation pipeline.

    Pipeline: optimize → soil → fertilizer match → Monte Carlo → advisory.
    """

    def __init__(
        self,
        climate_service: ClimateService | None = None,
        township_service: TownshipService | None = None,
    ) -> None:
        """Initialize with dependencies."""
        self._climate = climate_service or get_climate_service()
        self._townships = township_service or get_township_service()
        self._fertilizers = get_all_fertilizers()

    async def recommend(
        self,
        township_ids: list[str],
        crop_ids: list[str],
        risk_tolerance: float,
        season: str,
        top_fertilizers: int = 3,
    ) -> list[TownshipRecommendationResult]:
        """Generate recommendations for one or more townships.

        Args:
            township_ids: List of township IDs to generate recommendations for.
            crop_ids: Crop IDs to include in portfolio optimization.
            risk_tolerance: Risk tolerance parameter (0-1).
            season: Growing season (monsoon/dry).
            top_fertilizers: Number of top fertilizer recommendations per crop.

        Returns:
            List of TownshipRecommendationResult objects.
        """
        tasks = [
            self._recommend_township(
                tid, crop_ids, risk_tolerance, season, top_fertilizers
            )
            for tid in township_ids
        ]
        return await asyncio.gather(*tasks)

    async def _recommend_township(
        self,
        township_id: str,
        crop_ids: list[str],
        risk_tolerance: float,
        season: str,
        top_fertilizers: int,
    ) -> TownshipRecommendationResult:
        """Generate recommendation for a single township."""
        township = self._townships.get_by_id(township_id)
        if township is None:
            msg = f"Unknown township: '{township_id}'"
            raise ValueError(msg)

        crops = self._resolve_crops(crop_ids)

        # Step 1: Climate assessment
        climate_result = await self._climate.assess_risk(township_id, season)
        if climate_result is None:
            msg = f"Climate assessment failed for {township_id}"
            raise RuntimeError(msg)
        risk_profile, _ = climate_result

        # Step 2: Portfolio optimization
        opt_result = await asyncio.to_thread(
            optimize_portfolio,
            crops,
            risk_profile.drought_probability,
            risk_profile.flood_probability,
            risk_tolerance,
        )

        expected_returns = compute_expected_returns(
            crops,
            risk_profile.drought_probability,
            risk_profile.flood_probability,
        )

        # Step 3: Soil profile lookup
        soil = get_soil_profile(township_id)

        # Step 4: Fertilizer matching per crop
        crop_results: list[CropFertilizerResult] = []
        for i, crop in enumerate(crops):
            weight = opt_result.weights[crop.id]
            if weight < 0.01:
                continue

            income = round(float(expected_returns[i]) * weight, 2)
            fertilizer_recs = self._match_for_crop(
                crop, soil, top_fertilizers
            )
            crop_results.append(
                CropFertilizerResult(
                    crop=crop,
                    weight=weight,
                    expected_income=income,
                    fertilizers=fertilizer_recs,
                )
            )

        # Step 5: Monte Carlo confidence
        weights_dict = opt_result.weights
        sim_result = await asyncio.to_thread(
            run_monte_carlo,
            crops,
            weights_dict,
            risk_profile.drought_probability,
            risk_profile.flood_probability,
            DEFAULT_NUM_SIMULATIONS,
        )

        success_prob = 1.0 - sim_result.prob_catastrophic_loss
        confidence = {
            "num_simulations": DEFAULT_NUM_SIMULATIONS,
            "mean_income": sim_result.mean_income,
            "median_income": sim_result.median_income,
            "percentile_5": sim_result.percentile_5,
            "percentile_95": sim_result.percentile_95,
            "prob_catastrophic_loss": sim_result.prob_catastrophic_loss,
            "success_probability": round(success_prob, 4),
        }

        return TownshipRecommendationResult(
            township_id=township_id,
            township_name=township["name"],
            season=season,
            soil=soil,
            crop_results=crop_results,
            expected_income=opt_result.expected_income_per_ha,
            risk_reduction_pct=opt_result.risk_reduction_pct,
            confidence=confidence,
        )

    def _match_for_crop(
        self,
        crop: CropProfile,
        soil: SoilProfile | None,
        top_n: int,
    ) -> list[FertilizerRecommendation]:
        """Match fertilizers for a single crop given soil conditions."""
        requirement = get_nutrient_requirement(crop.id)
        if requirement is None or soil is None:
            return []

        return match_fertilizers(
            crop_id=crop.id,
            requirement=requirement,
            soil=soil,
            fertilizers=self._fertilizers,
            top_n=top_n,
        )

    async def calculate_demo_roi(
        self,
        township_id: str,
        crop_id: str,
        area_hectares: float,
        season: str,
    ) -> dict:
        """Calculate ROI for a demo crop scenario.

        Returns a dict with cost, revenue, risk, and recommendation data.
        """
        township = self._townships.get_by_id(township_id)
        if township is None:
            msg = f"Unknown township: '{township_id}'"
            raise ValueError(msg)

        crop = get_crop_by_id(crop_id)
        if crop is None:
            msg = f"Unknown crop: '{crop_id}'"
            raise ValueError(msg)

        # Soil and fertilizer
        soil = get_soil_profile(township_id)
        top_fert = self._match_for_crop(crop, soil, top_n=1)
        best_fert = top_fert[0] if top_fert else None

        # Fertilizer cost
        fert_cost = 0
        if best_fert:
            fert_cost = int(best_fert.cost_per_ha_mmk * area_hectares)

        # Seed cost
        seed_cost = int(
            SEED_COST_MMK_PER_HA.get(crop_id, DEFAULT_SEED_COST)
            * area_hectares
        )

        total_input = fert_cost + seed_cost

        # Expected revenue
        expected_revenue = int(
            crop.avg_yield_kg_per_ha
            * crop.avg_price_mmk_per_kg
            * area_hectares
        )
        expected_profit = expected_revenue - total_input

        # Climate risk for Monte Carlo
        climate_result = await self._climate.assess_risk(township_id, season)
        success_prob = 0.7
        catastrophic_prob = 0.1
        if climate_result is not None:
            risk_profile, _ = climate_result
            # Single-crop simulation
            sim = await asyncio.to_thread(
                run_monte_carlo,
                [crop],
                {crop.id: 1.0},
                risk_profile.drought_probability,
                risk_profile.flood_probability,
                DEFAULT_NUM_SIMULATIONS,
            )
            catastrophic_prob = sim.prob_catastrophic_loss
            success_prob = 1.0 - catastrophic_prob

        # Reimbursement exposure = total input if demo fails
        reimbursement = int(total_input * (1.0 - success_prob))

        return {
            "township_id": township_id,
            "township_name": township["name"],
            "crop_id": crop_id,
            "crop_name": crop.name_en,
            "area_hectares": area_hectares,
            "season": season,
            "fertilizer_cost_mmk": fert_cost,
            "seed_cost_mmk": seed_cost,
            "total_input_cost_mmk": total_input,
            "expected_revenue_mmk": expected_revenue,
            "expected_profit_mmk": expected_profit,
            "success_probability": round(success_prob, 4),
            "catastrophic_loss_probability": round(catastrophic_prob, 4),
            "reimbursement_exposure_mmk": reimbursement,
            "recommended_fertilizer": best_fert,
            "soil": soil,
        }

    def _resolve_crops(self, crop_ids: list[str]) -> list[CropProfile]:
        """Resolve crop IDs to CropProfile objects."""
        crops: list[CropProfile] = []
        for cid in crop_ids:
            crop = get_crop_by_id(cid)
            if crop is None:
                msg = f"Unknown crop: '{cid}'"
                raise ValueError(msg)
            crops.append(crop)
        return crops


@lru_cache(maxsize=1)
def get_recommendation_service() -> RecommendationService:
    """Return singleton RecommendationService instance."""
    return RecommendationService()
