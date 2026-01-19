from fastapi.responses import JSONResponse
from ..schema import Products
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)


async def fetch_product_by_id_controller(product_id, db_session: AsyncSession):
    try:
        product_data_id = await db_session.execute(
            select(Products).where(Products.product_id == product_id)
        )
        result = product_data_id.scalar_one_or_none()

        if result is None:
            logger.info(f"No product found for {product_id}")
            return JSONResponse(content=f"No product found for {product_id}", status_code=404)
        
        logger.info(f"Data fetched for product id {product_id} successfully !!")
        return result
    except Exception as e:
        logger.error("An error raised while fetching a product by id: ", e)
        raise e

async def fetch_product_by_name_customization_controller(product_name, category, min_price, max_price, db_session: AsyncSession):
    try:
        product_data_name_query = select(Products).where(Products.product_name == product_name)
        if min_price is not None and max_price is not None and category is not None:
            product_data_name_query = product_data_name_query.where(Products.price.between(min_price, max_price) and Products.category == category)
        elif min_price is not None and max_price is not None:
            product_data_name_query = product_data_name_query.where(Products.price.between(min_price, max_price))
        elif min_price is not None:
            product_data_name_query = product_data_name_query.where(Products.price >= min_price)
        elif max_price is not None:
            product_data_name_query = product_data_name_query.where(Products.price <= max_price)
        elif category is not None:
            product_data_name_query = product_data_name_query.where(Products.category == category)

        result = await db_session.execute(product_data_name_query)
        products = result.scalars().all()

        if products == []:
            logger.info(f"No product found for {product_name}")
            return JSONResponse(content=f"No product found for {product_name}", status_code=404)

        logger.info(f"Custimization query processed: {product_data_name_query}")
        logger.info(f"Data fetched for product id {product_name} successfully !!")
        return products
    except Exception as e:
        logger.error(f"An error raised while fetching a product by customized filters: {str(e)}")
        raise e

async def fetch_all_paginated_products(page_no, per_page, db_session: AsyncSession):
    try:
        # get the total count of products stored in db
        total_query = await db_session.execute(select(func.count()).select_from(Products))
        total = total_query.scalar_one_or_none()

        # get products for the requested page
        product_for_page_query = await db_session.execute(select(Products).offset((page_no-1) * per_page).limit(per_page))
        product_for_page = product_for_page_query.scalars().all()

        # calculate total pages
        pages = (total + per_page - 1) // per_page

        response = {
            "items": product_for_page,
            "total": total,
            "page": page_no,
            "per_page": per_page,
            "pages": pages
        }

        logger.info(f"Fetched paginated data for products for page number {page_no}")
        return response
    except Exception as e:
        logger.error(f"An error raised while fetching products {str(e)}")
        raise e
