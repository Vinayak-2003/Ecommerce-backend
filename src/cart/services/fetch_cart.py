from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger
from ..schemas import CartItem

logger = get_logger(__name__)

def fetch_cart_current_user(page_no: int, per_page: int, token: str, db_session: Session):
    try:
        current_user_id = get_current_user_id(token)
        total_current_user_cart = db_session.query(CartItem).filter(
            CartItem.user_id == current_user_id
        ).count()

        print("__________total_current_user_cart____________", total_current_user_cart)
        if total_current_user_cart is None:
            logger.info(f"Cart is empty for current user {current_user_id}")
            return {
                "cart_items": 0,
                "total_cart_items": total_current_user_cart,
                "total_pages": total_pages,
                "current_page": page_no,
                "per_page": per_page
            }

        current_user_cart_page = db_session.query(CartItem).offset((page_no-1)*per_page).limit(per_page).all()

        total_pages = (total_current_user_cart + per_page - 1) // per_page

        response = {
            "cart_items": current_user_cart_page,
            "total_cart_items": total_current_user_cart,
            "total_pages": total_pages,
            "current_page": page_no,
            "per_page": per_page
        }

        logger.info(f"Fetched paginated cart products for current user {current_user_id}")
        return response
    except Exception as e:
        logger.error(f"An error occurred while fetching cart details: {str(e)}")
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching cart details: {str(e)}"
        )