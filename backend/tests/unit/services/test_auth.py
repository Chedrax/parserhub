from unittest.mock import AsyncMock, Mock

import pytest

from parserhub.core.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from parserhub.core.security import hash_password, verify_password
from parserhub.models.user import User
from parserhub.services.auth import AuthService
from tests.factories.user import (
    generate_email,
    generate_password,
    generate_user,
    generate_username,
)


@pytest.fixture
def uow() -> Mock:
    uow = Mock()
    uow.users = Mock()

    uow.users.get_by_email = AsyncMock()
    uow.users.get_by_username = AsyncMock()
    uow.users.create = AsyncMock()
    uow.commit = AsyncMock()

    return uow


@pytest.fixture
def auth_service(uow: Mock) -> AuthService:
    return AuthService(uow=uow)


@pytest.mark.asyncio
async def test_register_creates_user(
    auth_service: AuthService,
    uow: Mock,
) -> None:
    uow.users.get_by_email.return_value = None
    uow.users.get_by_username.return_value = None

    email = generate_email()
    password = generate_password()

    user = await auth_service.register(
        email=email,
        username=generate_username(),
        password=password,
    )

    assert isinstance(user, User)
    assert user.email == email
    assert user.username == user.username
    assert user.password_hash != password
    assert verify_password(
        password=password,
        hashed_password=user.password_hash,
    )

    uow.users.create.assert_awaited_once_with(user=user)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_rejects_existing_email(
    auth_service: AuthService,
    uow: Mock,
) -> None:
    password = generate_password()

    existing_user = generate_user(password_hash=hash_password(password=password))

    uow.users.get_by_email.return_value = existing_user

    with pytest.raises(
        UserAlreadyExistsError,
        match="User with this email already exists",
    ):
        await auth_service.register(
            email=existing_user.email,
            username=generate_username(),
            password=password,
        )

    uow.users.get_by_username.assert_not_awaited()
    uow.users.create.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_rejects_existing_username(
    auth_service: AuthService,
    uow: Mock,
) -> None:
    password = generate_password()

    existing_user = generate_user(password_hash=hash_password(password=password))

    uow.users.get_by_email.return_value = None
    uow.users.get_by_username.return_value = existing_user

    with pytest.raises(
        UserAlreadyExistsError,
        match="User with this username already exists",
    ):
        await auth_service.register(
            email=generate_email(),
            username=existing_user.username,
            password=password,
        )

    uow.users.create.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_authenticate_returns_access_token(
    auth_service: AuthService,
    uow: Mock,
) -> None:
    password = generate_password()

    user = generate_user(password_hash=hash_password(password=password))

    uow.users.get_by_email.return_value = user

    token = await auth_service.authenticate(
        email=user.email,
        password=password,
    )

    assert isinstance(token, str)
    assert token

    uow.users.get_by_email.assert_awaited_once_with(
        email=user.email,
    )


@pytest.mark.asyncio
async def test_authenticate_rejects_unknown_email(
    auth_service: AuthService,
    uow: Mock,
) -> None:
    uow.users.get_by_email.return_value = None

    with pytest.raises(
        InvalidCredentialsError,
        match="Invalid email or password",
    ):
        await auth_service.authenticate(
            email=generate_email(),
            password=generate_password(),
        )


@pytest.mark.asyncio
async def test_authenticate_rejects_invalid_password(
    auth_service: AuthService,
    uow: Mock,
) -> None:
    password = generate_password()

    user = generate_user(password_hash=hash_password(password=password))

    uow.users.get_by_email.return_value = user

    with pytest.raises(
        InvalidCredentialsError,
        match="Invalid email or password",
    ):
        await auth_service.authenticate(
            email=user.email,
            password=generate_password(),
        )


@pytest.mark.asyncio
async def test_authenticate_rejects_inactive_user(
    auth_service: AuthService,
    uow: Mock,
) -> None:
    password = generate_password()

    user = generate_user(
        is_active=False, password_hash=hash_password(password=password)
    )

    uow.users.get_by_email.return_value = user

    with pytest.raises(
        InactiveUserError,
        match="User account is inactive",
    ):
        await auth_service.authenticate(
            email=user.email,
            password=password,
        )
