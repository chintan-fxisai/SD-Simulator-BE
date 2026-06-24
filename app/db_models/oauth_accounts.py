from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.databse import Base


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    provider: Mapped[str] = mapped_column(String(50), nullable=False)

    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)

    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    access_token_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    refresh_token_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

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
        back_populates="oauth_accounts",
        foreign_keys=[user_id],
    )

    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id"),
        UniqueConstraint("user_id", "provider"),
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        Index(None, "user_id"),
        Index(None, "provider"),
    )