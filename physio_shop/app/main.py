"""
PhysioShop — FastAPI application entry point.

This module initializes the FastAPI application, configures middleware,
registers API routers, and manages the application lifespan (startup/shutdown).
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from app.api.health import router as health_router
from app.api.v1.router import router as v1_router
from app.config import get_settings
from app.core.cors import configure_cors
from app.core.exception_handlers import register_exception_handlers
from app.database import engine
from app.models import Base

logger = logging.getLogger("physiostore")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database connected and tables ensured")
    except Exception as exc:
        logger.warning("Database unavailable at startup: %s", exc)

    logger.info("%s v%s started", settings.APP_NAME, settings.APP_VERSION)
    yield

    try:
        await engine.dispose()
    except Exception:
        pass
    logger.info("%s stopped", settings.APP_NAME)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Profesjonalne REST API dla sklepu z akcesoriami fizjoterapeutycznymi.",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    configure_cors(app, settings)
    app.add_middleware(GZipMiddleware, minimum_size=500)

    register_exception_handlers(app)

    app.include_router(health_router, prefix="/api")
    app.include_router(v1_router)

    @app.get("/", include_in_schema=False)
    async def root():
        return {"name": settings.APP_NAME, "version": settings.APP_VERSION, "docs": "/docs"}

    return app


app = create_app()
