"""
Service module for updating user profiles and roles.
"""
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from utilities.logger_middleware import get_logger
from utilities.password_validation import get_hashed_password

from ..model import UserOut, UserRoleUpdateAdmin, UserUpdate
from ..schema import User

logger = get_logger(__name__)

settings = get_settings()


async def update_current_user(
    token: str, user_update_details: UserUpdate, db_session: AsyncSession
):
    """
    Updates the profile details of the currently authenticated user.
    """
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, settings.ALGORITHM)
        current_user_email = payload.get("sub")

        if current_user_email is None:
            logger.error("Missing username in token payload")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong Credentials !! Missing Username",
            )

        current_user_details_query = await db_session.execute(
            select(User).filter(User.user_email == current_user_email)
        )
        current_user_details = current_user_details_query.scalar_one_or_none()

        if current_user_details is None:
            logger.error(f"User {current_user_email} not found during update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

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

        logger.info(f"Successfully updated user {current_user_email}")
        return UserOut.model_validate(current_user_details)
    except JWTError as exc:
        logger.error(f"Could not validate credentials: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("An error occurred while updating the user details")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def update_user_role_by_admin(
    email: str, user_role_update_details: UserRoleUpdateAdmin, db_session: AsyncSession
):
    """
    Updates a user's role in the database. Restricted to administrators.
    """
    try:
        current_user_details_query = await db_session.execute(
            select(User).filter(User.user_email == email)
        )
        current_user_details = current_user_details_query.scalar_one_or_none()

        if current_user_details is None:
            logger.warning(f"User with email {email} not found for role update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {email} not found"
            )

        logger.info("Started updating user role - access by admin ONLY !!")

        current_role = current_user_details.role
        updated_role = user_role_update_details.role
        logger.info(
            f"Changing role for {email} from {current_role} to {updated_role}"
        )

        current_user_details.role = updated_role

        await db_session.commit()
        await db_session.refresh(current_user_details)

        logger.info(f"Successfully updated role for user {email}")
        return JSONResponse(
            content={
                "message": f"Role updated from {current_role} to {updated_role} for user {email}",
            },
            status_code=status.HTTP_200_OK
        )
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("An error occurred while updating user role by admin")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
