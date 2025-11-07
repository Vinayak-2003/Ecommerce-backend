from ..model import ProductCreate
from ..schema import Products
from sqlalchemy.orm import Session

def create_new_product_controller(new_product_data: ProductCreate, db_session: Session):
    try:
        new_product = Products(**new_product_data.model_dump())
        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product)
        print("fetched new data and inserted into db", new_product)
        return new_product
    except Exception as e:
        db_session.rollback()
        print("An error raised while adding a new product data: ", e)
        raise e