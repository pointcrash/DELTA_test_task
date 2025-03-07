from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.dependencies import get_or_set_session_id
from core.models import db_helper, Package
from api.api_v1.crud import package as package_crud


async def get_package_by_id(
    package_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
    session_id: str = Depends(get_or_set_session_id),
) -> Package:
    """Dependency for getting package by id"""
    package = await package_crud.get_package_by_id(
        session=session,
        package_id=package_id,
        session_id=session_id,
    )

    if package is not None:
        return package

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
    )
