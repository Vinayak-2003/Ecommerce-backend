from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..model import AddressUpdate
from ..schema import Address
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def update_current_user_address(address_id: str, update_address: AddressUpdate,
                                token: str, db_session: Session):
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

        update_address_dict = update_address.model_dump(exclude_unset=True)

        for key, value in update_address_dict.items():
            setattr(stored_address, key, value)

        db_session.commit()
        db_session.refresh(stored_address)
        logger.info(f"Address is updated and stored in the database")
        return stored_address
    except Exception as e:
        logger.error(f"An error occurred while updating the address data: {str(e)}")
        db_session.rollback()
        raise e
    