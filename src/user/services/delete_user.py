"""
Service module for deleting users from the database.
"""
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..schema import User

logger = get_logger(__name__)


async def delete_user_by_email(email: str, db_session: AsyncSession):
    """
    Deletes a user from the database based on their email address.
    """
    try:
        stored_user_query = await db_session.execute(
            select(User).where(User.user_email == email)
        )
        stored_user = stored_user_query.scalar_one_or_none()

        if not stored_user:
            logger.error(f"User with the email - {email} does not exist !!")
            return JSONResponse(
                content={"message": f"User with {email} does not exist !!"}, 
                status_code=status.HTTP_404_NOT_FOUND
            )

        await db_session.delete(stored_user)
        await db_session.commit()

        logger.info(f"Successfully deleted the user with the email id - {email}")
        return JSONResponse(
            content={"message": f"User with email {email} deleted successfully!!"},
            status_code=status.HTTP_200_OK
        )
    except Exception:
        await db_session.rollback()
        logger.exception("An error occurred while deleting the user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
