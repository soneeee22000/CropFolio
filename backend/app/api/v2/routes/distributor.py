"""Distributor dashboard routes — farmer portfolio, loan summary, analytics."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_distributor
from app.infrastructure.database import get_session
from app.infrastructure.models import (
    CropPlan,
    Farm,
    Loan,
    LoanStatus,
    User,
    UserRole,
)

router = APIRouter()


class FarmerSummary(BaseModel):
    """Farmer in the distributor's portfolio."""

    id: uuid.UUID
    full_name: str
    full_name_mm: str | None
    phone_number: str | None
    township_id: str | None
    farm_count: int
    active_plan_count: int
    active_loan_count: int
    compliance_score: float | None
    credit_score: float | None


class FarmerDetailResponse(BaseModel):
    """Detailed farmer view with plans and loans."""

    id: uuid.UUID
    full_name: str
    full_name_mm: str | None
    phone_number: str | None
    township_id: str | None
    farms: list[dict]
    plans: list[dict]
    loans: list[dict]


class LoanPortfolioSummary(BaseModel):
    """Aggregate loan portfolio metrics."""

    total_loans: int
    active_loans: int
    total_disbursed_mmk: int
    total_repaid_mmk: int
    repayment_rate_pct: float
    default_count: int
    avg_compliance_score: float | None


class ComplianceOverviewItem(BaseModel):
    """Compliance summary per township."""

    township_id: str
    farmer_count: int
    avg_compliance: float | None
    compliant_count: int
    warning_count: int
    deviation_count: int


@router.get("/farmers", response_model=list[FarmerSummary])
async def list_farmers(
    distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[FarmerSummary]:
    """List all farmers with active loans under this distributor's org."""
    if distributor.organization_id is None:
        return []

    farmer_ids_stmt = (
        select(Loan.farmer_id)
        .where(Loan.organization_id == distributor.organization_id)
        .distinct()
    )
    result = await session.execute(farmer_ids_stmt)
    farmer_ids = [row[0] for row in result.all()]

    if not farmer_ids:
        return []

    farmers_result = await session.execute(
        select(User).where(User.id.in_(farmer_ids))
    )
    farmers = farmers_result.scalars().all()

    summaries = []
    for farmer in farmers:
        farm_count = await _count(
            session, Farm, Farm.farmer_id == farmer.id
        )
        plan_count = await _count(
            session, CropPlan,
            CropPlan.farmer_id == farmer.id,
            CropPlan.status == "active",
        )
        loan_count = await _count(
            session, Loan,
            Loan.farmer_id == farmer.id,
            Loan.status == LoanStatus.ACTIVE,
        )

        latest_loan = await session.execute(
            select(Loan)
            .where(Loan.farmer_id == farmer.id)
            .order_by(Loan.created_at.desc())
            .limit(1)
        )
        loan = latest_loan.scalar_one_or_none()

        summaries.append(
            FarmerSummary(
                id=farmer.id,
                full_name=farmer.full_name,
                full_name_mm=farmer.full_name_mm,
                phone_number=farmer.phone_number,
                township_id=farmer.township_id,
                farm_count=farm_count,
                active_plan_count=plan_count,
                active_loan_count=loan_count,
                compliance_score=(
                    loan.compliance_score if loan else None
                ),
                credit_score=(
                    loan.credit_score if loan else None
                ),
            )
        )
    return summaries


@router.get(
    "/farmers/{farmer_id}", response_model=FarmerDetailResponse
)
async def get_farmer_detail(
    farmer_id: uuid.UUID,
    distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> FarmerDetailResponse:
    """Get detailed farmer view with farms, plans, and loans."""
    farmer_result = await session.execute(
        select(User).where(
            User.id == farmer_id,
            User.role == UserRole.FARMER,
        )
    )
    farmer = farmer_result.scalar_one_or_none()
    if farmer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found",
        )

    farms_result = await session.execute(
        select(Farm)
        .where(Farm.farmer_id == farmer_id)
        .options(selectinload(Farm.plots))
    )
    farms = [
        {
            "id": str(f.id),
            "name": f.name,
            "township_id": f.township_id,
            "area_ha": f.total_area_hectares,
            "plot_count": len(f.plots) if f.plots else 0,
        }
        for f in farms_result.scalars().all()
    ]

    plans_result = await session.execute(
        select(CropPlan)
        .where(CropPlan.farmer_id == farmer_id)
        .order_by(CropPlan.created_at.desc())
        .limit(10)
    )
    plans = [
        {
            "id": str(p.id),
            "season": p.season.value,
            "year": p.year,
            "status": p.status.value,
            "crop_ids": p.crop_ids,
        }
        for p in plans_result.scalars().all()
    ]

    loans_result = await session.execute(
        select(Loan)
        .where(Loan.farmer_id == farmer_id)
        .order_by(Loan.created_at.desc())
        .limit(10)
    )
    loans = [
        {
            "id": str(ln.id),
            "principal_mmk": ln.principal_mmk,
            "status": ln.status.value,
            "total_repaid_mmk": ln.total_repaid_mmk,
            "compliance_score": ln.compliance_score,
            "credit_score": ln.credit_score,
        }
        for ln in loans_result.scalars().all()
    ]

    return FarmerDetailResponse(
        id=farmer.id,
        full_name=farmer.full_name,
        full_name_mm=farmer.full_name_mm,
        phone_number=farmer.phone_number,
        township_id=farmer.township_id,
        farms=farms,
        plans=plans,
        loans=loans,
    )


@router.get("/loans/summary", response_model=LoanPortfolioSummary)
async def get_loan_summary(
    distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> LoanPortfolioSummary:
    """Get aggregate loan portfolio metrics for the organization."""
    if distributor.organization_id is None:
        return LoanPortfolioSummary(
            total_loans=0, active_loans=0,
            total_disbursed_mmk=0, total_repaid_mmk=0,
            repayment_rate_pct=0.0, default_count=0,
            avg_compliance_score=None,
        )

    org_id = distributor.organization_id
    result = await session.execute(
        select(
            func.count(Loan.id).label("total"),
            func.count(Loan.id).filter(
                Loan.status == LoanStatus.ACTIVE
            ).label("active"),
            func.coalesce(
                func.sum(Loan.principal_mmk), 0
            ).label("disbursed"),
            func.coalesce(
                func.sum(Loan.total_repaid_mmk), 0
            ).label("repaid"),
            func.count(Loan.id).filter(
                Loan.status == LoanStatus.DEFAULTED
            ).label("defaulted"),
            func.avg(Loan.compliance_score).label("avg_comp"),
        ).where(Loan.organization_id == org_id)
    )
    row = result.one()

    total_disbursed = int(row.disbursed)
    total_repaid = int(row.repaid)
    repayment_rate = (
        (total_repaid / total_disbursed * 100)
        if total_disbursed > 0
        else 0.0
    )

    return LoanPortfolioSummary(
        total_loans=row.total,
        active_loans=row.active,
        total_disbursed_mmk=total_disbursed,
        total_repaid_mmk=total_repaid,
        repayment_rate_pct=round(repayment_rate, 2),
        default_count=row.defaulted,
        avg_compliance_score=(
            round(float(row.avg_comp), 4)
            if row.avg_comp is not None
            else None
        ),
    )


@router.get(
    "/compliance/overview",
    response_model=list[ComplianceOverviewItem],
)
async def get_compliance_overview(
    distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[ComplianceOverviewItem]:
    """Get compliance breakdown by township."""
    if distributor.organization_id is None:
        return []

    org_id = distributor.organization_id

    farmer_ids_stmt = (
        select(Loan.farmer_id)
        .where(Loan.organization_id == org_id)
        .distinct()
    )
    result = await session.execute(farmer_ids_stmt)
    farmer_ids = [row[0] for row in result.all()]

    if not farmer_ids:
        return []

    farmers_result = await session.execute(
        select(User).where(User.id.in_(farmer_ids))
    )
    farmers = farmers_result.scalars().all()

    township_map: dict[str, list[User]] = {}
    for f in farmers:
        tid = f.township_id or "unknown"
        township_map.setdefault(tid, []).append(f)

    overview = []
    for tid, township_farmers in township_map.items():
        scores: list[float] = []
        for f in township_farmers:
            loan_result = await session.execute(
                select(Loan.compliance_score)
                .where(
                    Loan.farmer_id == f.id,
                    Loan.compliance_score.isnot(None),
                )
                .order_by(Loan.created_at.desc())
                .limit(1)
            )
            score = loan_result.scalar_one_or_none()
            if score is not None:
                scores.append(score)

        avg_score = (
            sum(scores) / len(scores) if scores else None
        )
        compliant = sum(1 for s in scores if s >= 0.8)
        warning = sum(1 for s in scores if 0.5 <= s < 0.8)
        deviation = sum(1 for s in scores if s < 0.5)

        overview.append(
            ComplianceOverviewItem(
                township_id=tid,
                farmer_count=len(township_farmers),
                avg_compliance=(
                    round(avg_score, 4) if avg_score else None
                ),
                compliant_count=compliant,
                warning_count=warning,
                deviation_count=deviation,
            )
        )

    return overview


async def _count(
    session: AsyncSession, model: type, *filters: object
) -> int:
    """Count rows matching filters."""
    stmt = select(func.count()).select_from(model).where(*filters)
    result = await session.execute(stmt)
    return result.scalar_one()
