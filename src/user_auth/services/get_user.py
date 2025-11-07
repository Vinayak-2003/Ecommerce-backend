from sqlalchemy.orm import Session
from ..model import UserOut
from ..schema import User

def get_user_by_email_controller(email: str, db_session: Session):
    try:
        user_details = db_session.query(User).filter(User.user_email == email).first()
        return UserOut.model_validate(user_details)
    except Exception as e:
        raise e