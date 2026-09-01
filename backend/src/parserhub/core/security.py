from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from parserhub.core.config import get_settings

password_hash = PasswordHash.recommended()

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a plaintext password."""

    return password_hash.hash(password=password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""

    return password_hash.verify(password=password, hash=hashed_password)


def create_access_token(subject: str) -> str:
    """Create a JWT access token for the given subject."""

    now = datetime.now(tz=UTC)
    settings = get_settings()

    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expires_at,
    }

    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        payload=payload,
        key=settings.secret_key.get_secret_value(),
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token."""

    settings = get_settings()

    return jwt.decode(  # pyright: ignore[reportUnknownMemberType]
        token,
        settings.secret_key.get_secret_value(),
        algorithms=[ALGORITHM],
    )
