"""
Service module for fetching all addresses associated with the current user.
"""
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..schema import Address

logger = get_logger(__name__)


async def all_current_user_addresses(token: str, db_session: AsyncSession):
    """
    Fetches all shipping addresses for the currently authenticated user.
    """
    try:
        current_user_id = await get_current_user_id(token)
        address_list_query = await db_session.execute(
            select(Address).where(Address.user_id == current_user_id)
        )
        address_list = address_list_query.scalars().all()

        logger.info(f"Successfully fetched {len(address_list)} addresses for user {current_user_id}")
        return address_list
    except Exception:
        logger.exception("An error occurred while fetching addresses")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
