from datetime import datetime
from enum import Enum
from pydantic import BaseModel, UUID4

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

class ProductUpdate(BaseModel):
    product_name: str | None = None
    description: str | None = None
    price: float | None = None
    discount_price: float | None = None
    currency: Currency | None = None
    available_quantity: int | None = None
    status: ProductStatus | None = None
    brand_id: UUID4 | None = None
    category: Category | None = None

class ProductCreate(BaseModel):
    product_name: str
    description: str
    price: float
    discount_price: float
    currency: Currency
    available_quantity: int
    status: ProductStatus
    brand_id: UUID4
    category: Category

class ProductOut(ProductCreate):
    product_id: UUID4
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True