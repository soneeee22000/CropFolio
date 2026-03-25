"""Loan lifecycle management service."""

from __future__ import annotations

import logging
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.infrastructure.models import (
    Loan,
    LoanRepayment,
    LoanStatus,
)

logger = logging.getLogger(__name__)


class LoanService:
    """Manages loan creation, disbursement, repayment, and status."""

    async def create_loan(
        self,
        session: AsyncSession,
        farmer_id: uuid.UUID,
        distributor_id: uuid.UUID,
        organization_id: uuid.UUID,
        principal_mmk: int,
        crop_plan_id: uuid.UUID | None = None,
        interest_rate_pct: float = 0.0,
        due_date: date | None = None,
        notes: str | None = None,
    ) -> Loan:
        """Create a new loan from distributor to farmer."""
        loan = Loan(
            id=uuid.uuid4(),
            farmer_id=farmer_id,
            distributor_id=distributor_id,
            organization_id=organization_id,
            crop_plan_id=crop_plan_id,
            principal_mmk=principal_mmk,
            interest_rate_pct=interest_rate_pct,
            due_date=due_date,  # type: ignore[arg-type]
            status=LoanStatus.PENDING,
            notes=notes,
        )
        session.add(loan)
        await session.flush()
        logger.info("Loan %s created: %d MMK", loan.id, principal_mmk)
        return loan

    async def disburse_loan(
        self,
        session: AsyncSession,
        loan_id: uuid.UUID,
        distributor_id: uuid.UUID,
    ) -> Loan:
        """Mark a pending loan as disbursed (active)."""
        loan = await self._get_loan(session, loan_id)
        if loan.distributor_id != distributor_id:
            msg = "Unauthorized: not your loan"
            raise ValueError(msg)
        if loan.status != LoanStatus.PENDING:
            msg = f"Cannot disburse loan in status '{loan.status.value}'"
            raise ValueError(msg)
        loan.status = LoanStatus.ACTIVE
        loan.disbursed_at = datetime.now(timezone.utc)
        await session.flush()
        return loan

    async def record_repayment(
        self,
        session: AsyncSession,
        loan_id: uuid.UUID,
        amount_mmk: int,
        recorded_by: uuid.UUID,
    ) -> LoanRepayment:
        """Record a loan repayment and update totals."""
        loan = await self._get_loan(session, loan_id)
        if loan.status not in (LoanStatus.ACTIVE, LoanStatus.PENDING):
            msg = f"Cannot repay loan in status '{loan.status.value}'"
            raise ValueError(msg)

        repayment = LoanRepayment(
            id=uuid.uuid4(),
            loan_id=loan_id,
            amount_mmk=amount_mmk,
            recorded_by=recorded_by,
        )
        session.add(repayment)

        loan.total_repaid_mmk += amount_mmk
        if loan.total_repaid_mmk >= loan.principal_mmk:
            loan.status = LoanStatus.REPAID
            logger.info("Loan %s fully repaid", loan_id)

        await session.flush()
        return repayment

    async def get_farmer_loans(
        self,
        session: AsyncSession,
        farmer_id: uuid.UUID,
    ) -> list[Loan]:
        """List all loans for a farmer."""
        result = await session.execute(
            select(Loan)
            .where(Loan.farmer_id == farmer_id)
            .options(selectinload(Loan.repayments))
            .order_by(Loan.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_distributor_loans(
        self,
        session: AsyncSession,
        organization_id: uuid.UUID,
    ) -> list[Loan]:
        """List all loans for a distributor's organization."""
        result = await session.execute(
            select(Loan)
            .where(Loan.organization_id == organization_id)
            .options(selectinload(Loan.repayments))
            .order_by(Loan.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_loan_detail(
        self,
        session: AsyncSession,
        loan_id: uuid.UUID,
    ) -> Loan:
        """Get a single loan with repayments."""
        return await self._get_loan(session, loan_id)

    async def _get_loan(
        self, session: AsyncSession, loan_id: uuid.UUID
    ) -> Loan:
        """Fetch a loan by ID."""
        result = await session.execute(
            select(Loan)
            .where(Loan.id == loan_id)
            .options(selectinload(Loan.repayments))
        )
        loan = result.scalar_one_or_none()
        if loan is None:
            msg = "Loan not found"
            raise ValueError(msg)
        return loan
