"""
Service module for handling user login and session initiation.
"""
from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from utilities.logger_middleware import get_logger
from utilities.password_validation import verify_password
from utilities.token_creation import (create_access_token,
                                      create_new_refresh_token,
                                      create_refresh_token)

from ...user.model import UserLoginSchema
from ...user.schema import User
from ..model import TokenSchema
from ..schema import RefreshToken

settings = get_settings()
logger = get_logger(__name__)


async def user_login_controller(
    user_login_details: UserLoginSchema, response: Response, db_session: AsyncSession
):
    """
    Handles the user login process.
    Verifies credentials, generates access and refresh tokens, and sets the refresh token in a cookie.
    """
    try:
        fetch_user_details_from_db_query = await db_session.execute(
            select(User).where(User.user_email == user_login_details.username)
        )
        fetch_user_details_from_db = (
            fetch_user_details_from_db_query.scalar_one_or_none()
        )

        if fetch_user_details_from_db is None:
            logger.error(
                "User with the current user credentials, username %s does not exists !!",
                user_login_details.username
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found !! Please Signup"
            )

        hashed_password = fetch_user_details_from_db.password
        login_user_password = user_login_details.password

        is_verified_user = verify_password(login_user_password, hashed_password)

        if is_verified_user is False:
            logger.error("Wrong username or password !!")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong Email or Password!!",
            )

        logger.info(
            f"User - {user_login_details.username} login successful, creating token"
        )
        token_details = {
            "user_id": str(fetch_user_details_from_db.user_id),
            "sub": user_login_details.username,
            "role": fetch_user_details_from_db.role,
        }

        access_token = create_access_token(token_details)
        refresh_token_payload = create_new_refresh_token()

        # Store the refresh token in the database
        refresh_token_data = RefreshToken(
            **refresh_token_payload,
            user_id=fetch_user_details_from_db.user_id,
            revoked=False,
        )

        db_session.add(refresh_token_data)
        await db_session.commit()
        await db_session.refresh(refresh_token_data)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token_data.token,
            httponly=True,
            samesite="strict",
            secure=True,
            max_age=settings.REFRESH_TOKEN_EXPIRE_TIME,
        )

        logger.info(
            f"Successfully generated token for user {user_login_details.username}"
        )
        return TokenSchema(
            access_token=access_token,
        )
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("Unexpected error during user login")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
