"""
Stock management Celery tasks.

check_low_stock_after_order  — triggered immediately after an order is placed.
daily_stock_report           — scheduled by Beat every morning at 08:00.
"""

import logging
from decimal import Decimal

from sqlalchemy import select

from app.celery_app import celery_app
from app.config import get_settings
from app.database import async_session_factory
from app.models.product import Product
from app.models.user import User
from app.tasks import run_async
from app.tasks.email_tasks import _base_template, _send_email

logger = logging.getLogger(__name__)
settings = get_settings()


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _get_low_stock_products(threshold: int) -> list[dict]:
    """Return all active products with stock below threshold."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Product).where(
                Product.is_active == True,
                Product.stock_quantity <= threshold,
            ).order_by(Product.stock_quantity.asc())
        )
        products = result.scalars().all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "sku": p.sku,
                "stock": p.stock_quantity,
            }
            for p in products
        ]


async def _get_manager_emails() -> list[str]:
    """Fetch emails of all managers and admins."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(User.email).where(User.role.in_(["admin", "manager"]))
        )
        return [row[0] for row in result.all()]


def _low_stock_email_html(products: list[dict], threshold: int) -> str:
    rows = ""
    for p in products:
        color = "#f87171" if p["stock"] == 0 else "#fbbf24"
        rows += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     color:#cbd5e1;">{p['name']}</td>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     color:#94a3b8;font-size:12px;">{p['sku']}</td>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     text-align:center;font-weight:800;color:{color};">
            {p['stock']} szt.
          </td>
        </tr>"""

    body = f"""
    <h2 style="color:#fbbf24;font-weight:900;margin:0 0 8px;">
      ⚠️ Alert niskiego stanu magazynowego</h2>
    <p style="color:#94a3b8;margin:0 0 24px;">
      {len(products)} {"produkt wymaga" if len(products) == 1 else "produktów wymaga"}
      uzupełnienia stanu (próg: <strong style="color:#e2e8f0;">{threshold} szt.</strong>).</p>

    <table width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;">
      <thead>
        <tr>
          <th style="text-align:left;color:#64748b;padding-bottom:8px;
                     border-bottom:1px solid rgba(148,163,184,.2);">Produkt</th>
          <th style="text-align:left;color:#64748b;padding-bottom:8px;
                     border-bottom:1px solid rgba(148,163,184,.2);">SKU</th>
          <th style="text-align:center;color:#64748b;padding-bottom:8px;
                     border-bottom:1px solid rgba(148,163,184,.2);">Stan</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>

    <p style="margin:20px 0 0;font-size:13px;color:#64748b;">
      Zaloguj się do panelu admina aby zaktualizować stany magazynowe.</p>
    """
    return _base_template("Alert magazynowy – PhysioStore", body)


# ── Tasks ─────────────────────────────────────────────────────────────────────

@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def check_low_stock_after_order(self, product_ids: list[int]) -> None:
    """
    Check stock levels for specific products right after an order is placed.
    If any product drops below LOW_STOCK_THRESHOLD, email all managers.

    Called from OrderService.create_order() with the IDs of ordered products.
    """
    try:
        threshold = settings.LOW_STOCK_THRESHOLD

        async def _check():
            async with async_session_factory() as session:
                result = await session.execute(
                    select(Product).where(
                        Product.id.in_(product_ids),
                        Product.is_active == True,
                        Product.stock_quantity <= threshold,
                    )
                )
                low = result.scalars().all()
                if not low:
                    return

                products = [
                    {"id": p.id, "name": p.name, "sku": p.sku, "stock": p.stock_quantity}
                    for p in low
                ]
                manager_emails = await _get_manager_emails()
                return products, manager_emails

        result = run_async(_check())
        if not result:
            return

        products, manager_emails = result
        html = _low_stock_email_html(products, threshold)
        subject = f"⚠️ Niski stan magazynowy – {len(products)} produktów"

        for email in manager_emails:
            _send_email(email, subject, html)

        logger.info(
            "Low-stock alert sent for %d products to %d managers",
            len(products), len(manager_emails),
        )
    except Exception as exc:
        logger.warning("check_low_stock_after_order retry %d: %s", self.request.retries, exc)
        raise self.retry(exc=exc)


@celery_app.task
def daily_stock_report() -> None:
    """
    Scheduled task (Beat): send a full low-stock report to all managers at 08:00.

    Runs even if no orders were placed — ensures managers always start the day
    with an accurate inventory overview.
    """
    threshold = settings.LOW_STOCK_THRESHOLD

    products = run_async(_get_low_stock_products(threshold))
    if not products:
        logger.info("daily_stock_report: all products above threshold — no email sent")
        return

    manager_emails = run_async(_get_manager_emails())
    if not manager_emails:
        logger.warning("daily_stock_report: no manager emails found")
        return

    html = _low_stock_email_html(products, threshold)
    subject = f"📋 Dzienny raport magazynowy – {len(products)} produktów do uzupełnienia"

    for email in manager_emails:
        _send_email(email, subject, html)

    logger.info(
        "Daily stock report: %d products, sent to %d managers",
        len(products), len(manager_emails),
    )
