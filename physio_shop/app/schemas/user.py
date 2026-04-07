"""User schemas — registration, login, and response models."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# --- Request schemas ---

class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    full_name: str = Field(min_length=1, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


# --- Response schemas ---

class UserResponse(BaseModel):
    """Public user data returned by the API."""
    id: int
    email: str
    full_name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    """Paginated list of users."""
    items: list[UserResponse]
    total: int
    skip: int
    limit: int


# --- Auth response ---

class TokenResponse(BaseModel):
    """JWT token response after login."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Decoded JWT payload."""
    sub: str  # user email
    role: str
    exp: int | None = None
