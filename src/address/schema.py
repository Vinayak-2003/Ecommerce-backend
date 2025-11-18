from sqlalchemy import Column, String, ForeignKey, Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from enum import Enum
from database.base import Base
from uuid import uuid4

class AddressType(str, Enum):
    HOME = "home"
    OFFICE = "office"
    OTHER = "other"

class Address(Base):
    __tablename__ = 'address'

    address_id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    
    address_type = Column(SQLEnum(AddressType), nullable=False)
    receiver_name = Column(String(100))
    receiver_email = Column(String(320), nullable=False)
    receiver_contact = Column(String(10), nullable=False)
    
    address_line_1 = Column(String(200), nullable=False)
    address_line_2 = Column(String(200), nullable=True)
    landmark = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(50), nullable=False)
    country = Column(String(100), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="address")