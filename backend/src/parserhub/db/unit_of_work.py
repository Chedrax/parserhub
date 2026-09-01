from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.repositories.user import UserRepository


class UnitOfWork:
    """Manage database repositories and transaction boundaries."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session=session)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
