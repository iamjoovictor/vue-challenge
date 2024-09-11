from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..middleware.utils_db import get_session
from ..middleware.security import get_current_user
from ..controllers import category_controller
from ..schemas import category_schema
from typing import List

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Responsible for managing Category routes

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 09, 2024           
"""

router = APIRouter(tags=["category"], prefix="/category")

# Create
@router.post('/', response_model=category_schema.Category)
async def create_categoy(
    category_create: category_schema.CategoryCreate, db: AsyncSession = Depends(get_session), current_user: bool = Depends(get_current_user)
):
    """
    Create a new category.
    """
    return await category_controller.create_category(db=db, category_create=category_create)

# Read
@router.get("/", response_model=List[category_schema.Category])
async def get_all_categories(db: AsyncSession = Depends(get_session), current_user: bool = Depends(get_current_user)):
    """
    Get all Categories from database.
    """
    return await category_controller.get_all_categories(db=db)

# Update
@router.put('/', response_model=None)
async def update_category(
    category_update: category_schema.Category, db: AsyncSession = Depends(get_session), current_user: bool = Depends(get_current_user)
):
    """
    Update an  category.
    """
    return await category_controller.update_category(db=db, category_update=category_update)

# Delete
@router.delete('/', response_model=None)
async def delete_category(
    id_category: int = Query(gt=0, example=1), db: AsyncSession = Depends(get_session), current_user: bool = Depends(get_current_user)
):
    """
    Delete an category.
    """
    return await category_controller.delete_category(db=db, id_category=id_category)