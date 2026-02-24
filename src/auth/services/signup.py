"""
Service module for user registration and signup operations.
"""
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger
from utilities.password_validation import get_hashed_password

from ...user.model import UserCreate, UserOut
from ...user.schema import User

logger = get_logger(__name__)


async def create_user_signup(new_user_data: UserCreate, db_session: AsyncSession):
    """
    Handles new user registration.
    Checks for existing email, hashes the password, and saves the new user to the database.
    """
    try:
        user_dict = new_user_data.model_dump()
        user_email = user_dict.get("user_email")
        is_user_present_query = await db_session.execute(
            select(User).where(User.user_email == user_email)
        )

        if is_user_present_query.scalar_one_or_none():
            logger.warning(f"User with email ID - {user_email} already exists!!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email ID - {user_email} already exists!!",
            )

        user_password = user_dict.get("password")
        user_hashed_password = get_hashed_password(user_password)
        user_dict["password"] = user_hashed_password
        hashed_user_data = User(**user_dict)

        db_session.add(hashed_user_data)
        await db_session.commit()
        await db_session.refresh(hashed_user_data)

        logger.info(f"Successfully created a new user with email {user_email}")
        return UserOut.model_validate(hashed_user_data)
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        await db_session.rollback()
        logger.exception("An error occurred during signup")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
