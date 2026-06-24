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

from app.core.databse import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    
    assigned_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="roles",
        foreign_keys=[user_id],
    )
    
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="user_roles")
    
    assigned_by_user: Mapped["User | None"] = relationship(
        "User",
        back_populates="assigned",
        foreign_keys=[assigned_by],
    )
    
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", "tenant_id"),
        ForeignKeyConstraint(
            ["role_id"],["roles.id"],
            ondelete="CASCADE"
        ),

        ForeignKeyConstraint(
            ["user_id"],["users.id"],
        ),

        ForeignKeyConstraint(
            ["tenant_id"],["tenants.id"],
        ),
        ForeignKeyConstraint(
            ["assigned_by"],["users.id"],
        ),
        Index(None, "user_id"),
        Index(None, "tenant_id"),
        Index(None, "role_id"),
    )