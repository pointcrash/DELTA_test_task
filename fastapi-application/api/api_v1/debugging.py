import logging

from fastapi import HTTPException, status, APIRouter

from core.config import settings
from tasks.calculate_delivery_cost import calculate_delivery_cost

log = logging.getLogger(__name__)

router = APIRouter(prefix=settings.api.v1.debug, tags=["Debug"])


@router.post(
    "/calculate-delivery-cost",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=dict,
)
async def run_calculate_delivery_cost():
    """Run delivery cost calculation for debugging."""
    try:
        await calculate_delivery_cost()
        log.info("Delivery cost calculation completed")
        return {"message": "Delivery cost calculation completed"}

    except Exception:
        log.error(
            f"Failed to calculate delivery cost",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate delivery cost",
        )
