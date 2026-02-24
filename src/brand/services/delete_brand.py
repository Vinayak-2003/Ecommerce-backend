"""
Service module for deleting brands from the database.
"""
from fastapi import HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..schema import Brands

logger = get_logger(__name__)


async def delete_brand_controller(brand_id, db_session: AsyncSession):
    """
    Deletes a specific brand from the database by its ID.
    """
    try:
        stored_brand_data_query = await db_session.execute(
            select(Brands).where(Brands.brand_id == brand_id)
        )
        stored_brand_data = stored_brand_data_query.scalar_one_or_none()

        if stored_brand_data is None:
            logger.warning(f"Brand with ID {brand_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with ID {brand_id} not found !!"
            )

        await db_session.delete(stored_brand_data)
        await db_session.commit()
        logger.info(f"Brand ID {brand_id} deleted successfully")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        await db_session.rollback()
        raise
    except Exception:
        await db_session.rollback()
        logger.exception("An error occurred while deleting the brand")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
