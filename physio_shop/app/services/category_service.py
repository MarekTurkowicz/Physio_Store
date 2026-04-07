"""Category service — category management business logic."""

import re

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsException
from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryListResponse, CategoryResponse


def _slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    # Replace Polish characters
    replacements = {
        "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n",
        "ó": "o", "ś": "s", "ź": "z", "ż": "z",
    }
    for pl_char, ascii_char in replacements.items():
        text = text.replace(pl_char, ascii_char)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repo = CategoryRepository(session)

    async def create_category(self, data: CategoryCreate) -> CategoryResponse:
        """Create a new category with auto-generated slug."""
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise AlreadyExistsException(
                message="Kategoria o tej nazwie już istnieje",
                detail=f"Nazwa: {data.name}",
            )

        slug = _slugify(data.name)
        category = await self.repo.create(
            name=data.name,
            slug=slug,
            description=data.description,
        )
        return CategoryResponse.model_validate(category)

    async def list_categories(self) -> CategoryListResponse:
        """List all categories."""
        categories = await self.repo.get_all(limit=100)
        total = await self.repo.count()
        return CategoryListResponse(
            items=[CategoryResponse.model_validate(c) for c in categories],
            total=total,
        )
