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
import sqlalchemy



class UserTenant(Base):
    __tablename__ = "user_tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False"))
    
    is_owner: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("False"))
    
    invited_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    
    joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="memberships",
        foreign_keys=[user_id],
    )
    
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="memberships")
    
    invited_by: Mapped["User | None"] = relationship(
        "User",
        back_populates="invited_memberships",
        foreign_keys=[invited_by_user_id],
    )



    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["invited_by_user_id"], ["users.id"], ondelete="SET NULL"),
        UniqueConstraint("user_id", "tenant_id"),
        Index(None, "tenant_id", "is_active"),
    )
