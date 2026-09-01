from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from parserhub.db.session import get_db_session
from parserhub.db.unit_of_work import UnitOfWork
from parserhub.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from parserhub.schemas.error import ErrorResponse
from parserhub.schemas.user import UserResponse
from parserhub.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

session_dependency = Depends(get_db_session)


def get_auth_service(
    session: AsyncSession = session_dependency,
) -> AuthService:
    """Create an AuthService for the current request."""

    return AuthService(uow=UnitOfWork(session=session))


auth_service_dependency = Depends(get_auth_service)


@router.post(
    path="/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "User with this email or username already exists",
        },
    },
)
async def register(
    request: RegisterRequest,
    service: AuthService = auth_service_dependency,
) -> UserResponse:
    """Register a new user."""

    user = await service.register(
        email=str(request.email),
        username=request.username,
        password=request.password,
    )

    return UserResponse.model_validate(obj=user)


@router.post(
    path="/login",
    response_model=TokenResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Invalid email or password",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "User account is inactive",
        },
    },
)
async def login(
    request: LoginRequest,
    service: AuthService = auth_service_dependency,
) -> TokenResponse:
    """Authenticate a user and return an access token."""

    access_token = await service.authenticate(
        email=str(request.email),
        password=request.password,
    )

    return TokenResponse(
        access_token=access_token,
    )
