from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from ..schema import Address
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def all_current_user_addresses(token: str, db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)
        address_list_query = await db_session.execute(select(Address).where(Address.user_id == current_user_id))
        address_list = address_list_query.scalars().all()

        if address_list is None:
            logger.info(f"No address found for the current user with user id {current_user_id}")
            return JSONResponse(
                content=f"No address found for current user with user id {current_user_id}"
            )

        logger.info(f"All address for the current user {current_user_id} is fetched successfully !!")
        return address_list
    except Exception as e:
        logger.error("An error raised while fetching a addresses: ", e)
        await db_session.rollback()
        raise e
