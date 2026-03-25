"""CropFolio API v2 — authenticated endpoints for B2B2C platform."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v2.routes.auth import router as auth_router
from app.api.v2.routes.compliance import router as compliance_router
from app.api.v2.routes.content import router as content_router
from app.api.v2.routes.distributor import router as distributor_router
from app.api.v2.routes.farms import router as farms_router
from app.api.v2.routes.feed import router as feed_router
from app.api.v2.routes.loans import router as loans_router
from app.api.v2.routes.plans import router as plans_router

api_v2_router = APIRouter()
api_v2_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_v2_router.include_router(
    farms_router, prefix="/farms", tags=["farms"]
)
api_v2_router.include_router(
    plans_router, prefix="/plans", tags=["plans"]
)
api_v2_router.include_router(
    loans_router, prefix="/loans", tags=["loans"]
)
api_v2_router.include_router(
    compliance_router, prefix="/compliance", tags=["compliance"]
)
api_v2_router.include_router(
    feed_router, prefix="/feed", tags=["feed"]
)
api_v2_router.include_router(
    content_router, prefix="/content", tags=["content"]
)
api_v2_router.include_router(
    distributor_router, prefix="/distributor", tags=["distributor"]
)
