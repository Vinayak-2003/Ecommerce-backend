from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from ..model import UserUpdate, UserRoleUpdateAdmin, UserOut
from ..schema import User
from config import get_settings
from utilities.password_validation import get_hashed_password
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

settings = get_settings()

async def update_current_user(token: str, user_update_details: UserUpdate, db_session: AsyncSession):
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
        current_user_email = payload.get("sub")

        if current_user_email is None:
            logger.error("Wrong username or password")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong Credentials !! Missing Username"
            )
        
        current_user_details_query = await db_session.execute(select(User).filter(
            User.user_email == current_user_email))
        current_user_details = current_user_details_query.scalar_one_or_none()

        user_update_details_dict = user_update_details.model_dump(exclude_unset=True)

        logger.info("Fetched user details and started updating")
        for key, value in user_update_details_dict.items():
            if key == "password":
                new_hashed_password = get_hashed_password(value)
                setattr(current_user_details, "password", new_hashed_password)
            else:
                setattr(current_user_details, key, value)

        await db_session.commit()
        await db_session.refresh(current_user_details)

        logger.info(f"Successfully updated and saved user with {current_user_email} updated !!")
        return UserOut.model_validate(current_user_details)
    except Exception as e:
        logger.error("An error raised while updating the user details: ", e)
        await db_session.rollback()
        raise e
    

async def update_user_role_by_admin(email: str, user_role_update_details: UserRoleUpdateAdmin, db_session: AsyncSession):
    try:
        current_user_details_query = await db_session.execute(select(User).filter(
            User.user_email == email))
        current_user_details = current_user_details_query.scalar_one_or_none()

        logger.info("Started updating user role - access by admin ONLY !!")

        current_role = current_user_details.role
        updated_role = user_role_update_details.role
        logger.info(f"Fetched current role as {current_role} and new role as {updated_role} - access by admin ONLY !!")
        
        current_user_details.role = updated_role

        await db_session.commit()
        await db_session.refresh(current_user_details)
        user_out = UserOut.model_validate(current_user_details)

        logger.info(f"Successfully updated and saved user role - access by admin ONLY !!")
        return JSONResponse(
            content={
                "message": f"Role updated from {current_role} to {updated_role} for user {email}",
            }
        )
    except Exception as e:
        logger.error("An error raised while updating user role - access by admin ONLY !!: ", e)
        await db_session.rollback()
        raise e