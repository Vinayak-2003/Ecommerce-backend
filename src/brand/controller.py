from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlalchemy.orm import Session

from database.base import get_db_session
from model import BrandCreate

from services.get_brands import fetch_all_paginated_brands
from services.add_brand import create_brand_controller
from services.delete_brand import delete_brand_controller

brand_route = APIRouter(
    prefix="/api/v1/brand",
    tags=["Brand"]
)

# GET all brand names
@brand_route.get("/get-all-brand")
def get_all_brands(page_no: int = Query(default=1, ge=1),
                   per_page: int = Query(default=10, ge=1, le=100),
                   db: Session = Depends(get_db_session)):
    return fetch_all_paginated_brands(page_no, per_page, db)

# CREATE a new brand data
@brand_route.post("/add-brand")
def add_new_brand(new_brand_data: BrandCreate,
                  db: Session = Depends(get_db_session)
                ):
    return create_brand_controller(new_brand_data, db)

# DELETE a brand
@brand_route.delete("/delete-brand/{brand_id}")
def delete_brand(brand_id: str,
                   db: Session = Depends(get_db_session)):
    return delete_brand_controller(brand_id, db)