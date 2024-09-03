import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from instrument_registry.lifespan import cached_data

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def get_root() -> JSONResponse:
    return JSONResponse(content=cached_data["index"])
