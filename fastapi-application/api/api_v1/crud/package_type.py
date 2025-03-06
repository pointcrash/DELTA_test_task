from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import PackageType


async def get_all(
    session: AsyncSession,
) -> Sequence[PackageType]:
    stmt = select(PackageType).order_by(PackageType.id)
    result = await session.scalars(stmt)
    return result.all()
