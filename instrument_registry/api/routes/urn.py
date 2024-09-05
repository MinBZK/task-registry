import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from instrument_registry.lifespan import cached_data

router = APIRouter()

logger = logging.getLogger(__name__)


# Optional parameter 'version' is included, but not used. In a new ticket
# versioning of instruments should be handled.
@router.get("/")
async def get_instrument(urn: str, version: str = "latest") -> JSONResponse:
    try:
        instrument_content = cached_data["urn_mapper"][urn]
        return JSONResponse(content=instrument_content)
    except KeyError:
        logging.exception(f"urn {urn} not found.")
        return JSONResponse({"error": "URN does not exist in the instrument registry "}, status_code=404)
