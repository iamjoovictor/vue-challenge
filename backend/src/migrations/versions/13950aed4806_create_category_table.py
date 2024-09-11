"""create_category_table

Revision ID: 13950aed4806
Revises: 
Create Date: 2024-09-09 18:55:01.421086

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '13950aed4806'
down_revision = None
branch_labels = None
depends_on = None

table_name = 'category'

def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, primary_key=True, comment='Category identifier'),
        sa.Column('name', sa.String(100), comment='Category name')
    )

def downgrade() -> None:
    op.drop_table(table_name)