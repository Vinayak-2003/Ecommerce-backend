from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from ..schemas import CartItem
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def delete_cart_current_user(cart_id: str, token: str, db_session: Session):
    try:
        current_user_id = get_current_user_id(token)
        cart_details = db_session.query(CartItem).filter(
            CartItem.user_id == current_user_id,
            CartItem.cart_item_id == cart_id
        ).one_or_none()

        db_session.delete(cart_details)
        db_session.commit()
        
        logger.info(f"Successfully deleted cart item id {cart_id}")
        return JSONResponse(
            content=f"Successfully deleted cart id {cart_id}"
        )
    except Exception as e:
        logger.error(f"An error occurred while deleting cart details: {str(e)}")
        db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting cart details: {str(e)}"
        )