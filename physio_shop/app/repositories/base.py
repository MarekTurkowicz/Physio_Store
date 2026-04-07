"""
Generic CRUD repository — base class for all repositories.
Provides common database operations using SQLAlchemy async.
"""

from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

# TypeVar bound to our Base so repos are typed to specific models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic async CRUD repository.

    Usage:
        class ProductRepo(BaseRepository[Product]):
            def __init__(self, session):
                super().__init__(Product, session)
    """

    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: int) -> ModelType | None:
        """Get a single record by primary key."""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: list | None = None,
    ) -> Sequence[ModelType]:
        """Get a paginated list of records with optional filters."""
        stmt = select(self.model)
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self, filters: list | None = None) -> int:
        """Count records matching optional filters."""
        stmt = select(func.count()).select_from(self.model)
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def create(self, **kwargs: Any) -> ModelType:
        """Create a new record from keyword arguments."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()  # Assigns ID without committing
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: ModelType, **kwargs: Any) -> ModelType:
        """Update an existing record's fields."""
        for key, value in kwargs.items():
            if value is not None:
                setattr(instance, key, value)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        """Hard-delete a record."""
        await self.session.delete(instance)
        await self.session.flush()
