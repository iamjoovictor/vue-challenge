from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..middleware.utils_db import get_session
from ..controllers import product_controller
from ..middleware.security import get_current_user
from ..schemas import product_schema
from typing import List

""""
    @copyright  ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Responsible for managing Product routes

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 09, 2024           
"""

router = APIRouter(tags=["product"], prefix="/product")

# Create
@router.post('/', response_model=product_schema.Product)
async def create_product(
    product_create: product_schema.ProductCreate, db: AsyncSession = Depends(get_session), current_user: bool = Depends(get_current_user)
):
    """
    Create a new product.

    **Request body:** `ProductCreate` — name, price, expiration_date, image (optional), id_category (optional).

    **Returns:** The created `Product` object including the generated `id`.

    **Errors:**
    - `409 Conflict` — a product with the same name already exists.
    - `500 Internal Server Error` — unexpected database error.
    """
    return await product_controller.create_product(db=db, product_create=product_create)

# Read
@router.get("/", response_model=List[product_schema.Product])
async def get_all_products(db: AsyncSession = Depends(get_session), current_user: bool = Depends(get_current_user)):
    """
    Return the full list of products stored in the database.

    **Returns:** A list of `Product` objects (may be empty).

    **Errors:**
    - `500 Internal Server Error` — unexpected database error.
    """
    return await product_controller.get_all_products(db=db)

# Update
@router.put('/', response_model=None)
async def update_product(
    product_update: product_schema.Product, db: AsyncSession = Depends(get_session), current_user: bool = Depends(get_current_user)
):
    """
    Update an existing product.

    **Request body:** Full `Product` object (must include the `id` of the record to update).

    **Errors:**
    - `404 Not Found` — no product with the given `id` exists.
    - `409 Conflict` — another product already uses the requested name.
    - `500 Internal Server Error` — unexpected database error.
    """
    return await product_controller.update_product(db=db, product_update=product_update)

# Delete
@router.delete('/', response_model=None)
async def delete_product(
    id_product: int = Query(gt=0, example=1), db: AsyncSession = Depends(get_session), current_user: bool = Depends(get_current_user)
):
    """
    Delete a product by its ID.

    **Query parameter:** `id_product` (integer > 0) — the ID of the product to delete.

    **Errors:**
    - `404 Not Found` — no product with the given `id_product` exists.
    - `500 Internal Server Error` — unexpected database error.
    """
    return await product_controller.delete_product(db=db, id_product=id_product)