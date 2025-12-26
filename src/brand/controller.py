from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_db_session
from .model import BrandCreate

from .services.get_brands import fetch_all_paginated_brands
from .services.add_brand import create_brand_controller
from .services.delete_brand import delete_brand_controller

brand_route = APIRouter(
    prefix="/api/v1/brand",
    tags=["Brand"]
)

# GET all brand names
@brand_route.get("/get-all-brand")
async def get_all_brands(page_no: int = Query(default=1, ge=1),
                   per_page: int = Query(default=10, ge=1, le=100),
                   db: AsyncSession = Depends(get_db_session)):
    return await fetch_all_paginated_brands(page_no, per_page, db)

# CREATE a new brand data
@brand_route.post("/add-brand")
async def add_new_brand(new_brand_data: BrandCreate,
                  db: AsyncSession = Depends(get_db_session)
                ):
    return await create_brand_controller(new_brand_data, db)

# DELETE a brand
@brand_route.delete("/delete-brand/{brand_id}")
async def delete_brand(brand_id: str,
                   db: AsyncSession = Depends(get_db_session)):
    return await delete_brand_controller(brand_id, db)