"""
Service module for removing items from the user's shopping cart.
"""
from fastapi import HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..schemas import CartItem

logger = get_logger(__name__)


async def delete_cart_current_user(cart_id: str, token: str, db_session: AsyncSession):
    """
    Removes a specific cart item for the authenticated user by its ID.
    """
    try:
        current_user_id = await get_current_user_id(token)
        cart_details_query = await db_session.execute(
            select(CartItem).where(
                CartItem.user_id == current_user_id, CartItem.cart_item_id == cart_id
            )
        )
        cart_details = cart_details_query.scalar_one_or_none()

        if cart_details is None:
            logger.warning(f"Cart item ID {cart_id} not found for user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        await db_session.delete(cart_details)
        await db_session.commit()

        logger.info(f"Successfully deleted cart item ID {cart_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("An error occurred while deleting cart details")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
