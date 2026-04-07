"""Auth service — registration and login business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsException, UnauthorizedException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import TokenResponse, UserCreate, UserResponse


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def register(self, data: UserCreate) -> UserResponse:
        """
        Register a new user.
        Raises AlreadyExistsException if email is taken.
        """
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise AlreadyExistsException(
                message="Użytkownik z tym adresem email już istnieje",
                detail=f"Email: {data.email}",
            )

        user = await self.repo.create(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role="customer",
        )
        return UserResponse.model_validate(user)

    async def login(self, email: str, password: str) -> TokenResponse:
        """
        Authenticate user and return JWT token.
        Raises UnauthorizedException if credentials are invalid.
        """
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException(
                message="Nieprawidłowy email lub hasło",
            )

        token = create_access_token(
            data={"sub": user.email, "role": user.role}
        )
        return TokenResponse(access_token=token)
