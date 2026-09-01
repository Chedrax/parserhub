from fastapi import APIRouter, Depends, status

from parserhub.core.dependencies import get_current_user
from parserhub.models.user import User
from parserhub.schemas.error import ErrorResponse
from parserhub.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

current_user_dependency = Depends(get_current_user)


@router.get(
    path="/me",
    response_model=UserResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Authentication is required or the access token is invalid.",
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_current_user_info(
    current_user: User = current_user_dependency,
) -> UserResponse:
    """Return the currently authenticated user."""

    return UserResponse.model_validate(obj=current_user)
