"""
Service module for updating order statuses, typically for administrative use.
"""
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..model import OrderUpdate
from ..schema import Order

logger = get_logger(__name__)


async def update_user_order_status(update_status: OrderUpdate, token: str, db_session: AsyncSession):
    """
    Updates the status of an order. Typically used by administrators.
    """
    try:
        updated_status = update_status.order_status

        fetched_order_query = await db_session.execute(
            select(Order).where(
                Order.user_id == update_status.user_id,
                Order.order_id == update_status.order_id,
            )
        )
        fetched_order = fetched_order_query.scalar_one_or_none()

        if fetched_order is None:
            logger.warning(f"Order ID {update_status.order_id} not found for user {update_status.user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        old_status = fetched_order.order_status
        fetched_order.order_status = updated_status

        await db_session.commit()
        await db_session.refresh(fetched_order)

        msg = f"Status updated for order {update_status.order_id} from {old_status} to {updated_status}"
        logger.info(msg)
        return JSONResponse(
            content={"message": msg},
            status_code=status.HTTP_200_OK,
        )
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("An error occurred while updating order status")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
