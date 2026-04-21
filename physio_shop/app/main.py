"""
PhysioShop — FastAPI application entry point.

This module initializes the FastAPI application, configures middleware,
registers API routers, and manages the application lifespan (startup/shutdown).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.v1.router import router as v1_router
from app.config import get_settings
from app.core.exception_handlers import register_exception_handlers
from app.database import engine
from app.models import Base

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.

    During startup:
        - Ensures database tables are created (development convenience).
        - Logs application start message.

    During shutdown:
        - Disposes of the SQLAlchemy engine to close connections.
        - Logs application stop message.

    Args:
        app (FastAPI): The physical FastAPI application instance.
    """
    # Startup: try to create tables, but don't fail if DB is unavailable
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print(f"✓ Database connected and tables created")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print(f"ℹ️  Application will continue, but DB operations may fail")
        print(f"ℹ️  Make sure DATABASE_URL environment variable is set correctly")

    print(f"🏥 {settings.APP_NAME} v{settings.APP_VERSION} started!")

    yield

    # Shutdown: dispose engine
    try:
        await engine.dispose()
    except Exception:
        pass
    print(f"👋 {settings.APP_NAME} stopped.")


def create_app() -> FastAPI:
    """
    Application factory pattern to create and configure the FastAPI app.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Profesjonalne REST API dla sklepu z akcesoriami fizjoterapeutycznymi.",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register custom exception handlers for structured error responses
    register_exception_handlers(app)

    # Mount API routers with appropriate prefixes
    app.include_router(health_router, prefix="/api")
    app.include_router(v1_router)

    return app


# Main application instance used by ASGI servers (like Uvicorn)
app = create_app()
