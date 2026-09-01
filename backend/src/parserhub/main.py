from typing import cast

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.types import ExceptionHandler

from parserhub.api.router import router as api_router
from parserhub.core.exception_handlers import (
    authentication_error_handler,
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

app = FastAPI(
    title="ParserHub API",
    version="0.1.0",
)


app.include_router(router=api_router)


app.add_exception_handler(
    exc_class_or_status_code=AuthenticationError,
    handler=cast(ExceptionHandler, authentication_error_handler),
)

app.add_exception_handler(
    exc_class_or_status_code=UserAlreadyExistsError,
    handler=cast(ExceptionHandler, user_already_exists_handler),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidCredentialsError,
    handler=cast(ExceptionHandler, invalid_credentials_handler),
)

app.add_exception_handler(
    exc_class_or_status_code=InactiveUserError,
    handler=cast(ExceptionHandler, inactive_user_handler),
)

app.add_exception_handler(
    exc_class_or_status_code=RequestValidationError,
    handler=cast(ExceptionHandler, validation_error_handler),
)
