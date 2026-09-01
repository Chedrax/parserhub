from fastapi import APIRouter, status

from parserhub.core.config import get_settings
from parserhub.core.version import get_app_version
from parserhub.schemas.version import VersionResponse

router = APIRouter(
    tags=["Operational"],
)


@router.get(
    path="/version",
    response_model=VersionResponse,
    status_code=status.HTTP_200_OK,
)
async def get_version() -> VersionResponse:
    """Return the application version and environment."""

    settings = get_settings()

    return VersionResponse(
        version=get_app_version(),
        environment=settings.environment,
    )
