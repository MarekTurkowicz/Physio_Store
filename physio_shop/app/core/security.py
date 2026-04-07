"""
Security utilities for JWT authentication and password hashing.

This module provides functions for secure password storage using bcrypt and
token-based authentication using JSON Web Tokens (JWT).
"""

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()


def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using the bcrypt algorithm with a random salt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The resulting salt-prefixed bcrypt hash as a UTF-8 string.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored bcrypt hash.

    Args:
        plain_password (str): The password attempt in plain-text.
        hashed_password (str): The correct password's stored bcrypt hash.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    pwd_bytes = plain_password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hash_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generates a signed JWT access token for a user session.

    Args:
        data (dict): Payload data to include in the token (e.g., {"sub": user_email}).
        expires_delta (timedelta, optional): Custom expiration duration.
            Defaults to settings.ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: Encoded and signed JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """
    Decodes and validates a JWT access token.

    Args:
        token (str): The encoded JWT string to verify.

    Returns:
        dict | None: The decoded payload dictionary if valid and not expired,
            otherwise None.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
