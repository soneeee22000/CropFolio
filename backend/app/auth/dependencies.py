"""FastAPI dependency injection for authentication and authorization."""

from __future__ import annotations

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_handler import decode_access_token
from app.infrastructure.database import get_session
from app.infrastructure.models import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/auth/distributor/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> User:
    """Decode JWT and return the authenticated user from the database."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
    except JWTError as err:
        raise credentials_exception from err

    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError as err:
        raise credentials_exception from err

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise credentials_exception

    return user


async def get_current_farmer(
    user: User = Depends(get_current_user),  # noqa: B008
) -> User:
    """Require the authenticated user to have the farmer role."""
    if user.role != UserRole.FARMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Farmer role required",
        )
    return user


async def get_current_distributor(
    user: User = Depends(get_current_user),  # noqa: B008
) -> User:
    """Require the authenticated user to have the distributor role."""
    if user.role != UserRole.DISTRIBUTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Distributor role required",
        )
    return user


async def get_current_admin(
    user: User = Depends(get_current_user),  # noqa: B008
) -> User:
    """Require the authenticated user to have the admin role."""
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return user


def get_org_filter(
    user: User = Depends(get_current_user),  # noqa: B008
) -> uuid.UUID | None:
    """Extract organization_id from the authenticated user for query scoping."""
    return user.organization_id
