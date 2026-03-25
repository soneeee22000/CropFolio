"""Farm and plot management routes for farmers."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_farmer
from app.infrastructure.database import get_session
from app.infrastructure.models import Farm, Plot, User

router = APIRouter()


class FarmCreateSchema(BaseModel):
    """Request to register a new farm."""

    name: str = Field(..., max_length=255)
    name_mm: str | None = Field(None, max_length=255)
    township_id: str = Field(..., max_length=50)
    total_area_hectares: float = Field(..., gt=0)
    latitude: float | None = None
    longitude: float | None = None


class PlotCreateSchema(BaseModel):
    """Request to add a plot to a farm."""

    name: str | None = Field(None, max_length=100)
    area_hectares: float = Field(..., gt=0)
    soil_type: str | None = Field(None, max_length=50)
    latitude: float | None = None
    longitude: float | None = None


class PlotResponse(BaseModel):
    """Plot data in API responses."""

    id: uuid.UUID
    name: str | None
    area_hectares: float
    soil_type: str | None
    latitude: float | None
    longitude: float | None


class FarmResponse(BaseModel):
    """Farm data in API responses."""

    id: uuid.UUID
    name: str
    name_mm: str | None
    township_id: str
    total_area_hectares: float
    latitude: float | None
    longitude: float | None
    plots: list[PlotResponse] = []


@router.get("/", response_model=list[FarmResponse])
async def list_farms(
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[FarmResponse]:
    """List all farms belonging to the authenticated farmer."""
    result = await session.execute(
        select(Farm)
        .where(Farm.farmer_id == farmer.id)
        .options(selectinload(Farm.plots))
        .order_by(Farm.created_at.desc())
    )
    farms = result.scalars().all()
    return [_farm_to_response(f) for f in farms]


@router.post(
    "/",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_farm(
    body: FarmCreateSchema,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> FarmResponse:
    """Register a new farm for the authenticated farmer."""
    farm = Farm(
        id=uuid.uuid4(),
        farmer_id=farmer.id,
        name=body.name,
        name_mm=body.name_mm,
        township_id=body.township_id,
        total_area_hectares=body.total_area_hectares,
        latitude=body.latitude,
        longitude=body.longitude,
    )
    session.add(farm)
    await session.flush()
    return _farm_to_response(farm)


@router.get("/{farm_id}", response_model=FarmResponse)
async def get_farm(
    farm_id: uuid.UUID,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> FarmResponse:
    """Get a specific farm with its plots."""
    result = await session.execute(
        select(Farm)
        .where(Farm.id == farm_id, Farm.farmer_id == farmer.id)
        .options(selectinload(Farm.plots))
    )
    farm = result.scalar_one_or_none()
    if farm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )
    return _farm_to_response(farm)


@router.post(
    "/{farm_id}/plots",
    response_model=PlotResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_plot(
    farm_id: uuid.UUID,
    body: PlotCreateSchema,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> PlotResponse:
    """Add a plot to a farm."""
    result = await session.execute(
        select(Farm).where(
            Farm.id == farm_id, Farm.farmer_id == farmer.id
        )
    )
    farm = result.scalar_one_or_none()
    if farm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    plot = Plot(
        id=uuid.uuid4(),
        farm_id=farm_id,
        name=body.name,
        area_hectares=body.area_hectares,
        soil_type=body.soil_type,
        latitude=body.latitude,
        longitude=body.longitude,
    )
    session.add(plot)
    await session.flush()
    return PlotResponse(
        id=plot.id,
        name=plot.name,
        area_hectares=plot.area_hectares,
        soil_type=plot.soil_type,
        latitude=plot.latitude,
        longitude=plot.longitude,
    )


def _farm_to_response(farm: Farm) -> FarmResponse:
    """Convert a Farm ORM model to response schema."""
    plots = [
        PlotResponse(
            id=p.id,
            name=p.name,
            area_hectares=p.area_hectares,
            soil_type=p.soil_type,
            latitude=p.latitude,
            longitude=p.longitude,
        )
        for p in (farm.plots if farm.plots else [])
    ]
    return FarmResponse(
        id=farm.id,
        name=farm.name,
        name_mm=farm.name_mm,
        township_id=farm.township_id,
        total_area_hectares=farm.total_area_hectares,
        latitude=farm.latitude,
        longitude=farm.longitude,
        plots=plots,
    )
