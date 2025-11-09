from sqlalchemy.orm import Session
from ..model import UserOut
from ..schema import User
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def get_user_by_email_controller(email: str, db_session: Session):
    try:
        user_details = db_session.query(User).filter(User.user_email == email).first()
        logger.info(f"Successfully fetched the user with email id - {email}")
        return UserOut.model_validate(user_details)
    except Exception as e:
        db_session.rollback()
        logger.error("An error raised while fetching the user", e)
        raise e