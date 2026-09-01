from enum import StrEnum


def enum_values(enum: type[StrEnum]) -> list[str]:
    """Return enum values for SQLAlchemy Enum values_callable."""
    return [member.value for member in enum]


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
