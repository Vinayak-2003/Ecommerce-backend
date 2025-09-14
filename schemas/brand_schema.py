from sqlalchemy import Column, String
from database.base import Base
from uuid import UUID, uuid4

class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(String, primary_key=True, nullable=False, default=str(uuid4())[:8])
    brand_name = Column(String(200), nullable=False)