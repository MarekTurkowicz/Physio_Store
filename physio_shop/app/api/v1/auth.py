"""Auth endpoints — registration, login, logout."""

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.common import MessageResponse
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new customer account.
    Fires a welcome email task in the background after creation.
    """
    service = AuthService(db)
    return await service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Login and receive a JWT access token.

    Rate-limited: blocked for 15 minutes after 5 consecutive failures.
    Returns HTTP 429 when the limit is exceeded.
    """
    service = AuthService(db)
    return await service.login(data.email, data.password)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    authorization: str = Header(..., description="Bearer <token>"),
):
    """
    Invalidate the current JWT token.

    Adds the token's jti to the Redis blacklist so that any subsequent
    request with the same token is rejected (HTTP 401), even if it
    hasn't expired yet. The blacklist entry auto-expires when the token
    would have expired naturally — no manual cleanup needed.
    """
    if not authorization.startswith("Bearer "):
        return MessageResponse(message="Wylogowano")

    token = authorization.removeprefix("Bearer ").strip()

    # AuthService.logout doesn't need a DB session
    from app.services.auth_service import AuthService as _AuthService
    await _AuthService(session=None).logout(token)  # type: ignore[arg-type]

    return MessageResponse(message="Wylogowano pomyślnie")
