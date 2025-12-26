from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from .model import OrderCreate, OrderOut, OrderUpdate
from ..user_auth.controller import oauth2_scheme
from database.base import get_db_session

from .services.get_order import fetch_all_paginated_orders, fetch_current_user_order_by_id
from .services.create_order import create_order_current_user
from .services.cancel_order import delete_current_user_order
from .services.update_order_status import update_user_order_status

order_route = APIRouter(
    prefix="/api/v1/orders",
    tags=["Order"]
)

@order_route.get("/fetch-orders/me")
async def fetch_all_orders(token: Annotated[str, Depends(oauth2_scheme)],
                     page_no: int = Query(default=1, ge=1),
                     per_page: int = Query(default=10, ge=1, le=100),
                     db: AsyncSession = Depends(get_db_session)
                    ):
    return await fetch_all_paginated_orders(token, page_no, per_page, db)


@order_route.get("/fetch-order/me/{order_id}", response_model=OrderOut)
async def fetch_order_by_id(order_id: str,
                      token: Annotated[str, Depends(oauth2_scheme)],
                     db: AsyncSession = Depends(get_db_session)
                    ):
    return await fetch_current_user_order_by_id(order_id, token, db)


@order_route.post("/create-order/me", response_model=OrderOut)
async def create_order(new_order: OrderCreate,
                 token: Annotated[str, Depends(oauth2_scheme)],
                 db: AsyncSession = Depends(get_db_session)
                ):
    return await create_order_current_user(new_order, token, db)


# can be access by admins only 
@order_route.put("/update-status")
async def update_order_status(update_status: OrderUpdate,
                        token: Annotated[str, Depends(oauth2_scheme)],
                        db: AsyncSession = Depends(get_db_session)
                    ):
    return await update_user_order_status(update_status, token, db)


@order_route.delete("/cancel-order/me/{order_id}")
async def cancel_order(token: Annotated[str, Depends(oauth2_scheme)],
                 order_id: str,
                 db: AsyncSession = Depends(get_db_session)
                ):
    return await delete_current_user_order(token, order_id, db)