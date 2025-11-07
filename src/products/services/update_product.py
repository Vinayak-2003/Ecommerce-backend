from fastapi import HTTPException
from ..model import ProductUpdate
from ..schema import Products
from sqlalchemy.orm import Session

def update_product_controller(product_id, updated_product_data, db_session: Session):
    try:
        stored_product = db_session.query(Products).get(product_id)
        if not stored_product:
            raise HTTPException(status_code=404, detail="Product not found !!")
        
        updated_product_data_dict = updated_product_data.model_dump(exclude_unset=True)
        print("----------------", updated_product_data_dict)
        for key, value in updated_product_data_dict.items():
            setattr(stored_product, key, value)

        db_session.commit()
        db_session.refresh(stored_product)

        return stored_product
    except Exception as e:
        db_session.rollback()
        print("An error raised while updating a new product data: ", e)
        raise e