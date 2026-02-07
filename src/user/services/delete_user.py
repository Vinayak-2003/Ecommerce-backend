from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schema import User
from fastapi.responses import JSONResponse
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def delete_user_by_email(email: str, db_session: AsyncSession):
    try:
        stored_user_query = await db_session.execute(select(User).where(User.user_email == email))
        stored_user = stored_user_query.scalar_one_or_none()

        if not stored_user:
            logger.error(f"User with the email - {email} does not exists !!")
            return JSONResponse(
                content=f"User with {email} does not exists !!",
                status_code=404
            )
        
        await db_session.delete(stored_user)
        await db_session.commit()
        await db_session.refresh()

        logger.info(f"Successfully deleted the user with the email id - {email}")
        return JSONResponse(
            content=f"User with email {email} deleted successsfully!!",
        )
    except Exception as e:
        await db_session.rollback()
        logger.error("An error raised while deleting the user", e)
        raise e
    