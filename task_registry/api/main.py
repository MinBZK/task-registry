from fastapi import APIRouter
from task_registry.api.routes import health, instruments, measures, requirements, urns

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"], include_in_schema=False)
api_router.include_router(instruments.router, prefix="/instruments", tags=["instruments"])
api_router.include_router(measures.router, prefix="/measures", tags=["measures"])
api_router.include_router(requirements.router, prefix="/requirements", tags=["requirements"])
api_router.include_router(urns.router, prefix="/urns", tags=["urn"])
