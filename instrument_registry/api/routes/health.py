from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/live", response_class=JSONResponse)
async def liveness() -> dict[str, str]:
    return {"status": "ok"}
