"""
Service module for creating a new shipping address for the authenticated user.
"""
from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ...user.services.current_user import get_current_user_id
from ..model import AddressCreate
from ..schema import Address

logger = get_logger(__name__)


async def create_current_user_address(
    new_address: AddressCreate, token: str, db_session: AsyncSession
):
    """
    Creates a new shipping address for the currently authenticated user.
    If the new address is set as default, it unsets existing default addresses.
    """
    try:
        current_user_id = await get_current_user_id(token)
        address_entry = Address(user_id=current_user_id, **new_address.model_dump())

        # marking all addresses as not default if new address is default
        if address_entry.is_default:
            await db_session.execute(
                update(Address)
                .where(Address.user_id == current_user_id)
                .values(is_default=False)
            )

        db_session.add(address_entry)
        await db_session.commit()
        await db_session.refresh(address_entry)
        logger.info(f"Successfully created address ID {address_entry.address_id} for user {current_user_id}")
        return address_entry
    except Exception:
        logger.exception("An error occurred while creating a new address")
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
