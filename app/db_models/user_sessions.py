from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
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


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    tenant_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

    session_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    access_token_jti: Mapped[str | None] = mapped_column(String(120), nullable=True)

    device_id: Mapped[str] = mapped_column(String(120), nullable=False)

    device_name: Mapped[str | None] = mapped_column(String(150), nullable=True)

    device_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)

    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sqlalchemy.text("True"))

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

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
        back_populates="sessions",
        foreign_keys=[user_id],
    )

    tenant: Mapped["Tenant | None"] = relationship(
        "Tenant",
        back_populates="sessions",
        foreign_keys=[tenant_id],
    )

    revoked_tokens: Mapped[list["RevokedJwtToken"]] = relationship(
        "RevokedJwtToken",
        back_populates="session",
        cascade="all, delete-orphan",
        foreign_keys="RevokedJwtToken.session_id",
    )

    __table_args__ = (
        UniqueConstraint("session_token_hash"),
        UniqueConstraint("refresh_token_hash"),
        UniqueConstraint("access_token_jti"),
        UniqueConstraint("user_id", "device_id"),
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="SET NULL"),
        Index(None, "user_id", "is_active"),
        Index(None, "tenant_id"),
        Index(None, "expires_at"),
    )