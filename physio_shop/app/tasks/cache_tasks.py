"""
Cache management Celery task.

cleanup_product_cache — scheduled by Beat every hour.
Removes stale product list keys so the next request fetches fresh data.
"""

import logging

import redis as sync_redis

from app.celery_app import celery_app
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@celery_app.task
def cleanup_product_cache() -> None:
    """
    Delete all product list cache keys (pattern: products:*).

    Scheduled every hour by Celery Beat. Forces the next search/list
    request to rebuild the cache from the database, ensuring stale
    product data (updated stock, prices, availability) is evicted.

    Individual product detail keys (product:{id}) are intentionally
    kept — they are invalidated on demand when a product is modified.
    """
    client = sync_redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        deleted = 0
        for key in client.scan_iter(match="products:*"):
            client.delete(key)
            deleted += 1
        logger.info("cleanup_product_cache: deleted %d keys", deleted)
    except sync_redis.RedisError as exc:
        logger.error("cleanup_product_cache failed: %s", exc)
    finally:
        client.close()
