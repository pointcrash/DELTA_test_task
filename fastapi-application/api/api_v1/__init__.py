from fastapi import APIRouter

from core.config import settings

from .package_type import router as package_type_router
from .package import router as package_router
from .debugging import router as debug_router


router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(package_router)
router.include_router(package_type_router)
router.include_router(debug_router)
