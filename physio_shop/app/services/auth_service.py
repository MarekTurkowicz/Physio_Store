"""Auth service — registration, login, and logout business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import rate_limit_check, rate_limit_reset, token_blacklist_add
from app.config import get_settings
from app.core.exceptions import AlreadyExistsException, TooManyRequestsException, UnauthorizedException
from app.core.security import (
    create_access_token,
    decode_access_token,
    get_token_ttl,
    hash_password,
    verify_password,
)
from app.repositories.user_repo import UserRepository
from app.schemas.user import TokenResponse, UserCreate, UserResponse

settings = get_settings()


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def register(self, data: UserCreate) -> UserResponse:
        """
        Register a new user.
        Fires a welcome email task after successful creation.
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

        # Fire-and-forget welcome email
        from app.tasks.email_tasks import send_welcome_email
        send_welcome_email.delay(
            user_email=user.email,
            user_name=user.full_name,
        )

        return UserResponse.model_validate(user)

    async def login(self, email: str, password: str) -> TokenResponse:
        """
        Authenticate user and return JWT token.

        Applies Redis-backed rate limiting: blocks after LOGIN_MAX_ATTEMPTS
        failed attempts for LOGIN_BLOCK_SECONDS seconds.
        Resets the counter on successful login.
        """
        # Rate limit check (based on email)
        blocked, info = await rate_limit_check(email)
        if blocked:
            raise TooManyRequestsException(
                message=f"Zbyt wiele nieudanych prób logowania. "
                        f"Spróbuj ponownie za {info} sekund.",
            )

        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException(message="Nieprawidłowy email lub hasło")

        # Successful login — reset attempt counter
        await rate_limit_reset(email)

        token = create_access_token(data={"sub": user.email, "role": user.role})
        return TokenResponse(access_token=token)

    async def logout(self, token: str) -> None:
        """
        Invalidate a JWT token by adding its jti to the Redis blacklist.
        The key TTL is set to the token's remaining lifetime so it
        auto-expires without manual cleanup.
        """
        payload = decode_access_token(token)
        if payload is None:
            return  # already expired — nothing to blacklist

        jti = payload.get("jti")
        if jti:
            ttl = get_token_ttl(payload)
            await token_blacklist_add(jti, ttl)
