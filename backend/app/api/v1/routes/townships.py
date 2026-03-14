"""Township API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.schemas.townships import TownshipListResponse, TownshipResponse
from app.services.township_service import TownshipService, get_township_service

router = APIRouter(prefix="/townships", tags=["townships"])


@router.get("/", response_model=TownshipListResponse)
async def list_townships(
    service: TownshipService = Depends(get_township_service),
) -> TownshipListResponse:
    """List all Myanmar townships with coordinates."""
    townships = service.get_all()
    return TownshipListResponse(
        count=service.get_count(),
        townships=[TownshipResponse(**t) for t in townships],
    )


@router.get("/{township_id}", response_model=TownshipResponse)
async def get_township(
    township_id: str,
    service: TownshipService = Depends(get_township_service),
) -> TownshipResponse:
    """Get a single township by ID."""
    township = service.get_by_id(township_id)
    if township is None:
        raise HTTPException(status_code=404, detail=f"Township '{township_id}' not found")
    return TownshipResponse(**township)
