from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from ..models import product_model
from ..schemas import product_schema
from ..middleware.utils_db import exec_sql

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Responsible for performing operations on database.

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 09, 2024           
"""

model = product_model.Product

# Create
async def create_product(db: AsyncSession, product: product_schema.ProductCreate) -> product_schema.Product:
    product_data = product if isinstance(product, dict) else product.dict()
    db_product = model(**product_data)
    db.add(db_product)
    
    await db.flush()
    await db.refresh(db_product)
    await db.commit()
    
    return db_product

# Read
async def get_all_products(db: AsyncSession) -> list[product_schema.Product]:
    response = await db.execute(select(model))
    return response.scalars().all()

async def get_product_by_id(db: AsyncSession, id: str):
    response = await db.execute(
        select(model).
        where(model.id == id)
    )
    
    return response.scalars().first()

async def get_product_by_name(db: AsyncSession, name: str) -> product_schema.Product:
    response = await db.execute(
        select(model).
        where(model.name == name)
    )
    
    return response.scalars().first()

# Update
async def update_product(db: AsyncSession, product_update: product_schema.Product):
    await db.execute(
        update(model).
        values(dict(product_update)).
        where(model.id == product_update.id)
    )
    await db.commit()

# Delete
async def delete_product(db: AsyncSession, id_product: int):
    await db.execute(
        delete(model).
        where(model.id == id_product)
    )
    await db.commit()