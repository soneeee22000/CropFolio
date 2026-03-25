"""Crop plan generation, management, and task tracking routes."""

from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_farmer
from app.infrastructure.database import get_session
from app.infrastructure.models import User
from app.services.plan_service import PlanService

router = APIRouter()

_plan_service = PlanService()


class PlanGenerateSchema(BaseModel):
    """Request to generate a crop plan for a plot."""

    plot_id: uuid.UUID
    crop_ids: list[str] = Field(..., min_length=1)
    season: str = Field(..., pattern="^(monsoon|dry)$")
    year: int = Field(..., ge=2024, le=2030)
    risk_tolerance: float = Field(0.5, ge=0.0, le=1.0)


class ApplicationReportSchema(BaseModel):
    """Request to report a fertilizer application."""

    actual_rate_kg_per_ha: float = Field(..., gt=0)
    actual_date: date
    notes: str | None = None


class ApplicationResponse(BaseModel):
    """Fertilizer application data in API responses."""

    id: uuid.UUID
    crop_id: str
    fertilizer_id: str
    fertilizer_name: str
    stage: str
    planned_rate_kg_per_ha: float
    actual_rate_kg_per_ha: float | None
    planned_day: int
    actual_date: date | None
    applied: bool
    notes: str | None


class PlanResponse(BaseModel):
    """Crop plan data in API responses."""

    id: uuid.UUID
    plot_id: uuid.UUID
    season: str
    year: int
    status: str
    crop_ids: list[str]
    risk_tolerance: float
    portfolio_weights: dict | None
    optimizer_result: dict | None
    confidence_metrics: dict | None
    applications: list[ApplicationResponse] = []


@router.post(
    "/generate",
    response_model=PlanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_plan(
    body: PlanGenerateSchema,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> PlanResponse:
    """Generate a new crop plan using the full optimization pipeline."""
    try:
        plan = await _plan_service.generate_plan(
            session=session,
            farmer_id=farmer.id,
            plot_id=body.plot_id,
            crop_ids=body.crop_ids,
            season=body.season,
            year=body.year,
            risk_tolerance=body.risk_tolerance,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _plan_to_response(plan)


@router.get("/", response_model=list[PlanResponse])
async def list_plans(
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[PlanResponse]:
    """List all crop plans for the authenticated farmer."""
    plans = await _plan_service.get_farmer_plans(session, farmer.id)
    return [_plan_to_response(p) for p in plans]


@router.get("/today", response_model=list[ApplicationResponse])
async def today_tasks(
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[ApplicationResponse]:
    """Get pending fertilizer applications for active plans."""
    apps = await _plan_service.get_today_tasks(session, farmer.id)
    return [_app_to_response(a) for a in apps]


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: uuid.UUID,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> PlanResponse:
    """Get a specific crop plan with its applications."""
    try:
        plan = await _plan_service.get_plan_detail(
            session, plan_id, farmer.id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return _plan_to_response(plan)


@router.post("/{plan_id}/accept", response_model=PlanResponse)
async def accept_plan(
    plan_id: uuid.UUID,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> PlanResponse:
    """Accept a draft plan (sets status to active)."""
    try:
        plan = await _plan_service.accept_plan(
            session, plan_id, farmer.id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return _plan_to_response(plan)


@router.post("/{plan_id}/reject", response_model=PlanResponse)
async def reject_plan(
    plan_id: uuid.UUID,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> PlanResponse:
    """Reject a draft plan (sets status to abandoned)."""
    try:
        plan = await _plan_service.reject_plan(
            session, plan_id, farmer.id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return _plan_to_response(plan)


@router.post(
    "/applications/{application_id}/report",
    response_model=ApplicationResponse,
)
async def report_application(
    application_id: uuid.UUID,
    body: ApplicationReportSchema,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ApplicationResponse:
    """Report that a fertilizer application has been completed."""
    try:
        app = await _plan_service.report_application(
            session=session,
            application_id=application_id,
            farmer_id=farmer.id,
            actual_rate=body.actual_rate_kg_per_ha,
            actual_date=body.actual_date,
            notes=body.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return _app_to_response(app)


def _app_to_response(app: object) -> ApplicationResponse:
    """Convert a FertilizerApplication ORM model to response."""
    return ApplicationResponse(
        id=app.id,  # type: ignore[attr-defined]
        crop_id=app.crop_id,  # type: ignore[attr-defined]
        fertilizer_id=app.fertilizer_id,  # type: ignore[attr-defined]
        fertilizer_name=app.fertilizer_name,  # type: ignore[attr-defined]
        stage=app.stage,  # type: ignore[attr-defined]
        planned_rate_kg_per_ha=app.planned_rate_kg_per_ha,  # type: ignore[attr-defined]
        actual_rate_kg_per_ha=app.actual_rate_kg_per_ha,  # type: ignore[attr-defined]
        planned_day=app.planned_day,  # type: ignore[attr-defined]
        actual_date=app.actual_date,  # type: ignore[attr-defined]
        applied=app.applied,  # type: ignore[attr-defined]
        notes=app.notes,  # type: ignore[attr-defined]
    )


def _plan_to_response(plan: object) -> PlanResponse:
    """Convert a CropPlan ORM model to response."""
    apps = []
    if hasattr(plan, "applications") and plan.applications:  # type: ignore[attr-defined]
        apps = [_app_to_response(a) for a in plan.applications]  # type: ignore[attr-defined]

    return PlanResponse(
        id=plan.id,  # type: ignore[attr-defined]
        plot_id=plan.plot_id,  # type: ignore[attr-defined]
        season=plan.season.value if hasattr(plan.season, "value") else plan.season,  # type: ignore[attr-defined]
        year=plan.year,  # type: ignore[attr-defined]
        status=plan.status.value if hasattr(plan.status, "value") else plan.status,  # type: ignore[attr-defined]
        crop_ids=plan.crop_ids,  # type: ignore[attr-defined]
        risk_tolerance=plan.risk_tolerance,  # type: ignore[attr-defined]
        portfolio_weights=plan.portfolio_weights,  # type: ignore[attr-defined]
        optimizer_result=plan.optimizer_result,  # type: ignore[attr-defined]
        confidence_metrics=plan.confidence_metrics,  # type: ignore[attr-defined]
        applications=apps,
    )
