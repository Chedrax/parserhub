from parserhub.core.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from parserhub.core.security import create_access_token, hash_password, verify_password
from parserhub.db.unit_of_work import UnitOfWork
from parserhub.models.user import User


class AuthService:
    """Service responsible for authentication business logic."""

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def register(
        self,
        email: str,
        username: str,
        password: str,
    ) -> User:
        """Register a new user."""

        existing_user = await self.uow.users.get_by_email(email=email)

        if existing_user is not None:
            raise UserAlreadyExistsError("User with this email already exists")

        existing_user = await self.uow.users.get_by_username(username=username)

        if existing_user is not None:
            raise UserAlreadyExistsError("User with this username already exists")

        user = User(
            email=email,
            username=username,
            password_hash=hash_password(password=password),
        )

        await self.uow.users.create(user=user)
        await self.uow.commit()

        return user

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> str:
        """Authenticate a user and return an access token."""

        user = await self.uow.users.get_by_email(email=email)

        if user is None:
            raise InvalidCredentialsError("Invalid email or password")

        if not verify_password(password=password, hashed_password=user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_active:
            raise InactiveUserError("User account is inactive")

        return create_access_token(subject=str(user.id))
