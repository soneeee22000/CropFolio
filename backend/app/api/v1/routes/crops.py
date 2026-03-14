"""Crop API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.crops import CropListResponse, CropResponse
from app.domain.crops import get_all_crops, get_crop_by_id

router = APIRouter(prefix="/crops", tags=["crops"])


@router.get("/", response_model=CropListResponse)
async def list_crops() -> CropListResponse:
    """List all available Myanmar crop profiles."""
    crops = get_all_crops()
    return CropListResponse(
        count=len(crops),
        crops=[CropResponse(**vars(c)) for c in crops],
    )


@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(crop_id: str) -> CropResponse:
    """Get a single crop profile by ID."""
    crop = get_crop_by_id(crop_id)
    if crop is None:
        raise HTTPException(status_code=404, detail=f"Crop '{crop_id}' not found")
    return CropResponse(**vars(crop))
