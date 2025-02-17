from fastapi import APIRouter

from src.core.config import settings

from .client_parking_router import router as client_parking_router
from .client_router import router as client_router
from .parkins_router import router as parkins_router

router = APIRouter(
    prefix=settings.api_vi_prefix,
)

router.include_router(
    router=client_router,
)
router.include_router(
    router=parkins_router,
)
router.include_router(
    router=client_parking_router,
)
