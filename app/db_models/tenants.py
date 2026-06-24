from __future__ import annotations

import uuid
from typing import TYPE_CHECKING
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
    CheckConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy

from app.core.databse import Base

if TYPE_CHECKING:
    from app.db_models.users import User
    from app.db_models.roles import Role

class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    tenant_email: Mapped[str] = mapped_column(String(255), nullable=False)

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False"))

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False"))

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False"))

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
        nullable=True,
        server_default=func.now(),
    )

    owner: Mapped["User | None"] = relationship(
        "User",
        back_populates="owned_tenants",
        foreign_keys=[owner_id],
    )

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        back_populates="tenant",
        foreign_keys="Role.tenant_id"
    )

    memberships: Mapped[list["UserTenant"]] = relationship(
        "UserTenant",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )


    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="tenant",
        foreign_keys="UserSession.tenant_id",
    )

    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="tenant",
        cascade="all, delete-orphan",
        foreign_keys="UserRole.tenant_id",
    )
    __table_args__ = (
        ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
        UniqueConstraint("id", "tenant_email", "owner_id"),
    )