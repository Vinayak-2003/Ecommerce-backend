from fastapi import HTTPException, status
from ..model import UserCreate, UserOut
from ..schema import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utilities.password_validation import get_hashed_password
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def create_user_signup(new_user_data: UserCreate, db_session: AsyncSession):
    try:
        user_dict = new_user_data.model_dump()
        user_email = user_dict.get("user_email")
        is_user_present_query = await db_session.execute(select(User).where(User.user_email == user_email))
        is_user_present = is_user_present_query.scalar_one_or_none()

        if is_user_present:
            logger.warning(f"User with email ID - {user_email} already exists!!")
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f"User with email ID - {user_email} already exists!!"
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
    except Exception as e:
        await db_session.rollback()
        logger.error("An error occurred while signup", e)
        raise e