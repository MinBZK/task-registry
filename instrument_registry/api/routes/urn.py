import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from instrument_registry.lifespan import cached_data

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/")
async def get_instrument(urn: str) -> JSONResponse:
    try:
        instrument_content = cached_data["urn_mapper"][urn]
        return JSONResponse(content=instrument_content)
    except KeyError:
        logging.exception(f"urn {urn} not found.")
        return JSONResponse({"error": "URN does not exist in the instrument registry "}, status_code=404)
