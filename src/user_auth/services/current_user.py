from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from config import get_settings
from ..schema import User
from ..model import UserOut
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

settings = get_settings()

async def fetch_current_user(token: str, db_session: AsyncSession):
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
        current_user_email = payload.get("sub")

        if current_user_email is None:
            logger.error(f"An error occurred while fetching the current user, may be due to wrong credentials or missing username")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong Credentials !! Missing Username"
            )
        
        user_details_query = await db_session.execute(select(User).where(User.user_email == current_user_email))
        user_details = user_details_query.scalar_one_or_none()
        
        logger.info(f"Successfully fetched the active user details")
        return UserOut.model_validate(user_details)
    except Exception as e:
        raise e
    
async def get_current_user_id(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
        current_user_id = payload.get("user_id")
        logger.info(f"Current User ID fetched for processing")
        return current_user_id
    except Exception as e:
        logger.error(f"An error occurred while fetching current user id: {str(e)}")
        raise e