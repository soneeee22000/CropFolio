"""Authentication routes for farmer (phone+OTP) and distributor (email+password)."""

from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.jwt_handler import create_access_token
from app.auth.otp_service import create_otp, verify_otp
from app.auth.password_handler import hash_password, verify_password
from app.auth.schemas import (
    DistributorLoginSchema,
    DistributorRegisterSchema,
    OTPRequestSchema,
    OTPVerifySchema,
    TokenResponse,
    UserProfileResponse,
)
from app.infrastructure.database import get_session
from app.infrastructure.models import User, UserRole

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/farmer/request-otp", status_code=status.HTTP_200_OK)
async def request_farmer_otp(
    body: OTPRequestSchema,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict[str, str]:
    """Send an OTP to the farmer's phone number.

    In dev mode, returns the OTP in the response.
    In production, the OTP would be sent via SMS gateway.
    """
    code = await create_otp(session, body.phone_number)
    return {"message": "OTP sent", "otp_dev_only": code}


@router.post("/farmer/verify-otp", response_model=TokenResponse)
async def verify_farmer_otp(
    body: OTPVerifySchema,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> TokenResponse:
    """Verify OTP and authenticate farmer.

    If the phone number is not registered, creates a new farmer account
    (requires full_name in the request body).
    """
    is_valid = await verify_otp(session, body.phone_number, body.code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP code",
        )

    result = await session.execute(
        select(User).where(User.phone_number == body.phone_number)
    )
    user = result.scalar_one_or_none()
    is_new = False

    if user is None:
        if not body.full_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="full_name is required for first-time registration",
            )
        user = User(
            id=uuid.uuid4(),
            phone_number=body.phone_number,
            role=UserRole.FARMER,
            full_name=body.full_name,
            full_name_mm=body.full_name_mm,
            township_id=body.township_id,
            preferred_language="mm",
        )
        session.add(user)
        await session.flush()
        is_new = True
        logger.info("New farmer registered: %s", user.id)

    token = create_access_token(
        user_id=user.id,
        role=user.role.value,
        organization_id=user.organization_id,
    )
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        role=user.role.value,
        is_new_user=is_new,
    )


@router.post("/distributor/login", response_model=TokenResponse)
async def login_distributor(
    body: DistributorLoginSchema,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> TokenResponse:
    """Authenticate a distributor with email and password."""
    result = await session.execute(
        select(User).where(
            User.email == body.email,
            User.role == UserRole.DISTRIBUTOR,
        )
    )
    user = result.scalar_one_or_none()

    if user is None or user.password_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    token = create_access_token(
        user_id=user.id,
        role=user.role.value,
        organization_id=user.organization_id,
    )
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        role=user.role.value,
    )


@router.post(
    "/distributor/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_distributor(
    body: DistributorRegisterSchema,
    session: AsyncSession = Depends(get_session),  # noqa: B008
    _admin: User = Depends(get_current_user),  # noqa: B008
) -> TokenResponse:
    """Register a new distributor account (admin-only)."""
    if _admin.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required to register distributors",
        )

    existing = await session.execute(
        select(User).where(User.email == body.email)
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        id=uuid.uuid4(),
        email=body.email,
        password_hash=hash_password(body.password),
        role=UserRole.DISTRIBUTOR,
        full_name=body.full_name,
        full_name_mm=body.full_name_mm,
        organization_id=body.organization_id,
        preferred_language="en",
    )
    session.add(user)
    await session.flush()

    token = create_access_token(
        user_id=user.id,
        role=user.role.value,
        organization_id=user.organization_id,
    )
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        role=user.role.value,
        is_new_user=True,
    )


@router.get("/me", response_model=UserProfileResponse)
async def get_profile(
    user: User = Depends(get_current_user),  # noqa: B008
) -> UserProfileResponse:
    """Return the authenticated user's profile."""
    return UserProfileResponse(
        id=user.id,
        phone_number=user.phone_number,
        email=user.email,
        role=user.role.value,
        full_name=user.full_name,
        full_name_mm=user.full_name_mm,
        preferred_language=user.preferred_language,
        township_id=user.township_id,
        organization_id=user.organization_id,
    )
