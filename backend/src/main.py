from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.config.config import get_settings
from src.config.logging import configure_logging
from src.core.common import get_app_version
from src.core.error import init_global_errors
from src.data.db import init_db
from src.route import router as api_router
from src.shared.middleware.error_boundary import ErrorBoundaryMiddleware
from src.shared.middleware.logging import LoggingMiddleware
from src.shared.middleware.request_id import RequestIdMiddleware
from src.shared.middleware.timing import TimingMiddleware
from src.shared.observability.metrics import PrometheusMiddleware, render_metrics


@asynccontextmanager
async def lifespan(_app: FastAPI):
    configure_logging()
    logger.info("Starting Trade API v{}", get_app_version())
    # await init_db(_app)
    yield
    logger.info("Shutting down Trade API")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Trade API",
        version=get_app_version(),
        docs_url="/docs",
        lifespan=lifespan,
    )

    # Global error handlers (outermost)
    init_global_errors(app)

    # Middleware (last-added runs innermost)
    app.add_middleware(ErrorBoundaryMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestIdMiddleware)

    if settings.cors_origin_list:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origin_list,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if settings.metrics_enabled:
        app.add_middleware(PrometheusMiddleware)

        @app.get("/metrics", include_in_schema=False)
        async def metrics():
            body, content_type = render_metrics()
            from fastapi.responses import Response

            return Response(content=body, media_type=content_type)

    # Routers
    app.include_router(api_router, prefix="")

    init_db(app)

    return app


app = create_app()
