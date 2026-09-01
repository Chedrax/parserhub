import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.db.session import async_session_factory
from parserhub.db.unit_of_work import UnitOfWork
from parserhub.repositories.user import UserRepository
from tests.factories.user import (
    generate_user,
)


@pytest.mark.asyncio
async def test_unit_of_work_commit(db_session: AsyncSession) -> None:
    async with UnitOfWork(session=db_session) as uow:
        user = generate_user()

        await uow.users.create(user=user)
        await uow.commit()

    assert user.id is not None

    async with async_session_factory() as verification_session:
        repository = UserRepository(session=verification_session)

        result = await repository.get_by_id(user_id=user.id)

        assert result is not None
        assert result.id == user.id

        await verification_session.delete(instance=result)
        await verification_session.commit()


@pytest.mark.asyncio
async def test_unit_of_work_rollback(
    db_session: AsyncSession,
) -> None:
    async with UnitOfWork(session=db_session) as uow:
        user = generate_user()

        with pytest.raises(RuntimeError):
            await uow.users.create(user=user)
            raise RuntimeError("Something went wrong")

    async with async_session_factory() as verification_session:
        repository = UserRepository(session=verification_session)

        result = await repository.get_by_id(user_id=user.id)

    assert result is None
