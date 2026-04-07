"""
Celery task packages for PhysioStore.

Helper utility for running async code inside synchronous Celery tasks.
"""

import asyncio


def run_async(coro):
    """
    Execute an async coroutine from a synchronous Celery task context.

    Creates a fresh event loop per task to avoid conflicts with any existing
    event loop in the worker process.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
        asyncio.set_event_loop(None)
