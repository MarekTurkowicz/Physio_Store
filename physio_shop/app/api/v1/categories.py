"""Category endpoints — list and create categories."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_manager
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryListResponse, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=CategoryListResponse)
async def list_categories(db: AsyncSession = Depends(get_db)):
    """List all product categories (public)."""
    service = CategoryService(db)
    return await service.list_categories()


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _manager: User = Depends(require_manager),
):
    """Create a new category (manager and admin only)."""
    service = CategoryService(db)
    return await service.create_category(data)
