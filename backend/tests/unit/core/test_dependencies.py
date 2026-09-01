from unittest.mock import AsyncMock, Mock, patch

import jwt
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.core.dependencies import get_current_user
from parserhub.core.exceptions import AuthenticationError
from tests.factories.user import generate_id, generate_user


@pytest.fixture
def session() -> AsyncSession:
    return Mock(spec=AsyncSession)


@pytest.fixture
def credentials() -> Mock:
    credentials = Mock()
    credentials.credentials = "valid-token"

    return credentials


@pytest.fixture
def user_repository() -> Mock:
    repository = Mock()
    repository.get_by_id = AsyncMock()

    return repository


@pytest.fixture
def uow(user_repository: Mock) -> Mock:
    uow = Mock()
    uow.users = user_repository

    return uow


@pytest.mark.asyncio
async def test_get_current_user_returns_user(
    credentials: Mock,
    session: AsyncSession,
    uow: Mock,
) -> None:
    user = generate_user()

    uow.users.get_by_id.return_value = user

    with patch(
        "parserhub.core.dependencies.decode_access_token",
        return_value={"sub": str(user.id)},
    ):
        with patch(
            "parserhub.core.dependencies.UnitOfWork",
            return_value=uow,
        ):
            result = await get_current_user(
                credentials=credentials,
                session=session,
            )

    assert result is user

    uow.users.get_by_id.assert_awaited_once_with(
        user_id=user.id,
    )


@pytest.mark.asyncio
async def test_get_current_user_rejects_invalid_token(
    credentials: Mock,
    session: AsyncSession,
    uow: Mock,
) -> None:
    with patch(
        "parserhub.core.dependencies.decode_access_token",
        side_effect=jwt.InvalidTokenError,
    ):
        with pytest.raises(
            AuthenticationError,
            match="Invalid authentication credentials",
        ):
            await get_current_user(
                credentials=credentials,
                session=session,
            )

    uow.users.get_by_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_current_user_rejects_missing_subject(
    credentials: Mock,
    session: AsyncSession,
    uow: Mock,
) -> None:
    with patch(
        "parserhub.core.dependencies.decode_access_token",
        return_value={},
    ):
        with pytest.raises(
            AuthenticationError,
            match="Invalid authentication credentials",
        ):
            await get_current_user(
                credentials=credentials,
                session=session,
            )

    uow.users.get_by_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_current_user_rejects_non_string_subject(
    credentials: Mock,
    session: AsyncSession,
    uow: Mock,
) -> None:
    with patch(
        "parserhub.core.dependencies.decode_access_token",
        return_value={"sub": 123},
    ):
        with pytest.raises(
            AuthenticationError,
            match="Invalid authentication credentials",
        ):
            await get_current_user(
                credentials=credentials,
                session=session,
            )

    uow.users.get_by_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_current_user_rejects_invalid_uuid(
    credentials: Mock,
    session: AsyncSession,
    uow: Mock,
) -> None:
    with patch(
        "parserhub.core.dependencies.decode_access_token",
        return_value={"sub": "not-a-uuid"},
    ):
        with pytest.raises(
            AuthenticationError,
            match="Invalid authentication credentials",
        ):
            await get_current_user(
                credentials=credentials,
                session=session,
            )

    uow.users.get_by_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_current_user_rejects_unknown_user(
    credentials: Mock,
    session: AsyncSession,
    uow: Mock,
) -> None:
    user_id = generate_id()

    uow.users.get_by_id.return_value = None

    with patch(
        "parserhub.core.dependencies.decode_access_token",
        return_value={"sub": user_id.hex},
    ):
        with patch(
            "parserhub.core.dependencies.UnitOfWork",
            return_value=uow,
        ):
            with pytest.raises(
                AuthenticationError,
                match="Invalid authentication credentials",
            ):
                await get_current_user(
                    credentials=credentials,
                    session=session,
                )

    uow.users.get_by_id.assert_awaited_once_with(
        user_id=user_id,
    )


@pytest.mark.asyncio
async def test_get_current_user_rejects_inactive_user(
    credentials: Mock,
    session: AsyncSession,
    uow: Mock,
) -> None:
    user = generate_user(is_active=False)

    uow.users.get_by_id.return_value = user

    with patch(
        "parserhub.core.dependencies.decode_access_token",
        return_value={"sub": str(user.id)},
    ):
        with patch(
            "parserhub.core.dependencies.UnitOfWork",
            return_value=uow,
        ):
            with pytest.raises(
                AuthenticationError,
                match="Invalid authentication credentials",
            ):
                await get_current_user(
                    credentials=credentials,
                    session=session,
                )

    uow.users.get_by_id.assert_awaited_once_with(
        user_id=user.id,
    )
