import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models.roles import Role
from app.db_models.tenants import Tenant
from app.db_models.user_role import UserRole
from app.db_models.user_tenant import UserTenant
from app.db_models.users import User
from app.pydantic_schemas.responses.auth.verify_email import VerifyEmailResponse
from app.services.email_service.link_generator import (
    EmailVerificationTokenError,
    EmailVerificationTokenExpired,
    verify_registration_email_token,
)


logger = logging.getLogger(__name__)


def _mark_available_status_fields_true(model_instance) -> None:
    if hasattr(model_instance, "is_active"):
        model_instance.is_active = True
    if hasattr(model_instance, "is_verified"):
        model_instance.is_verified = True


async def verify_registration_email_service(token: str, db: AsyncSession) -> VerifyEmailResponse:
    try:
        payload = verify_registration_email_token(token)
        user_id = UUID(payload["sub"])
        email = payload["email"].lower().strip()
    except EmailVerificationTokenExpired as exc:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={"status": "unverified", "detail": str(exc)},
        ) from exc
    except (EmailVerificationTokenError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "unverified", "detail": "Invalid verification link."},
        ) from exc

    user = await db.scalar(
        select(User).where(
            User.id == user_id,
            func.lower(User.email) == email,
            User.is_deleted.is_(False),
        )
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "unverified", "detail": "User not found for this verification link."},
        )

    was_already_verified = user.is_verified and user.is_active

    try:
        _mark_available_status_fields_true(user)
        user.email_verified_at = datetime.now(timezone.utc)

        tenant = await db.scalar(
            select(Tenant).where(
                Tenant.owner_id == user.id,
                func.lower(Tenant.tenant_email) == email,
                Tenant.is_deleted.is_(False),
            )
        )

        if tenant is not None:
            _mark_available_status_fields_true(tenant)

            user_tenant = await db.scalar(
                select(UserTenant).where(
                    UserTenant.user_id == user.id,
                    UserTenant.tenant_id == tenant.id,
                )
            )
            if user_tenant is not None:
                _mark_available_status_fields_true(user_tenant)

            roles = (
                await db.scalars(
                    select(Role)
                    .join(UserRole, UserRole.role_id == Role.id)
                    .where(
                        UserRole.user_id == user.id,
                        UserRole.tenant_id == tenant.id,
                        Role.tenant_id == tenant.id,
                        Role.is_deleted.is_(False),
                    )
                )
            ).all()
            for role in roles:
                _mark_available_status_fields_true(role)

        await db.commit()
        await db.refresh(user)
        logger.info("Verified registration email for %s", email)
    except Exception as exc:
        await db.rollback()
        logger.exception("Failed to verify registration email for %s", email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "unverified", "detail": "Email verification failed."},
        ) from exc

    return VerifyEmailResponse(
        status="verified",
        detail="Email is already verified." if was_already_verified else "Email verified successfully.",
    )
