from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.databse import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    permission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="permissions",
        foreign_keys=[role_id],
    )

    permission: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="roles",
        foreign_keys=[permission_id],
    )

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id"),
        ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["permission_id"], ["permissions.id"], ondelete="CASCADE"),
        Index(None, "role_id"),
        Index(None, "permission_id"),
    )