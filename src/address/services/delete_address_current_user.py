from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schema import Address
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def delete_current_user_address(address_id: str, token: str, db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)
        stored_address_query = await db_session.execute(select(Address).where(
            Address.address_id == address_id,
            Address.user_id == current_user_id
        ))
        stored_address = stored_address_query.scalar_one_or_none()

        if not stored_address:
            logger.error(f"Address not found with {address_id} and {current_user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Address not found with {address_id} and {current_user_id}")
        
        logger.info(f"Address found with {address_id} and {current_user_id}")

        await db_session.delete(stored_address)
        await db_session.commit()
        logger.info(f"Address deleted with {address_id} successfully !!")
        return JSONResponse(content={
                                    "msg": f"Address deleted with {address_id} successfully !!"
                                },
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"An error occurred while deleting the address data: {str(e)}")
        await db_session.rollback()
        raise e
    