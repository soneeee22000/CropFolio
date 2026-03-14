"""Pydantic schemas for multi-township comparison API."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class CompareRequest(BaseModel):
    """Request body for multi-township comparison."""

    township_ids: list[str] = Field(min_length=2, max_length=3)
    crop_ids: list[str] = Field(min_length=2, max_length=10)
    season: Literal["monsoon", "dry"] = "monsoon"
    risk_tolerance: float = Field(default=0.5, ge=0.0, le=1.0)


class CompareResponse(BaseModel):
    """Response from multi-township comparison."""

    townships: list[Any]
    season: str
