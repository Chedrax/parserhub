import pytest
from jwt import InvalidTokenError

from parserhub.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from tests.factories.user import generate_id


def test_password_hash_is_not_plaintext() -> None:
    password = "super-secret-password"

    hashed_password = hash_password(password=password)

    assert hashed_password != password


def test_password_verification() -> None:
    password = "super-secret-password"

    hashed_password = hash_password(password=password)

    assert verify_password(password=password, hashed_password=hashed_password)
    assert not verify_password(
        password="wrong-password", hashed_password=hashed_password
    )


def test_access_token_contains_subject() -> None:
    user_id = generate_id()
    token = create_access_token(subject=user_id.hex)
    payload = decode_access_token(token=token)

    assert payload["sub"] == user_id.hex
    assert "iat" in payload
    assert "exp" in payload


def test_invalid_access_token() -> None:
    with pytest.raises(expected_exception=InvalidTokenError):
        decode_access_token(token="invalid-token")
