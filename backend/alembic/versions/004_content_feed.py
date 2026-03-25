"""Add content and content_interactions tables.

Revision ID: 004_content_feed
Revises: 003_loans_compliance
Create Date: 2026-03-25
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "004_content_feed"
down_revision = "003_loans_compliance"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create content and content_interactions tables."""
    content_type = postgresql.ENUM(
        "weather_alert", "pest_alert", "fertilizer_reminder",
        "tip", "market_update",
        name="contenttype", create_type=False,
    )
    content_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "content",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("organization_id", sa.UUID(), nullable=True),
        sa.Column(
            "content_type",
            sa.Enum(
                "weather_alert", "pest_alert", "fertilizer_reminder",
                "tip", "market_update", name="contenttype",
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("title_mm", sa.String(255), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("body_mm", sa.Text(), nullable=True),
        sa.Column("audio_url", sa.String(500), nullable=True),
        sa.Column("township_ids", postgresql.JSONB(), nullable=True),
        sa.Column("crop_ids", postgresql.JSONB(), nullable=True),
        sa.Column(
            "published", sa.Boolean(),
            server_default="false", nullable=False,
        ),
        sa.Column(
            "published_at", sa.DateTime(timezone=True), nullable=True,
        ),
        sa.Column(
            "expires_at", sa.DateTime(timezone=True), nullable=True,
        ),
        sa.Column("created_by", sa.UUID(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"]
        ),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_content_type", "content",
        ["content_type", "published"],
    )
    op.create_index(
        "idx_content_org", "content", ["organization_id"],
    )

    op.create_table(
        "content_interactions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("content_id", sa.UUID(), nullable=False),
        sa.Column("farmer_id", sa.UUID(), nullable=False),
        sa.Column(
            "viewed", sa.Boolean(),
            server_default="false", nullable=False,
        ),
        sa.Column(
            "viewed_at", sa.DateTime(timezone=True), nullable=True,
        ),
        sa.Column("helpful", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()"), nullable=False,
        ),
        sa.ForeignKeyConstraint(["content_id"], ["content.id"]),
        sa.ForeignKeyConstraint(["farmer_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop content tables."""
    op.drop_table("content_interactions")
    op.drop_table("content")
    sa.Enum(
        "weather_alert", "pest_alert", "fertilizer_reminder",
        "tip", "market_update", name="contenttype",
    ).drop(op.get_bind(), checkfirst=True)
