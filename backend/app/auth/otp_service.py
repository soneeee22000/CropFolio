"""OTP generation, storage, and verification for farmer phone auth."""

from __future__ import annotations

import logging
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.infrastructure.models import OTPCode

logger = logging.getLogger(__name__)

OTP_LENGTH = 6


def generate_otp_code() -> str:
    """Generate a cryptographically secure 6-digit OTP."""
    return "".join(secrets.choice("0123456789") for _ in range(OTP_LENGTH))


async def create_otp(session: AsyncSession, phone_number: str) -> str:
    """Create and store a new OTP for the given phone number.

    Returns the plaintext OTP code (for dev: returned in response;
    for prod: sent via SMS gateway).
    """
    code = generate_otp_code()
    otp = OTPCode(
        id=uuid.uuid4(),
        phone_number=phone_number,
        code=code,
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(seconds=settings.otp_ttl_seconds)
        ),
        verified=False,
    )
    session.add(otp)
    await session.flush()
    logger.info("OTP created for phone %s...%s", phone_number[:4], phone_number[-2:])
    return code


async def verify_otp(
    session: AsyncSession, phone_number: str, code: str
) -> bool:
    """Verify an OTP code for the given phone number.

    Marks the OTP as verified on success. Returns False if code is
    invalid, expired, or already used.
    """
    stmt = (
        select(OTPCode)
        .where(
            OTPCode.phone_number == phone_number,
            OTPCode.code == code,
            OTPCode.verified.is_(False),
            OTPCode.expires_at > datetime.now(timezone.utc),
        )
        .order_by(OTPCode.created_at.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    otp = result.scalar_one_or_none()

    if otp is None:
        logger.warning(
            "OTP verification failed for phone %s...%s",
            phone_number[:4],
            phone_number[-2:],
        )
        return False

    otp.verified = True
    await session.flush()
    return True
