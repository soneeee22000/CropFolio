"""Recommendation API routes — crop + fertilizer + confidence for distributors."""

import logging
from dataclasses import asdict

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.v1.schemas.recommend import (
    ConfidenceMetrics,
    CropRecommendationResponse,
    DemoROIRequest,
    DemoROIResponse,
    FertilizerPlanResponse,
    FertilizerRecommendationResponse,
    MicronutrientFlagResponse,
    NutrientInteractionFlagResponse,
    RecommendRequest,
    RecommendResponse,
    ROIEstimateResponse,
    SoilProfileResponse,
    StageApplicationResponse,
    TownshipRecommendation,
)
from app.domain.fertilizers import get_soil_profile
from app.services.recommendation_service import (
    RecommendationService,
    get_recommendation_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommend", tags=["recommend"])
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=RecommendResponse)
@limiter.limit("10/minute")
async def generate_recommendations(
    request: Request,
    body: RecommendRequest = Body(...),  # noqa: B008
    service: RecommendationService = Depends(get_recommendation_service),  # noqa: B008
) -> RecommendResponse:
    """Generate crop + fertilizer recommendations for one or more townships."""
    try:
        results = await service.recommend(
            township_ids=body.township_ids,
            crop_ids=body.crop_ids,
            risk_tolerance=body.risk_tolerance,
            season=body.season,
            top_fertilizers=body.top_fertilizers,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        logger.warning("Recommendation pipeline error: %s", e)
        raise HTTPException(status_code=503, detail=str(e)) from e

    recommendations: list[TownshipRecommendation] = []
    for r in results:
        soil_resp = None
        if r.soil is not None:
            soil_resp = SoilProfileResponse(**asdict(r.soil))

        crop_recs = []
        for cr in r.crop_results:
            plan_resp = None
            if cr.fertilizer_plan is not None:
                fp = cr.fertilizer_plan
                plan_resp = FertilizerPlanResponse(
                    crop_id=fp.crop_id,
                    applications=[
                        StageApplicationResponse(
                            stage=a.stage,
                            day=a.day,
                            fertilizer_id=a.fertilizer_id,
                            fertilizer_name=a.fertilizer_name,
                            rate_kg_per_ha=a.rate_kg_per_ha,
                            cost_mmk=a.cost_mmk,
                        )
                        for a in fp.applications
                    ],
                    nutrient_totals=fp.nutrient_totals,
                    micronutrient_flags=[
                        MicronutrientFlagResponse(
                            nutrient=mf.nutrient,
                            severity=mf.severity,
                            recommendation=mf.recommendation,
                        )
                        for mf in fp.micronutrient_flags
                    ],
                    interaction_flags=[
                        NutrientInteractionFlagResponse(
                            ratio_name=nf.ratio_name,
                            actual_ratio=nf.actual_ratio,
                            optimal_range=nf.optimal_range,
                            recommendation=nf.recommendation,
                        )
                        for nf in fp.interaction_flags
                    ],
                    roi_estimate=ROIEstimateResponse(
                        total_cost_mmk=fp.roi_estimate.total_cost_mmk,
                        expected_yield_increase_pct=fp.roi_estimate.expected_yield_increase_pct,
                        return_ratio=fp.roi_estimate.return_ratio,
                    ),
                    lp_feasible=fp.lp_feasible,
                )

            crop_recs.append(
                CropRecommendationResponse(
                    crop_id=cr.crop.id,
                    crop_name=cr.crop.name_en,
                    crop_name_mm=cr.crop.name_mm,
                    portfolio_weight=round(cr.weight, 4),
                    expected_income_per_ha=cr.expected_income,
                    fertilizers=[
                        FertilizerRecommendationResponse(**asdict(f))
                        for f in cr.fertilizers
                    ],
                    fertilizer_plan=plan_resp,
                )
            )

        confidence = None
        if r.confidence is not None:
            confidence = ConfidenceMetrics(**r.confidence)

        recommendations.append(
            TownshipRecommendation(
                township_id=r.township_id,
                township_name=r.township_name,
                season=r.season,
                soil=soil_resp,
                crops=crop_recs,
                confidence=confidence,
                expected_income_per_ha=round(r.expected_income, 2),
                risk_reduction_pct=round(r.risk_reduction_pct, 2),
                ai_advisory=r.ai_advisory,
                ai_advisory_mm=r.ai_advisory_mm,
            )
        )

    return RecommendResponse(
        recommendations=recommendations,
        total_townships=len(recommendations),
    )


@router.post("/demo-roi", response_model=DemoROIResponse)
@limiter.limit("10/minute")
async def calculate_demo_roi(
    request: Request,
    body: DemoROIRequest = Body(...),  # noqa: B008
    service: RecommendationService = Depends(get_recommendation_service),  # noqa: B008
) -> DemoROIResponse:
    """Calculate ROI for a demo crop scenario."""
    try:
        result = await service.calculate_demo_roi(
            township_id=body.township_id,
            crop_id=body.crop_id,
            area_hectares=body.area_hectares,
            season=body.season,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        logger.warning("Demo ROI calculation error: %s", e)
        raise HTTPException(status_code=503, detail=str(e)) from e

    fert_resp = None
    if result["recommended_fertilizer"] is not None:
        fert_resp = FertilizerRecommendationResponse(
            **asdict(result["recommended_fertilizer"])
        )

    soil_resp = None
    if result["soil"] is not None:
        soil_resp = SoilProfileResponse(**asdict(result["soil"]))

    return DemoROIResponse(
        township_id=result["township_id"],
        township_name=result["township_name"],
        crop_id=result["crop_id"],
        crop_name=result["crop_name"],
        area_hectares=result["area_hectares"],
        season=result["season"],
        fertilizer_cost_mmk=result["fertilizer_cost_mmk"],
        seed_cost_mmk=result["seed_cost_mmk"],
        total_input_cost_mmk=result["total_input_cost_mmk"],
        expected_revenue_mmk=result["expected_revenue_mmk"],
        expected_profit_mmk=result["expected_profit_mmk"],
        success_probability=result["success_probability"],
        catastrophic_loss_probability=result["catastrophic_loss_probability"],
        reimbursement_exposure_mmk=result["reimbursement_exposure_mmk"],
        recommended_fertilizer=fert_resp,
        soil=soil_resp,
    )


@router.get(
    "/soil/{township_id}",
    response_model=SoilProfileResponse,
)
@limiter.limit("30/minute")
async def get_township_soil(
    request: Request,
    township_id: str,
) -> SoilProfileResponse:
    """Get soil profile for a township."""
    soil = get_soil_profile(township_id)
    if soil is None:
        raise HTTPException(
            status_code=404,
            detail=f"No soil profile for township '{township_id}'",
        )
    return SoilProfileResponse(**asdict(soil))
