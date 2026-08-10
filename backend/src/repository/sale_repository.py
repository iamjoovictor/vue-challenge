from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from ..models.sale_model import Sale
from ..models.product_model import Product
from ..models.user_model import User
from ..models.category_model import Category


async def create_sale(db: AsyncSession, product_id: int, user_id: int, quantity: int) -> Sale:
    sale = Sale(product_id=product_id, user_id=user_id, quantity=quantity)
    db.add(sale)
    await db.flush()
    await db.refresh(sale)
    await db.commit()
    return sale


async def get_last_4_sales(db: AsyncSession) -> list:
    result = await db.execute(
        select(
            Sale.id,
            Sale.sold_at,
            Sale.quantity,
            User.username,
            Product.name.label('product_name'),
        )
        .join(Product, Sale.product_id == Product.id)
        .join(User, Sale.user_id == User.id)
        .order_by(Sale.sold_at.desc())
        .limit(4)
    )
    return [dict(row) for row in result.mappings().all()]


async def get_top_10_products_by_sales(db: AsyncSession) -> list:
    result = await db.execute(
        select(
            Product.name,
            func.sum(Sale.quantity).label('total'),
        )
        .join(Product, Sale.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .order_by(func.sum(Sale.quantity).desc())
        .limit(10)
    )
    return [dict(row) for row in result.mappings().all()]


async def get_sales_by_category(db: AsyncSession) -> list:
    result = await db.execute(
        select(
            Category.name,
            func.sum(Sale.quantity).label('total'),
        )
        .join(Product, Sale.product_id == Product.id)
        .join(Category, Product.id_category == Category.id)
        .group_by(Category.id, Category.name)
        .order_by(func.sum(Sale.quantity).desc())
    )
    rows = [dict(row) for row in result.mappings().all()]

    if len(rows) <= 3:
        return rows

    top3 = rows[:3]
    others_total = sum(r['total'] for r in rows[3:])
    top3.append({'name': 'Outros', 'total': others_total})
    return top3
