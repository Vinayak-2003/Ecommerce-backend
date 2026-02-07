from fastapi import HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from utilities.logger_middleware import get_logger
from ..schema import RefreshToken

logger = get_logger(__name__)

async def user_logout_controller(request: Request, response: Response, db_session: AsyncSession):
    try:
        refresh_token = request.cookies.get("refresh_token")

        if refresh_token is None:
            logger.error(f"Refresh token not found in cookies")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token not found in cookies"
            )
        
        # check if the provided refresh token exists in the database
        check_refresh_token_query = await db_session.execute(select(RefreshToken).filter(
            RefreshToken.token == refresh_token
        ))
        refresh_token_details_from_db = check_refresh_token_query.scalar_one_or_none()

        if refresh_token_details_from_db is None:
            logger.error(f"Invalid refresh token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid refresh token"
            )
        
        # revoke the refresh token in the database
        refresh_token_details_from_db.revoked = True
        await db_session.commit()

        # remove the refresh token cookie from the client
        response.delete_cookie(key="refresh_token",
                               httponly=True,
                               samesite="strict",
                                secure=True
                            )

        return {"detail": "Logout successful"}
    except HTTPException:
        raise
