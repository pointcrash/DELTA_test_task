from typing import List

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.package import PackageRead, PackageCreate, PackageId
from .crud import package as package_crud
from core.config import settings
from core.models import db_helper, Package
from .dependencies import get_or_set_session_id, get_package_by_id

router = APIRouter(prefix=settings.api.v1.packages, tags=["Package"])


@router.get("", response_model=List[PackageRead])
async def get_all_packages(
    session: AsyncSession = Depends(db_helper.session_getter),
    session_id: str = Depends(get_or_set_session_id),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    type_id: int | None = Query(None),
    has_delivery_cost: bool | None = Query(None),
):
    packages = await package_crud.get_all(
        session=session,
        session_id=session_id,
    )
    return packages


@router.post("", response_model=PackageId, status_code=status.HTTP_201_CREATED)
async def create_package(
    package_create: PackageCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    session_id: str = Depends(get_or_set_session_id),
):
    package = await package_crud.create_package(
        session=session,
        package_create=package_create,
        session_id=session_id,
    )
    return package


@router.get("/{package_id}", response_model=PackageRead)
async def get_package(
    package: Package = Depends(get_package_by_id),
):
    return package
