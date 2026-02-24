"""
Service module for updating quantities of items in the user's shopping cart.
"""
from fastapi import HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..models import CartItemUpdate
from ..schemas import CartItem

logger = get_logger(__name__)


async def update_cart_current_user(
    cart_id: str, updated_data: CartItemUpdate, token: str, db_session: AsyncSession
):
    """
    Updates the quantity of an existing cart item for the authenticated user.
    """
    try:
        current_user_id = await get_current_user_id(token)
        stored_data_query = await db_session.execute(
            select(CartItem).where(
                CartItem.user_id == current_user_id, CartItem.cart_item_id == cart_id
            )
        )
        stored_data = stored_data_query.scalar_one_or_none()

        if stored_data is None:
            logger.error(f"Cart item {cart_id} not found for user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Cart item not found"
            )

        update_quantity = updated_data.quantity
        new_quantity = stored_data.quantity + update_quantity

        if new_quantity < 0:
            logger.error(f"Invalid quantity update: results in {new_quantity}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Quantity cannot be less than 0"
            )

        if new_quantity == 0:
            logger.info(f"Cart item {cart_id} removed (quantity becomes 0)")
            await db_session.delete(stored_data)
            await db_session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        stored_data.quantity = new_quantity
        stored_data.total_quantity_amount = (
            stored_data.quantity * stored_data.product_amount
        )

        await db_session.commit()
        await db_session.refresh(stored_data)

        logger.info(f"Successfully updated quantity for cart item {cart_id}")
        return JSONResponse(
            content={"message": f"Quantity updated for cart ID {cart_id}"},
            status_code=status.HTTP_200_OK
        )
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("An error occurred while updating cart details")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
