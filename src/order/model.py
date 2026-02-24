from datetime import datetime
from enum import Enum
from typing import List

from pydantic import UUID4, BaseModel


class OrderStatus(str, Enum):
    """
    Enum representing the possible statuses of an order.
    """
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PACKED = "PACKED"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURN_REQUESTED = "RETURN_REQUESTED"
    RETURNED = "RETURNED"
    DELAY = "DELAY"


class PaymentMethod(str, Enum):
    """
    Enum representing supported payment methods.
    """
    COD = "COD"
    UPI = "UPI"
    Wallet = "Wallet"
    Card = "Card"


class OrderItemCreate(BaseModel):
    """
    Schema for creating an individual item within an order.
    """
    product_id: UUID4
    quantity: int


class OrderItemOut(BaseModel):
    """
    Schema for representing an order item in responses.
    """
    product_id: UUID4
    product_name: str
    price_at_purchase: float
    quantity: int
    total_price: float


class OrderCreate(BaseModel):
    """
    Schema for creating a new order.
    """
    items: List[OrderItemCreate]
    payment_method: PaymentMethod = PaymentMethod.UPI


class OrderUpdate(BaseModel):
    """
    Schema for updating an order's status.
    """
    user_id: UUID4
    order_id: UUID4
    order_status: OrderStatus


class OrderOut(BaseModel):
    """
    Schema for representing a full order in responses.
    """
    order_id: UUID4
    user_id: UUID4
    shipping_address_id: UUID4
    order_status: OrderStatus
    items: List[OrderItemOut]
    total_items: int
    total_amount: float
    order_placed_datetime: datetime
    order_updated_datetime: datetime
