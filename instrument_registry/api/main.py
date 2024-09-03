from fastapi import APIRouter
from instrument_registry.api.routes import health, instruments, root, urn

api_router = APIRouter()
api_router.include_router(root.router)
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(instruments.router, prefix="/instruments", tags=["instruments"])
api_router.include_router(urn.router, prefix="/urn", tags=["urns"])
