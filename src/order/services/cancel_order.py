from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException

from ..schema import Order
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def delete_current_user_order(token, order_id, db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)

        order_details_id_query = await db_session.execute(select(Order).where(
            Order.user_id == current_user_id,
            Order.order_id == order_id
        ))
        order_details_id = order_details_id_query.scalar_one_or_none()

        order_details_id.order_status = "CANCELLED"

        await db_session.commit()
        await db_session.refresh(order_details_id)
        logger.info(f"Successfully canceled order of order id: {order_id}")
        return JSONResponse(
            content={"msg": f"Successfully canceled order of order id: {order_id}"},
            status_code=status.HTTP_202_ACCEPTED
        )
    except Exception as e:
        logger.error(f"An error occurred while cancelling the order id {str(e)}")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
        
    