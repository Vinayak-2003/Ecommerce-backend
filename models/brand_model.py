from pydantic import BaseModel

class BrandCreate(BaseModel):
    brand_name: str
