from decimal import Decimal
from sqlalchemy import update

from core.models import db_helper, Package
from utils import get_usd_to_rub_rate

WEIGHT_FACTOR = "0.5"
CONTENT_FACTOR = "0.01"


async def calculate_delivery_cost():
    async with db_helper.session_factory() as session:
        usd_rate = await get_usd_to_rub_rate()

        stmt = (
            update(Package)
            .where(Package.delivery_cost.is_(None))
            .values(
                delivery_cost=(
                    Package.weight * Decimal(WEIGHT_FACTOR)
                    + Package.content_cost * Decimal(CONTENT_FACTOR)
                )
                * usd_rate,
            )
        )

        await session.execute(stmt)
        await session.commit()
