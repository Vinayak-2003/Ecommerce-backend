from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..model import UserOut
from ..schema import User
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def get_user_by_email_controller(email: str, db_session: AsyncSession):
    try:
        user_details_query = await db_session.execute(select(User).filter(User.user_email == email))
        user_details = user_details_query.scalar_one_or_none()

        logger.info(f"Successfully fetched the user with email id - {email}")
        return UserOut.model_validate(user_details)
    except Exception as e:
        await db_session.rollback()
        logger.error("An error raised while fetching the user", e)
        raise e