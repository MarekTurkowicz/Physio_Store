"""
Async database engine and session factory.

This module configures the SQLAlchemy async engine and provides a dependency
for FastAPI to manage database sessions during the request-response cycle.
Works with both SQLite (local development) and PostgreSQL (Docker environment).
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings

settings = get_settings()

# Initialize the asynchronous SQLAlchemy engine.
# echo=settings.DEBUG enables SQL logging for development.
# connect_args={"check_same_thread": False} is required for SQLite.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

# Factory for creating async database sessions.
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:  # type: ignore[misc]
    """
    FastAPI dependency that provides an asynchronous database session.

    The session is automatically committed upon successful completion of the request
    or rolled back if an exception occurs. The session is closed when the context
    generator is exhausted.

    Yields:
        AsyncSession: An active SQLAlchemy async session.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
