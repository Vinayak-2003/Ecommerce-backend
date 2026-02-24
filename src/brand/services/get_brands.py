"""
Service module for fetching brand details from the database.
"""
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.logger_middleware import get_logger

from ..schema import Brands

logger = get_logger(__name__)


async def fetch_all_paginated_brands(page_no, per_page, db_session: AsyncSession):
    """
    Fetches a paginated list of all product brands from the database.
    """
    try:
        total_brands_query = await db_session.execute(
            select(func.count()).select_from(Brands)
        )
        total_brands = total_brands_query.scalar_one()

        brand_for_page_query = await db_session.execute(
            select(Brands).offset((page_no - 1) * per_page).limit(per_page)
        )
        brand_for_page = brand_for_page_query.scalars().all()

        pages = (total_brands + per_page - 1) // per_page

        response = {
            "items": brand_for_page,
            "total": total_brands,
            "page": page_no,
            "per_page": per_page,
            "pages": pages,
        }

        logger.info(f"Fetched paginated data for brands for page number {page_no}")
        return response
    except Exception:
        logger.exception("An error occurred while fetching paginated brand data")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
