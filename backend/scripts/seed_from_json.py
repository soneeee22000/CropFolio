"""Seed PostgreSQL with initial data from existing JSON files.

Creates a default organization (Awba Myanmar) and an admin user.
Existing static JSON data (crops, townships, fertilizers) remains
served from JSON files via v1 endpoints — this script seeds only
the new B2B2C tables.

Usage:
    cd backend
    python -m scripts.seed_from_json
"""

from __future__ import annotations

import asyncio
import logging
import uuid

from sqlalchemy import select

from app.auth.password_handler import hash_password
from app.infrastructure.database import async_session_factory, init_db
from app.infrastructure.models import Organization, User, UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AWBA_ORG_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
ADMIN_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")


async def seed() -> None:
    """Seed the database with initial organization and admin user."""
    await init_db()

    async with async_session_factory() as session:
        existing_org = await session.execute(
            select(Organization).where(Organization.id == AWBA_ORG_ID)
        )
        if existing_org.scalar_one_or_none() is None:
            org = Organization(
                id=AWBA_ORG_ID,
                name="Awba Myanmar",
                name_mm="အော်ဘ မြန်မာ",
                org_type="distributor",
            )
            session.add(org)
            logger.info("Created organization: Awba Myanmar")
        else:
            logger.info("Organization already exists, skipping")

        existing_admin = await session.execute(
            select(User).where(User.id == ADMIN_ID)
        )
        if existing_admin.scalar_one_or_none() is None:
            admin = User(
                id=ADMIN_ID,
                email="admin@cropfolio.io",
                password_hash=hash_password("cropfolio-admin-2026"),
                role=UserRole.ADMIN,
                full_name="CropFolio Admin",
                organization_id=AWBA_ORG_ID,
                preferred_language="en",
            )
            session.add(admin)
            logger.info("Created admin user: admin@cropfolio.io")
        else:
            logger.info("Admin user already exists, skipping")

        await session.commit()
        logger.info("Seed complete")


if __name__ == "__main__":
    asyncio.run(seed())
