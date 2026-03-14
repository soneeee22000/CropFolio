"""Monte Carlo simulation API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.simulator import SimulateRequest, SimulateResponse
from app.services.portfolio_service import PortfolioService, get_portfolio_service

router = APIRouter(prefix="/simulate", tags=["simulator"])


@router.post("/", response_model=SimulateResponse)
async def run_simulation(
    request: SimulateRequest,
    service: PortfolioService = Depends(get_portfolio_service),
) -> SimulateResponse:
    """Run Monte Carlo simulation for a crop portfolio."""
    try:
        result = await service.simulate(
            crop_ids=request.crop_ids,
            weights=request.weights,
            township_id=request.township_id,
            num_simulations=request.num_simulations,
            season=request.season,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Township '{request.township_id}' not found",
        )
    return result
