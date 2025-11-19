from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..schema import Address
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def delete_current_user_address(address_id: str, token: str, db_session: Session):
    try:
        current_user_id = get_current_user_id(token)
        stored_address = db_session.query(Address).filter(
            Address.address_id == address_id,
            Address.user_id == current_user_id
        ).first()

        if not stored_address:
            logger.error(f"Address not found with {address_id} and {current_user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Address not found with {address_id} and {current_user_id}")
        
        logger.info(f"Address found with {address_id} and {current_user_id}")

        db_session.delete(stored_address)
        db_session.commit()
        logger.info(f"Address deleted with {address_id} successfully !!")
        return JSONResponse(content={
                                    "msg": f"Address deleted with {address_id} successfully !!"
                                },
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"An error occurred while deleting the address data: {str(e)}")
        db_session.rollback()
        raise e
    