"""Pydantic schemas for Advisory API."""

from typing import Literal

from pydantic import BaseModel, Field


class AdvisoryRequest(BaseModel):
    """Request to generate a full township advisory."""

    township_id: str = Field(
        min_length=1, max_length=64, pattern=r"^[a-z0-9_-]+$"
    )
    season: Literal["monsoon", "dry"] = "monsoon"


class QueryRequest(BaseModel):
    """Request to ask a question about a township."""

    township_id: str = Field(
        min_length=1, max_length=64, pattern=r"^[a-z0-9_-]+$"
    )
    season: Literal["monsoon", "dry"] = "monsoon"
    question: str = Field(min_length=3, max_length=500)


class AdvisorySectionResponse(BaseModel):
    """A single advisory section with bilingual content."""

    title: str
    content: str
    content_mm: str


class AdvisoryResponse(BaseModel):
    """Full advisory response with 5 structured sections."""

    township_id: str
    township_name: str
    season: str
    executive_brief: AdvisorySectionResponse
    crop_strategy: AdvisorySectionResponse
    fertilizer_plan: AdvisorySectionResponse
    risk_warnings: AdvisorySectionResponse
    market_outlook: AdvisorySectionResponse
    generated_at: str
    has_ai: bool


class QueryResponse(BaseModel):
    """Response to a free-form advisory query."""

    answer: str
    answer_mm: str
    confidence: float
    data_sources: list[str]
    has_ai: bool
