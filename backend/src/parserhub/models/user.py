import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    String,
    Uuid,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from parserhub.core.constants import (
    EMAIL_MAX_LENGTH,
    USERNAME_MAX_LENGTH,
)
from parserhub.db.base import Base
from parserhub.models.enums import UserRole, enum_values


class User(Base):
    """Database model representing an application user."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default_factory=uuid.uuid4,
        init=False,
    )

    email: Mapped[str] = mapped_column(
        String(length=EMAIL_MAX_LENGTH),
        unique=True,
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(length=USERNAME_MAX_LENGTH),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", native_enum=True, values_callable=enum_values),
        nullable=False,
        default=UserRole.USER,
        server_default=UserRole.USER.value,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        init=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
