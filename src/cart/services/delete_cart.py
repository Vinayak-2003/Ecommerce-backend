from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse

from ..schemas import CartItem
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def delete_cart_current_user(cart_id: str, token: str, db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)
        cart_details_query = await db_session.execute(select(CartItem).where(
            CartItem.user_id == current_user_id,
            CartItem.cart_item_id == cart_id
        ))
        cart_details = cart_details_query.scalar_one_or_none()

        await db_session.delete(cart_details)
        await db_session.commit()
        
        logger.info(f"Successfully deleted cart item id {cart_id}")
        return JSONResponse(
            content=f"Successfully deleted cart id {cart_id}"
        )
    except Exception as e:
        logger.error(f"An error occurred while deleting cart details: {str(e)}")
        await db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting cart details: {str(e)}"
        )