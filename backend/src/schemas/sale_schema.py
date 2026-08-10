from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime


class SaleCreate(BaseModel):
    product_id: int
    quantity: int

    @field_validator('quantity')
    @classmethod
    def quantity_positive(cls, v):
        if v < 1:
            raise ValueError('Quantity must be at least 1')
        return v


class Sale(BaseModel):
    id: int
    product_id: int
    user_id: int
    quantity: int
    sold_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SaleHistoryItem(BaseModel):
    id: int
    sold_at: datetime
    username: str
    product_name: str
    quantity: int


class ProductSaleItem(BaseModel):
    name: str
    total: int


class CategorySaleItem(BaseModel):
    name: str
    total: int
