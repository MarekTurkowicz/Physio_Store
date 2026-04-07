"""Product repository — data access for Product model."""

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def get_by_sku(self, sku: str) -> Product | None:
        """Find product by SKU code."""
        stmt = select(Product).where(Product.sku == sku)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def search(
        self,
        query: str | None = None,
        category_id: int | None = None,
        is_active: bool | None = True,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Product], int]:
        """
        Search products with optional filters.
        Returns (products, total_count) tuple.
        """
        filters = []

        if query:
            search_term = f"%{query}%"
            filters.append(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                )
            )

        if category_id is not None:
            filters.append(Product.category_id == category_id)

        if is_active is not None:
            filters.append(Product.is_active == is_active)

        products = await self.get_all(skip=skip, limit=limit, filters=filters)
        total = await self.count(filters=filters)
        return list(products), total
