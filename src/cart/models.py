from pydantic import BaseModel, UUID4
from datetime import datetime

class CartItemCreate(BaseModel):
    product_id: UUID4
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemOut(BaseModel):
    cart_item_id: UUID4
    user_id: UUID4
    product_id: UUID4
    quantity: int
    product_amount: int
    total_quantity_amount: int

    created_datetime: datetime
    last_updated_datetime: datetime

    class Config:
        orm_mode = True