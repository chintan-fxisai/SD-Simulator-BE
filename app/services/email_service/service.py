import asyncio
import logging
import smtplib
from email.message import EmailMessage
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config.config import settings
from app.services.email_service.link_generator import create_registration_verification_link


logger = logging.getLogger(__name__)
TEMPLATE_DIR = Path(__file__).resolve().parent


def _require_email_settings() -> None:
    missing = [
        name
        for name, value in {
            "SMTP_HOST": settings.SMTP_HOST,
            "SMTP_FROM_EMAIL": settings.SMTP_FROM_EMAIL,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing email configuration: {', '.join(missing)}")


def _render_template(template_name: str, context: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    return template.render(**context)


def _send_email(to_email: str, subject: str, html_body: str, text_body: str) -> None:
    _require_email_settings()

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    message["To"] = to_email
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    if settings.SMTP_USE_SSL:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            _login_if_configured(smtp)
            smtp.send_message(message)
        return

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        if settings.SMTP_USE_TLS:
            smtp.starttls()
        _login_if_configured(smtp)
        smtp.send_message(message)


def _login_if_configured(smtp: smtplib.SMTP) -> None:
    if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
        smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)


async def send_registration_verification_email(
    *,
    user_id: str,
    email: str,
    first_name: str | None,
    tenant_name: str,
) -> str:
    verification_link = create_registration_verification_link(
        user_id=user_id,
        email=email,
    )
    display_name = first_name or email.split("@", 1)[0]
    subject = "Verify your email address"
    context = {
        "app_name": settings.APP_NAME or "Event Management System",
        "display_name": display_name,
        "tenant_name": tenant_name,
        "verification_link": verification_link,
        "expires_in_minutes": settings.EMAIL_VERIFICATION_EXPIRE_MINUTES,
    }
    html_body = _render_template("register.html", context)
    text_body = (
        f"Hi {display_name},\n\n"
        f"Verify your email for {context['app_name']} by opening this link:\n"
        f"{verification_link}\n\n"
        f"This link expires in {settings.EMAIL_VERIFICATION_EXPIRE_MINUTES} minutes."
    )

    await asyncio.to_thread(
        _send_email,
        email,
        subject,
        html_body,
        text_body,
    )
    logger.info("Sent registration verification email to %s", email)
    return verification_link
