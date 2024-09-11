from sqlalchemy import Column, Integer, String
from ..config.config_db import Base

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
