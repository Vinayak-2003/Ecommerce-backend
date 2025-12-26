from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..model import AddressCreate, AddressOut
from ..schema import Address
from ...user_auth.services.current_user import get_current_user_id
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def create_current_user_address(new_address: AddressCreate,
                                token: str,
                                db_session: AsyncSession):
    try:
        current_user_id = await get_current_user_id(token)
        new_address = Address(
            user_id = current_user_id,
            **new_address.model_dump()
        )

        # marking all address as not default if current address is default
        if new_address.is_default:
            await db_session.execute(select(Address).where(
                Address.user_id == current_user_id
            ).values(is_default = False))

        await db_session.add(new_address)
        await db_session.commit()
        await db_session.refresh(new_address)
        logger.info(f"An address is created for {current_user_id}")
        return new_address
    except Exception as e:
        logger.error(f"An error occurred while creating a new address for {current_user_id}: {str(e)}")
        await db_session.rollback()
        raise e