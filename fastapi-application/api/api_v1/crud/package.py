from decimal import Decimal
from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Package
from core.schemas.package import PackageCreate


async def get_all(
    session: AsyncSession,
    session_id: str,
    page: int,
    page_size: int,
    type_id: int | None,
    has_delivery_cost: bool | None,
) -> Sequence[Package]:
    stmt = (
        select(Package)
        .where(Package.session_id == session_id)
        .options(joinedload(Package.type))
    )

    if type_id is not None:
        stmt = stmt.where(Package.type_id == type_id)

    if has_delivery_cost is not None:
        if has_delivery_cost:
            stmt = stmt.where(Package.delivery_cost > Decimal("0"))
        else:
            stmt = stmt.where(Package.delivery_cost.is_(None))

    stmt = stmt.limit(page_size).offset((page - 1) * page_size)

    result = await session.scalars(stmt)
    return result.all()


async def get_package_by_id(
    session: AsyncSession,
    package_id: int,
    session_id: str,
) -> Package | None:
    stmt = (
        select(Package)
        .where(
            and_(
                Package.id == package_id,
                Package.session_id == session_id,
            )
        )
        .options(joinedload(Package.type))
    )
    return await session.scalar(stmt)


async def create_package(
    package_create: PackageCreate,
    session: AsyncSession,
    session_id: str,
) -> Package:
    package = Package(
        **package_create.model_dump(),
        session_id=session_id,
    )
    session.add(package)
    try:
        await session.commit()
        return package
    except IntegrityError:
        await session.rollback()
        raise
