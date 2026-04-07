"""
Security utilities for JWT authentication and password hashing.

This module provides functions for secure password storage using bcrypt and
token-based authentication using JSON Web Tokens (JWT).
"""

import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()


def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using the bcrypt algorithm with a random salt.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored bcrypt hash.
    """
    pwd_bytes = plain_password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hash_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generates a signed JWT access token with a unique jti claim.
    The jti (JWT ID) allows individual tokens to be blacklisted on logout.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({
        "exp": expire,
        "jti": str(uuid.uuid4()),  # unique token ID for blacklisting
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """
    Decodes and validates a JWT access token.
    Returns the payload dict (including jti) if valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_token_ttl(payload: dict) -> int:
    """
    Returns remaining seconds until token expiry.
    Used to set TTL when blacklisting a token.
    """
    exp = payload.get("exp", 0)
    remaining = int(exp - datetime.now(timezone.utc).timestamp())
    return max(remaining, 0)
