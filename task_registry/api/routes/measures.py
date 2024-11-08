import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from task_registry.data import Index, TaskType
from task_registry.lifespan import CACHED_REGISTRY

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    summary="Overview of all the measures in the task registry",
    description="This endpoint returns a JSON with all the measures in the task registry.",
    responses={200: {"description": "JSON with all the measures."}},
)
async def get_measures() -> Index:
    return CACHED_REGISTRY.get_tasks_index(TaskType.MEASURES)


# Optional parameter 'version' is included, but not used. In a new ticket
# versioning of measures should be handled.
@router.get(
    "/urn/{urn}",
    summary="Get the contents of the specific measure by URN",
    description="This endpoint returns a JSON with the contents of a specific measure identified by URN"
    " and version.",
    responses={
        200: {"description": "JSON with the specific contents of the measure."},
        400: {"description": "The URN does not exist or is not valid."},
    },
)
async def get_measure(urn: str, version: str = "latest") -> JSONResponse:
    try:
        content = CACHED_REGISTRY.get_task(urn, TaskType.MEASURES)
        return JSONResponse(content=content)
    except KeyError as err:
        raise HTTPException(status_code=400, detail=f"invalid urn: {urn}") from err
