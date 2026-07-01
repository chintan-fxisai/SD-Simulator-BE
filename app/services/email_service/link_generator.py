import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode, urljoin

from app.config.config import settings


REGISTRATION_EMAIL_TOKEN_TYPE = "registration_email_verification"


class EmailVerificationTokenError(ValueError):
    pass


class EmailVerificationTokenExpired(EmailVerificationTokenError):
    pass


def _base64_url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _base64_url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


def create_registration_email_token(user_id: str, email: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES
    )
    payload = {
        "sub": user_id,
        "email": email,
        "type": REGISTRATION_EMAIL_TOKEN_TYPE,
        "exp": int(expires_at.timestamp()),
    }
    payload_text = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    encoded_payload = _base64_url_encode(payload_text.encode("utf-8"))
    signature = _sign_payload(encoded_payload)
    return f"{encoded_payload}.{_base64_url_encode(signature)}"


def verify_registration_email_token(token: str) -> dict:
    try:
        encoded_payload, encoded_signature = token.split(".", 1)
    except ValueError as exc:
        raise EmailVerificationTokenError("Invalid verification token.") from exc

    expected_signature = _sign_payload(encoded_payload)

    try:
        actual_signature = _base64_url_decode(encoded_signature)
    except (ValueError, TypeError) as exc:
        raise EmailVerificationTokenError("Invalid verification token.") from exc

    if not hmac.compare_digest(actual_signature, expected_signature):
        raise EmailVerificationTokenError("Invalid verification token.")

    try:
        payload = json.loads(_base64_url_decode(encoded_payload).decode("utf-8"))
    except (ValueError, TypeError, UnicodeDecodeError) as exc:
        raise EmailVerificationTokenError("Invalid verification token.") from exc

    if payload.get("type") != REGISTRATION_EMAIL_TOKEN_TYPE:
        raise EmailVerificationTokenError("Invalid verification token type.")

    expires_at = payload.get("exp")
    if not isinstance(expires_at, int):
        raise EmailVerificationTokenError("Invalid verification token expiry.")

    if expires_at < int(datetime.now(timezone.utc).timestamp()):
        raise EmailVerificationTokenExpired("Verification link has expired.")

    if not payload.get("sub") or not payload.get("email"):
        raise EmailVerificationTokenError("Invalid verification token payload.")

    return payload


def create_registration_verification_link(user_id: str, email: str) -> str:
    token = create_registration_email_token(user_id=user_id, email=email)
    base_url = settings.BACKEND_BASE_URL.rstrip("/") + "/"
    verification_path = settings.EMAIL_VERIFICATION_PATH.lstrip("/")
    verification_url = urljoin(base_url, verification_path)
    return f"{verification_url}?{urlencode({'token': token})}"


def _sign_payload(encoded_payload: str) -> bytes:
    return hmac.new(
        settings.JWT_SECRET_KEY.encode("utf-8"),
        encoded_payload.encode("ascii"),
        hashlib.sha256,
    ).digest()

