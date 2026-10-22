from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.container import Container
from app.infrastructure.config import Settings, get_settings
from app.presentation.api.errors import register_error_handlers
from app.presentation.api.routes import router


def create_app(settings: Settings | None = None) -> FastAPI:
    container = Container(settings or get_settings())

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        container.startup()
        yield
        container.database.engine.dispose()

    app = FastAPI(title=container.settings.app_name, version="0.1.0", lifespan=lifespan)
    app.state.container = container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=container.settings.cors_origin_list,
        allow_origin_regex=container.settings.cors_origin_regex,
        allow_methods=["GET", "POST", "PUT"],
        allow_headers=["Content-Type", "X-Rsvp-Token", "X-Admin-Key"],
    )
    register_error_handlers(app)
    app.include_router(router)

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
