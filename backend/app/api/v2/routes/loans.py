"""Loan management routes for distributors and farmers."""

from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import (
    get_current_distributor,
    get_current_user,
)
from app.infrastructure.database import get_session
from app.infrastructure.models import User
from app.services.loan_service import LoanService

router = APIRouter()
_loan_service = LoanService()


class LoanCreateSchema(BaseModel):
    """Distributor creates a loan for a farmer."""

    farmer_id: uuid.UUID
    principal_mmk: int = Field(..., gt=0)
    crop_plan_id: uuid.UUID | None = None
    interest_rate_pct: float = Field(0.0, ge=0.0)
    due_date: date | None = None
    notes: str | None = None


class RepaymentSchema(BaseModel):
    """Record a loan repayment."""

    amount_mmk: int = Field(..., gt=0)


class RepaymentResponse(BaseModel):
    """Repayment data in API response."""

    id: uuid.UUID
    amount_mmk: int
    repaid_at: str


class LoanResponse(BaseModel):
    """Loan data in API responses."""

    id: uuid.UUID
    farmer_id: uuid.UUID
    distributor_id: uuid.UUID
    organization_id: uuid.UUID
    crop_plan_id: uuid.UUID | None
    principal_mmk: int
    interest_rate_pct: float
    status: str
    total_repaid_mmk: int
    compliance_score: float | None
    credit_score: float | None
    due_date: date | None
    notes: str | None
    repayments: list[RepaymentResponse] = []


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_loan(
    body: LoanCreateSchema,
    distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> LoanResponse:
    """Create a new loan for a farmer (distributor-only)."""
    if distributor.organization_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Distributor must belong to an organization",
        )
    try:
        loan = await _loan_service.create_loan(
            session=session,
            farmer_id=body.farmer_id,
            distributor_id=distributor.id,
            organization_id=distributor.organization_id,
            principal_mmk=body.principal_mmk,
            crop_plan_id=body.crop_plan_id,
            interest_rate_pct=body.interest_rate_pct,
            due_date=body.due_date,
            notes=body.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return _loan_to_response(loan)


@router.get("/", response_model=list[LoanResponse])
async def list_loans(
    user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[LoanResponse]:
    """List loans — farmers see their loans, distributors see org loans."""
    if user.role.value == "farmer":
        loans = await _loan_service.get_farmer_loans(session, user.id)
    elif user.organization_id is not None:
        loans = await _loan_service.get_distributor_loans(
            session, user.organization_id
        )
    else:
        loans = []
    return [_loan_to_response(ln) for ln in loans]


@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
    loan_id: uuid.UUID,
    _user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> LoanResponse:
    """Get loan detail."""
    try:
        loan = await _loan_service.get_loan_detail(session, loan_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return _loan_to_response(loan)


@router.post("/{loan_id}/disburse", response_model=LoanResponse)
async def disburse_loan(
    loan_id: uuid.UUID,
    distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> LoanResponse:
    """Mark a loan as disbursed (distributor-only)."""
    try:
        loan = await _loan_service.disburse_loan(
            session, loan_id, distributor.id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return _loan_to_response(loan)


@router.post(
    "/{loan_id}/repayments",
    response_model=RepaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def record_repayment(
    loan_id: uuid.UUID,
    body: RepaymentSchema,
    user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> RepaymentResponse:
    """Record a loan repayment."""
    try:
        repayment = await _loan_service.record_repayment(
            session, loan_id, body.amount_mmk, user.id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return RepaymentResponse(
        id=repayment.id,
        amount_mmk=repayment.amount_mmk,
        repaid_at=str(repayment.repaid_at),
    )


def _loan_to_response(loan: object) -> LoanResponse:
    """Convert a Loan ORM model to response schema."""
    repayments = []
    if hasattr(loan, "repayments") and loan.repayments:  # type: ignore[attr-defined]
        repayments = [
            RepaymentResponse(
                id=r.id,
                amount_mmk=r.amount_mmk,
                repaid_at=str(r.repaid_at),
            )
            for r in loan.repayments  # type: ignore[attr-defined]
        ]
    return LoanResponse(
        id=loan.id,  # type: ignore[attr-defined]
        farmer_id=loan.farmer_id,  # type: ignore[attr-defined]
        distributor_id=loan.distributor_id,  # type: ignore[attr-defined]
        organization_id=loan.organization_id,  # type: ignore[attr-defined]
        crop_plan_id=loan.crop_plan_id,  # type: ignore[attr-defined]
        principal_mmk=loan.principal_mmk,  # type: ignore[attr-defined]
        interest_rate_pct=loan.interest_rate_pct,  # type: ignore[attr-defined]
        status=loan.status.value if hasattr(loan.status, "value") else loan.status,  # type: ignore[attr-defined]
        total_repaid_mmk=loan.total_repaid_mmk,  # type: ignore[attr-defined]
        compliance_score=loan.compliance_score,  # type: ignore[attr-defined]
        credit_score=loan.credit_score,  # type: ignore[attr-defined]
        due_date=loan.due_date,  # type: ignore[attr-defined]
        notes=loan.notes,  # type: ignore[attr-defined]
        repayments=repayments,
    )
