from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.db.session import async_session_factory, engine


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest_asyncio.fixture(autouse=True)
async def dispose_engine() -> AsyncGenerator[None, None]:
    yield

    await engine.dispose()
