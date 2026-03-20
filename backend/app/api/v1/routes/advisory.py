"""Advisory API routes — AI-powered township advisories and Q&A."""

from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends, HTTPException, Request

from app.api.v1.schemas.advisory import (
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySectionResponse,
    QueryRequest,
    QueryResponse,
)
from app.core.limiter import limiter
from app.services.advisory_service import AdvisoryService, get_advisory_service
from app.services.township_service import TownshipService, get_township_service

router = APIRouter(prefix="/advisory", tags=["advisory"])

FALLBACK_CONTENT = "AI advisory unavailable. Please check your Gemini API key."
FALLBACK_CONTENT_MM = (
    "AI အကြံပြုချက် မရရှိနိုင်ပါ။ Gemini API key ကို စစ်ဆေးပါ။"
)

FALLBACK_SECTIONS = {
    "executive_brief": AdvisorySectionResponse(
        title="Executive Brief",
        content=FALLBACK_CONTENT,
        content_mm=FALLBACK_CONTENT_MM,
    ),
    "crop_strategy": AdvisorySectionResponse(
        title="Crop Strategy",
        content=FALLBACK_CONTENT,
        content_mm=FALLBACK_CONTENT_MM,
    ),
    "fertilizer_plan": AdvisorySectionResponse(
        title="Fertilizer Plan",
        content=FALLBACK_CONTENT,
        content_mm=FALLBACK_CONTENT_MM,
    ),
    "risk_warnings": AdvisorySectionResponse(
        title="Risk Warnings",
        content=FALLBACK_CONTENT,
        content_mm=FALLBACK_CONTENT_MM,
    ),
    "market_outlook": AdvisorySectionResponse(
        title="Market Outlook",
        content=FALLBACK_CONTENT,
        content_mm=FALLBACK_CONTENT_MM,
    ),
}


@router.post("/generate", response_model=AdvisoryResponse)
@limiter.limit("10/minute")
async def generate_advisory(
    request: Request,
    body: AdvisoryRequest = Body(...),  # noqa: B008
    service: AdvisoryService = Depends(get_advisory_service),  # noqa: B008
    townships: TownshipService = Depends(get_township_service),  # noqa: B008
) -> AdvisoryResponse:
    """Generate a full AI advisory for a township."""
    township = townships.get_by_id(body.township_id)
    if township is None:
        raise HTTPException(status_code=400, detail="Unknown township")

    result = await service.generate_advisory(body.township_id, body.season)

    if result is None:
        now = datetime.now(tz=timezone.utc).isoformat()
        return AdvisoryResponse(
            township_id=body.township_id,
            township_name=township["name"],
            season=body.season,
            executive_brief=FALLBACK_SECTIONS["executive_brief"],
            crop_strategy=FALLBACK_SECTIONS["crop_strategy"],
            fertilizer_plan=FALLBACK_SECTIONS["fertilizer_plan"],
            risk_warnings=FALLBACK_SECTIONS["risk_warnings"],
            market_outlook=FALLBACK_SECTIONS["market_outlook"],
            generated_at=now,
            has_ai=False,
        )

    return AdvisoryResponse(
        township_id=body.township_id,
        township_name=township["name"],
        season=body.season,
        executive_brief=AdvisorySectionResponse(
            title=result.executive_brief.title,
            content=result.executive_brief.content,
            content_mm=result.executive_brief.content_mm,
        ),
        crop_strategy=AdvisorySectionResponse(
            title=result.crop_strategy.title,
            content=result.crop_strategy.content,
            content_mm=result.crop_strategy.content_mm,
        ),
        fertilizer_plan=AdvisorySectionResponse(
            title=result.fertilizer_plan.title,
            content=result.fertilizer_plan.content,
            content_mm=result.fertilizer_plan.content_mm,
        ),
        risk_warnings=AdvisorySectionResponse(
            title=result.risk_warnings.title,
            content=result.risk_warnings.content,
            content_mm=result.risk_warnings.content_mm,
        ),
        market_outlook=AdvisorySectionResponse(
            title=result.market_outlook.title,
            content=result.market_outlook.content,
            content_mm=result.market_outlook.content_mm,
        ),
        generated_at=result.generated_at,
        has_ai=True,
    )


@router.post("/query", response_model=QueryResponse)
@limiter.limit("10/minute")
async def query_advisory(
    request: Request,
    body: QueryRequest = Body(...),  # noqa: B008
    service: AdvisoryService = Depends(get_advisory_service),  # noqa: B008
    townships: TownshipService = Depends(get_township_service),  # noqa: B008
) -> QueryResponse:
    """Answer a free-form question about a township."""
    township = townships.get_by_id(body.township_id)
    if township is None:
        raise HTTPException(status_code=400, detail="Unknown township")

    result = await service.answer_query(
        body.township_id, body.season, body.question
    )

    if result is None:
        return QueryResponse(
            answer="AI advisory unavailable. Please check your Gemini API key.",
            answer_mm="AI အကြံပြုချက် မရရှိနိုင်ပါ။ Gemini API key ကို စစ်ဆေးပါ။",
            confidence=0.0,
            data_sources=[],
            has_ai=False,
        )

    return QueryResponse(
        answer=result.answer,
        answer_mm=result.answer_mm,
        confidence=result.confidence,
        data_sources=result.data_sources,
        has_ai=True,
    )
