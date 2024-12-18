import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from task_registry.data import Index, TaskType
from task_registry.lifespan import CACHED_REGISTRY

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/{urn}",
    summary="Get the contents of the specific URN.",
    description="This endpoint returns a JSON with the contents of a specific URN"
    " and version.",
    responses={
        200: {"description": "JSON with the specific contents of the URN."},
        400: {"description": "The URN does not exist or is not valid."},
    },
)
async def get_urn(urn: str, version: str = "latest") -> JSONResponse:
    for taskType in TaskType:
        if CACHED_REGISTRY.has_urn(urn, taskType):
            return JSONResponse(content=CACHED_REGISTRY.get_task(urn, taskType))
    raise HTTPException(status_code=400, detail=f"Unknown urn: {urn}")
