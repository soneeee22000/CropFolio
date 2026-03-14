"""Pydantic schemas for township API responses."""

from __future__ import annotations

from pydantic import BaseModel


class TownshipResponse(BaseModel):
    """Single township response."""

    id: str
    name: str
    name_mm: str
    region: str
    latitude: float
    longitude: float


class TownshipListResponse(BaseModel):
    """List of townships response."""

    count: int
    townships: list[TownshipResponse]
