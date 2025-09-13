from schemas.products_schema import Products

def fetch_all_paginated_products(page_no, per_page, db):
    # get the total count of products stored in db
    total = db.query(Products).count()

    # get products for the requested page
    product_for_page = db.query(Products).Offset((page_no-1) * per_page).limit(per_page).all()

    # calculate total pages
    pages = (total + per_page - 1) // per_page

    return {
        "items": product_for_page,
        "total": total,
        "page": page_no,
        "per page": per_page,
        "pages": pages
    }