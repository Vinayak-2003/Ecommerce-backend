from ..schema import Products
from sqlalchemy.orm import Session
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def fetch_product_by_id_controller(product_id, db_session: Session):
    try:
        product_data_id = db_session.query(Products).get(product_id)
        logger.info(f"Data fetched for product id {product_id} successfully !!")
        return product_data_id
    except Exception as e:
        logger.error("An error raised while fetching a product by id: ", e)
        db_session.rollback()
        raise e

def fetch_product_by_name_customization_controller(product_name, category, min_price, max_price, db_session: Session):
    try:
        product_data_name_query = db_session.query(Products).filter(Products.product_name == product_name)
        if min_price is not None and max_price is not None and category is not None:
            product_data_name_query = product_data_name_query.filter(Products.price.between(min_price, max_price) and Products.category == category)
        elif min_price is not None and max_price is not None:
            product_data_name_query = product_data_name_query.filter(Products.price.between(min_price, max_price))
        elif min_price is not None:
            product_data_name_query = product_data_name_query.filter(Products.price >= min_price)
        elif max_price is not None:
            product_data_name_query = product_data_name_query.filter(Products.price <= max_price)
        elif category is not None:
            product_data_name_query = product_data_name_query.filter(Products.category == category)

        logger.info(f"Custimization query processed: {product_data_name_query}")
        logger.info(f"Data fetched for product id {product_name} successfully !!")
        return product_data_name_query.all()
    except Exception as e:
        logger.error("An error raised while fetching a product by customized filters: ", e)
        db_session.rollback()
        raise e

def fetch_all_paginated_products(page_no, per_page, db_session: Session):
    try:
        # get the total count of products stored in db
        total = db_session.query(Products).count()

        # get products for the requested page
        product_for_page = db_session.query(Products).offset((page_no-1) * per_page).limit(per_page).all()

        # calculate total pages
        pages = (total + per_page - 1) // per_page

        response = {
            "items": product_for_page,
            "total": total,
            "page": page_no,
            "per page": per_page,
            "pages": pages
        }

        logger.info(f"Fetched paginated data for products for page number {page_no}")
        return response
    except Exception as e:
        logger.error("An error raised while fetching products: ", e)
        db_session.rollback()
        raise e
