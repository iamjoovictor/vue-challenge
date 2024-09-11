from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductCreate(BaseModel):
    name: str
    price: float
    expiration_date: date
    image: Optional[str]
    id_category: Optional[int]

class Product(ProductCreate):
    id: int

    class Config:
        orm_mode = True