from fastapi import APIRouter

from parserhub.api.v1.endpoints import auth, users

router = APIRouter(prefix="/api/v1")

router.include_router(router=auth.router)
router.include_router(router=users.router)
