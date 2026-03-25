"""Farmer personalized content feed routes."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_farmer
from app.infrastructure.database import get_session
from app.infrastructure.models import User
from app.services.feed_service import FeedService

router = APIRouter()
_feed_service = FeedService()


class ContentFeedItem(BaseModel):
    """Content item in the farmer feed."""

    id: uuid.UUID
    content_type: str
    title: str
    title_mm: str | None
    body: str
    body_mm: str | None
    audio_url: str | None
    published_at: str | None


class HelpfulSchema(BaseModel):
    """Mark content as helpful or not."""

    helpful: bool


@router.get("/", response_model=list[ContentFeedItem])
async def get_feed(
    limit: int = Query(20, ge=1, le=50),
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[ContentFeedItem]:
    """Get personalized content feed for the farmer."""
    items = await _feed_service.get_personalized_feed(
        session=session,
        farmer_id=farmer.id,
        township_id=farmer.township_id,
        limit=limit,
    )
    return [
        ContentFeedItem(
            id=c.id,
            content_type=c.content_type.value,
            title=c.title,
            title_mm=c.title_mm,
            body=c.body,
            body_mm=c.body_mm,
            audio_url=c.audio_url,
            published_at=(
                str(c.published_at) if c.published_at else None
            ),
        )
        for c in items
    ]


@router.post("/{content_id}/view")
async def mark_viewed(
    content_id: uuid.UUID,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Response:
    """Mark a content item as viewed."""
    await _feed_service.mark_viewed(session, content_id, farmer.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{content_id}/helpful")
async def mark_helpful(
    content_id: uuid.UUID,
    body: HelpfulSchema,
    farmer: User = Depends(get_current_farmer),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Response:
    """Mark whether content was helpful."""
    await _feed_service.mark_helpful(
        session, content_id, farmer.id, body.helpful
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
