"""
Pydantic models for product-related data transfer.
Defines schemas for product creation, updates, and status enumerations.
"""
from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel


class ProductStatus(str, Enum):
    """
    Enumeration of product availability statuses.
    """
    Active = "Active"
    Inactive = "Inactive"
    Discontinued = "Discontinued"


class Currency(str, Enum):
    """
    Enumeration of supported currencies.
    """
    Inr = "INR"
    Usd = "USD"
    Euro = "EURO"
    Pound = "POUND STERLING"
    Yen = "YEN"
    Ruble = "RUSSIAN RUBLE"


class Category(str, Enum):
    """
    Enumeration of product categories.
    """
    Men = "Men"
    Women = "Women"
    Kids = "Kids"


class ProductUpdate(BaseModel):
    """
    Schema for updating product details.
    """
    product_name: str | None = None
    description: str | None = None
    price: float | None = None
    discount_price: float | None = None
    currency: Currency | None = None
    available_quantity: int | None = None
    status: ProductStatus | None = None
    brand_id: str | None = None
    category: Category | None = None


class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    """
    product_name: str
    description: str
    price: float
    discount_price: float
    currency: Currency
    available_quantity: int
    status: ProductStatus
    brand_id: str
    category: Category
    product_image: str


class ProductOut(ProductCreate):
    """
    Schema for representing product data in responses.
    """
    product_id: UUID4
    updated_at: datetime
    created_at: datetime

    class Config:
        """
        Pydantic configuration for the ProductOut model.
        """
        orm_mode = True
