"""
Service module for adding new products to the database.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..model import ProductCreate
from ..schema import Products

logger = get_logger(__name__)


async def create_new_product_controller(
    new_product_data: ProductCreate, db_session: AsyncSession
):
    """
    Creates a new product entry in the database.
    """
    try:
        new_product = Products(**new_product_data.model_dump())
        db_session.add(new_product)
        await db_session.commit()
        await db_session.refresh(new_product)
        logger.info(f"Successfully created product: {new_product.product_name}")
        return new_product
    except Exception:
        await db_session.rollback()
        logger.exception("An error occurred while creating a new product")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
