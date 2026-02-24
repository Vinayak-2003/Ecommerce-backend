"""
Pydantic models for user-related data transfer.
Defines schemas for user registration, profile updates, and authentication.
"""
from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import UUID4, BaseModel, EmailStr, Field


class UserRoles(str, Enum):
    """
    Enumeration of available user roles in the system.
    """
    ADMIN = "admin"
    SELLER = "seller"
    CUSTOMER = "customer"


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    user_email: EmailStr
    user_contact: Annotated[str, Field(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(
        ..., min_length=10, max_length=15
    )
    password: str


class UserOut(BaseModel):
    """
    Schema for representing user data in responses.
    """
    user_id: UUID4
    user_email: EmailStr
    user_contact: str
    role: UserRoles
    user_created_time: datetime
    user_updated_time: datetime
    user_last_login_time: datetime | None

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """
    Schema for updating user profile details.
    """
    user_contact: Annotated[str | None, Field(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(
        ..., min_length=10, max_length=15
    )
    password: str | None = None


class UserRoleUpdateAdmin(BaseModel):
    """
    Schema for administrative role updates.
    """
    role: UserRoles | None = None  # only admin should update this


class UserLoginSchema(BaseModel):
    """
    Schema for user login credentials.
    """
    user_email: EmailStr
    password: str
