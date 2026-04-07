"""
Shared FastAPI dependencies — DB session and auth.
Used via Depends() in endpoint functions.
"""

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import token_blacklist_check
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User
from app.repositories.user_repo import UserRepository


async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency that extracts and validates the JWT token from the Authorization header.

    Checks (in order):
    1. Header format
    2. Signature & expiry (decode_access_token)
    3. Token blacklist — rejects tokens invalidated by logout
    4. User existence in DB

    Returns the authenticated User ORM instance.
    """
    if not authorization.startswith("Bearer "):
        raise UnauthorizedException(
            message="Nieprawidłowy format tokenu. Użyj: Bearer <token>"
        )

    token = authorization.removeprefix("Bearer ").strip()
    payload = decode_access_token(token)

    if payload is None:
        raise UnauthorizedException(message="Token wygasł lub jest nieprawidłowy")

    # Check token blacklist (logout invalidation)
    jti: str | None = payload.get("jti")
    if jti and await token_blacklist_check(jti):
        raise UnauthorizedException(message="Token został unieważniony. Zaloguj się ponownie")

    email: str | None = payload.get("sub")
    if email is None:
        raise UnauthorizedException(message="Nieprawidłowy token")

    repo = UserRepository(db)
    user = await repo.get_by_email(email)
    if user is None:
        raise UnauthorizedException(message="Użytkownik nie istnieje")

    return user


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency that ensures the current user has admin role."""
    if current_user.role != "admin":
        raise ForbiddenException(message="Wymagane uprawnienia administratora")
    return current_user


async def require_manager(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency that ensures the current user is at least a store manager."""
    if current_user.role not in ["admin", "manager"]:
        raise ForbiddenException(
            message="Wymagane uprawnienia menadżera sklepu lub administratora"
        )
    return current_user
