"""add_quantity_to_product

Revision ID: cc33dd44ee55
Revises: bb22cc33dd44
Create Date: 2026-08-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'cc33dd44ee55'
down_revision = 'bb22cc33dd44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('product', sa.Column('quantity', sa.Integer, nullable=False, server_default='0', comment='Units in stock'))


def downgrade() -> None:
    op.drop_column('product', 'quantity')
