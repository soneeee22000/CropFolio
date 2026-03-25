"""Pydantic request/response schemas for authentication endpoints."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field


class OTPRequestSchema(BaseModel):
    """Request to send an OTP to a farmer's phone."""

    phone_number: str = Field(
        ...,
        min_length=8,
        max_length=20,
        examples=["+959123456789"],
        description="Myanmar phone number with country code",
    )


class OTPVerifySchema(BaseModel):
    """Request to verify an OTP and authenticate."""

    phone_number: str = Field(..., min_length=8, max_length=20)
    code: str = Field(..., min_length=6, max_length=6)
    full_name: str | None = Field(
        None,
        max_length=255,
        description="Required on first login (registration)",
    )
    full_name_mm: str | None = Field(None, max_length=255)
    township_id: str | None = Field(None, max_length=50)


class DistributorLoginSchema(BaseModel):
    """Distributor email + password login."""

    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8)


class DistributorRegisterSchema(BaseModel):
    """Admin-only: register a new distributor account."""

    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., max_length=255)
    full_name_mm: str | None = Field(None, max_length=255)
    organization_id: uuid.UUID


class TokenResponse(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str = "bearer"
    user_id: uuid.UUID
    role: str
    is_new_user: bool = False


class UserProfileResponse(BaseModel):
    """Current user profile."""

    id: uuid.UUID
    phone_number: str | None = None
    email: str | None = None
    role: str
    full_name: str
    full_name_mm: str | None = None
    preferred_language: str
    township_id: str | None = None
    organization_id: uuid.UUID | None = None
