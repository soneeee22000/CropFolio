"""Monte Carlo simulation API routes."""

from fastapi import APIRouter, Body, Depends, HTTPException, Request

from app.api.v1.schemas.simulator import (
    HistogramBin,
    SimulateRequest,
    SimulateResponse,
    SimulationStats,
)
from app.core.limiter import limiter
from app.domain.results import SimulationServiceResult
from app.services.portfolio_service import PortfolioService, get_portfolio_service

router = APIRouter(prefix="/simulate", tags=["simulator"])


def _to_simulate_response(
    result: SimulationServiceResult,
) -> SimulateResponse:
    """Map domain SimulationServiceResult to API SimulateResponse."""
    return SimulateResponse(
        township_id=result.township_id,
        township_name=result.township_name,
        season=result.season,
        num_simulations=result.num_simulations,
        stats=SimulationStats(
            mean_income=result.stats.mean_income,
            median_income=result.stats.median_income,
            std_dev=result.stats.std_dev,
            percentile_5=result.stats.percentile_5,
            percentile_95=result.stats.percentile_95,
            prob_catastrophic_loss=result.stats.prob_catastrophic_loss,
            value_at_risk_95=result.stats.value_at_risk_95,
        ),
        histogram=[
            HistogramBin(
                bin_start=b.bin_start,
                bin_end=b.bin_end,
                count=b.count,
                frequency=b.frequency,
            )
            for b in result.histogram
        ],
    )


@router.post("/", response_model=SimulateResponse)
@limiter.limit("10/minute")
async def run_simulation(
    request: Request,
    body: SimulateRequest = Body(...),  # noqa: B008
    service: PortfolioService = Depends(get_portfolio_service),  # noqa: B008
) -> SimulateResponse:
    """Run Monte Carlo simulation for a crop portfolio."""
    try:
        result = await service.simulate(
            crop_ids=body.crop_ids,
            weights=body.weights,
            township_id=body.township_id,
            num_simulations=body.num_simulations,
            season=body.season,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Township '{body.township_id}' not found",
        )
    return _to_simulate_response(result)
