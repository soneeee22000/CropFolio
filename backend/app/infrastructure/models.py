"""SQLAlchemy ORM models for the CropFolio B2B2C platform."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class UserRole(str, enum.Enum):
    """User role within the platform."""

    FARMER = "farmer"
    DISTRIBUTOR = "distributor"
    ADMIN = "admin"


class Organization(Base):
    """Multi-tenancy root — each distributor company is one organization."""

    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_mm: Mapped[str | None] = mapped_column(String(255))
    org_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="distributor"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    users: Mapped[list[User]] = relationship("User", back_populates="organization")


class User(Base):
    """Platform user — polymorphic across farmer, distributor, admin roles."""

    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_phone", "phone_number", unique=True),
        Index("idx_users_email", "email", unique=True),
        Index("idx_users_org", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id")
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name_mm: Mapped[str | None] = mapped_column(String(255))
    preferred_language: Mapped[str] = mapped_column(String(5), default="mm")
    township_id: Mapped[str | None] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    organization: Mapped[Organization | None] = relationship(
        "Organization", back_populates="users"
    )


class OTPCode(Base):
    """One-time password for farmer phone authentication."""

    __tablename__ = "otp_codes"
    __table_args__ = (Index("idx_otp_phone", "phone_number", "verified"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# ──────────────────────────────────────────────────────
# Phase 2: Farm & Plan Management
# ──────────────────────────────────────────────────────


class SeasonType(str, enum.Enum):
    """Growing season type."""

    MONSOON = "monsoon"
    DRY = "dry"


class PlanStatus(str, enum.Enum):
    """Crop plan lifecycle status."""

    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class Farm(Base):
    """A farmer's registered farm."""

    __tablename__ = "farms"
    __table_args__ = (Index("idx_farms_farmer", "farmer_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_mm: Mapped[str | None] = mapped_column(String(255))
    township_id: Mapped[str] = mapped_column(String(50), nullable=False)
    total_area_hectares: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    farmer: Mapped[User] = relationship("User")
    plots: Mapped[list[Plot]] = relationship(
        "Plot", back_populates="farm", cascade="all, delete-orphan"
    )


class Plot(Base):
    """A subdivision of a farm for individual crop planning."""

    __tablename__ = "plots"
    __table_args__ = (Index("idx_plots_farm", "farm_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farms.id"), nullable=False
    )
    name: Mapped[str | None] = mapped_column(String(100))
    area_hectares: Mapped[float] = mapped_column(Float, nullable=False)
    soil_type: Mapped[str | None] = mapped_column(String(50))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    farm: Mapped[Farm] = relationship("Farm", back_populates="plots")
    crop_plans: Mapped[list[CropPlan]] = relationship(
        "CropPlan", back_populates="plot"
    )


class CropPlan(Base):
    """A crop plan for one plot in one season — stores optimizer snapshot."""

    __tablename__ = "crop_plans"
    __table_args__ = (
        Index("idx_crop_plans_farmer", "farmer_id"),
        Index("idx_crop_plans_plot_season", "plot_id", "season", "year"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    plot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("plots.id"), nullable=False
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    distributor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    season: Mapped[SeasonType] = mapped_column(
        Enum(SeasonType), nullable=False
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[PlanStatus] = mapped_column(
        Enum(PlanStatus), default=PlanStatus.DRAFT
    )
    crop_ids: Mapped[dict] = mapped_column(JSONB, nullable=False)
    risk_tolerance: Mapped[float] = mapped_column(Float, default=0.5)
    portfolio_weights: Mapped[dict | None] = mapped_column(JSONB)
    optimizer_result: Mapped[dict | None] = mapped_column(JSONB)
    fertilizer_plans: Mapped[dict | None] = mapped_column(JSONB)
    confidence_metrics: Mapped[dict | None] = mapped_column(JSONB)
    ai_advisory: Mapped[str | None] = mapped_column(Text)
    ai_advisory_mm: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    plot: Mapped[Plot] = relationship("Plot", back_populates="crop_plans")
    farmer: Mapped[User] = relationship("User", foreign_keys=[farmer_id])
    applications: Mapped[list[FertilizerApplication]] = relationship(
        "FertilizerApplication",
        back_populates="crop_plan",
        cascade="all, delete-orphan",
    )


class FertilizerApplication(Base):
    """A single scheduled fertilizer application within a crop plan."""

    __tablename__ = "fertilizer_applications"
    __table_args__ = (
        Index("idx_fert_app_plan", "crop_plan_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    crop_plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("crop_plans.id"), nullable=False
    )
    crop_id: Mapped[str] = mapped_column(String(50), nullable=False)
    fertilizer_id: Mapped[str] = mapped_column(String(50), nullable=False)
    fertilizer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    stage: Mapped[str] = mapped_column(String(50), nullable=False)
    planned_rate_kg_per_ha: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    actual_rate_kg_per_ha: Mapped[float | None] = mapped_column(Float)
    planned_day: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_date: Mapped[datetime | None] = mapped_column(Date)
    applied: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    crop_plan: Mapped[CropPlan] = relationship(
        "CropPlan", back_populates="applications"
    )


# ──────────────────────────────────────────────────────
# Phase 3: Loan-Compliance System
# ──────────────────────────────────────────────────────


class LoanStatus(str, enum.Enum):
    """Loan lifecycle status."""

    PENDING = "pending"
    ACTIVE = "active"
    REPAID = "repaid"
    DEFAULTED = "defaulted"
    WRITTEN_OFF = "written_off"


class ComplianceLevel(str, enum.Enum):
    """Compliance check result level."""

    COMPLIANT = "compliant"
    WARNING = "warning"
    DEVIATION = "deviation"
    UNKNOWN = "unknown"


class Loan(Base):
    """Fertilizer loan from distributor to farmer, tied to a crop plan."""

    __tablename__ = "loans"
    __table_args__ = (
        Index("idx_loans_farmer", "farmer_id"),
        Index("idx_loans_distributor", "distributor_id"),
        Index("idx_loans_org", "organization_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    distributor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
    )
    crop_plan_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("crop_plans.id")
    )
    principal_mmk: Mapped[int] = mapped_column(Integer, nullable=False)
    interest_rate_pct: Mapped[float] = mapped_column(Float, default=0.0)
    disbursed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    due_date: Mapped[datetime | None] = mapped_column(Date)
    status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus), default=LoanStatus.PENDING
    )
    total_repaid_mmk: Mapped[int] = mapped_column(Integer, default=0)
    compliance_score: Mapped[float | None] = mapped_column(Float)
    credit_score: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    farmer: Mapped[User] = relationship("User", foreign_keys=[farmer_id])
    distributor: Mapped[User] = relationship(
        "User", foreign_keys=[distributor_id]
    )
    crop_plan: Mapped[CropPlan | None] = relationship("CropPlan")
    repayments: Mapped[list[LoanRepayment]] = relationship(
        "LoanRepayment", back_populates="loan"
    )


class LoanRepayment(Base):
    """Individual loan repayment record."""

    __tablename__ = "loan_repayments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("loans.id"), nullable=False
    )
    amount_mmk: Mapped[int] = mapped_column(Integer, nullable=False)
    repaid_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    recorded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )

    loan: Mapped[Loan] = relationship("Loan", back_populates="repayments")


class ComplianceCheck(Base):
    """Periodic compliance snapshot for a crop plan."""

    __tablename__ = "compliance_checks"
    __table_args__ = (
        Index("idx_compliance_plan", "crop_plan_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    crop_plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("crop_plans.id"), nullable=False
    )
    check_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    level: Mapped[ComplianceLevel] = mapped_column(
        Enum(ComplianceLevel), nullable=False
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    deviations: Mapped[dict | None] = mapped_column(JSONB)
    sar_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    checked_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    crop_plan: Mapped[CropPlan] = relationship("CropPlan")


class CreditScoreHistory(Base):
    """Historical credit score record for a farmer."""

    __tablename__ = "credit_score_history"
    __table_args__ = (
        Index("idx_credit_farmer", "farmer_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    factors: Mapped[dict] = mapped_column(JSONB, nullable=False)
    season: Mapped[SeasonType] = mapped_column(
        Enum(SeasonType), nullable=False
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
