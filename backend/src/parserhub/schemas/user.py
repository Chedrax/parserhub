from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from parserhub.models.enums import UserRole


class UserResponse(BaseModel):
    """Public user representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime
