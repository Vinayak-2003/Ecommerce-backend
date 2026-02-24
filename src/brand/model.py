"""
Pydantic models for brand-related data transfer.
"""
from pydantic import BaseModel


class BrandCreate(BaseModel):
    """
    Schema for creating a new brand.
    """
    brand_name: str
