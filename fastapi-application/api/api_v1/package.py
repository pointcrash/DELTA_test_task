from typing import List

from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.package import PackageRead, PackageCreate, PackageId, PackageAssign
from .crud import package as package_crud
from core.config import settings
from core.models import db_helper, Package
from .crud.package import assign_package_to_company
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

    try:
        packages = await package_crud.get_all(
            session=session,
            session_id=session_id,
            page=page,
            page_size=page_size,
            type_id=type_id,
            has_delivery_cost=has_delivery_cost,
        )
        return packages

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post("", response_model=PackageId, status_code=status.HTTP_201_CREATED)
async def create_package(
    package_create: PackageCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    session_id: str = Depends(get_or_set_session_id),
):
    try:
        package = await package_crud.create_package(
            session=session,
            package_create=package_create,
            session_id=session_id,
        )
        return package

    except IntegrityError as e:
        await session.rollback()
        if "foreign key" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail=f"Invalid type_id: {package_create.type_id} does not exist",
            )
        raise HTTPException(
            status_code=500, detail=f"Database integrity error: {str(e)}"
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {str(e)}"
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/{package_id}", response_model=PackageRead)
async def get_package(
    package: Package = Depends(get_package_by_id),
):
    return package


@router.post("/{package_id}/assign", response_model=dict)
async def assign_package(
    package_id: int,
    assign_data: PackageAssign,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    company_id = assign_data.delivery_service_id

    if company_id <= 0:
        raise HTTPException(
            status_code=400, detail="Transport company ID must be positive"
        )

    success = await assign_package_to_company(
        package_id,
        company_id,
        session,
    )

    if success:
        return {"message": f"Package {package_id} assigned to company {company_id}"}
    else:
        raise HTTPException(
            status_code=409, detail="Package already assigned or does not exist"
        )
