from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String,
        unique=False,
        nullable=False,
    )
    temporary_password_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True,
    )


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )


class AccessRequest(Base):
    __tablename__ = "access_requests"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id")
    )

    reason: Mapped[str] = mapped_column()

    duration_days: Mapped[int] = mapped_column()

    status: Mapped[str] = mapped_column()

    requester_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    recipient_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )