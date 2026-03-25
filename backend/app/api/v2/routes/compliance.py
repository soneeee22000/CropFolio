"""Compliance overview and scoring routes."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_user
from app.domain.compliance_scorer import (
    ApplicationRecord,
    ComplianceResult,
    compute_compliance_score,
)
from app.infrastructure.database import get_session
from app.infrastructure.models import CropPlan, User

router = APIRouter()


class ComplianceResponse(BaseModel):
    """Compliance scoring result for a crop plan."""

    plan_id: uuid.UUID
    overall_score: float
    timing_score: float
    quantity_score: float
    crop_selection_score: float
    sar_score: float
    reporting_score: float
    level: str
    deviations: list[str]


@router.get(
    "/plan/{plan_id}",
    response_model=ComplianceResponse,
)
async def get_plan_compliance(
    plan_id: uuid.UUID,
    user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ComplianceResponse:
    """Compute compliance score for a specific crop plan."""
    result = await session.execute(
        select(CropPlan)
        .where(CropPlan.id == plan_id)
        .options(selectinload(CropPlan.applications))
    )
    plan = result.scalar_one_or_none()
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )

    if (
        plan.farmer_id != user.id
        and user.role.value != "distributor"
        and user.role.value != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this plan",
        )

    compliance = _compute_for_plan(plan)
    return ComplianceResponse(
        plan_id=plan.id,
        overall_score=compliance.overall_score,
        timing_score=compliance.timing_score,
        quantity_score=compliance.quantity_score,
        crop_selection_score=compliance.crop_selection_score,
        sar_score=compliance.sar_score,
        reporting_score=compliance.reporting_score,
        level=compliance.level,
        deviations=compliance.deviations,
    )


@router.get(
    "/farmer/{farmer_id}",
    response_model=list[ComplianceResponse],
)
async def get_farmer_compliance(
    farmer_id: uuid.UUID,
    user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[ComplianceResponse]:
    """Get compliance scores for all plans of a farmer."""
    if (
        user.id != farmer_id
        and user.role.value not in ("distributor", "admin")
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    result = await session.execute(
        select(CropPlan)
        .where(CropPlan.farmer_id == farmer_id)
        .options(selectinload(CropPlan.applications))
    )
    plans = result.scalars().all()

    responses = []
    for plan in plans:
        compliance = _compute_for_plan(plan)
        responses.append(
            ComplianceResponse(
                plan_id=plan.id,
                overall_score=compliance.overall_score,
                timing_score=compliance.timing_score,
                quantity_score=compliance.quantity_score,
                crop_selection_score=compliance.crop_selection_score,
                sar_score=compliance.sar_score,
                reporting_score=compliance.reporting_score,
                level=compliance.level,
                deviations=compliance.deviations,
            )
        )
    return responses


def _compute_for_plan(plan: CropPlan) -> ComplianceResult:
    """Build ApplicationRecords from ORM and compute compliance."""
    apps = [
        ApplicationRecord(
            planned_day=a.planned_day,
            actual_day=(
                (a.actual_date - a.actual_date).days  # type: ignore[operator]
                if a.actual_date
                else None
            ),
            planned_rate=a.planned_rate_kg_per_ha,
            actual_rate=a.actual_rate_kg_per_ha,
            applied=a.applied,
        )
        for a in (plan.applications or [])
    ]

    max_day = max(
        (a.planned_day for a in apps), default=0
    )

    return compute_compliance_score(
        applications=apps,
        crop_ids_planned=(
            plan.crop_ids
            if isinstance(plan.crop_ids, list)
            else list(plan.crop_ids)
        ),
        current_day=max_day,
    )
