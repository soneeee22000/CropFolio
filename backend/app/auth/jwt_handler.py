"""JWT token creation and verification."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings

ALGORITHM = settings.jwt_algorithm
SECRET = settings.jwt_secret_key


def create_access_token(
    user_id: uuid.UUID,
    role: str,
    organization_id: uuid.UUID | None = None,
    expires_hours: int | None = None,
) -> str:
    """Create a signed JWT access token."""
    if expires_hours is None:
        expires_hours = (
            settings.jwt_farmer_expiry_hours
            if role == "farmer"
            else settings.jwt_distributor_expiry_hours
        )

    payload = {
        "sub": str(user_id),
        "role": role,
        "org_id": str(organization_id) if organization_id else None,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_hours),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, str | None]:
    """Decode and verify a JWT access token.

    Returns the payload dict with keys: sub, role, org_id.
    Raises JWTError on invalid or expired tokens.
    """
    try:
        payload: dict[str, str | None] = jwt.decode(
            token, SECRET, algorithms=[ALGORITHM]
        )
        if payload.get("sub") is None:
            raise JWTError("Token missing subject claim")
        return payload
    except JWTError:
        raise
