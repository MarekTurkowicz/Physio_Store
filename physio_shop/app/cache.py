"""Redis cache module for PhysioShop.

Provides:
- Generic key/value cache with TTL
- Rate limiting (login brute-force protection)
- JWT token blacklist (logout invalidation)
- Manager dashboard stats cache
"""

import json
from typing import Any

import redis.asyncio as redis

from app.config import get_settings

settings = get_settings()


def get_redis_client() -> redis.Redis:
    """Create a new Redis client instance."""
    return redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
        retry_on_timeout=False,
        health_check_interval=30,
    )


redis_client: redis.Redis = get_redis_client()

# ── Key prefixes ──────────────────────────────────────────────────────────────
_BLACKLIST_PREFIX = "token_blacklist:"
_RATE_LIMIT_PREFIX = "rate_limit:login:"
_STATS_PREFIX = "stats:"


# ── Generic cache ─────────────────────────────────────────────────────────────

async def cache_get(key: str) -> Any | None:
    """Get a value from cache. Returns None on miss or Redis unavailability."""
    try:
        value = await redis_client.get(key)
        if value is not None:
            return json.loads(value)
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        return None
    return None


async def cache_set(key: str, value: Any, ttl: int | None = None) -> None:
    """Set a value in cache with optional TTL (defaults to CACHE_TTL from settings)."""
    try:
        ttl = ttl or settings.CACHE_TTL
        await redis_client.set(key, json.dumps(value, default=str), ex=ttl)
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        pass


async def cache_delete(key: str) -> None:
    """Delete a key from cache."""
    try:
        await redis_client.delete(key)
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        pass


async def cache_delete_pattern(pattern: str) -> None:
    """Delete all keys matching a pattern (e.g. 'product:*')."""
    try:
        async for key in redis_client.scan_iter(match=pattern):
            await redis_client.delete(key)
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        pass


async def cache_flush() -> None:
    """Flush the entire cache database."""
    try:
        await redis_client.flushdb()
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        pass


# ── Token blacklist ───────────────────────────────────────────────────────────

async def token_blacklist_add(jti: str, ttl_seconds: int) -> None:
    """
    Add a token's jti to the blacklist.
    TTL is set to the token's remaining lifetime so the key auto-expires.
    Called on logout.
    """
    if ttl_seconds <= 0:
        return
    try:
        key = f"{_BLACKLIST_PREFIX}{jti}"
        await redis_client.set(key, "1", ex=ttl_seconds)
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        pass


async def token_blacklist_check(jti: str) -> bool:
    """
    Returns True if the token has been blacklisted (i.e. user has logged out).
    """
    try:
        key = f"{_BLACKLIST_PREFIX}{jti}"
        return await redis_client.exists(key) == 1
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        return False  # fail open — don't block valid users if Redis is down


# ── Rate limiting (login) ─────────────────────────────────────────────────────

async def rate_limit_check(identifier: str) -> tuple[bool, int]:
    """
    Check and increment the login attempt counter for an identifier (email).

    Returns:
        (is_blocked, current_attempt_count)
        is_blocked=True means the identifier is currently rate-limited.
    """
    try:
        key = f"{_RATE_LIMIT_PREFIX}{identifier}"
        count = await redis_client.incr(key)
        if count == 1:
            # First attempt — set the expiry window
            await redis_client.expire(key, settings.LOGIN_BLOCK_SECONDS)
        if count > settings.LOGIN_MAX_ATTEMPTS:
            ttl = await redis_client.ttl(key)
            return True, int(ttl)
        return False, count
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        return False, 0  # fail open


async def rate_limit_reset(identifier: str) -> None:
    """Reset login attempt counter after a successful login."""
    try:
        await redis_client.delete(f"{_RATE_LIMIT_PREFIX}{identifier}")
    except (redis.ConnectionError, redis.TimeoutError, OSError):
        pass


# ── Dashboard stats cache ─────────────────────────────────────────────────────

async def stats_cache_get(key: str) -> Any | None:
    """Get cached dashboard stat value."""
    return await cache_get(f"{_STATS_PREFIX}{key}")


async def stats_cache_set(key: str, value: Any, ttl: int = 60) -> None:
    """Cache a dashboard stat with short TTL (default 60s)."""
    await cache_set(f"{_STATS_PREFIX}{key}", value, ttl=ttl)
