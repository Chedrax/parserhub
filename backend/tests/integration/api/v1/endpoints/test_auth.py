import pytest
from fastapi import status
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.main import app
from parserhub.models.user import User
from tests.factories.user import (
    generate_email,
    generate_password,
    generate_username,
)


@pytest.fixture
def api_client() -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    )


@pytest.mark.asyncio
async def test_register_success(
    api_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    email = generate_email()
    username = generate_username()
    password = generate_password()

    async with api_client:
        response = await api_client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password,
            },
        )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["email"] == email
    assert data["username"] == username
    assert "password" not in data
    assert "password_hash" not in data
    assert "id" in data

    result = await db_session.execute(
        User.__table__.select().where(User.email == email)
    )
    row = result.one()

    assert row.email == email
    assert row.username == username
    assert row.password_hash != password

    await db_session.execute(delete(User).where(User.id == row.id))
    await db_session.commit()


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(
    api_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    email = generate_email()
    username = generate_username()

    async with api_client:
        first_response = await api_client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "username": username,
                "password": generate_password(),
            },
        )

        second_response = await api_client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "username": generate_username(),
                "password": generate_password(),
            },
        )

    assert first_response.status_code == status.HTTP_201_CREATED
    assert second_response.status_code == status.HTTP_409_CONFLICT

    await db_session.execute(delete(User).where(User.email == email))
    await db_session.commit()


@pytest.mark.asyncio
async def test_register_rejects_duplicate_username(
    api_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    email = generate_email()
    username = generate_username()

    async with api_client:
        first_response = await api_client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "username": username,
                "password": generate_password(),
            },
        )

        second_email = generate_email()

        second_response = await api_client.post(
            "/api/v1/auth/register",
            json={
                "email": second_email,
                "username": username,
                "password": generate_password(),
            },
        )

    assert first_response.status_code == status.HTTP_201_CREATED
    assert second_response.status_code == status.HTTP_409_CONFLICT

    await db_session.execute(delete(User).where(User.username == username))
    await db_session.commit()


@pytest.mark.asyncio
async def test_register_rejects_invalid_request(
    api_client: AsyncClient,
) -> None:
    async with api_client:
        response = await api_client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "username": "",
                "password": "",
            },
        )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_login_success(
    api_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    email = generate_email()
    username = generate_username()
    password = generate_password()

    async with api_client:
        register_response = await api_client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password,
            },
        )

        login_response = await api_client.post(
            "/api/v1/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

    assert register_response.status_code == status.HTTP_201_CREATED
    assert login_response.status_code == status.HTTP_200_OK

    data = login_response.json()

    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["access_token"]

    await db_session.execute(delete(User).where(User.email == email))
    await db_session.commit()


@pytest.mark.asyncio
async def test_login_rejects_unknown_email(
    api_client: AsyncClient,
) -> None:
    async with api_client:
        response = await api_client.post(
            "/api/v1/auth/login",
            json={
                "email": generate_email(),
                "password": generate_password(),
            },
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_rejects_invalid_password(
    api_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    email = generate_email()
    username = generate_username()

    async with api_client:
        register_response = await api_client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "username": username,
                "password": generate_password(),
            },
        )

        login_response = await api_client.post(
            "/api/v1/auth/login",
            json={
                "email": email,
                "password": generate_password(),
            },
        )

    assert register_response.status_code == status.HTTP_201_CREATED
    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED

    await db_session.execute(delete(User).where(User.email == email))
    await db_session.commit()
