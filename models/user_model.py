from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import Annotated
from enum import Enum
from datetime import datetime

class UserRoles(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    CUSTOMER = "customer"

class UserCreate(BaseModel):
    user_email: EmailStr
    user_contact: Annotated[str, Field(pattern=r'^\+?[1-9]\d{1,14}$')]
    password: str

class UserOut(BaseModel):
    user_id: UUID4
    user_email: EmailStr
    user_contact: str
    role: UserRoles
    user_created_time: datetime
    user_updated_time: datetime
    user_last_login_time: datetime | None

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    user_contact: Annotated[str | None, Field(pattern=r'^\+?[1-9]\d{1,14}$')] = None
    password: str | None = None
    
class UserRoleUpdateAdmin(BaseModel):
    role: UserRoles | None = None       # only admin should update this

class UserLoginSchema(BaseModel):
    user_email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
