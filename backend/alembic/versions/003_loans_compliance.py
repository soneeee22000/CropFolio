"""Add loans, loan_repayments, compliance_checks, credit_score_history.

Revision ID: 003_loans_compliance
Revises: 002_farms_plans
Create Date: 2026-03-25
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "003_loans_compliance"
down_revision = "002_farms_plans"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create loan and compliance tables."""
    loan_status = postgresql.ENUM(
        "pending", "active", "repaid", "defaulted", "written_off",
        name="loanstatus", create_type=False,
    )
    loan_status.create(op.get_bind(), checkfirst=True)

    compliance_level = postgresql.ENUM(
        "compliant", "warning", "deviation", "unknown",
        name="compliancelevel", create_type=False,
    )
    compliance_level.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "loans",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farmer_id", sa.UUID(), nullable=False),
        sa.Column("distributor_id", sa.UUID(), nullable=False),
        sa.Column("organization_id", sa.UUID(), nullable=False),
        sa.Column("crop_plan_id", sa.UUID(), nullable=True),
        sa.Column("principal_mmk", sa.Integer(), nullable=False),
        sa.Column(
            "interest_rate_pct", sa.Float(),
            server_default="0.0", nullable=False,
        ),
        sa.Column(
            "disbursed_at", sa.DateTime(timezone=True), nullable=True,
        ),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "pending", "active", "repaid", "defaulted",
                "written_off", name="loanstatus",
            ),
            server_default="pending", nullable=False,
        ),
        sa.Column(
            "total_repaid_mmk", sa.Integer(),
            server_default="0", nullable=False,
        ),
        sa.Column("compliance_score", sa.Float(), nullable=True),
        sa.Column("credit_score", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(["farmer_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["distributor_id"], ["users.id"]),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"]
        ),
        sa.ForeignKeyConstraint(["crop_plan_id"], ["crop_plans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_loans_farmer", "loans", ["farmer_id"])
    op.create_index("idx_loans_distributor", "loans", ["distributor_id"])
    op.create_index("idx_loans_org", "loans", ["organization_id"])

    op.create_table(
        "loan_repayments",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("loan_id", sa.UUID(), nullable=False),
        sa.Column("amount_mmk", sa.Integer(), nullable=False),
        sa.Column(
            "repaid_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.Column("recorded_by", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(["loan_id"], ["loans.id"]),
        sa.ForeignKeyConstraint(["recorded_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "compliance_checks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("crop_plan_id", sa.UUID(), nullable=False),
        sa.Column("check_date", sa.Date(), nullable=False),
        sa.Column(
            "level",
            sa.Enum(
                "compliant", "warning", "deviation", "unknown",
                name="compliancelevel",
            ),
            nullable=False,
        ),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("deviations", postgresql.JSONB(), nullable=True),
        sa.Column(
            "sar_verified", sa.Boolean(),
            server_default="false", nullable=False,
        ),
        sa.Column("checked_by", sa.UUID(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["crop_plan_id"], ["crop_plans.id"]
        ),
        sa.ForeignKeyConstraint(["checked_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_compliance_plan", "compliance_checks", ["crop_plan_id"]
    )

    op.create_table(
        "credit_score_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farmer_id", sa.UUID(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("factors", postgresql.JSONB(), nullable=False),
        sa.Column(
            "season",
            sa.Enum("monsoon", "dry", name="seasontype"),
            nullable=False,
        ),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(["farmer_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_credit_farmer", "credit_score_history", ["farmer_id"]
    )


def downgrade() -> None:
    """Drop loan and compliance tables."""
    op.drop_table("credit_score_history")
    op.drop_table("compliance_checks")
    op.drop_table("loan_repayments")
    op.drop_table("loans")
    sa.Enum(
        "pending", "active", "repaid", "defaulted", "written_off",
        name="loanstatus",
    ).drop(op.get_bind(), checkfirst=True)
    sa.Enum(
        "compliant", "warning", "deviation", "unknown",
        name="compliancelevel",
    ).drop(op.get_bind(), checkfirst=True)
