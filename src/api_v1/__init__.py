from fastapi import APIRouter


from .routers import router as router_api_v1
from ..core.config import settings

router = APIRouter(
    prefix=settings.api_vi_prefix,
)

router.include_router(router_api_v1)
