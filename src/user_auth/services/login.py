from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..model import UserLoginSchema, TokenSchema, UserOut
from ..schema import User
from utilities.password_validation import verify_password
from utilities.token_creation import create_access_token, create_refresh_token

def user_login_controller(user_login_details: UserLoginSchema, db_session: Session):
    try:
        print(user_login_details.__dict__, "______________", type(user_login_details))
        # user_login_dict = user_login_details.

        fetch_user_details_from_db = db_session.query(User).filter(User.user_email == user_login_details.username).first()
        if fetch_user_details_from_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found !! Please Signup"
            )
        
        hashed_password = fetch_user_details_from_db.password
        login_user_password = user_login_details.password

        is_verified_user = verify_password(login_user_password, hashed_password)

        if is_verified_user is False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong Email or Password!!"
            )
        
        token_details = {
            "sub": user_login_details.username,
            "role": fetch_user_details_from_db.role
        }

        access_token = create_access_token(token_details)
        refresh_token = create_refresh_token(token_details)

        return TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except Exception as e:
        raise e