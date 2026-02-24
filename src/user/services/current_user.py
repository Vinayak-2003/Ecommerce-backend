"""
Service module for fetching and validating the currently authenticated user.
"""
from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from utilities.logger_middleware import get_logger

from ..model import UserOut
from ..schema import User

logger = get_logger(__name__)

settings = get_settings()


async def fetch_current_user(token: str, db_session: AsyncSession):
    """
    Retrieves the currently authenticated user's details from the database using the JWT token.
    """
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
        current_user_email = payload.get("sub")

        if current_user_email is None:
            logger.error(
                "An error occurred while fetching the current user: missing username"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong Credentials !! Missing Username",
            )

        user_details_query = await db_session.execute(
            select(User).where(User.user_email == current_user_email)
        )
        user_details = user_details_query.scalar_one_or_none()

        logger.info("Successfully fetched the active user details")
        return UserOut.model_validate(user_details)
    except JWTError as exc:
        logger.error(f"Could not validate credentials while fetching current user: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error while fetching current user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


async def get_current_user_id(token: str):
    """
    Extracts the user ID from the provided JWT token.
    """
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
        current_user_id = payload.get("user_id")
        logger.info("Current User ID fetched for processing")
        return current_user_id
    except JWTError as exc:
        logger.error(f"Could not validate credentials: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except Exception:
        logger.exception("Unexpected error while extracting user ID from token")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
