# from __future__ import annotations

# import uuid
# from datetime import datetime

# from sqlalchemy import (
#     Boolean,
#     DateTime,
#     ForeignKey,
#     ForeignKeyConstraint,
#     Index,
#     String,
#     Text,
#     UniqueConstraint,
#     func,
# )
# from sqlalchemy.dialects.postgresql import INET, UUID
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.core.databse import Base


# class Tenant(Base):
#     __tablename__ = "tenants"

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
#     status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")
#     created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("users.id", ondelete="SET NULL"),
#         nullable=True,
#     )
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#         onupdate=func.now(),
#     )

#     created_by: Mapped[User | None] = relationship(
#         "User",
#         back_populates="created_tenants",
#         foreign_keys=[created_by_user_id],
#     )
#     memberships: Mapped[list[UserTenant]] = relationship(
#         "UserTenant",
#         back_populates="tenant",
#         cascade="all, delete-orphan",
#     )
#     roles: Mapped[list[Role]] = relationship(
#         "Role",
#         back_populates="tenant",
#         cascade="all, delete-orphan",
#     )
#     user_roles: Mapped[list[UserRole]] = relationship(
#         "UserRole",
#         back_populates="tenant",
#         cascade="all, delete-orphan",
#     )
#     sessions: Mapped[list[UserSession]] = relationship(
#         "UserSession",
#         back_populates="tenant",
#     )


# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
#     password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
#     full_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
#     status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")
#     is_super_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
#     email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
#     last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#         onupdate=func.now(),
#     )

#     created_tenants: Mapped[list[Tenant]] = relationship(
#         "Tenant",
#         back_populates="created_by",
#         foreign_keys="Tenant.created_by_user_id",
#     )
#     memberships: Mapped[list[UserTenant]] = relationship(
#         "UserTenant",
#         back_populates="user",
#         cascade="all, delete-orphan",
#         foreign_keys="UserTenant.user_id",
#     )
#     invited_memberships: Mapped[list[UserTenant]] = relationship(
#         "UserTenant",
#         back_populates="invited_by",
#         foreign_keys="UserTenant.invited_by_user_id",
#     )
#     oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
#         "OAuthAccount",
#         back_populates="user",
#         cascade="all, delete-orphan",
#     )
#     roles: Mapped[list[UserRole]] = relationship(
#         "UserRole",
#         back_populates="user",
#         cascade="all, delete-orphan",
#         foreign_keys="UserRole.user_id",
#     )
#     assigned_roles: Mapped[list[UserRole]] = relationship(
#         "UserRole",
#         back_populates="assigned_by",
#         foreign_keys="UserRole.assigned_by_user_id",
#     )
#     sessions: Mapped[list[UserSession]] = relationship(
#         "UserSession",
#         back_populates="user",
#         cascade="all, delete-orphan",
#     )


# class UserTenant(Base):
#     __tablename__ = "user_tenants"
#     __table_args__ = (
#         UniqueConstraint("user_id", "tenant_id"),
#         Index(None, "tenant_id", "status"),
#     )

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     user_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     tenant_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("tenants.id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")
#     is_owner: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
#     invited_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("users.id", ondelete="SET NULL"),
#         nullable=True,
#     )
#     joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#         onupdate=func.now(),
#     )

#     user: Mapped[User] = relationship(
#         "User",
#         back_populates="memberships",
#         foreign_keys=[user_id],
#     )
#     tenant: Mapped[Tenant] = relationship("Tenant", back_populates="memberships")
#     invited_by: Mapped[User | None] = relationship(
#         "User",
#         back_populates="invited_memberships",
#         foreign_keys=[invited_by_user_id],
#     )


# class OAuthAccount(Base):
#     __tablename__ = "oauth_accounts"
#     __table_args__ = (
#         UniqueConstraint("provider", "provider_user_id"),
#         UniqueConstraint("user_id", "provider"),
#     )

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     user_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     provider: Mapped[str] = mapped_column(String(50), nullable=False)
#     provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
#     email: Mapped[str | None] = mapped_column(String(255), nullable=True)
#     access_token_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
#     refresh_token_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
#     token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#         onupdate=func.now(),
#     )

#     user: Mapped[User] = relationship("User", back_populates="oauth_accounts")


# class Role(Base):
#     __tablename__ = "roles"
#     __table_args__ = (
#         UniqueConstraint("tenant_id", "slug"),
#         UniqueConstraint("id", "tenant_id"),
#         Index(None, "tenant_id", "name"),
#     )

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     tenant_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("tenants.id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#     slug: Mapped[str] = mapped_column(String(100), nullable=False)
#     description: Mapped[str | None] = mapped_column(Text, nullable=True)
#     is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#         onupdate=func.now(),
#     )

#     tenant: Mapped[Tenant] = relationship("Tenant", back_populates="roles")
#     permissions: Mapped[list[RolePermission]] = relationship(
#         "RolePermission",
#         back_populates="role",
#         cascade="all, delete-orphan",
#         overlaps="tenant,user_roles",
#     )
#     users: Mapped[list[UserRole]] = relationship(
#         "UserRole",
#         back_populates="role",
#         cascade="all, delete-orphan",
#         overlaps="tenant,user_roles",
#     )


# class Permission(Base):
#     __tablename__ = "permissions"
#     __table_args__ = (
#         UniqueConstraint("resource", "action"),
#     )

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     resource: Mapped[str] = mapped_column(String(100), nullable=False)
#     action: Mapped[str] = mapped_column(String(80), nullable=False)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     description: Mapped[str | None] = mapped_column(Text, nullable=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )

#     roles: Mapped[list[RolePermission]] = relationship(
#         "RolePermission",
#         back_populates="permission",
#         cascade="all, delete-orphan",
#     )


# class RolePermission(Base):
#     __tablename__ = "role_permissions"

#     role_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("roles.id", ondelete="CASCADE"),
#         primary_key=True,
#     )
#     permission_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("permissions.id", ondelete="CASCADE"),
#         primary_key=True,
#     )
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )

#     role: Mapped[Role] = relationship("Role", back_populates="permissions")
#     permission: Mapped[Permission] = relationship("Permission", back_populates="roles")


# class UserRole(Base):
#     __tablename__ = "user_roles"
#     __table_args__ = (
#         UniqueConstraint("user_id", "role_id", "tenant_id"),
#         ForeignKeyConstraint(
#             ["role_id", "tenant_id"],
#             ["roles.id", "roles.tenant_id"],
#             ondelete="CASCADE",
#         ),
#         Index(None, "user_id", "tenant_id"),
#     )

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     user_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
#     tenant_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("tenants.id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     assigned_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("users.id", ondelete="SET NULL"),
#         nullable=True,
#     )
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )

#     user: Mapped[User] = relationship(
#         "User",
#         back_populates="roles",
#         foreign_keys=[user_id],
#     )
#     role: Mapped[Role] = relationship("Role", back_populates="users", overlaps="tenant,user_roles")
#     tenant: Mapped[Tenant] = relationship("Tenant", back_populates="user_roles", overlaps="role,users")
#     assigned_by: Mapped[User | None] = relationship(
#         "User",
#         back_populates="assigned_roles",
#         foreign_keys=[assigned_by_user_id],
#     )


# class UserSession(Base):
#     __tablename__ = "user_sessions"
#     __table_args__ = (
#         UniqueConstraint("session_token_hash"),
#         UniqueConstraint("refresh_token_hash"),
#         UniqueConstraint("user_id", "device_id"),
#         Index(None, "user_id", "revoked_at", "expires_at"),
#     )

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     user_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#     )
#     tenant_id: Mapped[uuid.UUID | None] = mapped_column(
#         UUID(as_uuid=True),
#         ForeignKey("tenants.id", ondelete="SET NULL"),
#         nullable=True,
#     )
#     session_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)
#     refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)
#     access_token_jti: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
#     device_id: Mapped[str] = mapped_column(String(120), nullable=False)
#     device_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
#     device_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
#     ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
#     user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
#     expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
#     revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
#     last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         server_default=func.now(),
#         onupdate=func.now(),
#     )

#     user: Mapped[User] = relationship("User", back_populates="sessions")
#     tenant: Mapped[Tenant | None] = relationship("Tenant", back_populates="sessions")
