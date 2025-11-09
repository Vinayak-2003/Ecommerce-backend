from sqlalchemy.orm import Session
from ..schema import Products
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def delete_product_controller(product_id, db_session: Session):
    try:
        stored_product = db_session.query(Products).get(product_id)
        if not stored_product:
            raise HTTPException(status_code=404, detail="Product not found !!")
        
        db_session.delete(stored_product)
        db_session.commit()
        logger.info("Data with product ID {product_id} deleted successfully !!")
        return JSONResponse({"details": f"Data with product ID {product_id} deleted successfully !!"})
    except Exception as e:
        db_session.rollback()
        logger.error("An error raised while deleteing a product data: ", e)
        raise e