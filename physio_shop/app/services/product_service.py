"""Product service — product management business logic with Redis caching."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache_delete, cache_delete_pattern, cache_get, cache_set
from app.core.exceptions import AlreadyExistsException, NotFoundException
from app.repositories.product_repo import ProductRepository
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)

PRODUCT_CACHE_KEY = "product:{product_id}"
PRODUCT_LIST_CACHE_KEY = "products:q={query}:cat={category_id}:s={skip}:l={limit}"


class ProductService:
    def __init__(self, session: AsyncSession):
        self.repo = ProductRepository(session)

    async def create_product(self, data: ProductCreate) -> ProductResponse:
        """Create a new product. Raises if SKU already exists."""
        existing = await self.repo.get_by_sku(data.sku)
        if existing:
            raise AlreadyExistsException(
                message="Produkt z tym SKU już istnieje",
                detail=f"SKU: {data.sku}",
            )

        product = await self.repo.create(**data.model_dump())
        response = ProductResponse.model_validate(product)
        await cache_delete_pattern("products:*")
        return response

    async def get_product(self, product_id: int) -> ProductResponse:
        """Get product details by ID. Uses Redis cache."""
        cache_key = PRODUCT_CACHE_KEY.format(product_id=product_id)
        cached = await cache_get(cache_key)
        if cached:
            return ProductResponse.model_validate(cached)

        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(
                message="Produkt nie znaleziony",
                detail=f"ID: {product_id}",
            )
        response = ProductResponse.model_validate(product)
        await cache_set(cache_key, response.model_dump(mode="json"))
        return response

    async def update_product(self, product_id: int, data: ProductUpdate) -> ProductResponse:
        """Update product fields. Only non-None values are applied."""
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(message="Produkt nie znaleziony")

        if data.sku and data.sku != product.sku:
            existing = await self.repo.get_by_sku(data.sku)
            if existing:
                raise AlreadyExistsException(message="Produkt z tym SKU już istnieje")

        update_data = data.model_dump(exclude_unset=True)
        product = await self.repo.update(product, **update_data)
        response = ProductResponse.model_validate(product)

        await cache_delete(PRODUCT_CACHE_KEY.format(product_id=product_id))
        await cache_delete_pattern("products:*")
        return response

    async def delete_product(self, product_id: int) -> None:
        """Soft-delete a product by setting is_active=False."""
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(message="Produkt nie znaleziony")
        await self.repo.update(product, is_active=False)

        await cache_delete(PRODUCT_CACHE_KEY.format(product_id=product_id))
        await cache_delete_pattern("products:*")

    async def search_products(
        self,
        query: str | None = None,
        category_id: int | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> ProductListResponse:
        """Search and filter products with pagination. Uses Redis cache."""
        cache_key = PRODUCT_LIST_CACHE_KEY.format(
            query=query, category_id=category_id, skip=skip, limit=limit
        )
        cached = await cache_get(cache_key)
        if cached:
            return ProductListResponse.model_validate(cached)

        products, total = await self.repo.search(
            query=query,
            category_id=category_id,
            is_active=True,
            skip=skip,
            limit=limit,
        )
        response = ProductListResponse(
            items=[ProductResponse.model_validate(p) for p in products],
            total=total,
            skip=skip,
            limit=limit,
        )
        await cache_set(cache_key, response.model_dump(mode="json"))
        return response
