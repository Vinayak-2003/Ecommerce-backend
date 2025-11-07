from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..schema import Brands

def delete_brand_controller(brand_id, db_session: Session):
    try:
        stored_brand_data = db_session.query(Brands).get(brand_id)
        db_session.delete(stored_brand_data)
        db_session.commit()
        return JSONResponse({"details": f"Data with product ID {brand_id} deleted successfully !!"})
    except Exception as e:
        db_session.rollback()
        print("An error raised while deleteing a product data: ", e)
        raise e