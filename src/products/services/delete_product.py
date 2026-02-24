"""
Service module for deleting products from the database.
"""
from fastapi import HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..schema import Products

logger = get_logger(__name__)


async def delete_product_controller(product_id, db_session: AsyncSession):
    """
    Deletes a specific product from the database by its ID.
    """
    try:
        stored_product_query = await db_session.execute(
            select(Products).where(Products.product_id == product_id)
        )
        stored_product = stored_product_query.scalar_one_or_none()

        if not stored_product:
            logger.warning(f"Product with ID {product_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Product not found !!"
            )

        await db_session.delete(stored_product)
        await db_session.commit()
        logger.info(f"Product ID {product_id} deleted successfully")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        await db_session.rollback()
        logger.exception("An error occurred while deleting the product")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
