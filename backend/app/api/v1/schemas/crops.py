"""Pydantic schemas for crop API responses."""

from __future__ import annotations

from pydantic import BaseModel


class CropResponse(BaseModel):
    """Single crop profile response."""

    id: str
    name_en: str
    name_mm: str
    category: str
    growing_season: str
    drought_tolerance: float
    flood_tolerance: float
    avg_yield_kg_per_ha: float
    yield_variance: float
    avg_price_mmk_per_kg: float
    price_variance: float
    nitrogen_requirement: int
    phosphorus_requirement: int
    potassium_requirement: int
    yield_data_source: str
    price_data_source: str
    data_confidence: str


class CropListResponse(BaseModel):
    """List of crops response."""

    count: int
    crops: list[CropResponse]
