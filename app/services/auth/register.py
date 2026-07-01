import logging

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models.users import User
from app.db_models.tenants import Tenant
from app.db_models.user_tenant import UserTenant
from app.db_models.roles import Role
from app.db_models.user_role import UserRole
from app.pydantic_schemas.requests.auth.register import RegisterUserRequest
from app.pydantic_schemas.responses.auth.register import RegisterUserResponse
from app.utils.security import hash_password
from app.services.email_service.service import send_registration_verification_email


logger = logging.getLogger(__name__)


async def register_user_service(
    payload: RegisterUserRequest,
    db: AsyncSession,
) -> RegisterUserResponse:
    email = payload.email.lower().strip()
    tenant_name = payload.tenant_name.strip()

    existing_user = await db.scalar(
        select(User).where(
            func.lower(User.email) == email,
            User.is_deleted.is_(False),
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    try:
        user = User(
            email=email,
            password_hash=hash_password(payload.password),
            first_name=payload.first_name.strip() if payload.first_name else None,
            last_name=payload.last_name.strip() if payload.last_name else None,
            is_super_admin=payload.is_super_admin,
        )
        db.add(user)
        await db.flush()
        logger.info("User created with email %s", email)

        tenant = Tenant(
            tenant_email=email,
            owner_id=user.id,
            name=tenant_name,
        )
        db.add(tenant)
        await db.flush()
        logger.info("Tenant created for email %s", email)

        user_tenant = UserTenant(
            user_id=user.id,
            tenant_id=tenant.id,
            invited_by_user_id=None,
            is_owner=True,
            is_active=True,
        )
        db.add(user_tenant)
        await db.flush()
        logger.info("User-Tenant created mapping for user with email %s", email)

        if payload.is_super_admin:
            role_name = "Super Admin"
        elif payload.is_venue_manager:
            role_name = "Venue Manager"
        elif payload.is_attendee:
            role_name = "attendee"
        else:
            role_name = "attendee"

        role = Role(
            tenant_id=tenant.id,
            name=role_name,
            description=f"{role_name} role for {tenant_name}.",
        )
        db.add(role)
        await db.flush()
        logger.info("SUPER ADMIN role for user with email %s", email)

        user_role = UserRole(
            user_id=user.id,
            tenant_id=tenant.id,
            role_id=role.id,
            assigned_by=user.id,
        )
        db.add(user_role)
        await db.flush()
        logger.info("User-Role mapping created for user with email %s", email)

        await db.commit()
        await db.refresh(user)
        await db.refresh(tenant)
        await db.refresh(user_tenant)
        await db.refresh(role)
        await db.refresh(user_role)
        logger.info("Created final user tenant role membership for email %s", email)
    except Exception:
        await db.rollback()
        logger.exception("Rolled back registration for email %s", email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occured while creating user",
        )

    try:
        await send_registration_verification_email(
            user_id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            tenant_name=tenant.name,
        )
    except Exception:
        logger.exception("Failed to send registration verification email to %s", email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User registered, but verification email could not be sent.",
        )

    return RegisterUserResponse(
        status="success",
        message="User registered successfully. Verification email sent.",
        user={
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_super_admin": user.is_super_admin,
            "tenant_name": tenant.name,
        },
    )

