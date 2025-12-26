from sqlalchemy.ext.asyncio import AsyncSession
from ..model import BrandCreate
from ..schema import Brands
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def create_brand_controller(new_brand: BrandCreate, db_session: AsyncSession):
    try:
        new_brand_dict = Brands(**new_brand.model_dump())
        db_session.add(new_brand_dict)
        await db_session.commit()
        await db_session.refresh(new_brand_dict)
        logger.info("fetched new brand data and inserted into db", new_brand_dict)
        return new_brand_dict
    except Exception as e:
        await db_session.rollback()
        logger.error("An error occurred while inserting brand data in db", e)
        raise e
    