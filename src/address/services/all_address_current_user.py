from sqlalchemy.orm import Session
from ..schema import Address

from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def all_current_user_addresses(token: str, db: Session):
    try:
        current_user_id = get_current_user_id(token)
        address_list = db.query(Address).filter(Address.user_id == current_user_id).all()
        logger.info(f"All address for the current user {current_user_id} is fetched successfully !!")
        return address_list
    except Exception as e:
        logger.error("An error raised while fetching a addresses: ", e)
        db.rollback()
        raise e
