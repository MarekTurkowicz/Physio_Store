"""Order schemas — create, status update, and response models."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.product import ProductResponse
from app.schemas.user import UserResponse


# --- Nested item schemas ---

class OrderItemCreate(BaseModel):
    """Single item in a new order."""
    product_id: int
    quantity: int = Field(gt=0)


class OrderItemResponse(BaseModel):
    """Order item data returned by the API."""
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    product: ProductResponse

    model_config = {"from_attributes": True}


# --- Order schemas ---

class OrderCreate(BaseModel):
    """Schema for placing a new order."""
    shipping_address: str = Field(min_length=5, max_length=500)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderStatusUpdate(BaseModel):
    """Schema for admin status change."""
    status: str = Field(pattern=r"^(pending|confirmed|shipped|delivered|cancelled)$")


class OrderResponse(BaseModel):
    """Order data returned by the API."""
    id: int
    status: str
    total_amount: Decimal
    shipping_address: str
    user: UserResponse
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    """Paginated list of orders."""
    items: list[OrderResponse]
    total: int
    skip: int
    limit: int
