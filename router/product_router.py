from fastapi import APIRouter, Depends, Query
from models.product_model import ProductCreate, ProductOut, ProductUpdate
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database.base import get_db_session

product_route = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
    )

# get API routes
@product_route.get("/all-products",
                   response_model=List[ProductOut])
def fetch_all_products(page_no: int = Query(default=1, ge=1),
                       per_page: int = Query(default=10, ge=1, le=100),
                       db: Session = Depends(get_db_session)):
    pass

@product_route.get("/product-by-id/{product_id}",
                   response_model=ProductOut)
def fetch_product_by_id(product_id: UUID,
                        db: Session = Depends(get_db_session)
                    ):
    pass

@product_route.get("/product-by-name/{product_name}",
                   response_model=List[ProductOut])
def fetch_product_by_name(product_name: str,
                          category: str | None = None,
                          min_price: int | None = None,
                          max_price: int | None = None,
                          db: Session = Depends(get_db_session)
                        ):
    pass

# post API routes
@product_route.post("/add-product",
                    response_model=ProductOut)
def create_new_product(new_product_data: ProductCreate,
                       db: Session = Depends(get_db_session)
                    ):
    pass

# put API routes
@product_route.put("/update-product/{product_id}",
                   response_model=ProductOut)
def update_product(product_id: UUID,
                   updated_product_data: ProductUpdate,
                   db: Session = Depends(get_db_session)
                ):
    pass

# patch API routes
@product_route.patch("/partial-update-product/{product_id}",
                     response_model=ProductOut)
def partial_update_product(product_id: UUID,
                           updated_product_data: ProductUpdate,
                           db: Session = Depends(get_db_session)
                        ):
    pass

# delete API route
@product_route.delete("/delete-product/{product_id}")
def delete_product(product_id: UUID,
                   db: Session = Depends(get_db_session)
                ):
    pass