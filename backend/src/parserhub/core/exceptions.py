class ParserHubError(Exception):
    """Base exception for application-level errors."""


class UserAlreadyExistsError(ParserHubError):
    """Raised when a user with the given credentials already exists."""


class InvalidCredentialsError(ParserHubError):
    """Raised when authentication credentials are invalid."""


class InactiveUserError(ParserHubError):
    """Raised when an inactive user attempts to authenticate."""


class AuthenticationError(ParserHubError):
    """Raised when authentication credentials are invalid."""
