"""
Service module for updating product details in the database.
"""
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..model import ProductUpdate
from ..schema import Products

logger = get_logger(__name__)


async def update_product_controller(
    product_id, updated_product_data: ProductUpdate, db_session: AsyncSession
):
    """
    Updates an existing product in the database with the provided data.
    """
    try:
        stored_product_query = await db_session.execute(
            select(Products).where(Products.product_id == product_id)
        )
        stored_product = stored_product_query.scalar_one_or_none()

        if not stored_product:
            logger.error(f"Product with ID {product_id} is not present")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Product not found !!"
            )

        updated_product_data_dict = updated_product_data.model_dump(exclude_unset=True)

        if not updated_product_data_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No fields are provided for update !!"
            )

        for key, value in updated_product_data_dict.items():
            setattr(stored_product, key, value)

        await db_session.commit()
        await db_session.refresh(stored_product)

        logger.info(f"Successfully updated product ID {product_id}")
        return stored_product
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        await db_session.rollback()
        logger.exception("An error occurred while updating product data")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
