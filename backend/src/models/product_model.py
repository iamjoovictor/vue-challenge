from sqlalchemy import Column, Integer, Boolean, String, Date, Float, ForeignKey
from ..config.config_db import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    price = Column(Float)
    expiration_date = Column(Date)
    image = Column(String(255))
    id_category = Column(Integer, ForeignKey("category.id"))
