"""Category schemas — create and response models."""

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """Schema for creating a new category."""
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class CategoryResponse(BaseModel):
    """Category data returned by the API."""
    id: int
    name: str
    slug: str
    description: str | None

    model_config = {"from_attributes": True}


class CategoryListResponse(BaseModel):
    """List of categories."""
    items: list[CategoryResponse]
    total: int
