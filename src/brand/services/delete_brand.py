from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schema import Brands
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def delete_brand_controller(brand_id, db_session: AsyncSession):
    try:
        stored_brand_data_query = await db_session.execute(select(Brands).where(Brands.brand_id == brand_id))
        stored_brand_data = stored_brand_data_query.scalar_one_or_none()

        if stored_brand_data is None:
            logger.info(f"Brand with brand id {brand_id} not found !!")
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with brand id {brand_id} not found !!"
            )

        await db_session.delete(stored_brand_data)
        await db_session.commit()
        logger.info(f"Data with brand ID {brand_id} deleted successfully !!")
        return JSONResponse({"details": f"Data with brand ID {brand_id} deleted successfully !!"})
    except Exception as e:
        await db_session.rollback()
        logger.error("An error raised while deleteing a brand data: ", e)
        raise e