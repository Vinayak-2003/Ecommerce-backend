from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from ..schema import Order
from ..model import OrderUpdate
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def update_user_order_status(update_status, token, db_session: Session):
    try:
        update_status_dict = update_status.model_dump()
        updated_status = update_status_dict["order_status"]

        fetched_order_details = db_session.query(Order).filter(
            Order.user_id == update_status.user_id,
            Order.order_id == update_status.order_id
        ).one_or_none()

        print(type(fetched_order_details), "_________________________", fetched_order_details)

        fetched_order_details.order_status = updated_status

        db_session.commit()
        db_session.refresh(fetched_order_details)

        logger.info(f"Status updated for order id {update_status.order_id} from {fetched_order_details.order_status} to {updated_status}")
        return JSONResponse(
            content={"msg": f"Status updated for order id {update_status.order_id} from {fetched_order_details.order_status} to {updated_status}"},
            status_code=status.HTTP_202_ACCEPTED
        )
    except Exception as e:
        logger.error(f"An error occurred while updating the order status: {str(e)}")
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    