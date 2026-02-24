"""
Service module for retrieving user details by email.
"""
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..model import UserOut
from ..schema import User

logger = get_logger(__name__)


async def get_user_by_email_controller(email: str, db_session: AsyncSession):
    """
    Retrieves a user's details from the database based on their email address.
    """
    try:
        user_details_query = await db_session.execute(
            select(User).filter(User.user_email == email)
        )
        user_details = user_details_query.scalar_one_or_none()

        if user_details is None:
            logger.warning(f"User with email {email} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {email} not found"
            )

        logger.info(f"Successfully fetched the user with email id - {email}")
        return UserOut.model_validate(user_details)
    except HTTPException:
        raise
    except Exception:
        logger.exception("An error occurred while fetching the user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
