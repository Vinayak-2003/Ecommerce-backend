"""
Pydantic models for cart-related data transfer.
"""
from datetime import datetime

from pydantic import UUID4, BaseModel


class CartItemCreate(BaseModel):
    """
    Schema for adding an item to the cart.
    """
    product_id: UUID4
    quantity: int


class CartItemUpdate(BaseModel):
    """
    Schema for updating a cart item's quantity.
    """
    quantity: int


class CartItemOut(BaseModel):
    """
    Schema for representing a cart item in responses.
    """
    cart_item_id: UUID4
    user_id: UUID4
    product_id: UUID4
    quantity: int
    product_amount: int
    total_quantity_amount: int

    created_datetime: datetime
    last_updated_datetime: datetime

    class Config:
        """
        Pydantic configuration for the CartItemOut model.
        """
        orm_mode = True
