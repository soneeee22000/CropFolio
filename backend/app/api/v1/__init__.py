"""API v1 router aggregating all sub-routers."""

from fastapi import APIRouter

from app.api.v1.routes.climate import router as climate_router
from app.api.v1.routes.crops import router as crops_router
from app.api.v1.routes.optimizer import router as optimizer_router
from app.api.v1.routes.simulator import router as simulator_router
from app.api.v1.routes.townships import router as townships_router

api_v1_router = APIRouter()
api_v1_router.include_router(townships_router)
api_v1_router.include_router(crops_router)
api_v1_router.include_router(climate_router)
api_v1_router.include_router(optimizer_router)
api_v1_router.include_router(simulator_router)
