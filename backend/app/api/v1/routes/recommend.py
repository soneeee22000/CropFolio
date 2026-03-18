"""Recommendation API routes — crop + fertilizer + confidence for distributors."""

from dataclasses import asdict

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.v1.schemas.recommend import (
    ConfidenceMetrics,
    CropRecommendationResponse,
    DemoROIRequest,
    DemoROIResponse,
    FertilizerRecommendationResponse,
    RecommendRequest,
    RecommendResponse,
    SoilProfileResponse,
    TownshipRecommendation,
)
from app.domain.fertilizers import get_soil_profile
from app.services.recommendation_service import (
    RecommendationService,
    get_recommendation_service,
)

router = APIRouter(prefix="/recommend", tags=["recommend"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=RecommendResponse)
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

    recommendations: list[TownshipRecommendation] = []
    for r in results:
        soil_resp = None
        if r.soil is not None:
            soil_resp = SoilProfileResponse(**asdict(r.soil))

        crop_recs = [
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
            )
            for cr in r.crop_results
        ]

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
async def get_township_soil(township_id: str) -> SoilProfileResponse:
    """Get soil profile for a township."""
    soil = get_soil_profile(township_id)
    if soil is None:
        raise HTTPException(
            status_code=404,
            detail=f"No soil profile for township '{township_id}'",
        )
    return SoilProfileResponse(**asdict(soil))
