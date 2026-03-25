"""Unit tests for authentication module (JWT, OTP, password)."""

from __future__ import annotations

import uuid

import pytest
from jose import jwt

from app.auth.jwt_handler import (
    ALGORITHM,
    SECRET,
    create_access_token,
    decode_access_token,
)
from app.auth.otp_service import generate_otp_code
from app.auth.password_handler import hash_password, verify_password


class TestPasswordHandler:
    """Tests for bcrypt password hashing and verification."""

    def test_hash_produces_different_output(self) -> None:
        """Hashing the same password twice produces different hashes."""
        h1 = hash_password("test-password")
        h2 = hash_password("test-password")
        assert h1 != h2

    def test_verify_correct_password(self) -> None:
        """Correct password verifies successfully."""
        hashed = hash_password("my-secret-password")
        assert verify_password("my-secret-password", hashed) is True

    def test_verify_wrong_password(self) -> None:
        """Wrong password fails verification."""
        hashed = hash_password("my-secret-password")
        assert verify_password("wrong-password", hashed) is False


class TestJWTHandler:
    """Tests for JWT creation and verification."""

    def test_create_token_returns_string(self) -> None:
        """Token creation returns a non-empty string."""
        user_id = uuid.uuid4()
        token = create_access_token(user_id=user_id, role="farmer")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self) -> None:
        """Valid token decodes to the correct payload."""
        user_id = uuid.uuid4()
        org_id = uuid.uuid4()
        token = create_access_token(
            user_id=user_id,
            role="distributor",
            organization_id=org_id,
        )
        payload = decode_access_token(token)
        assert payload["sub"] == str(user_id)
        assert payload["role"] == "distributor"
        assert payload["org_id"] == str(org_id)

    def test_decode_farmer_token_no_org(self) -> None:
        """Farmer token with no org_id decodes correctly."""
        user_id = uuid.uuid4()
        token = create_access_token(user_id=user_id, role="farmer")
        payload = decode_access_token(token)
        assert payload["sub"] == str(user_id)
        assert payload["role"] == "farmer"
        assert payload["org_id"] is None

    def test_decode_expired_token_raises(self) -> None:
        """Expired token raises JWTError."""
        from jose import JWTError

        user_id = uuid.uuid4()
        token = create_access_token(
            user_id=user_id, role="farmer", expires_hours=-1
        )
        with pytest.raises(JWTError):
            decode_access_token(token)

    def test_decode_tampered_token_raises(self) -> None:
        """Tampered token raises JWTError."""
        from jose import JWTError

        user_id = uuid.uuid4()
        token = create_access_token(user_id=user_id, role="farmer")
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(JWTError):
            decode_access_token(tampered)

    def test_decode_wrong_secret_raises(self) -> None:
        """Token signed with wrong secret raises JWTError."""
        from jose import JWTError

        user_id = uuid.uuid4()
        payload = {"sub": str(user_id), "role": "farmer"}
        token = jwt.encode(payload, "wrong-secret", algorithm=ALGORITHM)
        with pytest.raises(JWTError):
            decode_access_token(token)

    def test_token_contains_expiry(self) -> None:
        """Token payload includes exp and iat claims."""
        user_id = uuid.uuid4()
        token = create_access_token(user_id=user_id, role="admin")
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        assert "exp" in payload
        assert "iat" in payload


class TestOTPGeneration:
    """Tests for OTP code generation."""

    def test_otp_is_six_digits(self) -> None:
        """Generated OTP is exactly 6 digits."""
        code = generate_otp_code()
        assert len(code) == 6
        assert code.isdigit()

    def test_otp_generates_unique_codes(self) -> None:
        """Multiple OTP generations produce different codes (probabilistic)."""
        codes = {generate_otp_code() for _ in range(100)}
        assert len(codes) > 50
