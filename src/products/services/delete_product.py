from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schema import Products
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def delete_product_controller(product_id, db_session: AsyncSession):
    try:
        stored_product_query = await db_session.execute(select(Products).where(Products.product_id == product_id))
        stored_product = stored_product_query.scalar_one_or_none()

        if not stored_product:
            raise HTTPException(status_code=404, detail="Product not found !!")
        
        await db_session.delete(stored_product)
        await db_session.commit()
        logger.info(f"Data with product ID {product_id} deleted successfully !!")
        return JSONResponse(
            content=f"Data with product ID {product_id} deleted successfully !!",
            status_code=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        await db_session.rollback()
        logger.error(f"An error raised while deleteing a product data: {str(e)}")
        raise e