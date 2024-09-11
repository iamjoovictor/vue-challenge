"""create_product_table

Revision ID: dd9499ba0c30
Revises: 13950aed4806
Create Date: 2024-09-09 18:55:15.873233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd9499ba0c30'
down_revision = '13950aed4806'
branch_labels = None
depends_on = None

table_name = 'product'

def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, primary_key=True, comment='Product identifier'),
        sa.Column('name', sa.String(200), comment='Product name'),
        sa.Column('price',  sa.Float, comment='Product value'),
        sa.Column('expiration_date',  sa.Date, comment='Product expiration date'),
        sa.Column('image',  sa.String(255), comment='Product image url'),
        sa.Column('id_category',  sa.Integer, sa.ForeignKey("category.id"), comment= 'Category identifier associated with the product'),
    )


def downgrade() -> None:
    op.drop_table(table_name)
