from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from config import get_settings
from ..schema import User
from ..model import UserOut

settings = get_settings()

def fetch_current_user(token: str, db_session: Session):
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
        current_user_email = payload.get("sub")

        if current_user_email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong Credentials !! Missing Username"
            )
        
        user_details = db_session.query(User).filter(User.user_email == current_user_email).first()
        return UserOut.model_validate(user_details)
    except Exception as e:
        raise e