"""Fertilizer catalog API routes."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.fertilizers import FertilizerListResponse, FertilizerResponse
from app.domain.fertilizers import get_all_fertilizers, get_fertilizer_by_id

router = APIRouter(prefix="/fertilizers", tags=["fertilizers"])


@router.get("/", response_model=FertilizerListResponse)
async def list_fertilizers() -> FertilizerListResponse:
    """List all available fertilizer products."""
    fertilizers = get_all_fertilizers()
    return FertilizerListResponse(
        count=len(fertilizers),
        fertilizers=[FertilizerResponse(**asdict(f)) for f in fertilizers],
    )


@router.get("/{fertilizer_id}", response_model=FertilizerResponse)
async def get_fertilizer(fertilizer_id: str) -> FertilizerResponse:
    """Get a single fertilizer profile by ID."""
    fert = get_fertilizer_by_id(fertilizer_id)
    if fert is None:
        raise HTTPException(
            status_code=404,
            detail=f"Fertilizer '{fertilizer_id}' not found",
        )
    return FertilizerResponse(**asdict(fert))
