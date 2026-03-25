"""Add farms, plots, crop_plans, fertilizer_applications tables.

Revision ID: 002_farms_plans
Revises: 001_initial
Create Date: 2026-03-25
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "002_farms_plans"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create farms, plots, crop_plans, fertilizer_applications tables."""
    season_enum = postgresql.ENUM(
        "monsoon", "dry", name="seasontype", create_type=False
    )
    season_enum.create(op.get_bind(), checkfirst=True)

    plan_status_enum = postgresql.ENUM(
        "draft", "active", "completed", "abandoned",
        name="planstatus", create_type=False,
    )
    plan_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "farms",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farmer_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("name_mm", sa.String(255), nullable=True),
        sa.Column("township_id", sa.String(50), nullable=False),
        sa.Column("total_area_hectares", sa.Float(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(["farmer_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_farms_farmer", "farms", ["farmer_id"])

    op.create_table(
        "plots",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("farm_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("area_hectares", sa.Float(), nullable=False),
        sa.Column("soil_type", sa.String(50), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(["farm_id"], ["farms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_plots_farm", "plots", ["farm_id"])

    op.create_table(
        "crop_plans",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("plot_id", sa.UUID(), nullable=False),
        sa.Column("farmer_id", sa.UUID(), nullable=False),
        sa.Column("distributor_id", sa.UUID(), nullable=True),
        sa.Column(
            "season",
            sa.Enum("monsoon", "dry", name="seasontype"),
            nullable=False,
        ),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "draft", "active", "completed", "abandoned",
                name="planstatus",
            ),
            server_default="draft",
            nullable=False,
        ),
        sa.Column("crop_ids", postgresql.JSONB(), nullable=False),
        sa.Column(
            "risk_tolerance", sa.Float(),
            server_default="0.5", nullable=False,
        ),
        sa.Column("portfolio_weights", postgresql.JSONB(), nullable=True),
        sa.Column("optimizer_result", postgresql.JSONB(), nullable=True),
        sa.Column("fertilizer_plans", postgresql.JSONB(), nullable=True),
        sa.Column("confidence_metrics", postgresql.JSONB(), nullable=True),
        sa.Column("ai_advisory", sa.Text(), nullable=True),
        sa.Column("ai_advisory_mm", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(["plot_id"], ["plots.id"]),
        sa.ForeignKeyConstraint(["farmer_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["distributor_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_crop_plans_farmer", "crop_plans", ["farmer_id"]
    )
    op.create_index(
        "idx_crop_plans_plot_season", "crop_plans",
        ["plot_id", "season", "year"],
    )

    op.create_table(
        "fertilizer_applications",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("crop_plan_id", sa.UUID(), nullable=False),
        sa.Column("crop_id", sa.String(50), nullable=False),
        sa.Column("fertilizer_id", sa.String(50), nullable=False),
        sa.Column("fertilizer_name", sa.String(100), nullable=False),
        sa.Column("stage", sa.String(50), nullable=False),
        sa.Column(
            "planned_rate_kg_per_ha", sa.Float(), nullable=False
        ),
        sa.Column("actual_rate_kg_per_ha", sa.Float(), nullable=True),
        sa.Column("planned_day", sa.Integer(), nullable=False),
        sa.Column("actual_date", sa.Date(), nullable=True),
        sa.Column(
            "applied", sa.Boolean(),
            server_default="false", nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["crop_plan_id"], ["crop_plans.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_fert_app_plan", "fertilizer_applications", ["crop_plan_id"]
    )


def downgrade() -> None:
    """Drop farms, plots, crop_plans, fertilizer_applications tables."""
    op.drop_table("fertilizer_applications")
    op.drop_table("crop_plans")
    op.drop_table("plots")
    op.drop_table("farms")
    sa.Enum("monsoon", "dry", name="seasontype").drop(
        op.get_bind(), checkfirst=True
    )
    sa.Enum(
        "draft", "active", "completed", "abandoned", name="planstatus"
    ).drop(op.get_bind(), checkfirst=True)
