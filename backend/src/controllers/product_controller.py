from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.repository import product_repository
from src.schemas import product_schema
from src.middleware.utils import SERVER_ERROR
from sqlalchemy.exc import IntegrityError

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Responsible for managing the flow to do CRUD on product table.

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 09, 2024           
"""

# Create
async def create_product(db: AsyncSession, product_create:product_schema.ProductCreate) -> product_schema.Product:
    try:
        product = await product_repository.get_product_by_name(db=db, name=product_create.name)
    except Exception as ex:
        raise SERVER_ERROR
    
    if product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Already exists product with name {0}".format(product_create.name)
        )
    try:
        return await product_repository.create_product(db=db, product=product_create)
    except Exception as ex:
        raise SERVER_ERROR

# Read
async def get_all_products(db: AsyncSession) -> list[product_schema.Product]:
    try:
        return await product_repository.get_all_products(db=db) 
     
    except Exception as ex:
        raise SERVER_ERROR

# Update
async def update_product(db: AsyncSession, product_update: product_schema.Product) -> None:
    try:
        product = await product_repository.get_product_by_id(db=db, id=product_update.id)
    except Exception as ex: 
        raise SERVER_ERROR
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    try:
        product_by_name = await product_repository.get_product_by_name(db=db, name=product_update.name)
    except Exception as ex: 
        raise SERVER_ERROR
    
    if product_by_name and product_by_name.id != product_update.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Already exists product with name {0}".format(product_update.name)
        )
    try:
        return await product_repository.update_product(db=db, product_update=product_update)
    except Exception as ex:
        raise SERVER_ERROR    
    
# Delete
async def delete_product(db: AsyncSession, id_product: int):
    try:
        product = await product_repository.get_product_by_id(db=db, id=id_product)
    except Exception as ex: 
        raise SERVER_ERROR
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    try:
        return await product_repository.delete_product(db=db, id_product=id_product)
    
    except IntegrityError as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Integrity error occurred with error {0}".format(ex.orig.args[0]))
    except Exception as ex:
        raise SERVER_ERROR
