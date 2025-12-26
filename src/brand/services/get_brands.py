from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..schema import Brands
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

async def fetch_all_paginated_brands(page_no, per_page, db_session: AsyncSession):
    try:
        total_brands_query = await db_session.execute(select(func.count()).select_from(Brands))
        total_brands = total_brands_query.scalar_one_or_none()

        brand_for_page_query = await db_session.execute(select(Brands).offset((page_no-1) * per_page).limit(per_page))
        brand_for_page = brand_for_page_query.scalars().all()

        pages = (total_brands + per_page - 1) // per_page

        response = {
            "items": brand_for_page,
            "total": total_brands,
            "page": page_no,
            "per page": per_page,
            "total pages": pages,
        }

        logger.info(f"Fetched paginated data for brands for page number {page_no}")
        return response
    except Exception as e:
        await db_session.rollback()
        logger.error("An error raised while fetching brand data: ", e)
        raise e