from fastapi import APIRouter

from parserhub.api.v1.endpoints.auth import router as auth_router
from parserhub.api.v1.endpoints.users import router as users_router

router = APIRouter(prefix="/v1")

router.include_router(router=auth_router)
router.include_router(router=users_router)
