"""Tests for Redis cache integration."""

import json

import pytest
import pytest_asyncio
import redis.asyncio as redis

from app.config import get_settings

settings = get_settings()


@pytest_asyncio.fixture
async def redis_conn():
    """Fresh Redis connection per test, flushed before and after."""
    client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.aclose()


@pytest.mark.asyncio
async def test_redis_ping(redis_conn):
    """Redis should be reachable and respond to PING."""
    result = await redis_conn.ping()
    assert result is True


@pytest.mark.asyncio
async def test_set_and_get(redis_conn):
    """Should store and retrieve a value from cache."""
    data = {"name": "Wałek do masażu", "price": 59.99}
    await redis_conn.set("test:key", json.dumps(data), ex=300)
    result = json.loads(await redis_conn.get("test:key"))
    assert result["name"] == "Wałek do masażu"
    assert result["price"] == 59.99


@pytest.mark.asyncio
async def test_get_miss(redis_conn):
    """Should return None for a non-existent key."""
    result = await redis_conn.get("test:nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_set_with_ttl(redis_conn):
    """Should store a value with custom TTL."""
    await redis_conn.set("test:ttl", json.dumps({"data": "temporary"}), ex=10)
    result = json.loads(await redis_conn.get("test:ttl"))
    assert result["data"] == "temporary"

    ttl = await redis_conn.ttl("test:ttl")
    assert 0 < ttl <= 10


@pytest.mark.asyncio
async def test_delete(redis_conn):
    """Should delete a specific key."""
    await redis_conn.set("test:delete", json.dumps({"data": "to be removed"}))
    assert await redis_conn.get("test:delete") is not None

    await redis_conn.delete("test:delete")
    assert await redis_conn.get("test:delete") is None


@pytest.mark.asyncio
async def test_delete_pattern(redis_conn):
    """Should delete all keys matching a pattern."""
    await redis_conn.set("product:1", json.dumps({"id": 1}))
    await redis_conn.set("product:2", json.dumps({"id": 2}))
    await redis_conn.set("product:3", json.dumps({"id": 3}))
    await redis_conn.set("other:key", json.dumps({"id": 99}))

    async for key in redis_conn.scan_iter(match="product:*"):
        await redis_conn.delete(key)

    assert await redis_conn.get("product:1") is None
    assert await redis_conn.get("product:2") is None
    assert await redis_conn.get("product:3") is None
    assert await redis_conn.get("other:key") is not None


@pytest.mark.asyncio
async def test_overwrite(redis_conn):
    """Should overwrite an existing key."""
    await redis_conn.set("test:overwrite", json.dumps({"version": 1}))
    await redis_conn.set("test:overwrite", json.dumps({"version": 2}))
    result = json.loads(await redis_conn.get("test:overwrite"))
    assert result["version"] == 2


@pytest.mark.asyncio
async def test_complex_data(redis_conn):
    """Should handle complex nested data structures."""
    data = {
        "items": [
            {"id": 1, "name": "Taśma TheraBand", "price": "89.99"},
            {"id": 2, "name": "Piłka lacrosse", "price": "24.90"},
        ],
        "total": 2,
        "skip": 0,
        "limit": 20,
    }
    await redis_conn.set("products:list", json.dumps(data))
    result = json.loads(await redis_conn.get("products:list"))
    assert result == data
    assert len(result["items"]) == 2


@pytest.mark.asyncio
async def test_flush(redis_conn):
    """Should clear all keys in the database."""
    await redis_conn.set("key:1", "a")
    await redis_conn.set("key:2", "b")

    await redis_conn.flushdb()

    assert await redis_conn.get("key:1") is None
    assert await redis_conn.get("key:2") is None


@pytest.mark.asyncio
async def test_product_cache_key_format():
    """Product cache keys should follow the expected naming convention."""
    from app.services.product_service import PRODUCT_CACHE_KEY, PRODUCT_LIST_CACHE_KEY

    key = PRODUCT_CACHE_KEY.format(product_id=42)
    assert key == "product:42"

    list_key = PRODUCT_LIST_CACHE_KEY.format(
        query=None, category_id=1, skip=0, limit=20
    )
    assert "cat=1" in list_key
    assert "s=0" in list_key
    assert "l=20" in list_key


@pytest.mark.asyncio
async def test_incr_and_expire(redis_conn):
    """Should support atomic increment (useful for rate limiting)."""
    await redis_conn.set("counter", 0)
    await redis_conn.incr("counter")
    await redis_conn.incr("counter")
    await redis_conn.incr("counter")
    val = int(await redis_conn.get("counter"))
    assert val == 3
