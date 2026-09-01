from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard API error response based on RFC 9457."""

    type: str
    title: str
    status: int
    detail: str
    code: str
    errors: list[dict[str, Any]] | None = None
