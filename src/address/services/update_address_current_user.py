"""
Service module for updating shipping addresses of the authenticated user.
"""
from fastapi import HTTPException, status
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..model import AddressUpdate
from ..schema import Address

logger = get_logger(__name__)


async def update_current_user_address(
    address_id: str, update_address: AddressUpdate, token: str, db_session: AsyncSession
):
    """
    Updates an existing shipping address for the currently authenticated user.
    If the updated address is set as default, it unsets other existing default addresses.
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

        update_address_dict = update_address.model_dump(exclude_unset=True)

        # marking other addresses as not default if this one is being set as default
        if update_address.is_default:
            await db_session.execute(
                update(Address)
                .where(
                    Address.user_id == current_user_id, Address.address_id != address_id
                )
                .values(is_default=False)
            )

        for key, value in update_address_dict.items():
            setattr(stored_address, key, value)

        await db_session.commit()
        await db_session.refresh(stored_address)
        logger.info(f"Successfully updated address ID {address_id} for user {current_user_id}")
        return stored_address
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        logger.exception("An error occurred while updating the address")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
