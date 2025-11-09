from ..model import ProductCreate
from ..schema import Products
from sqlalchemy.orm import Session
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

def create_new_product_controller(new_product_data: ProductCreate, db_session: Session):
    try:
        new_product = Products(**new_product_data.model_dump())
        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product)
        logger.info("fetched new data and inserted into db", new_product)
        return new_product
    except Exception as e:
        db_session.rollback()
        logger.error("An error raised while creating a new product data: ", e)
        raise e