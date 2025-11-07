from sqlalchemy.orm import Session
from ..model import BrandCreate
from ..schema import Brands

def create_brand_controller(new_brand: BrandCreate, db_session: Session):
    try:
        new_brand_dict = Brands(**new_brand.model_dump())
        db_session.add(new_brand_dict)
        db_session.commit()
        db_session.refresh(new_brand_dict)
        print("fetched new data and inserted into db", new_brand_dict)
        return new_brand_dict
    except Exception as e:
        db_session.rollback()
        print("An error occurred while inserting brand data in db", e)
        raise e
    