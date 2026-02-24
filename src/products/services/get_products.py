"""
Service module for fetching products from the database.
"""
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..schema import Products

logger = get_logger(__name__)


async def fetch_product_by_id_controller(product_id, db_session: AsyncSession):
    """
    Fetches a single product from the database by its unique identifier.
    """
    try:
        product_data_id = await db_session.execute(
            select(Products).where(Products.product_id == product_id)
        )
        result = product_data_id.scalar_one_or_none()

        if result is None:
            logger.info(f"No product found for ID {product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No product found for ID {product_id}"
            )

        logger.info(f"Data fetched for product ID {product_id} successfully")
        return result
    except HTTPException:
        raise
    except Exception:
        logger.exception("An error occurred while fetching product by ID")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def fetch_product_by_name_customization_controller(
    product_name, category, min_price, max_price, db_session: AsyncSession
):
    """
    Fetches products matching a specific name, with optional category and price range filters.
    """
    try:
        query = select(Products).where(Products.product_name == product_name)
        
        if min_price is not None:
            query = query.where(Products.price >= min_price)
        if max_price is not None:
            query = query.where(Products.price <= max_price)
        if category is not None:
            query = query.where(Products.category == category)

        result = await db_session.execute(query)
        products = result.scalars().all()

        if not products:
            logger.info(f"No product found for {product_name} with specified filters")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No product found for {product_name}"
            )

        logger.info(f"Data fetched for product name {product_name} successfully")
        return products
    except HTTPException:
        raise
    except Exception:
        logger.exception("An error occurred while fetching products by customized filters")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def fetch_all_paginated_products(page_no, per_page, db_session: AsyncSession):
    """
    Fetches a paginated list of all products from the database.
    """
    try:
        # get the total count of products stored in db
        total_query = await db_session.execute(
            select(func.count()).select_from(Products)
        )
        total = total_query.scalar_one()

        # get products for the requested page
        product_for_page_query = await db_session.execute(
            select(Products).offset((page_no - 1) * per_page).limit(per_page)
        )
        product_for_page = product_for_page_query.scalars().all()

        # calculate total pages
        pages = (total + per_page - 1) // per_page

        response = {
            "items": product_for_page,
            "total": total,
            "page": page_no,
            "per_page": per_page,
            "pages": pages,
        }

        logger.info(f"Fetched paginated data for products for page number {page_no}")
        return response
    except Exception:
        logger.exception("An error occurred while fetching paginated products")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
