from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from ..models import category_model
from ..schemas import category_schema
from ..middleware.utils_db import exec_sql

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Responsible for performing operations on database.

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 09, 2024           
"""

model = category_model.Category

# Create
async def create_category(db: AsyncSession, category: category_schema.CategoryCreate) -> category_schema.Category:
    category_data = category if isinstance(category, dict) else category.dict()
    db_category = model(**category_data)
    db.add(db_category)
    
    await db.flush()
    await db.refresh(db_category)
    await db.commit()
    
    return db_category

# Read
async def get_all_categories(db: AsyncSession) -> list[category_schema.Category]:
    response = await db.execute(select(model))
    return response.scalars().all()

async def get_category_by_id(db: AsyncSession, id: str) -> category_schema.Category:
    response = await db.execute(
        select(model).
        where(model.id == id)
    )
    
    return response.scalars().first()

async def get_category_by_name(db: AsyncSession, name: str) -> category_schema.Category:
    response = await db.execute(
        select(model).
        where(model.name == name)
    )
    
    return response.scalars().first()

# Update
async def update_category(db: AsyncSession, category_update: category_schema.Category):
    await db.execute(
        update(model).
        values(dict(category_update)).
        where(model.id == category_update.id)
    )
    await db.commit()

# Delete
async def delete_category(db: AsyncSession, id_category: int):
    await db.execute(
        delete(model).
        where(model.id == id_category)
    )
    await db.commit()
