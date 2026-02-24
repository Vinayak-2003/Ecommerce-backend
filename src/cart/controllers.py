"""
Cart controller for the E-Commerce Backend.
Defines endpoints for managing the user's shopping cart, including adding,
fetching, updating, and deleting items.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_db_session

from ..auth.controller import oauth2_scheme
from .models import CartItemCreate, CartItemOut, CartItemUpdate
from .services.create_cart import create_cart_current_user
from .services.delete_cart import delete_cart_current_user
from .services.fetch_cart import fetch_cart_current_user
from .services.update_cart import update_cart_current_user

cart_route = APIRouter(prefix="/api/v1/cart", tags=["Cart"])


@cart_route.get("/fetch-by-user")
async def fetch_cart_by_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    page_no: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, lt=100),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Endpoint to fetch the shopping cart items for the authenticated user with pagination.
    """
    return await fetch_cart_current_user(page_no, per_page, token, db)


@cart_route.post("/create-product-cart", response_model=CartItemOut)
async def create_product_cart(
    create_cart_details: CartItemCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    """
    Endpoint to add an item to the shopping cart or increase its quantity.
    """
    return await create_cart_current_user(create_cart_details, token, db)


@cart_route.put("/update-by-id/{cart_id}")
async def update_cart(
    cart_id: str,
    update_cart_details: CartItemUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    """
    Endpoint to update the quantity of an item in the shopping cart.
    """
    return await update_cart_current_user(cart_id, update_cart_details, token, db)


@cart_route.delete("/delete-by-id/{cart_id}")
async def delete_cart(
    cart_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db_session),
):
    """
    Endpoint to remove an item from the shopping cart.
    """
    return await delete_cart_current_user(cart_id, token, db)
