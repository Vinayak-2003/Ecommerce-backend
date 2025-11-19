from sqlalchemy.orm import Session
from ..model import AddressCreate, AddressOut
from ..schema import Address
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def create_current_user_address(new_address: AddressCreate,
                                token: str,
                                db_session: Session):
    try:
        current_user_id = get_current_user_id(token)
        new_address = Address(
            user_id = current_user_id,
            **new_address.model_dump()
        )
        print(type(new_address), "_______________", new_address)
        db_session.add(new_address)
        db_session.commit()
        db_session.refresh(new_address)
        logger.info(f"An address is created for {current_user_id}")
        return new_address
    except Exception as e:
        logger.error(f"An error occurred while creating a new address for {current_user_id}: {str(e)}")
        db_session.rollback()
        raise e