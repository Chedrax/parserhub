import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.repositories.user import UserRepository
from tests.factories.user import (
    generate_user,
)


@pytest.mark.asyncio
async def test_get_user_by_id(db_session: AsyncSession) -> None:
    user = generate_user()

    repository = UserRepository(db_session)

    await repository.create(user=user)

    result = await repository.get_by_id(user_id=user.id)

    assert result is not None
    assert result.id == user.id
    assert result.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession) -> None:
    user = generate_user()

    repository = UserRepository(db_session)

    await repository.create(user=user)

    result = await repository.get_by_email(email=user.email)

    assert result is not None
    assert result.id == user.id


@pytest.mark.asyncio
async def test_get_user_by_username(db_session: AsyncSession) -> None:
    user = generate_user()

    repository = UserRepository(db_session)

    await repository.create(user=user)

    result = await repository.get_by_username(username=user.username)

    assert result is not None
    assert result.id == user.id
