"""
Celery application instance and Beat schedule configuration.

Broker & backend: Redis (shared with the cache layer).
Workers are started via:
    celery -A app.celery_app worker --loglevel=info
Beat scheduler:
    celery -A app.celery_app beat --loglevel=info
Flower monitoring:
    celery -A app.celery_app flower --port=5555
"""

from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

# Use explicit Celery URLs if provided, otherwise fall back to REDIS_URL
_broker = settings.CELERY_BROKER_URL or settings.REDIS_URL
_backend = settings.CELERY_RESULT_BACKEND or settings.REDIS_URL

celery_app = Celery(
    "physiostore",
    broker=_broker,
    backend=_backend,
    include=[
        "app.tasks.email_tasks",
        "app.tasks.stock_tasks",
        "app.tasks.report_tasks",
        "app.tasks.cache_tasks",
    ],
)

celery_app.conf.update(
    # Serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    # Reliability
    task_acks_late=True,           # acknowledge only after task completes
    worker_prefetch_multiplier=1,  # one task at a time per worker process
    task_track_started=True,       # report STARTED state before execution

    # Results
    result_expires=3600,           # keep results in Redis for 1 hour

    # Timezone
    timezone="Europe/Warsaw",
    enable_utc=True,
)

# ── Periodic tasks (Celery Beat) ──────────────────────────────────────────────
celery_app.conf.beat_schedule = {
    # Rebuild/clean the product list cache every hour
    "cleanup-product-cache-hourly": {
        "task": "app.tasks.cache_tasks.cleanup_product_cache",
        "schedule": crontab(minute=0),          # :00 every hour
    },
    # Email all managers a low-stock report every morning
    "daily-stock-report-8am": {
        "task": "app.tasks.stock_tasks.daily_stock_report",
        "schedule": crontab(hour=8, minute=0),  # 08:00 Warsaw time
    },
}
