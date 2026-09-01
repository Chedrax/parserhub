from typing import Any
from uuid import uuid4

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


async def create_user_and_login(
    api_client: AsyncClient,
    email: str,
    username: str,
    password: str,
) -> Any:
    register_response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": password,
        },
    )

    assert register_response.status_code == status.HTTP_201_CREATED

    login_response = await api_client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == status.HTTP_200_OK

    return login_response.json()["access_token"]


@pytest.mark.asyncio
async def test_get_current_user(
    api_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    email = generate_email()
    username = generate_username()
    password = generate_password()

    async with api_client:
        token = await create_user_and_login(
            api_client=api_client,
            email=email,
            username=username,
            password=password,
        )

        response = await api_client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["email"] == email
    assert data["username"] == username
    assert "password" not in data
    assert "password_hash" not in data

    await db_session.execute(delete(User).where(User.email == email))
    await db_session.commit()


@pytest.mark.asyncio
async def test_get_current_user_requires_authentication(
    api_client: AsyncClient,
) -> None:
    async with api_client:
        response = await api_client.get("/api/v1/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user_rejects_invalid_token(
    api_client: AsyncClient,
) -> None:
    async with api_client:
        response = await api_client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid-token"},
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user_rejects_nonexistent_user(
    api_client: AsyncClient,
) -> None:
    from parserhub.core.security import create_access_token

    token = create_access_token(subject=uuid4().hex)

    async with api_client:
        response = await api_client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
