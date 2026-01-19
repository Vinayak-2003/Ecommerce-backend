from fastapi import APIRouter, Depends, Query
from .model import ProductCreate, ProductOut, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from .services.add_products import create_new_product_controller
from .services.get_products import (fetch_product_by_id_controller,
                                               fetch_all_paginated_products, 
                                               fetch_product_by_name_customization_controller
                                            )
from .services.update_product import update_product_controller
from .services.delete_product import delete_product_controller

from database.base import get_db_session

product_route = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
)

# get API routes
@product_route.get("/all-products")
async def fetch_all_products(page_no: int = Query(default=1, ge=1),
                       per_page: int = Query(default=10, ge=1, le=100),
                       db: AsyncSession = Depends(get_db_session)):
    return await fetch_all_paginated_products(page_no, per_page, db)

@product_route.get("/product-by-id/{product_id}")
async def fetch_product_by_id(product_id: UUID,
                        db: AsyncSession = Depends(get_db_session)
                    ):
    return await fetch_product_by_id_controller(product_id, db)

@product_route.get("/product-by-name/{product_name}",
                   response_model=List[ProductOut])
async def fetch_product_by_name(product_name: str,
                          category: str | None = None,
                          min_price: int | None = None,
                          max_price: int | None = None,
                          db: AsyncSession = Depends(get_db_session)
                        ):
    return await fetch_product_by_name_customization_controller(product_name, category, min_price, max_price, db)

# post API routes
@product_route.post("/add-product",
                    response_model=ProductOut)
async def create_new_product(new_product_data: ProductCreate,
                       db: AsyncSession = Depends(get_db_session)
                    ):
    return await create_new_product_controller(new_product_data, db)

# put API routes
@product_route.put("/update-product/{product_id}",
                   response_model=ProductOut)
async def update_product(product_id: UUID,
                   updated_product_data: ProductUpdate,
                   db: AsyncSession = Depends(get_db_session)
                ):
    return await update_product_controller(product_id, updated_product_data, db)

# patch API routes
@product_route.patch("/partial-update-product/{product_id}",
                     response_model=ProductOut)
async def partial_update_product(product_id: UUID,
                           updated_product_data: ProductUpdate,
                           db: AsyncSession = Depends(get_db_session)
                        ):
    return await update_product_controller(product_id, updated_product_data, db)

# delete API route
@product_route.delete("/delete-product/{product_id}")
async def delete_product(product_id: UUID,
                   db: AsyncSession = Depends(get_db_session)
                ):
    return await delete_product_controller(product_id, db)