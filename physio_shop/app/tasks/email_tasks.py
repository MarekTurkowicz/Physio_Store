"""
Email Celery tasks.

All tasks accept only JSON-serializable primitive types so they survive
the broker serialization round-trip. HTML templates are defined inline.

SMTP configuration comes from settings (SMTP_HOST / SMTP_PORT / ...).
If SMTP_HOST is empty the email body is printed to the worker log instead
— useful for local development without a real mail server.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.celery_app import celery_app
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# ── SMTP helper ───────────────────────────────────────────────────────────────

def _send_email(to: str, subject: str, html: str) -> None:
    """Send an HTML email via SMTP or log it when SMTP is not configured."""
    if not settings.SMTP_HOST:
        logger.info("[EMAIL – no SMTP] To: %s | Subject: %s", to, subject)
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.sendmail(settings.SMTP_FROM, to, msg.as_string())
        logger.info("Email sent to %s: %s", to, subject)
    except Exception as exc:
        logger.error("Failed to send email to %s: %s", to, exc)
        raise


# ── HTML templates ────────────────────────────────────────────────────────────

def _base_template(title: str, body: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#07111f;font-family:'Segoe UI',Arial,sans-serif;color:#e2e8f0;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td align="center" style="padding:40px 20px;">
        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#0f172a;border-radius:16px;overflow:hidden;
                      border:1px solid rgba(148,163,184,0.15);">
          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#0d9488,#14b8a6);
                       padding:28px 36px;">
              <span style="font-size:22px;font-weight:900;color:#fff;
                           letter-spacing:-0.03em;">PhysioStore</span>
              <span style="display:block;font-size:11px;color:rgba(255,255,255,.7);
                           text-transform:uppercase;letter-spacing:.1em;
                           margin-top:4px;">Pro Rehabilitacja</span>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:36px;">
              {body}
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="padding:20px 36px;border-top:1px solid rgba(148,163,184,.12);
                       font-size:12px;color:#64748b;text-align:center;">
              © 2026 PhysioStore · ul. Rehabilitacyjna 12, 00-950 Warszawa
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def _order_items_html(items: list[dict]) -> str:
    rows = ""
    for item in items:
        rows += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     color:#cbd5e1;">{item['name']}</td>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     text-align:center;color:#94a3b8;">{item['quantity']}x</td>
          <td style="padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1);
                     text-align:right;color:#5eead4;font-weight:700;">
            {item['unit_price']} PLN
          </td>
        </tr>"""
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0"
           style="margin-top:16px;font-size:14px;">
      <thead>
        <tr>
          <th style="text-align:left;color:#64748b;font-weight:600;
                     padding-bottom:8px;border-bottom:1px solid rgba(148,163,184,.2);">
            Produkt</th>
          <th style="text-align:center;color:#64748b;font-weight:600;
                     padding-bottom:8px;border-bottom:1px solid rgba(148,163,184,.2);">
            Ilość</th>
          <th style="text-align:right;color:#64748b;font-weight:600;
                     padding-bottom:8px;border-bottom:1px solid rgba(148,163,184,.2);">
            Cena</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>"""


# ── Tasks ─────────────────────────────────────────────────────────────────────

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation(
    self,
    order_id: int,
    user_email: str,
    user_name: str,
    total: str,
    items: list[dict],
    shipping_address: str,
) -> None:
    """
    Send an order confirmation email immediately after the order is placed.

    Called from OrderService.create_order() after successful persistence.

    Args:
        order_id: Database ID of the created order.
        user_email: Recipient email.
        user_name: Customer's full name.
        total: Formatted total amount (e.g. "189.99").
        items: List of dicts with keys: name, quantity, unit_price.
        shipping_address: Delivery address string.
    """
    try:
        items_table = _order_items_html(items)
        body = f"""
        <h2 style="color:#5eead4;font-weight:900;margin:0 0 8px;">
          Zamówienie potwierdzone! 🎉</h2>
        <p style="color:#94a3b8;margin:0 0 24px;">
          Cześć <strong style="color:#e2e8f0;">{user_name}</strong>,<br/>
          Twoje zamówienie <strong style="color:#14b8a6;">#{order_id}</strong>
          zostało przyjęte i jest przetwarzane.</p>

        {items_table}

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;">
          <tr>
            <td style="padding:16px;background:rgba(20,184,166,.08);
                       border-radius:12px;border:1px solid rgba(20,184,166,.2);">
              <span style="color:#94a3b8;font-size:13px;">Do zapłaty:</span>
              <span style="display:block;font-size:26px;font-weight:900;
                           color:#14b8a6;margin-top:4px;">{total} PLN</span>
            </td>
          </tr>
        </table>

        <p style="margin:20px 0 0;font-size:13px;color:#64748b;">
          📦 Adres dostawy: {shipping_address}</p>
        <p style="margin:8px 0 0;font-size:13px;color:#64748b;">
          🚚 Szacowany czas dostawy: <strong style="color:#e2e8f0;">24h</strong></p>
        """
        html = _base_template(f"Potwierdzenie zamówienia #{order_id}", body)
        _send_email(user_email, f"✅ Zamówienie #{order_id} przyjęte – PhysioStore", html)
    except Exception as exc:
        logger.warning("send_order_confirmation retry %d: %s", self.request.retries, exc)
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_status_update(
    self,
    order_id: int,
    user_email: str,
    user_name: str,
    new_status: str,
) -> None:
    """
    Notify the customer every time their order status changes.

    Called from OrderService.update_status() after each transition.
    """
    STATUS_LABELS = {
        "confirmed":  ("Zamówienie potwierdzone",  "🟢", "#4ade80"),
        "shipped":    ("Zamówienie wysłane",        "📦", "#60a5fa"),
        "delivered":  ("Zamówienie dostarczone",    "🏠", "#5eead4"),
        "cancelled":  ("Zamówienie anulowane",      "❌", "#f87171"),
    }
    label, icon, color = STATUS_LABELS.get(
        new_status, (new_status.capitalize(), "ℹ️", "#94a3b8")
    )

    try:
        body = f"""
        <h2 style="color:{color};font-weight:900;margin:0 0 8px;">
          {icon} {label}</h2>
        <p style="color:#94a3b8;margin:0 0 24px;">
          Cześć <strong style="color:#e2e8f0;">{user_name}</strong>,<br/>
          status Twojego zamówienia
          <strong style="color:#14b8a6;">#{order_id}</strong>
          został zmieniony na:</p>

        <div style="display:inline-block;padding:12px 24px;
                    background:rgba(255,255,255,.05);border-radius:12px;
                    border:1px solid {color};font-size:18px;font-weight:800;
                    color:{color};">
          {label}
        </div>

        <p style="margin:24px 0 0;font-size:13px;color:#64748b;">
          W razie pytań skontaktuj się z nami:
          <a href="mailto:wsparcie@physiostore.pl"
             style="color:#14b8a6;">wsparcie@physiostore.pl</a></p>
        """
        html = _base_template(f"Status zamówienia #{order_id}", body)
        _send_email(user_email, f"{icon} Zamówienie #{order_id}: {label}", html)
    except Exception as exc:
        logger.warning("send_order_status_update retry %d: %s", self.request.retries, exc)
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, user_email: str, user_name: str) -> None:
    """
    Send a welcome email right after successful registration.

    Called from AuthService.register() after creating the user.
    """
    try:
        body = f"""
        <h2 style="color:#5eead4;font-weight:900;margin:0 0 8px;">
          Witaj w PhysioStore! 👋</h2>
        <p style="color:#94a3b8;margin:0 0 20px;">
          Cześć <strong style="color:#e2e8f0;">{user_name}</strong>,<br/>
          Cieszymy się, że dołączyłeś do naszej społeczności!</p>

        <table width="100%" cellpadding="0" cellspacing="0">
          {"".join(f'''
          <tr>
            <td style="padding:12px 0;border-bottom:1px solid rgba(148,163,184,.08);">
              <span style="margin-right:10px;">{icon}</span>
              <span style="color:#cbd5e1;">{text}</span>
            </td>
          </tr>''' for icon, text in [
              ("🛡️", "Certyfikowany sprzęt medyczny z atestem CE"),
              ("🚚", "Darmowa dostawa powyżej 150 PLN"),
              ("💎", "Program lojalnościowy – punkty za każdy zakup"),
              ("📋", "Indywidualne plany ćwiczeń do zamówień powyżej 200 PLN"),
          ])}
        </table>

        <div style="margin-top:28px;text-align:center;">
          <a href="http://localhost:3000/produkty"
             style="display:inline-block;padding:14px 32px;
                    background:linear-gradient(135deg,#0d9488,#14b8a6);
                    color:#fff;font-weight:700;border-radius:12px;
                    text-decoration:none;font-size:15px;">
            Przeglądaj sklep →
          </a>
        </div>
        """
        html = _base_template("Witaj w PhysioStore!", body)
        _send_email(user_email, "👋 Witaj w PhysioStore – zacznij zakupy!", html)
    except Exception as exc:
        logger.warning("send_welcome_email retry %d: %s", self.request.retries, exc)
        raise self.retry(exc=exc)
