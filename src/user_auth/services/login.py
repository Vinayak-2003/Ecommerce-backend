from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..model import UserLoginSchema, TokenSchema, UserOut
from ..schema import User
from utilities.password_validation import verify_password
from utilities.token_creation import create_access_token, create_refresh_token
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def user_login_controller(user_login_details: UserLoginSchema, db_session: Session):
    try:
        fetch_user_details_from_db = db_session.query(User).filter(User.user_email == user_login_details.username).first()
        if fetch_user_details_from_db is None:
            logger.error(f"User with the current user credentials, username {user_login_details.username} does not exists !!")
            raise HTTPException(
                detail="User not found !! Please Signup"
            )
        
        hashed_password = fetch_user_details_from_db.password
        login_user_password = user_login_details.password

        is_verified_user = verify_password(login_user_password, hashed_password)

        if is_verified_user is False:
            logger.error(f"Wrong username or password !!")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong Email or Password!!"
            )
        
        logger.info(f"User - {user_login_details.username} login successful, creating token")
        token_details = {
            "user_id": str(fetch_user_details_from_db.user_id),
            "sub": user_login_details.username,
            "role": fetch_user_details_from_db.role
        }

        access_token = create_access_token(token_details)
        refresh_token = create_refresh_token(token_details)

        logger.info(f"Successfully generated token for user {user_login_details.username}")
        return TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except Exception as e:
        logger.error("An error raised while user login: ", e)
        db_session.rollback()
        raise e