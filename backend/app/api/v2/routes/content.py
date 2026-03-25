"""Content management routes for distributors."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_distributor
from app.infrastructure.database import get_session
from app.infrastructure.models import User
from app.services.content_service import ContentService

router = APIRouter()
_content_service = ContentService()


class ContentCreateSchema(BaseModel):
    """Create a new content item."""

    content_type: str = Field(
        ...,
        pattern=(
            "^(weather_alert|pest_alert"
            "|fertilizer_reminder|tip|market_update)$"
        ),
    )
    title: str = Field(..., max_length=255)
    title_mm: str | None = Field(None, max_length=255)
    body: str
    body_mm: str | None = None
    audio_url: str | None = None
    township_ids: list[str] | None = None
    crop_ids: list[str] | None = None


class ContentResponse(BaseModel):
    """Content item in API responses."""

    id: uuid.UUID
    content_type: str
    title: str
    title_mm: str | None
    body: str
    body_mm: str | None
    audio_url: str | None
    published: bool
    published_at: str | None
    township_ids: list[str] | None
    crop_ids: list[str] | None


@router.get("/", response_model=list[ContentResponse])
async def list_content(
    distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> list[ContentResponse]:
    """List all content for the distributor's organization."""
    if distributor.organization_id is None:
        return []
    items = await _content_service.list_org_content(
        session, distributor.organization_id
    )
    return [_to_response(c) for c in items]


@router.post(
    "/",
    response_model=ContentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_content(
    body: ContentCreateSchema,
    distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ContentResponse:
    """Create a new content item (draft)."""
    content = await _content_service.create_content(
        session=session,
        content_type=body.content_type,
        title=body.title,
        title_mm=body.title_mm,
        body=body.body,
        body_mm=body.body_mm,
        audio_url=body.audio_url,
        organization_id=distributor.organization_id,
        created_by=distributor.id,
        township_ids=body.township_ids,
        crop_ids=body.crop_ids,
    )
    return _to_response(content)


@router.post("/{content_id}/publish", response_model=ContentResponse)
async def publish_content(
    content_id: uuid.UUID,
    _distributor: User = Depends(get_current_distributor),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ContentResponse:
    """Publish a draft content item."""
    try:
        content = await _content_service.publish_content(
            session, content_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return _to_response(content)


def _to_response(c: object) -> ContentResponse:
    """Convert Content ORM model to response."""
    return ContentResponse(
        id=c.id,  # type: ignore[attr-defined]
        content_type=(  # type: ignore[attr-defined]
            c.content_type.value  # type: ignore[attr-defined]
            if hasattr(c.content_type, "value")
            else c.content_type  # type: ignore[attr-defined]
        ),
        title=c.title,  # type: ignore[attr-defined]
        title_mm=c.title_mm,  # type: ignore[attr-defined]
        body=c.body,  # type: ignore[attr-defined]
        body_mm=c.body_mm,  # type: ignore[attr-defined]
        audio_url=c.audio_url,  # type: ignore[attr-defined]
        published=c.published,  # type: ignore[attr-defined]
        published_at=str(c.published_at) if c.published_at else None,  # type: ignore[attr-defined]
        township_ids=c.township_ids,  # type: ignore[attr-defined]
        crop_ids=c.crop_ids,  # type: ignore[attr-defined]
    )
