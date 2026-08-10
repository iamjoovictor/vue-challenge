"""create_sale_table

Revision ID: dd44ee55ff66
Revises: cc33dd44ee55
Create Date: 2026-08-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'dd44ee55ff66'
down_revision = 'cc33dd44ee55'
branch_labels = None
depends_on = None

table_name = 'sale'


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, primary_key=True, comment='Sale identifier'),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('product.id'), nullable=False, comment='Sold product'),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False, comment='User who registered the sale'),
        sa.Column('quantity', sa.Integer, nullable=False, comment='Units sold'),
        sa.Column('sold_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Sale timestamp'),
    )


def downgrade() -> None:
    op.drop_table(table_name)
