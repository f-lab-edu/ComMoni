from fastapi import APIRouter

from app.api.user.router import user_router
from app.api.commanage.router import commanage_router
from app.api.cominfo.router import cominfo_router
from app.api.auth.router import auth_router

from app.configs.config import settings

api_router = APIRouter(prefix=settings.API_PREFIX_ENDPOINT)

api_router.include_router(user_router, tags=["user"])
api_router.include_router(commanage_router, tags=["commanage"])
api_router.include_router(cominfo_router, tags=["cominfo"])
api_router.include_router(auth_router, tags=["auth"])
