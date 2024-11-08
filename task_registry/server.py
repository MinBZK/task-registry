from fastapi import FastAPI
from task_registry.api.main import api_router
from task_registry.core.config import LICENSE_NAME, LICENSE_URL, PROJECT_NAME, PROJECT_SUMMARY, VERSION
from task_registry.lifespan import lifespan


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
    return app


app = create_app()
