from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from parserhub.core.exceptions import (
    AuthenticationError,
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)


def create_error_response(
    *,
    status_code: int,
    title: str,
    detail: str,
    code: str,
    problem_type: str,
    errors: list[dict[str, Any]] | None = None,
) -> JSONResponse:
    """Create a standardized RFC 9457-style error response."""

    content: dict[str, Any] = {
        "type": f"https://parserhub.dev/problems/{problem_type}",
        "title": title,
        "status": status_code,
        "detail": detail,
        "code": code,
    }

    if errors is not None:
        content["errors"] = errors

    return JSONResponse(
        status_code=status_code,
        content=content,
    )


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
) -> JSONResponse:
    """Handle duplicate user registration errors."""

    return create_error_response(
        status_code=status.HTTP_409_CONFLICT,
        title="User already exists",
        detail=str(exc),
        code="USER_ALREADY_EXISTS",
        problem_type="user-already-exists",
    )


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
) -> JSONResponse:
    """Handle invalid authentication credentials."""

    return create_error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        title="Invalid credentials",
        detail=str(exc),
        code="INVALID_CREDENTIALS",
        problem_type="invalid-credentials",
    )


async def inactive_user_handler(
    request: Request,
    exc: InactiveUserError,
) -> JSONResponse:
    """Handle authentication attempts from inactive users."""

    return create_error_response(
        status_code=status.HTTP_403_FORBIDDEN,
        title="User account is inactive",
        detail=str(exc),
        code="USER_INACTIVE",
        problem_type="user-inactive",
    )


async def authentication_error_handler(
    request: Request,
    exc: AuthenticationError,
) -> JSONResponse:
    """Handle missing or invalid authentication."""

    return create_error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        title="Authentication required",
        detail=str(exc),
        code="AUTHENTICATION_REQUIRED",
        problem_type="authentication-required",
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle request validation errors."""

    errors = [
        {
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
        }
        for error in exc.errors()
    ]

    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        title="Validation error",
        detail="Request validation failed",
        code="VALIDATION_ERROR",
        problem_type="validation-error",
        errors=errors,
    )
