from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.core.exceptions import AuthenticationError
from parserhub.core.security import decode_access_token
from parserhub.db.session import get_db_session
from parserhub.db.unit_of_work import UnitOfWork
from parserhub.models.user import User

security_scheme = HTTPBearer()

credentials_dependency = Depends(security_scheme)
session_dependency = Depends(get_db_session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = credentials_dependency,
    session: AsyncSession = session_dependency,
) -> User:
    """Return the authenticated user from the access token."""

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError as exc:
        raise AuthenticationError("Invalid authentication credentials") from exc

    subject = payload.get("sub")

    if not isinstance(subject, str):
        raise AuthenticationError("Invalid authentication credentials")

    try:
        user_id = UUID(subject)
    except ValueError as exc:
        raise AuthenticationError("Invalid authentication credentials") from exc

    uow = UnitOfWork(session=session)

    user = await uow.users.get_by_id(user_id=user_id)

    if user is None:
        raise AuthenticationError("Invalid authentication credentials")

    if not user.is_active:
        raise AuthenticationError("Invalid authentication credentials")

    return user
