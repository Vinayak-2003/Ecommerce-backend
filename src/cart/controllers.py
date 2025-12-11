from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session

from .models import CartItemCreate, CartItemOut, CartItemUpdate
from ..user_auth.controller import oauth2_scheme
from database.base import get_db_session

from .services.create_cart import create_cart_current_user
from .services.delete_cart import delete_cart_current_user
from .services.fetch_cart import fetch_cart_current_user
from .services.update_cart import update_cart_current_user

cart_route = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"]
)

@cart_route.get("/fetch-by-user")
def fetch_cart_by_user(token: Annotated[str, Depends(oauth2_scheme)],
                        page_no: int = Query(default=1, ge=1),
                        per_page: int = Query(default=10, ge=1, lt=100),
                       db: Session = Depends(get_db_session)):
    return fetch_cart_current_user(page_no, per_page, token, db)

@cart_route.post("/create-product-cart", response_model=CartItemOut)
def create_product_cart(create_cart_details: CartItemCreate,
                        token: Annotated[str, Depends(oauth2_scheme)],
                        db: Session = Depends(get_db_session)):
    return create_cart_current_user(create_cart_details, token, db)

@cart_route.put("/update-by-id/{cart_id}")
def update_cart(cart_id: str,
                update_cart_details: CartItemUpdate,
                token: Annotated[str, Depends(oauth2_scheme)],
                db: Session = Depends(get_db_session)):
    return update_cart_current_user(cart_id, update_cart_details, token, db)

@cart_route.delete("/delete-by-id/{cart_id}")
def delete_cart(cart_id: str,
                token: Annotated[str, Depends(oauth2_scheme)],
                db: Session = Depends(get_db_session)):
    return delete_cart_current_user(cart_id, token, db)
