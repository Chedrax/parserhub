import pytest
from sqlalchemy import text

from parserhub.db.session import async_session_factory


@pytest.mark.asyncio
async def test_database_connection() -> None:
    async with async_session_factory() as session:
        result = await session.execute(statement=text(text="SELECT 1"))

    assert result.scalar_one() == 1
