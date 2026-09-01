from pydantic import BaseModel


class VersionResponse(BaseModel):
    """Application version response."""

    version: str
    environment: str
