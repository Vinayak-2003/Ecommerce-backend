from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import List
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PACKED = 'packed'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    RETURN_REQUESTED = 'return_requested'
    RETURNED = 'returned'
    DELAY = 'delay'

class PaymentMethod(str, Enum):
    COD = 'COD'
    UPI = 'UPI'
    Wallet = 'Wallet'
    Card = 'Card'

class OrderItemCreate(BaseModel):
    product_id: UUID4
    quantity: int

class OrderItemOut(BaseModel):
    product_id: UUID4
    product_name: str
    price_at_purchase: float
    quantity: int
    total_price: float

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: PaymentMethod
    shipping_address_id: UUID4

class OrderUpdate(BaseModel):
    order_status: OrderStatus | None = None

class OrderOut(BaseModel):
    order_id: UUID4
    user_id: UUID4
    shipping_address_id: UUID4
    order_status: OrderStatus
    items: List[OrderItemOut]
    total_items: int
    total_amount: float
    order_placed_datetime: datetime
    order_updated_datetime: datetime