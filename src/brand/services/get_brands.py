from sqlalchemy.orm import Session
from ..schema import Brands
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def fetch_all_paginated_brands(page_no, per_page, db_session: Session):
    try:
        total_brands = db_session.query(Brands).count()

        brand_for_page = db_session.query(Brands).offset((page_no-1) * per_page).limit(per_page).all()

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
        db_session.rollback()
        logger.error("An error raised while fetching brand data: ", e)
        raise e