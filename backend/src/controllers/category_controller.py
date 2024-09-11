from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.repository import category_repository
from src.schemas import category_schema
from src.middleware.utils import SERVER_ERROR
from sqlalchemy.exc import IntegrityError

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Responsible for managing the flow to do CRUD on category table.

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 09, 2024           
"""

# Create
async def create_category(db: AsyncSession, category_create:category_schema.CategoryCreate) -> category_schema.Category:
    try:
        category = await category_repository.get_category_by_name(db=db, name=category_create.name)
    except Exception as ex:
        raise SERVER_ERROR
    
    if category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Already exists category with name {0}".format(category_create.name)
        )
    try:
        return await category_repository.create_category(db=db, category=category_create)
    except Exception as ex:
        raise SERVER_ERROR

# Read
async def get_all_categories(db: AsyncSession) -> list[category_schema.Category]:
    try:
        return await category_repository.get_all_categories(db=db) 
     
    except Exception as ex:
        raise SERVER_ERROR
    
# Update
async def update_category(db: AsyncSession, category_update: category_schema.Category) -> None:
    try:
        category = await category_repository.get_category_by_id(db=db, id=category_update.id)
    except Exception as ex: 
        raise SERVER_ERROR
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    try:
        category_by_name = await category_repository.get_category_by_name(db=db, name=category_update.name)
    except Exception as ex: 
        raise SERVER_ERROR
    
    if category_by_name and category_by_name.id != category_update.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Already exists category with name {0}".format(category_update.name)
        )
    try:
        return await category_repository.update_category(db=db, category_update=category_update)
    except Exception as ex:
        raise SERVER_ERROR
    
# Delete
async def delete_category(db: AsyncSession, id_category: int) -> None:
    try:
        category = await category_repository.get_category_by_id(db=db, id=id_category)
    except Exception as ex: 
        raise SERVER_ERROR
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    try:
        return await category_repository.delete_category(db=db, id_category=id_category)
    
    except IntegrityError as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category cannot be removed as there is a product associated with it.")
    except Exception as ex:
        raise SERVER_ERROR
