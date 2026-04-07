"""Product endpoints — CRUD and search."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_manager
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=ProductListResponse)
async def list_products(
    q: str | None = Query(None, description="Search query (name or description)"),
    category_id: int | None = Query(None, description="Filter by category ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Search and list products (public). Supports text search and category filter."""
    service = ProductService(db)
    return await service.search_products(
        query=q, category_id=category_id, skip=skip, limit=limit
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Get product details by ID (public)."""
    service = ProductService(db)
    return await service.get_product(product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _manager: User = Depends(require_manager),
):
    """Create a new product (manager only)."""
    service = ProductService(db)
    return await service.create_product(data)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _manager: User = Depends(require_manager),
):
    """Update a product (manager only)."""
    service = ProductService(db)
    return await service.update_product(product_id, data)


@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    _manager: User = Depends(require_manager),
):
    """Soft-delete a product — sets is_active=False (manager only)."""
    service = ProductService(db)
    await service.delete_product(product_id)
    return MessageResponse(message="Produkt został dezaktywowany")
