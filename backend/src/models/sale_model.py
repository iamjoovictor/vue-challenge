from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..config.config_db import Base


class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sold_at = Column(DateTime, server_default=func.now())
