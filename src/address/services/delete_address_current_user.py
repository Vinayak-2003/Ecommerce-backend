"""
Service module for deleting shipping addresses of the authenticated user.
"""
from fastapi import HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..schema import Address

logger = get_logger(__name__)


async def delete_current_user_address(
    address_id: str, token: str, db_session: AsyncSession
):
    """
    Deletes a specific shipping address for the currently authenticated user by its ID.
    """
    try:
        current_user_id = await get_current_user_id(token)
        stored_address_query = await db_session.execute(
            select(Address).where(
                Address.address_id == address_id, Address.user_id == current_user_id
            )
        )
        stored_address = stored_address_query.scalar_one_or_none()

        if not stored_address:
            logger.warning(f"Address ID {address_id} not found for user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
            )

        await db_session.delete(stored_address)
        await db_session.commit()
        logger.info(f"Successfully deleted address ID {address_id} for user {current_user_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("An error occurred while deleting the address")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
