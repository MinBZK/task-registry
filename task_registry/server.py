from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest
from prometheus_client.process_collector import ProcessCollector
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.requests import Request
from starlette.responses import Response
from task_registry.api.main import api_router
from task_registry.core.config import LICENSE_NAME, LICENSE_URL, PROJECT_NAME, PROJECT_SUMMARY, VERSION
from task_registry.lifespan import lifespan

# Register process metrics collector (provides CPU, memory stats on Linux)
ProcessCollector(registry=REGISTRY)


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=PROJECT_NAME,
        summary=PROJECT_SUMMARY,
        version=VERSION,
        license_info={"name": LICENSE_NAME, "url": LICENSE_URL},
        docs_url="/",
    )
    app.include_router(api_router)

    Instrumentator(excluded_handlers=["/metrics", "/health"]).instrument(app)

    # TODO(security): /metrics and /health endpoints are currently exposed on the main port.
    # For production, consider running these on a separate internal port (e.g., 8001) to avoid
    # public exposure, or ensure they are blocked at the Ingress level.
    @app.get("/metrics", include_in_schema=False)
    async def metrics(_request: Request) -> Response:  # pyright: ignore[reportUnusedFunction]
        return Response(content=generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

    return app


app = create_app()
