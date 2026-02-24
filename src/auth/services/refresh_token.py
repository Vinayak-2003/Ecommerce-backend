"""
Service module for rotating refresh tokens and issuing new access tokens.
"""
from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from utilities.logger_middleware import get_logger
from utilities.token_creation import (create_access_token,
                                      create_new_refresh_token)

from ...user.schema import User
from ..model import RefreshRequest, TokenSchema
from ..schema import RefreshToken

logger = get_logger(__name__)
settings = get_settings()


async def create_refresh_access_token(
    request: Request, response: Response, db_session: AsyncSession
):
    """
    Creates a new access token using a valid refresh token from the request cookies.
    Also rotates the refresh token by revoking the old one and issuing a new one.
    """
    try:
        async with db_session.begin():
            refresh_token = request.cookies.get("refresh_token")

            # check if the provided refresh token exists in the database
            check_refresh_token_query = await db_session.execute(
                select(RefreshToken).filter(RefreshToken.token == refresh_token)
            )
            refresh_token_details_from_db = (
                check_refresh_token_query.scalar_one_or_none()
            )

            if refresh_token_details_from_db is None:
                logger.error("This is an invalid refresh token")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            # check if token is a valid refresh token and not expired
            current_datetime = datetime.utcnow()
            if refresh_token_details_from_db.expires_at < current_datetime:
                logger.error("The refresh token has expired")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token has expired, please login again",
                )

            if refresh_token_details_from_db.revoked:
                logger.error("The refresh token has been revoked")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token has been revoked, please login again",
                )

            # if the refresh token is valid, revoke the current refresh token and create a new one
            refresh_token_details_from_db.revoked = True

            # if the refresh token is valid, create a new access token
            user_details_query = await db_session.execute(
                select(User).filter(
                    User.user_id == refresh_token_details_from_db.user_id
                )
            )
            user_details = user_details_query.scalar_one_or_none()

            if user_details is None:
                logger.error("User associated with the refresh token does not exist")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User associated with the refresh token does not exist",
                )

            payload = {
                "user_id": str(user_details.user_id),
                "sub": user_details.user_email,
                "role": user_details.role,
            }
            access_token = create_access_token(subject=payload)
            refresh_token_payload = create_new_refresh_token()

            # Store the refresh token in the database
            refresh_token_data = RefreshToken(
                **refresh_token_payload, user_id=user_details.user_id, revoked=False
            )

            db_session.add(refresh_token_data)

            response.set_cookie(
                key="refresh_token",
                value=refresh_token_data.token,
                httponly=True,
                samesite="strict",
                secure=True,
                max_age=settings.REFRESH_TOKEN_EXPIRE_TIME,
            )

            return TokenSchema(
                access_token=access_token,
            )
    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error during refresh token rotation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
