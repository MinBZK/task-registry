import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from task_registry.data import Index, TaskType
from task_registry.lifespan import CACHED_REGISTRY

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    summary="Overview of all the instruments in the task registry.",
    description="This endpoint returns a JSON with all the instruments in the task registry.",
    responses={200: {"description": "JSON with all the instruments."}},
)
async def get_instruments() -> Index:
    return CACHED_REGISTRY.get_tasks_index(TaskType.INSTRUMENTS)


# Optional parameter 'version' is included, but not used. In a new ticket
# versioning of instruments should be handled.
@router.get(
    "/urn/{urn}",
    summary="Get the contents of the specific instrument which has given URN.",
    description="This endpoint returns a JSON with the contents of a specific instrument identified by URN"
    " and version.",
    responses={
        200: {"description": "JSON with the specific contents of the instrument."},
        400: {"description": "The URN does not exist or is not valid."},
    },
)
async def get_instrument(urn: str, version: str = "latest") -> JSONResponse:
    try:
        content = CACHED_REGISTRY.get_task(urn, TaskType.INSTRUMENTS)
        return JSONResponse(content=content)
    except KeyError as err:
        raise HTTPException(status_code=400, detail=f"invalid urn: {urn}") from err
