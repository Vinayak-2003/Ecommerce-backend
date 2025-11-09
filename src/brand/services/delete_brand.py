from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..schema import Brands
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def delete_brand_controller(brand_id, db_session: Session):
    try:
        stored_brand_data = db_session.query(Brands).get(brand_id)
        db_session.delete(stored_brand_data)
        db_session.commit()
        logger.info(f"Data with brand ID {brand_id} deleted successfully !!")
        return JSONResponse({"details": f"Data with brand ID {brand_id} deleted successfully !!"})
    except Exception as e:
        db_session.rollback()
        logger.error("An error raised while deleteing a brand data: ", e)
        raise e