"""Integration tests for Advisory API endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    """Use asyncio backend for anyio."""
    return "asyncio"


@pytest.fixture
async def client():
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_generate_advisory_valid_township(client: AsyncClient) -> None:
    """POST /advisory/generate returns 200 for valid township."""
    response = await client.post(
        "/api/v1/advisory/generate",
        json={"township_id": "mdy_amarapura", "season": "monsoon"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "township_id" in data
    assert "executive_brief" in data
    assert "has_ai" in data
    assert data["township_id"] == "mdy_amarapura"
    assert data["season"] == "monsoon"


@pytest.mark.anyio
async def test_generate_advisory_invalid_township(client: AsyncClient) -> None:
    """POST /advisory/generate returns 400 for unknown township."""
    response = await client.post(
        "/api/v1/advisory/generate",
        json={"township_id": "nonexistent_xyz", "season": "monsoon"},
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_query_advisory_valid(client: AsyncClient) -> None:
    """POST /advisory/query returns 200 with valid question."""
    response = await client.post(
        "/api/v1/advisory/query",
        json={
            "township_id": "mdy_amarapura",
            "season": "monsoon",
            "question": "What crops should I recommend?",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "has_ai" in data
    assert "confidence" in data


@pytest.mark.anyio
async def test_query_advisory_missing_question(client: AsyncClient) -> None:
    """POST /advisory/query returns 422 without question field."""
    response = await client.post(
        "/api/v1/advisory/query",
        json={
            "township_id": "mdy_amarapura",
            "season": "monsoon",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_generate_advisory_has_ai_field(client: AsyncClient) -> None:
    """Advisory response includes has_ai boolean (false without Gemini key)."""
    response = await client.post(
        "/api/v1/advisory/generate",
        json={"township_id": "mdy_amarapura", "season": "monsoon"},
    )
    data = response.json()
    assert isinstance(data["has_ai"], bool)
