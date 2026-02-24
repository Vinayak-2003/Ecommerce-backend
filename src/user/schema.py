"""
Database models for user-related data.
Includes the User model and its relationships with other entities.
"""
from enum import Enum
from uuid import uuid4

from sqlalchemy import TIMESTAMP, Column, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum

from database.base import Base


class UserRoles(str, Enum):
    """
    Enumeration of defined user roles in the system.
    """
    ADMIN = "admin"
    SELLER = "seller"
    CUSTOMER = "customer"


def get_enum_values(enum_class):
    """
    Helper function to get all values of an enumeration class.
    """
    return [member.value for member in enum_class]


class User(Base):
    """
    SQLAlchemy model representing a user in the system.
    """
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False, unique=True
    )
    user_email = Column(String(320), unique=True, nullable=False)
    user_contact = Column(String(10), nullable=False)
    password = Column(String, nullable=False)
    role = Column(
        SQLEnum(UserRoles, values_callable=get_enum_values),
        default=UserRoles.CUSTOMER,
        nullable=False,
    )

    user_created_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    user_updated_time = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    user_last_login_time = Column(TIMESTAMP, nullable=True)

    address = relationship("Address", back_populates="user", cascade="all, delete")
    orders = relationship("Order", back_populates="user", cascade="all, delete")
    cart_items = relationship(
        "CartItem", back_populates="user", cascade="all, delete-orphan"
    )
    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )
