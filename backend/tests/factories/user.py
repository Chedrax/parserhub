from uuid import UUID, uuid4

from parserhub.core.security import hash_password
from parserhub.models.enums import UserRole
from parserhub.models.user import User


def generate_id() -> UUID:
    """Generate a unique UUID for a test user."""

    return uuid4()


def generate_email() -> str:
    """Generate a unique test email address."""

    return f"test-{uuid4().hex}@example.com"


def generate_username() -> str:
    """Generate a unique test username."""

    return f"test_user_{uuid4().hex[:12]}"


def generate_password() -> str:
    """Generate a password for a test user."""

    return uuid4().hex


def generate_user(
    *,
    id: UUID | None = None,
    email: str | None = None,
    username: str | None = None,
    password_hash: str | None = None,
    is_active: bool = True,
    role: UserRole = UserRole.USER,
) -> User:
    """Create a test user with valid default values."""

    user = User(
        email=email or generate_email(),
        username=username or generate_username(),
        password_hash=password_hash or hash_password(password=generate_password()),
        is_active=is_active,
        role=role,
    )

    if id is not None:
        user.id = id

    return user
