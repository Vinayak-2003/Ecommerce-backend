from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..model import ProductUpdate
from ..schema import Products
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def update_product_controller(product_id, updated_product_data, db_session: Session):
    try:
        stored_product = db_session.query(Products).get(product_id)
        if not stored_product:
            logger.error(f"Product with {product_id} is not present")
            raise HTTPException(status_code=404, detail="Product not found !!")
        
        updated_product_data_dict = updated_product_data.model_dump(exclude_unset=True)
        for key, value in updated_product_data_dict.items():\
            setattr(stored_product, key, value)

        logger.info(f"Data is updated with the new data for product id {product_id}")
        db_session.commit()
        db_session.refresh(stored_product)

        logger.info(f"Successfully updated the data for product id {product_id}")
        return stored_product
    except Exception as e:
        db_session.rollback()
        logger.error("An error raised while updating product data: ", e)
        raise e