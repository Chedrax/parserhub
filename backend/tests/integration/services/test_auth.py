import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.core.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from parserhub.core.security import decode_access_token, hash_password, verify_password
from parserhub.db.unit_of_work import UnitOfWork
from parserhub.models.enums import UserRole
from parserhub.services.auth import AuthService
from tests.factories.user import (
    generate_email,
    generate_password,
    generate_user,
    generate_username,
)


@pytest.mark.asyncio
async def test_register_persists_user(
    db_session: AsyncSession,
) -> None:
    service = AuthService(
        uow=UnitOfWork(session=db_session),
    )

    password = generate_password()

    user = await service.register(
        email=generate_email(),
        username=generate_username(),
        password=password,
    )

    assert user.id is not None
    assert user.email == user.email
    assert user.username == user.username
    assert user.role == UserRole.USER
    assert user.is_active is True

    assert user.password_hash != password
    assert verify_password(
        password=password,
        hashed_password=user.password_hash,
    )

    result = await service.uow.users.get_by_id(user_id=user.id)

    assert result is not None
    assert result.id == user.id

    await db_session.delete(instance=result)
    await db_session.commit()


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(
    db_session: AsyncSession,
) -> None:
    service = AuthService(
        uow=UnitOfWork(session=db_session),
    )

    password = generate_password()

    user = await service.register(
        email=generate_email(),
        username=generate_username(),
        password=password,
    )

    with pytest.raises(UserAlreadyExistsError):
        await service.register(
            email=user.email,
            username=generate_username(),
            password=password,
        )

    result = await service.uow.users.get_by_email(
        email=user.email,
    )

    assert result is not None

    await db_session.delete(instance=result)
    await db_session.commit()


@pytest.mark.asyncio
async def test_register_rejects_duplicate_username(
    db_session: AsyncSession,
) -> None:
    service = AuthService(
        uow=UnitOfWork(session=db_session),
    )

    password = generate_password()

    user = await service.register(
        email=generate_email(),
        username=generate_username(),
        password=password,
    )

    with pytest.raises(UserAlreadyExistsError):
        await service.register(
            email=generate_email(),
            username=user.username,
            password=password,
        )

    result = await service.uow.users.get_by_username(
        username=user.username,
    )

    assert result is not None

    await db_session.delete(instance=result)
    await db_session.commit()


@pytest.mark.asyncio
async def test_authenticate_returns_valid_token(
    db_session: AsyncSession,
) -> None:
    service = AuthService(
        uow=UnitOfWork(session=db_session),
    )

    password = generate_password()

    user = generate_user(password_hash=hash_password(password=password))

    db_session.add(instance=user)
    await db_session.commit()
    await db_session.refresh(instance=user)

    token = await service.authenticate(
        email=user.email,
        password=password,
    )

    assert token

    payload = decode_access_token(token=token)

    assert payload["sub"] == str(user.id)
    assert "iat" in payload
    assert "exp" in payload

    await db_session.delete(instance=user)
    await db_session.commit()


@pytest.mark.asyncio
async def test_authenticate_rejects_invalid_password(
    db_session: AsyncSession,
) -> None:
    service = AuthService(
        uow=UnitOfWork(session=db_session),
    )

    password = generate_password()
    user = generate_user(password_hash=hash_password(password=password))

    db_session.add(instance=user)
    await db_session.commit()
    await db_session.refresh(instance=user)

    with pytest.raises(InvalidCredentialsError):
        await service.authenticate(
            email=user.email,
            password=generate_password(),
        )

    await db_session.delete(instance=user)
    await db_session.commit()


@pytest.mark.asyncio
async def test_authenticate_rejects_inactive_user(
    db_session: AsyncSession,
) -> None:
    service = AuthService(
        uow=UnitOfWork(session=db_session),
    )

    password = generate_password()
    user = generate_user(
        password_hash=hash_password(password=password),
        is_active=False,
    )

    db_session.add(instance=user)
    await db_session.commit()
    await db_session.refresh(instance=user)

    with pytest.raises(InactiveUserError):
        await service.authenticate(
            email=user.email,
            password=password,
        )

    await db_session.delete(instance=user)
    await db_session.commit()
