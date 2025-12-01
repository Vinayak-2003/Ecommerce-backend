from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException

from ..schema import Order
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def delete_current_user_order(token, order_id, db_session: Session):
    try:
        current_user_id = get_current_user_id(token)

        order_details_id = db_session.query(Order).filter(
            Order.user_id == current_user_id,
            Order.order_id == order_id
        ).one_or_none()

        order_details_id.order_status = "CANCELLED"

        db_session.commit()
        db_session.refresh(order_details_id)
        logger.info(f"Successfully canceled order of order id: {order_id}")
        return JSONResponse(
            content={"msg": f"Successfully canceled order of order id: {order_id}"},
            status_code=status.HTTP_202_ACCEPTED
        )
    except Exception as e:
        logger.error(f"An error occurred while cancelling the order id {str(e)}")
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
        
    