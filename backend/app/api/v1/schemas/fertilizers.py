"""Pydantic schemas for fertilizer API responses."""

from __future__ import annotations

from pydantic import BaseModel


class FertilizerResponse(BaseModel):
    """Single fertilizer profile response."""

    id: str
    name_en: str
    name_mm: str
    formulation: str
    nitrogen_pct: float
    phosphorus_pct: float
    potassium_pct: float
    sulfur_pct: float
    price_mmk_per_50kg: int
    application_rate_kg_per_ha: int
    availability: str
    notes: str


class FertilizerListResponse(BaseModel):
    """List of fertilizers response."""

    count: int
    fertilizers: list[FertilizerResponse]
