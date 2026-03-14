"""Multi-township comparison API routes."""

from fastapi import APIRouter, Body, Depends, HTTPException, Request

from app.api.v1.routes.optimizer import _to_optimize_response
from app.api.v1.schemas.compare import CompareRequest, CompareResponse
from app.core.limiter import limiter
from app.services.portfolio_service import PortfolioService, get_portfolio_service

router = APIRouter(prefix="/compare", tags=["compare"])


@router.post("/", response_model=CompareResponse)
@limiter.limit("5/minute")
async def compare_townships(
    request: Request,
    body: CompareRequest = Body(...),  # noqa: B008
    service: PortfolioService = Depends(get_portfolio_service),  # noqa: B008
) -> CompareResponse:
    """Compare portfolio optimization across multiple townships."""
    results = await service.compare_townships(
        township_ids=body.township_ids,
        crop_ids=body.crop_ids,
        risk_tolerance=body.risk_tolerance,
        season=body.season,
    )

    townships = []
    for tid, result in zip(body.township_ids, results):
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Township '{tid}' not found",
            )
        townships.append(_to_optimize_response(result).model_dump())

    return CompareResponse(
        townships=townships,
        season=body.season,
    )
