from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.middleware.request_logging import RequestLoggingMiddleware
from app.schemas.common import ApiResponse
from app.utils.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/", response_model=ApiResponse[dict[str, str]], tags=["root"])
    async def root() -> ApiResponse[dict[str, str]]:
        return ApiResponse(
            message="SD Simulator API is running",
            data={
                "status": "ok",
                "docs": "/docs",
                "health": "/health",
                "api_health": f"{settings.api_v1_prefix}/health",
            },
        )

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon() -> Response:
        return Response(status_code=204)

    @app.get("/health", response_model=ApiResponse[dict[str, str]], tags=["health"])
    async def root_health() -> ApiResponse[dict[str, str]]:
        return ApiResponse(message="Service is healthy", data={"status": "ok"})

    return app



app = create_app()
