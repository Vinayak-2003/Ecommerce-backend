from sqlalchemy.orm import Session
from ..schema import User
from fastapi.responses import JSONResponse
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def delete_user_by_email(email: str, db_session: Session):
    try:
        stored_user = db_session.query(User).get(email)

        if not stored_user:
            logger.error(f"User with the email - {email} does not exists !!")
            return JSONResponse(
                content=f"User with {email} does not exists !!",
                status_code=404
            )
        
        db_session.delete(stored_user)
        db_session.commit()
        db_session.refresh()

        logger.info(f"Successfully deleted the user with the email id - {email}")
        return JSONResponse(
            content=f"User with email {email} deleted successsfully!!",
        )
    except Exception as e:
        db_session.rollback()
        logger.error("An error raised while deleting the user", e)
        raise e
    