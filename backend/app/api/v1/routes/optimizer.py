"""Portfolio optimization API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.optimizer import OptimizeRequest, OptimizeResponse
from app.services.portfolio_service import PortfolioService, get_portfolio_service

router = APIRouter(prefix="/optimize", tags=["optimizer"])


@router.post("/", response_model=OptimizeResponse)
async def optimize_portfolio(
    request: OptimizeRequest,
    service: PortfolioService = Depends(get_portfolio_service),
) -> OptimizeResponse:
    """Run Markowitz portfolio optimization for crop allocation."""
    try:
        result = await service.optimize(
            crop_ids=request.crop_ids,
            township_id=request.township_id,
            risk_tolerance=request.risk_tolerance,
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
