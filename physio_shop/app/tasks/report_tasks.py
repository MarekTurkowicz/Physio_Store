"""
Sales report Celery task.

generate_sales_report — triggered manually via POST /api/v1/reports/generate
                         (manager-only endpoint). Queries orders for the
                         requested period, aggregates revenue, and emails
                         the report to the requesting manager.
"""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.celery_app import celery_app
from app.config import get_settings
from app.database import async_session_factory
from app.models.order import Order
from app.models.order import OrderItem
from app.models.product import Product
from app.tasks import run_async
from app.tasks.email_tasks import _base_template, _send_email

logger = logging.getLogger(__name__)
settings = get_settings()

PERIOD_DAYS = {"daily": 1, "weekly": 7, "monthly": 30}


async def _build_report(period: str) -> dict:
    """Query the DB and return aggregated sales stats for the given period."""
    days = PERIOD_DAYS.get(period, 7)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    async with async_session_factory() as session:
        # Total revenue & order count
        revenue_result = await session.execute(
            select(
                func.count(Order.id).label("order_count"),
                func.coalesce(func.sum(Order.total_amount), 0).label("total_revenue"),
            ).where(
                Order.created_at >= since,
                Order.status != "cancelled",
            )
        )
        row = revenue_result.one()
        order_count = int(row.order_count)
        total_revenue = float(row.total_revenue)

        # Top 5 products by units sold
        top_result = await session.execute(
            select(
                Product.name,
                func.sum(OrderItem.quantity).label("units_sold"),
                func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
            )
            .join(OrderItem, Product.id == OrderItem.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(
                Order.created_at >= since,
                Order.status != "cancelled",
            )
            .group_by(Product.id, Product.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(5)
        )
        top_products = [
            {"name": r.name, "units": int(r.units_sold), "revenue": float(r.revenue)}
            for r in top_result.all()
        ]

        # Status breakdown
        status_result = await session.execute(
            select(Order.status, func.count(Order.id).label("cnt"))
            .where(Order.created_at >= since)
            .group_by(Order.status)
        )
        status_breakdown = {r.status: int(r.cnt) for r in status_result.all()}

    return {
        "period": period,
        "days": days,
        "since": since.strftime("%Y-%m-%d %H:%M"),
        "order_count": order_count,
        "total_revenue": total_revenue,
        "top_products": top_products,
        "status_breakdown": status_breakdown,
    }


def _report_html(data: dict) -> str:
    period_label = {"daily": "Dzienny", "weekly": "Tygodniowy", "monthly": "Miesięczny"}.get(
        data["period"], data["period"].capitalize()
    )

    top_rows = ""
    for i, p in enumerate(data["top_products"], 1):
        top_rows += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     color:#94a3b8;">{i}</td>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     color:#cbd5e1;">{p['name']}</td>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     text-align:center;color:#5eead4;">{p['units']} szt.</td>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     text-align:right;color:#14b8a6;font-weight:700;">
            {p['revenue']:.2f} PLN</td>
        </tr>"""

    status_rows = "".join(
        f"<tr><td style='color:#94a3b8;padding:4px 0;'>{s.capitalize()}</td>"
        f"<td style='text-align:right;color:#cbd5e1;font-weight:700;'>{c}</td></tr>"
        for s, c in data["status_breakdown"].items()
    )

    body = f"""
    <h2 style="color:#5eead4;font-weight:900;margin:0 0 4px;">
      📊 {period_label} raport sprzedaży</h2>
    <p style="color:#64748b;font-size:13px;margin:0 0 28px;">
      Okres: ostatnie {data['days']} dni (od {data['since']} UTC)</p>

    <!-- KPI cards -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
      <tr>
        <td width="48%" style="padding:16px;background:rgba(20,184,166,.08);
                                border-radius:12px;border:1px solid rgba(20,184,166,.2);
                                text-align:center;">
          <span style="display:block;font-size:32px;font-weight:900;color:#14b8a6;">
            {data['order_count']}</span>
          <span style="font-size:12px;color:#64748b;text-transform:uppercase;
                       letter-spacing:.06em;">Zamówień</span>
        </td>
        <td width="4%"></td>
        <td width="48%" style="padding:16px;background:rgba(20,184,166,.08);
                                border-radius:12px;border:1px solid rgba(20,184,166,.2);
                                text-align:center;">
          <span style="display:block;font-size:28px;font-weight:900;color:#5eead4;">
            {data['total_revenue']:.2f} PLN</span>
          <span style="font-size:12px;color:#64748b;text-transform:uppercase;
                       letter-spacing:.06em;">Przychód</span>
        </td>
      </tr>
    </table>

    <!-- Top products -->
    <h3 style="color:#e2e8f0;font-weight:800;margin:0 0 12px;font-size:15px;">
      Top 5 produktów</h3>
    <table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;">
      <thead>
        <tr>
          <th style="text-align:left;color:#64748b;padding-bottom:8px;">#</th>
          <th style="text-align:left;color:#64748b;padding-bottom:8px;">Produkt</th>
          <th style="text-align:center;color:#64748b;padding-bottom:8px;">Sprzedano</th>
          <th style="text-align:right;color:#64748b;padding-bottom:8px;">Przychód</th>
        </tr>
      </thead>
      <tbody>{top_rows if top_rows else
              '<tr><td colspan="4" style="color:#64748b;padding:16px 0;">Brak danych</td></tr>'}</tbody>
    </table>

    <!-- Status breakdown -->
    <h3 style="color:#e2e8f0;font-weight:800;margin:28px 0 12px;font-size:15px;">
      Statusy zamówień</h3>
    <table width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;">
      {status_rows if status_rows else
       '<tr><td style="color:#64748b;">Brak zamówień w tym okresie</td></tr>'}
    </table>
    """
    return _base_template(f"{period_label} raport – PhysioStore", body)


# ── Task ──────────────────────────────────────────────────────────────────────

@celery_app.task(bind=True, max_retries=2, default_retry_delay=120)
def generate_sales_report(self, period: str, manager_email: str) -> None:
    """
    Generate and email a sales report for the given period.

    Args:
        period: "daily" | "weekly" | "monthly"
        manager_email: Recipient — the manager who requested the report.

    Triggered via POST /api/v1/reports/generate (manager-only endpoint).
    """
    if period not in PERIOD_DAYS:
        logger.error("generate_sales_report: unknown period '%s'", period)
        return

    try:
        data = run_async(_build_report(period))
        html = _report_html(data)
        period_label = {"daily": "Dzienny", "weekly": "Tygodniowy", "monthly": "Miesięczny"}.get(
            period, period
        )
        _send_email(
            manager_email,
            f"📊 {period_label} raport sprzedaży – PhysioStore",
            html,
        )
        logger.info(
            "Sales report (%s) sent to %s: %d orders, %.2f PLN",
            period, manager_email, data["order_count"], data["total_revenue"],
        )
    except Exception as exc:
        logger.warning("generate_sales_report retry %d: %s", self.request.retries, exc)
        raise self.retry(exc=exc)
