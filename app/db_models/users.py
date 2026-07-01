from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy
from app.core.databse import Base

from app.db_models.tenants import Tenant
from app.db_models.user_role import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email: Mapped[str] = mapped_column(String(255), nullable=False)
    
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    first_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    
    last_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False"))
    
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False"))

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False")) 
    
    is_super_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False"))
    
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    owned_tenants: Mapped[list["Tenant"]] = relationship(
        "Tenant",
        back_populates="owner",
        foreign_keys="Tenant.owner_id",
    )

    roles: Mapped[list["UserRole"]]  = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="UserRole.user_id"
    )
    
    assigned: Mapped[list["UserRole"]]  = relationship(
        "UserRole",
        back_populates="assigned_by_user",
        cascade="all, delete-orphan",
        foreign_keys="UserRole.assigned_by"
    )

    memberships: Mapped[list["UserTenant"]] = relationship(
        "UserTenant",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="UserTenant.user_id",
    )

    invited_memberships: Mapped[list["UserTenant"]] = relationship(
        "UserTenant",
        back_populates="invited_by",
        foreign_keys="UserTenant.invited_by_user_id",
    )

    oauth_accounts: Mapped[list["OAuthAccount"]] = relationship(
        "OAuthAccount",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="OAuthAccount.user_id",
    )

    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="UserSession.user_id",
    )

    revoked_tokens: Mapped[list["RevokedJwtToken"]] = relationship(
        "RevokedJwtToken",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="RevokedJwtToken.user_id",
    )
    __table_args__ = (
        Index(None, "is_deleted"),
        Index(None, "is_active")
    )