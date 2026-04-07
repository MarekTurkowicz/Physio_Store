"""Product schemas — create, update, and response models."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.category import CategoryResponse


class ProductCreate(BaseModel):
    """Schema for creating a new product."""
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    price: Decimal = Field(gt=0, decimal_places=2)
    stock_quantity: int = Field(ge=0, default=0)
    sku: str = Field(min_length=1, max_length=50)
    category_id: int
    is_active: bool = True


class ProductUpdate(BaseModel):
    """Schema for updating a product — all fields optional."""
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    stock_quantity: int | None = Field(None, ge=0)
    sku: str | None = Field(None, min_length=1, max_length=50)
    category_id: int | None = None
    is_active: bool | None = None


class ProductResponse(BaseModel):
    """Product data returned by the API."""
    id: int
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    sku: str
    is_active: bool
    category: CategoryResponse
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    """Paginated list of products."""
    items: list[ProductResponse]
    total: int
    skip: int
    limit: int
