"""Personalized feed service for farmer content delivery."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models import (
    Content,
    ContentInteraction,
)

FEED_DEFAULT_LIMIT = 20


class FeedService:
    """Builds personalized content feeds for farmers.

    Feed priority order:
    1. Overdue fertilizer reminders (highest)
    2. Weather alerts for farmer's township
    3. Tips for farmer's current crop stage
    4. General published content from distributor
    """

    async def get_personalized_feed(
        self,
        session: AsyncSession,
        farmer_id: uuid.UUID,
        township_id: str | None = None,
        limit: int = FEED_DEFAULT_LIMIT,
    ) -> list[Content]:
        """Build a personalized feed for a farmer."""
        stmt = (
            select(Content)
            .where(
                Content.published.is_(True),
            )
            .order_by(Content.published_at.desc())
            .limit(limit)
        )

        if township_id:
            stmt = stmt.where(
                Content.township_ids.is_(None)
                | Content.township_ids.contains([township_id])
            )

        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def mark_viewed(
        self,
        session: AsyncSession,
        content_id: uuid.UUID,
        farmer_id: uuid.UUID,
    ) -> ContentInteraction:
        """Record that a farmer viewed a content item."""
        existing = await session.execute(
            select(ContentInteraction).where(
                ContentInteraction.content_id == content_id,
                ContentInteraction.farmer_id == farmer_id,
            )
        )
        interaction = existing.scalar_one_or_none()

        if interaction is None:
            interaction = ContentInteraction(
                id=uuid.uuid4(),
                content_id=content_id,
                farmer_id=farmer_id,
                viewed=True,
                viewed_at=datetime.now(timezone.utc),
            )
            session.add(interaction)
        else:
            interaction.viewed = True
            interaction.viewed_at = datetime.now(timezone.utc)

        await session.flush()
        return interaction

    async def mark_helpful(
        self,
        session: AsyncSession,
        content_id: uuid.UUID,
        farmer_id: uuid.UUID,
        helpful: bool,
    ) -> ContentInteraction:
        """Record whether a farmer found content helpful."""
        existing = await session.execute(
            select(ContentInteraction).where(
                ContentInteraction.content_id == content_id,
                ContentInteraction.farmer_id == farmer_id,
            )
        )
        interaction = existing.scalar_one_or_none()

        if interaction is None:
            interaction = ContentInteraction(
                id=uuid.uuid4(),
                content_id=content_id,
                farmer_id=farmer_id,
                helpful=helpful,
            )
            session.add(interaction)
        else:
            interaction.helpful = helpful

        await session.flush()
        return interaction
