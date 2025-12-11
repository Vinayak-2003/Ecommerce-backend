from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, func, ForeignKey
from enum import Enum
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from database.base import Base

class ProductStatus(str, Enum):
    Active = "Active"
    Inactive = "Inactive"
    Discontinued = "Discontinued"

class Currency(str, Enum):
    Inr = "INR"
    Usd = "USD"
    Euro = "EURO"
    Pound = "POUND STERLING"
    Yen = "YEN"
    Ruble = "RUSSIAN RUBLE"

class Category(str, Enum):
    Men = "Men"
    Women = "Women"
    Kids = "Kids"

class Products(Base):
    __tablename__ = 'products'

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    product_name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=False)
    currency = Column(SQLEnum(Currency), nullable=False)
    available_quantity = Column(Integer, nullable=False)
    status = Column(SQLEnum(ProductStatus), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    brand_id = Column(String, ForeignKey("brands.brand_id"), nullable=False)
    category = Column(SQLEnum(Category), nullable=False)

    brand = relationship("Brands", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
