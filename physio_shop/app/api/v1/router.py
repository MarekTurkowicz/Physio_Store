"""
Aggregated v1 router — includes all v1 sub-routers.
Mounted at /api/v1 in main.py.
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.categories import router as categories_router
from app.api.v1.orders import router as orders_router
from app.api.v1.products import router as products_router
from app.api.v1.reports import router as reports_router
from app.api.v1.users import router as users_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(categories_router)
router.include_router(products_router)
router.include_router(orders_router)
router.include_router(reports_router)
