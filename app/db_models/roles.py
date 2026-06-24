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
from app.db_models.role_permissions import RolePermission

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

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

    tenant: Mapped[Tenant] = relationship(
        "Tenant",
        back_populates="roles",
        foreign_keys=[tenant_id]
        )
    
    users: Mapped[list[UserRole]] = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan",
        foreign_keys="UserRole.role_id"
    )

    permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
        foreign_keys="RolePermission.role_id",
    )


    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        Index(None, "tenant_id"),
        Index(None, "is_active")
    )