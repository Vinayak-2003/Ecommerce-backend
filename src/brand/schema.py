"""
Database models for brand-related data.
Includes the Brands model and its relationship with products.
"""
from uuid import UUID, uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database.base import Base


class Brands(Base):
    """
    SQLAlchemy model representing a product brand in the system.
    """
    __tablename__ = "brands"

    brand_id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid4())[:8]
    )
    brand_name = Column(String(200), nullable=False)

    products = relationship("Products", back_populates="brand")
