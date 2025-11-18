from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from enum import Enum
from database.base import Base
from uuid import uuid4

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


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    shipping_address_id = Column(UUID(as_uuid=True), ForeignKey("address.address_id"), nullable=False)
    
    payment_method = Column(SQLEnum(PaymentMethod), default=PaymentMethod.UPI, nullable=False)
    order_status = Column(SQLEnum(OrderStatus), nullable=False)
    total_items = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    order_placed_datetime = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    order_updated_datetime = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User", back_populates="orders")


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    
    product_name = Column(String(100), nullable=False)
    price_at_purchase = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")