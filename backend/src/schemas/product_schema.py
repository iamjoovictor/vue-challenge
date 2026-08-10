from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class ProductCreate(BaseModel):
    name: str
    price: float
    expiration_date: date
    image: Optional[str]
    id_category: Optional[int]
    quantity: int = 0

class Product(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)