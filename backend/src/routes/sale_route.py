from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..middleware.utils_db import get_session
from ..middleware.security import get_current_user
from ..controllers import sale_controller
from ..schemas import sale_schema

router = APIRouter(tags=["sale"], prefix="/sale")


@router.post("/", response_model=sale_schema.Sale, status_code=status.HTTP_201_CREATED)
async def create_sale(
    sale_create: sale_schema.SaleCreate,
    db: AsyncSession = Depends(get_session),
    current_username: str = Depends(get_current_user),
):
    return await sale_controller.create_sale(db=db, sale_create=sale_create, current_username=current_username)


@router.get("/history", response_model=List[sale_schema.SaleHistoryItem])
async def get_sales_history(
    db: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    return await sale_controller.get_sales_history(db=db)


@router.get("/by-product", response_model=List[sale_schema.ProductSaleItem])
async def get_top_products(
    db: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    return await sale_controller.get_top_products(db=db)


@router.get("/by-category", response_model=List[sale_schema.CategorySaleItem])
async def get_category_sales(
    db: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    return await sale_controller.get_category_sales(db=db)
