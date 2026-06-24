from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.databse import Base


class RevokedJwtToken(Base):
    __tablename__ = "revoked_jwt_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    session_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

    jti: Mapped[str] = mapped_column(String(120), nullable=False)

    token_type: Mapped[str] = mapped_column(String(30), nullable=False)

    revoke_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="revoked_tokens",
        foreign_keys=[user_id],
    )

    session: Mapped["UserSession | None"] = relationship(
        "UserSession",
        back_populates="revoked_tokens",
        foreign_keys=[session_id],
    )

    __table_args__ = (
        UniqueConstraint("jti"),
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["session_id"], ["user_sessions.id"], ondelete="SET NULL"),
        Index(None, "user_id"),
        Index(None, "session_id"),
        Index(None, "expires_at"),
    )