"""Content generation service wrapping existing Gemini advisory engine."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models import Content, ContentType

logger = logging.getLogger(__name__)


class ContentService:
    """Creates and manages content for the farmer feed."""

    async def create_content(
        self,
        session: AsyncSession,
        content_type: str,
        title: str,
        body: str,
        title_mm: str | None = None,
        body_mm: str | None = None,
        organization_id: uuid.UUID | None = None,
        created_by: uuid.UUID | None = None,
        township_ids: list[str] | None = None,
        crop_ids: list[str] | None = None,
        audio_url: str | None = None,
    ) -> Content:
        """Create a new content item (draft, not published)."""
        content = Content(
            id=uuid.uuid4(),
            organization_id=organization_id,
            content_type=ContentType(content_type),
            title=title,
            title_mm=title_mm,
            body=body,
            body_mm=body_mm,
            audio_url=audio_url,
            township_ids=township_ids,
            crop_ids=crop_ids,
            published=False,
            created_by=created_by,
        )
        session.add(content)
        await session.flush()
        return content

    async def publish_content(
        self,
        session: AsyncSession,
        content_id: uuid.UUID,
    ) -> Content:
        """Mark a content item as published."""
        result = await session.execute(
            select(Content).where(Content.id == content_id)
        )
        content = result.scalar_one_or_none()
        if content is None:
            msg = "Content not found"
            raise ValueError(msg)
        content.published = True
        content.published_at = datetime.now(timezone.utc)
        await session.flush()
        return content

    async def list_org_content(
        self,
        session: AsyncSession,
        organization_id: uuid.UUID,
    ) -> list[Content]:
        """List all content for an organization."""
        result = await session.execute(
            select(Content)
            .where(Content.organization_id == organization_id)
            .order_by(Content.created_at.desc())
        )
        return list(result.scalars().all())
