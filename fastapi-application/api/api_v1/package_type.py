from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from core.schemas.package_type import PackageTypeRead
from .crud import package_type as package_type_crud
from typing import List
from fastapi import APIRouter, Depends

router = APIRouter(prefix=settings.api.v1.package_types, tags=["PackageType"])


@router.get("", response_model=List[PackageTypeRead])
async def get_package_types(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await package_type_crud.get_all(session)
