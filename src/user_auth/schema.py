from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Enum as SQLEnum
from enum import Enum
from uuid import uuid4
from database.base import Base

class UserRoles(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    CUSTOMER = "customer"

def get_enum_values(enum_class):
    return [member.value for member in enum_class]

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False, unique=True)
    user_email = Column(String(320), unique=True, nullable=False)
    user_contact = Column(String(10), nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRoles, values_callable=get_enum_values), default=UserRoles.CUSTOMER, nullable=False)

    user_created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    user_updated_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    user_last_login_time = Column(TIMESTAMP, nullable=True)

    address = relationship("Address", back_populates="user", cascade="all, delete")
    orders = relationship("Order", back_populates="user", cascade="all, delete")
