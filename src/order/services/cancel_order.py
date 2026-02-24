"""
Service module for cancelling orders for the authenticated user.
"""
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..schema import Order

logger = get_logger(__name__)


async def delete_current_user_order(token: str, order_id: str, db_session: AsyncSession):
    """
    Cancels a specific order for the authenticated user by setting its status to 'CANCELLED'.
    """
    try:
        current_user_id = await get_current_user_id(token)

        order_details_query = await db_session.execute(
            select(Order).where(
                Order.user_id == current_user_id, Order.order_id == order_id
            )
        )
        order_details = order_details_query.scalar_one_or_none()

        if order_details is None:
            logger.warning(f"Order ID {order_id} not found for user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=" Order not found !!"
            )

        order_details.order_status = "CANCELLED"

        await db_session.commit()
        await db_session.refresh(order_details)
        logger.info(f"Successfully cancelled order {order_id}")
        return JSONResponse(
            content={"message": f"Successfully cancelled order ID {order_id}"},
            status_code=status.HTTP_200_OK,
        )
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("An error occurred while cancelling the order")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
