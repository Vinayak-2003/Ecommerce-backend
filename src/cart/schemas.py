"""
Database models for cart-related data.
Includes the CartItem model and its relationships with users and products.
"""
from uuid import uuid4

from sqlalchemy import (TIMESTAMP, Column, Float, ForeignKey, Integer, String,
                        func)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base


class CartItem(Base):
    """
    SQLAlchemy model representing an item in a user's shopping cart.
    """
    __tablename__ = "cart_items"

    cart_item_id = Column(
        UUID(as_uuid=True), default=uuid4, primary_key=True, nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False
    )

    quantity = Column(Integer, nullable=False)
    product_amount = Column(Float, nullable=False)
    total_quantity_amount = Column(Float, nullable=False)

    created_datetime = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    last_updated_datetime = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", back_populates="cart_items")
    product = relationship("Products", back_populates="cart_items")
