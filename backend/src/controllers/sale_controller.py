from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from fastapi import HTTPException, status
from ..repository import sale_repository, product_repository, user_repository
from ..schemas import sale_schema
from ..middleware.utils import SERVER_ERROR
from ..middleware.websocket_manager import manager
import json


async def create_sale(
    db: AsyncSession,
    sale_create: sale_schema.SaleCreate,
    current_username: str,
) -> sale_schema.Sale:
    try:
        product = await product_repository.get_product_by_id(db, sale_create.product_id)
    except Exception:
        raise SERVER_ERROR

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.quantity < sale_create.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock ({product.quantity} available)",
        )

    try:
        user = await user_repository.get_user_by_username(db, current_username)
    except Exception:
        raise SERVER_ERROR

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        sale = await sale_repository.create_sale(db, sale_create.product_id, user.id, sale_create.quantity)
        await db.execute(
            update(product.__class__)
            .where(product.__class__.id == product.id)
            .values(quantity=product.quantity - sale_create.quantity)
        )
        await db.commit()
    except Exception:
        raise SERVER_ERROR

    await manager.broadcast(json.dumps({
        "event": "sale_created",
        "product": product.name,
        "quantity": sale_create.quantity,
    }))

    return sale


async def get_sales_history(db: AsyncSession) -> list:
    try:
        return await sale_repository.get_last_4_sales(db)
    except Exception:
        raise SERVER_ERROR


async def get_top_products(db: AsyncSession) -> list:
    try:
        return await sale_repository.get_top_10_products_by_sales(db)
    except Exception:
        raise SERVER_ERROR


async def get_category_sales(db: AsyncSession) -> list:
    try:
        return await sale_repository.get_sales_by_category(db)
    except Exception:
        raise SERVER_ERROR
