import json
from unittest.mock import Mock

import pytest
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from parserhub.core.exception_handlers import (
    authentication_error_handler,
    create_error_response,
    inactive_user_handler,
    invalid_credentials_handler,
    user_already_exists_handler,
    validation_error_handler,
)
from parserhub.core.exceptions import (
    AuthenticationError,
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)


@pytest.fixture
def http_request() -> Request:
    return Mock(spec=Request)


def assert_error_response(
    response: JSONResponse,
    *,
    status_code: int,
    title: str,
    detail: str,
    code: str,
    problem_type: str,
) -> None:
    assert response.status_code == status_code
    assert response.media_type == "application/json"

    data = json.loads(bytes(response.body))

    assert data == {
        "type": f"https://parserhub.dev/problems/{problem_type}",
        "title": title,
        "status": status_code,
        "detail": detail,
        "code": code,
    }


def test_create_error_response() -> None:
    response = create_error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        title="Test error",
        detail="Something went wrong",
        code="TEST_ERROR",
        problem_type="test-error",
    )

    assert_error_response(
        response,
        status_code=status.HTTP_400_BAD_REQUEST,
        title="Test error",
        detail="Something went wrong",
        code="TEST_ERROR",
        problem_type="test-error",
    )


@pytest.mark.asyncio
async def test_user_already_exists_handler(
    http_request: Request,
) -> None:
    exc = UserAlreadyExistsError("User with this email already exists")

    response = await user_already_exists_handler(
        request=http_request,
        exc=exc,
    )

    assert_error_response(
        response,
        status_code=status.HTTP_409_CONFLICT,
        title="User already exists",
        detail=str(exc),
        code="USER_ALREADY_EXISTS",
        problem_type="user-already-exists",
    )


@pytest.mark.asyncio
async def test_invalid_credentials_handler(
    http_request: Request,
) -> None:
    exc = InvalidCredentialsError("Invalid email or password")

    response = await invalid_credentials_handler(
        request=http_request,
        exc=exc,
    )

    assert_error_response(
        response,
        status_code=status.HTTP_401_UNAUTHORIZED,
        title="Invalid credentials",
        detail=str(exc),
        code="INVALID_CREDENTIALS",
        problem_type="invalid-credentials",
    )


@pytest.mark.asyncio
async def test_inactive_user_handler(
    http_request: Request,
) -> None:
    exc = InactiveUserError("User account is inactive")

    response = await inactive_user_handler(
        request=http_request,
        exc=exc,
    )

    assert_error_response(
        response,
        status_code=status.HTTP_403_FORBIDDEN,
        title="User account is inactive",
        detail=str(exc),
        code="USER_INACTIVE",
        problem_type="user-inactive",
    )


@pytest.mark.asyncio
async def test_authentication_error_handler(
    http_request: Request,
) -> None:
    exc = AuthenticationError("Invalid authentication credentials")

    response = await authentication_error_handler(
        request=http_request,
        exc=exc,
    )

    assert_error_response(
        response,
        status_code=status.HTTP_401_UNAUTHORIZED,
        title="Authentication required",
        detail=str(exc),
        code="AUTHENTICATION_REQUIRED",
        problem_type="authentication-required",
    )


@pytest.mark.asyncio
async def test_validation_error_handler(
    http_request: Request,
) -> None:
    exc = RequestValidationError(
        errors=[
            {
                "type": "string_type",
                "loc": ("body", "email"),
                "msg": "Input should be a valid string",
                "input": 123,
            }
        ],
    )

    response = await validation_error_handler(
        request=http_request,
        exc=exc,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    data = json.loads(bytes(response.body))

    assert data["type"] == ("https://parserhub.dev/problems/validation-error")
    assert data["title"] == "Validation error"
    assert data["status"] == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert data["detail"] == "Request validation failed"
    assert data["code"] == "VALIDATION_ERROR"

    assert data["errors"] == [
        {
            "type": "string_type",
            "loc": ["body", "email"],
            "msg": "Input should be a valid string",
        }
    ]
