"""Common schemas — pagination, health, generic responses."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    app_name: str
    version: str


class PaginationParams(BaseModel):
    """Query parameters for paginated endpoints."""
    skip: int = 0
    limit: int = 20


class PaginatedResponse(BaseModel):
    """Wrapper for paginated list responses."""
    items: list
    total: int
    skip: int
    limit: int


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: str | None = None
