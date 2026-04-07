"""User service — user management business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserListResponse, UserResponse


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def get_me(self, email: str) -> UserResponse:
        """Get current user profile by email."""
        user = await self.repo.get_by_email(email)
        if not user:
            raise NotFoundException(message="Użytkownik nie znaleziony")
        return UserResponse.model_validate(user)

    async def list_users(self, skip: int = 0, limit: int = 20) -> UserListResponse:
        """List all users (admin only)."""
        users = await self.repo.get_all(skip=skip, limit=limit)
        total = await self.repo.count()
        return UserListResponse(
            items=[UserResponse.model_validate(u) for u in users],
            total=total,
            skip=skip,
            limit=limit,
        )
