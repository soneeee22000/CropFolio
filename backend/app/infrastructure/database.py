"""Async SQLAlchemy database engine, session factory, and base model."""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

logger = logging.getLogger(__name__)

_DEFAULT_DB_URL = (
    "postgresql+asyncpg://cropfolio:cropfolio@localhost:5432/cropfolio"
)
_db_available = settings.database_url != _DEFAULT_DB_URL

if _db_available:
    engine = create_async_engine(
        settings.database_url,
        echo=settings.log_level == "DEBUG",
        pool_size=10,
        max_overflow=20,
    )
    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
else:
    engine = None  # type: ignore[assignment]
    async_session_factory = None  # type: ignore[assignment]
    logger.warning(
        "DATABASE_URL not configured — v2 endpoints disabled, "
        "v1 endpoints still available"
    )


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ORM models."""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session for FastAPI dependency injection."""
    if async_session_factory is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not configured. Set DATABASE_URL.",
        )
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Create all tables from ORM models (dev/test only)."""
    if engine is None:
        logger.info("Skipping init_db — no database configured")
        return
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        logger.warning(
            "Database connection failed — v2 endpoints will "
            "return 503, v1 endpoints still work"
        )


async def close_db() -> None:
    """Dispose of the database engine connection pool."""
    if engine is not None:
        await engine.dispose()


def is_db_available() -> bool:
    """Check if database is configured and available."""
    return _db_available
