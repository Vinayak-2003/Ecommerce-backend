from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from ..schema import Order
from ...address.schema import Address
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def fetch_all_paginated_orders(token, page_no, per_page, db_session: Session):
    try:
        current_user_id = get_current_user_id(token)
        total_orders = db_session.query(Order).filter(Order.user_id == current_user_id).count()

        orders_for_page = db_session.query(Order).offset((page_no-1) * per_page).limit(per_page).all()

        total_pages = (total_orders + per_page - 1) // per_page

        response = {
            "orders": orders_for_page,
            "total_orders": total_orders,
            "page": page_no,
            "per page": per_page,
            "pages": total_pages
        }

        logger.info(f"Fetched paginated data for orders for page number {page_no}")
        return response
    except Exception as e:
        logger.error(f"An error raised while fetching orders: {str(e)}")
        db_session.rollback()
        raise e


def fetch_current_user_order_by_id(order_id, token, db_session: Session):
    try:
        current_user_id = get_current_user_id(token)

        order_details = db_session.query(Order).filter(
            Order.user_id == current_user_id,
            Order.order_id == order_id
        ).one_or_none()

        if order_details is None:
            logger.error("No order found")
            raise HTTPException(
                detail="No order found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        logger.info(f"Successfully fetched order of order id: {order_id}")
        return order_details
    except Exception as e:
        logger.error(f"An error occurred while fetching a order: {str(e)}")
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    