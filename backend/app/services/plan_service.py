"""Plan service: wraps RecommendationService with user context and persistence."""

from __future__ import annotations

import logging
import uuid
from dataclasses import asdict
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.infrastructure.models import (
    CropPlan,
    Farm,
    FertilizerApplication,
    PlanStatus,
    Plot,
    SeasonType,
)
from app.services.recommendation_service import (
    RecommendationService,
    get_recommendation_service,
)

logger = logging.getLogger(__name__)


class PlanService:
    """Generates, stores, and manages crop plans for individual farmers."""

    def __init__(
        self,
        recommendation_service: RecommendationService | None = None,
    ) -> None:
        """Initialize with the existing recommendation engine."""
        self._recommender = (
            recommendation_service or get_recommendation_service()
        )

    async def generate_plan(
        self,
        session: AsyncSession,
        farmer_id: uuid.UUID,
        plot_id: uuid.UUID,
        crop_ids: list[str],
        season: str,
        year: int,
        risk_tolerance: float = 0.5,
    ) -> CropPlan:
        """Generate a crop plan by running the full optimization pipeline.

        Looks up the plot's township, calls RecommendationService, and
        persists the result as a CropPlan with FertilizerApplications.
        """
        plot = await self._get_plot_for_farmer(
            session, plot_id, farmer_id
        )

        results = await self._recommender.recommend(
            township_ids=[plot.farm.township_id],
            crop_ids=crop_ids,
            risk_tolerance=risk_tolerance,
            season=season,
        )
        if not results:
            msg = "Recommendation engine returned no results"
            raise RuntimeError(msg)

        rec = results[0]

        weights = {
            cr.crop.id: round(cr.weight, 4)
            for cr in rec.crop_results
        }
        fert_plans_json = {
            cr.crop.id: _serialize_fert_plan(cr.fertilizer_plan)
            for cr in rec.crop_results
            if cr.fertilizer_plan is not None
        }
        optimizer_json = {
            "expected_income_per_ha": rec.expected_income,
            "risk_reduction_pct": rec.risk_reduction_pct,
        }

        plan = CropPlan(
            id=uuid.uuid4(),
            plot_id=plot_id,
            farmer_id=farmer_id,
            season=SeasonType(season),
            year=year,
            status=PlanStatus.DRAFT,
            crop_ids=crop_ids,
            risk_tolerance=risk_tolerance,
            portfolio_weights=weights,
            optimizer_result=optimizer_json,
            fertilizer_plans=fert_plans_json,
            confidence_metrics=rec.confidence,
        )
        session.add(plan)
        await session.flush()

        for cr in rec.crop_results:
            if cr.fertilizer_plan is None:
                continue
            for app in cr.fertilizer_plan.applications:
                fert_app = FertilizerApplication(
                    id=uuid.uuid4(),
                    crop_plan_id=plan.id,
                    crop_id=cr.crop.id,
                    fertilizer_id=app.fertilizer_id,
                    fertilizer_name=app.fertilizer_name,
                    stage=app.stage,
                    planned_rate_kg_per_ha=app.rate_kg_per_ha,
                    planned_day=app.day,
                )
                session.add(fert_app)

        await session.flush()
        logger.info("Plan %s generated for farmer %s", plan.id, farmer_id)
        return plan

    async def accept_plan(
        self,
        session: AsyncSession,
        plan_id: uuid.UUID,
        farmer_id: uuid.UUID,
    ) -> CropPlan:
        """Mark a draft plan as active (farmer accepted)."""
        plan = await self._get_plan(session, plan_id, farmer_id)
        if plan.status != PlanStatus.DRAFT:
            msg = f"Cannot accept plan in status '{plan.status.value}'"
            raise ValueError(msg)
        plan.status = PlanStatus.ACTIVE
        await session.flush()
        return plan

    async def reject_plan(
        self,
        session: AsyncSession,
        plan_id: uuid.UUID,
        farmer_id: uuid.UUID,
    ) -> CropPlan:
        """Mark a draft plan as abandoned (farmer rejected)."""
        plan = await self._get_plan(session, plan_id, farmer_id)
        if plan.status != PlanStatus.DRAFT:
            msg = f"Cannot reject plan in status '{plan.status.value}'"
            raise ValueError(msg)
        plan.status = PlanStatus.ABANDONED
        await session.flush()
        return plan

    async def report_application(
        self,
        session: AsyncSession,
        application_id: uuid.UUID,
        farmer_id: uuid.UUID,
        actual_rate: float,
        actual_date: date,
        notes: str | None = None,
    ) -> FertilizerApplication:
        """Record that a farmer applied fertilizer."""
        result = await session.execute(
            select(FertilizerApplication)
            .join(CropPlan)
            .where(
                FertilizerApplication.id == application_id,
                CropPlan.farmer_id == farmer_id,
            )
        )
        app = result.scalar_one_or_none()
        if app is None:
            msg = "Application not found or unauthorized"
            raise ValueError(msg)

        app.actual_rate_kg_per_ha = actual_rate
        app.actual_date = actual_date  # type: ignore[assignment]
        app.applied = True
        app.notes = notes
        await session.flush()
        return app

    async def get_farmer_plans(
        self,
        session: AsyncSession,
        farmer_id: uuid.UUID,
    ) -> list[CropPlan]:
        """List all plans for a farmer."""
        result = await session.execute(
            select(CropPlan)
            .where(CropPlan.farmer_id == farmer_id)
            .options(selectinload(CropPlan.applications))
            .order_by(CropPlan.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_plan_detail(
        self,
        session: AsyncSession,
        plan_id: uuid.UUID,
        farmer_id: uuid.UUID,
    ) -> CropPlan:
        """Get a single plan with its applications."""
        result = await session.execute(
            select(CropPlan)
            .where(
                CropPlan.id == plan_id,
                CropPlan.farmer_id == farmer_id,
            )
            .options(selectinload(CropPlan.applications))
        )
        plan = result.scalar_one_or_none()
        if plan is None:
            msg = "Plan not found"
            raise ValueError(msg)
        return plan

    async def get_today_tasks(
        self,
        session: AsyncSession,
        farmer_id: uuid.UUID,
    ) -> list[FertilizerApplication]:
        """Get pending fertilizer applications for active plans.

        Returns applications that haven't been applied yet,
        ordered by planned_day (soonest first).
        """
        result = await session.execute(
            select(FertilizerApplication)
            .join(CropPlan)
            .where(
                CropPlan.farmer_id == farmer_id,
                CropPlan.status == PlanStatus.ACTIVE,
                FertilizerApplication.applied.is_(False),
            )
            .order_by(FertilizerApplication.planned_day)
        )
        return list(result.scalars().all())

    async def _get_plan(
        self,
        session: AsyncSession,
        plan_id: uuid.UUID,
        farmer_id: uuid.UUID,
    ) -> CropPlan:
        """Fetch a plan ensuring it belongs to the farmer."""
        result = await session.execute(
            select(CropPlan).where(
                CropPlan.id == plan_id,
                CropPlan.farmer_id == farmer_id,
            )
        )
        plan = result.scalar_one_or_none()
        if plan is None:
            msg = "Plan not found or unauthorized"
            raise ValueError(msg)
        return plan

    async def _get_plot_for_farmer(
        self,
        session: AsyncSession,
        plot_id: uuid.UUID,
        farmer_id: uuid.UUID,
    ) -> Plot:
        """Fetch a plot ensuring it belongs to the farmer's farm."""
        result = await session.execute(
            select(Plot)
            .join(Farm)
            .where(
                Plot.id == plot_id,
                Farm.farmer_id == farmer_id,
            )
            .options(selectinload(Plot.farm))
        )
        plot = result.scalar_one_or_none()
        if plot is None:
            msg = "Plot not found or unauthorized"
            raise ValueError(msg)
        return plot


def _serialize_fert_plan(plan: object) -> dict:
    """Serialize a FertilizerPlan dataclass to JSON-safe dict."""
    try:
        return asdict(plan)  # type: ignore[arg-type]
    except Exception:
        return {"error": "serialization_failed"}
