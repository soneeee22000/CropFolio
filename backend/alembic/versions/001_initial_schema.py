"""Initial schema: organizations, users, otp_codes.

Revision ID: 001_initial
Revises:
Create Date: 2026-03-25
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create organizations, users, and otp_codes tables."""
    userrole_enum = postgresql.ENUM(
        "farmer", "distributor", "admin", name="userrole", create_type=False
    )
    userrole_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "organizations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("name_mm", sa.String(length=255), nullable=True),
        sa.Column(
            "org_type",
            sa.String(length=50),
            nullable=False,
            server_default="distributor",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column(
            "role",
            sa.Enum("farmer", "distributor", "admin", name="userrole"),
            nullable=False,
        ),
        sa.Column("organization_id", sa.UUID(), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("full_name_mm", sa.String(length=255), nullable=True),
        sa.Column(
            "preferred_language",
            sa.String(length=5),
            server_default="mm",
            nullable=False,
        ),
        sa.Column("township_id", sa.String(length=50), nullable=True),
        sa.Column(
            "is_active", sa.Boolean(), server_default="true", nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_users_phone", "users", ["phone_number"], unique=True
    )
    op.create_index("idx_users_email", "users", ["email"], unique=True)
    op.create_index("idx_users_org", "users", ["organization_id"])

    op.create_table(
        "otp_codes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "phone_number", sa.String(length=20), nullable=False
        ),
        sa.Column("code", sa.String(length=6), nullable=False),
        sa.Column(
            "expires_at", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column(
            "verified", sa.Boolean(), server_default="false", nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_otp_phone", "otp_codes", ["phone_number", "verified"]
    )


def downgrade() -> None:
    """Drop organizations, users, and otp_codes tables."""
    op.drop_table("otp_codes")
    op.drop_table("users")
    op.drop_table("organizations")
    sa.Enum("farmer", "distributor", "admin", name="userrole").drop(
        op.get_bind(), checkfirst=True
    )
