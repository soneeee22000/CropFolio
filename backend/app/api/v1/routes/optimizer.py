"""Portfolio optimization API routes."""

from fastapi import APIRouter, Body, Depends, HTTPException, Request

from app.api.v1.schemas.optimizer import (
    ClimateRiskSummary,
    CropWeight,
    OptimizeRequest,
    OptimizeResponse,
    PortfolioMetrics,
)
from app.core.limiter import limiter
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
