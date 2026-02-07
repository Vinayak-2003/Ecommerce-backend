from fastapi import HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...user.model import UserLoginSchema
from ...user.schema import User
from ..model import TokenSchema
from ..schema import RefreshToken
from utilities.password_validation import verify_password
from utilities.token_creation import create_access_token, create_refresh_token, create_new_refresh_token
from utilities.logger_middleware import get_logger
from config import get_settings

settings = get_settings()
logger = get_logger(__name__)

async def user_login_controller(user_login_details: UserLoginSchema, response: Response, db_session: AsyncSession):
    try:
        fetch_user_details_from_db_query = await db_session.execute(select(User).where(
            User.user_email == user_login_details.username))
        fetch_user_details_from_db = fetch_user_details_from_db_query.scalar_one_or_none()

        if fetch_user_details_from_db is None:
            logger.error(f"User with the current user credentials, username {user_login_details.username} does not exists !!")
            raise HTTPException(
                detail="User not found !! Please Signup"
            )
        
        hashed_password = fetch_user_details_from_db.password
        login_user_password = user_login_details.password

        is_verified_user = verify_password(login_user_password, hashed_password)

        if is_verified_user is False:
            logger.error(f"Wrong username or password !!")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Wrong Email or Password!!"
            )
        
        logger.info(f"User - {user_login_details.username} login successful, creating token")
        token_details = {
            "user_id": str(fetch_user_details_from_db.user_id),
            "sub": user_login_details.username,
            "role": fetch_user_details_from_db.role
        }

        access_token = create_access_token(token_details)
        refresh_token_payload = create_new_refresh_token()

        # Store the refresh token in the database
        refresh_token_data = RefreshToken(
            **refresh_token_payload,
            user_id = fetch_user_details_from_db.user_id,
            revoked = False
        )

        db_session.add(refresh_token_data)
        await db_session.commit()
        await db_session.refresh(refresh_token_data)

        response.set_cookie(key="refresh_token",
                            value=refresh_token_data.token,
                            httponly=True,
                            samesite="strict",
                            secure=True,
                            max_age=settings.REFRESH_TOKEN_EXPIRE_TIME
                            )

        logger.info(f"Successfully generated token for user {user_login_details.username}")
        return TokenSchema(
            access_token=access_token,
        )
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception as e:
        logger.exception("Unexpected error during user login")
        await db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
