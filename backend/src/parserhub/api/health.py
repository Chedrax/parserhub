from fastapi import APIRouter, status

from parserhub.schemas.health import HealthResponse

router = APIRouter(
    tags=["Operational"],
)


@router.get(
    path="/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
async def health_check() -> HealthResponse:
    """Return the health status of the application."""

    return HealthResponse(status="ok")
