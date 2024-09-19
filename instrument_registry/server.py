from fastapi import FastAPI
from instrument_registry.api.main import api_router
from instrument_registry.core.config import PROJECT_DESCRIPTION, PROJECT_NAME, VERSION
from instrument_registry.lifespan import lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=PROJECT_NAME,
        summary=PROJECT_DESCRIPTION,
        version=VERSION,
        docs_url="/",
    )

    app.include_router(api_router)

    return app


app = create_app()
