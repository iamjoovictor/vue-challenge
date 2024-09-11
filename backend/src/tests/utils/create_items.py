from sqlalchemy.ext.asyncio import AsyncSession
from src.models import category_model, product_model

async def add_register(db: AsyncSession, register):
    db.add(register)
    await db.commit()
    return register

async def create_category(db: AsyncSession):
    category = category_model.Category(
        name = 'test_category'
    )
    
    return await add_register(db, category)

async def create_product(db: AsyncSession):
    await create_category(db)
    
    product = product_model.Product(
        name = 'test_product',
        price = 0,
        expiration_date = '2024-09-10',
        image = None,
        id_category = 1
    )
    
    return await add_register(db, product)