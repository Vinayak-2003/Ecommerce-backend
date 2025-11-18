from pydantic import BaseModel, UUID4, Field, EmailStr
from typing import Annotated
from datetime import datetime
from enum import Enum

class AddressType(str, Enum):
    HOME = "home"
    OFFICE = "office"
    OTHER = "other"

class AddressCreate(BaseModel):
    address_type: AddressType
    receiver_name: str
    receiver_email: EmailStr
    receiver_contact: Annotated[str, Field(pattern=r'^\+?[1-9]\d{1,14}$')]
    address_line_1: str
    address_line_2: str | None = None
    landmark: str | None = None
    city: str
    state: str
    pincode: str
    country: str
    is_default: bool

class AddressUpdate(BaseModel):
    address_type: AddressType | None = None
    receiver_name: str | None = None
    receiver_email: EmailStr | None = None
    receiver_contact: Annotated[str | None, Field(pattern=r'^\+?[1-9]\d{1,14}$')] = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    landmark: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    country: str | None = None
    is_default: bool | None = None

class AddressOut(AddressCreate):
    address_id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime
