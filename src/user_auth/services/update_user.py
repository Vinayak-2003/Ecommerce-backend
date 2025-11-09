from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from jose import jwt
from ..model import UserUpdate, UserRoleUpdateAdmin, UserOut
from ..schema import User
from config import get_settings
from utilities.password_validation import get_hashed_password
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

settings = get_settings()

def update_current_user(token: str, user_update_details: UserUpdate, db_session: Session):
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
        current_user_email = payload.get("sub")

        if current_user_email is None:
            logger.error("Wrong username or password")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong Credentials !! Missing Username"
            )
        
        current_user_details = db_session.query(User).filter(User.user_email == current_user_email).first()
        user_update_details_dict = user_update_details.model_dump(exclude_unset=True)

        logger.info("Fetched user details and started updating")
        for key, value in user_update_details_dict.items():
            if key == "password":
                new_hashed_password = get_hashed_password(value)
                setattr(current_user_details, "password", new_hashed_password)
            else:
                setattr(current_user_details, key, value)

        db_session.commit()
        db_session.refresh(current_user_details)

        logger.info(f"Successfully updated and saved user with {current_user_email} updated !!")
        return UserOut.model_validate(current_user_details)
    except Exception as e:
        logger.error("An error raised while updating the user details: ", e)
        db_session.rollback()
        raise e
    

def update_user_role_by_admin(email: str, user_role_update_details: UserRoleUpdateAdmin, db_session: Session):
    try:
        current_user_details = db_session.query(User).filter(User.user_email == email).first()
        logger.info("Started updating user role - access by admin ONLY !!")

        current_role = current_user_details.role
        updated_role = user_role_update_details.role
        logger.info(f"Fetched current role as {current_role} and new role as {updated_role} - access by admin ONLY !!")
        
        current_user_details.role = updated_role

        db_session.commit()
        db_session.refresh(current_user_details)
        user_out = UserOut.model_validate(current_user_details)

        logger.info(f"Successfully updated and saved user role - access by admin ONLY !!")
        return JSONResponse(
            content={
                "message": f"Role updated from {current_role} to {updated_role} for user {email}",
            }
        )
    except Exception as e:
        logger.error("An error raised while updating user role - access by admin ONLY !!: ", e)
        db_session.rollback()
        raise e