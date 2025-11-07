from sqlalchemy.orm import Session
from ..schema import Brands

def fetch_all_paginated_brands(page_no, per_page, db_session: Session):
    total_brands = db_session.query(Brands).count()

    brand_for_page = db_session.query(Brands).offset((page_no-1) * per_page).limit(per_page).all()

    pages = (total_brands + per_page - 1) // per_page

    return {
        "items": brand_for_page,
        "total": total_brands,
        "page": page_no,
        "per page": per_page,
        "total pages": pages,
    }