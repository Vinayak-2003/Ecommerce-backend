"""
Service module for adding new brands to the database.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..model import BrandCreate
from ..schema import Brands

logger = get_logger(__name__)


async def create_brand_controller(new_brand: BrandCreate, db_session: AsyncSession):
    """
    Creates a new brand entry in the database.
    """
    try:
        new_brand_dict = Brands(**new_brand.model_dump())
        db_session.add(new_brand_dict)
        await db_session.commit()
        await db_session.refresh(new_brand_dict)
        logger.info(f"Successfully created brand: {new_brand_dict.brand_name}")
        return new_brand_dict
    except Exception:
        await db_session.rollback()
        logger.exception("An error occurred while adding a new brand")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
