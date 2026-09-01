from fastapi import APIRouter

from parserhub.api.health import router as health_router
from parserhub.api.v1.router import router as v1_router
from parserhub.api.version import router as version_router

router = APIRouter()

router.include_router(router=health_router)
router.include_router(router=version_router)
router.include_router(
    router=v1_router,
    prefix="/api",
)
