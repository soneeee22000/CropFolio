"""Portfolio optimization API routes."""

from fastapi import APIRouter, Body, Depends, HTTPException, Request

from app.api.v1.schemas.optimizer import (
    BayesianCropPrediction,
    ClimateRiskSummary,
    CropWeight,
    OptimizeBayesianRequest,
    OptimizeBayesianResponse,
    OptimizeRequest,
    OptimizeResponse,
    PortfolioMetrics,
)
from app.core.limiter import limiter
from app.domain.bayesian import EvidenceItem
from app.domain.results import PortfolioResult
from app.services.portfolio_service import PortfolioService, get_portfolio_service

router = APIRouter(prefix="/optimize", tags=["optimizer"])


def _to_optimize_response(result: PortfolioResult) -> OptimizeResponse:
    """Map domain PortfolioResult to API OptimizeResponse."""
    return OptimizeResponse(
        township_id=result.township_id,
        township_name=result.township_name,
        season=result.season,
        weights=[
            CropWeight(
                crop_id=cw.crop_id,
                crop_name=cw.crop_name,
                crop_name_mm=cw.crop_name_mm,
                weight=cw.weight,
                expected_income_per_ha=cw.expected_income_per_ha,
            )
            for cw in result.crop_weights
        ],
        metrics=PortfolioMetrics(
            expected_income_per_ha=result.metrics.expected_income_per_ha,
            income_std_dev=result.metrics.income_std_dev,
            sharpe_ratio=result.metrics.sharpe_ratio,
            risk_reduction_pct=result.metrics.risk_reduction_pct,
        ),
        climate_risk=ClimateRiskSummary(
            drought_probability=result.climate_risk.drought_probability,
            flood_probability=result.climate_risk.flood_probability,
            risk_level=result.climate_risk.risk_level,
            data_source=result.climate_risk.data_source,
        ),
    )


@router.post("/", response_model=OptimizeResponse)
@limiter.limit("10/minute")
async def optimize_portfolio(
    request: Request,
    body: OptimizeRequest = Body(...),  # noqa: B008
    service: PortfolioService = Depends(get_portfolio_service),  # noqa: B008
) -> OptimizeResponse:
    """Run Markowitz portfolio optimization for crop allocation."""
    try:
        result = await service.optimize(
            crop_ids=body.crop_ids,
            township_id=body.township_id,
            risk_tolerance=body.risk_tolerance,
            season=body.season,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Township '{body.township_id}' not found",
        )
    return _to_optimize_response(result)


@router.post("/bayesian", response_model=OptimizeBayesianResponse)
@limiter.limit("10/minute")
async def optimize_portfolio_bayesian_endpoint(
    request: Request,
    body: OptimizeBayesianRequest = Body(...),  # noqa: B008
    service: PortfolioService = Depends(get_portfolio_service),  # noqa: B008
) -> OptimizeBayesianResponse:
    """Run Bayesian portfolio optimization with evidence-based returns."""
    try:
        evidence_items = [
            EvidenceItem(variable=e.variable, value=e.value)
            for e in body.evidence
        ]
        result = await service.optimize_bayesian(
            crop_ids=body.crop_ids,
            township_id=body.township_id,
            risk_tolerance=body.risk_tolerance,
            season=body.season,
            evidence=evidence_items,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Township '{body.township_id}' not found",
        )

    portfolio_result, bayesian_result = result

    return OptimizeBayesianResponse(
        township_id=portfolio_result.township_id,
        township_name=portfolio_result.township_name,
        season=portfolio_result.season,
        model_type="bayesian",
        weights=[
            CropWeight(
                crop_id=cw.crop_id,
                crop_name=cw.crop_name,
                crop_name_mm=cw.crop_name_mm,
                weight=cw.weight,
                expected_income_per_ha=cw.expected_income_per_ha,
            )
            for cw in portfolio_result.crop_weights
        ],
        metrics=PortfolioMetrics(
            expected_income_per_ha=portfolio_result.metrics.expected_income_per_ha,
            income_std_dev=portfolio_result.metrics.income_std_dev,
            sharpe_ratio=portfolio_result.metrics.sharpe_ratio,
            risk_reduction_pct=portfolio_result.metrics.risk_reduction_pct,
        ),
        climate_risk=ClimateRiskSummary(
            drought_probability=portfolio_result.climate_risk.drought_probability,
            flood_probability=portfolio_result.climate_risk.flood_probability,
            risk_level=portfolio_result.climate_risk.risk_level,
            data_source=portfolio_result.climate_risk.data_source,
        ),
        bayesian_predictions=[
            BayesianCropPrediction(
                crop_id=pred.crop_id,
                yield_probabilities=pred.yield_probabilities,
                expected_yield_factor=pred.expected_yield_factor,
                evidence_used=pred.evidence_used,
            )
            for pred in bayesian_result.crop_predictions
        ],
    )
