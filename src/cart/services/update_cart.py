from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger
from ..schemas import CartItem
from ..models import CartItemUpdate

logger = get_logger(__name__)

def update_cart_current_user(cart_id: str, updated_data: CartItemUpdate, 
                             token: str, db_session: Session):
    try:
        current_user_id = get_current_user_id(token)
        stored_data = db_session.query(CartItem).filter(
            CartItem.user_id == current_user_id,
            CartItem.cart_item_id == cart_id
        ).one_or_none()

        if stored_data is None:
            logger.error("cart item not found !!")
            raise HTTPException(
                status_code=404,
                detail="Cart item not found"
            )

        update_quantity = updated_data.quantity
        new_quantity = stored_data.quantity + update_quantity

        if new_quantity < 0:
            logger.error(f"Quantity cannot be less than 0")
            raise HTTPException(
                status_code=400,
                detail="Quantity cannot be less than 0"
            )
        
        if new_quantity == 0:
            logger.info(f"Cart item {cart_id} removed (quantity becomes 0)")
            db_session.delete(stored_data)
            db_session.commit()
            return JSONResponse(
                content=f"Cart item {cart_id} removed (quantity becomes 0)"
            )
        
        stored_data.quantity = new_quantity
        stored_data.total_quantity_amount = stored_data.quantity * stored_data.product_amount

        db_session.commit()
        db_session.refresh(stored_data)
        
        logger.info(f"Successfully updated product quantity in the cart !!")
        return JSONResponse(
            content=f"Quantity updated for cart id {cart_id}"
        )
    except Exception as e:
        logger.error(f"An error occurred while updating cart details: {str(e)}")
        db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating cart details: {str(e)}"
        )