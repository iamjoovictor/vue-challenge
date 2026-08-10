"""create_password_reset_token_table

Revision ID: bb22cc33dd44
Revises: aa11bb22cc33
Create Date: 2026-08-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bb22cc33dd44'
down_revision = 'aa11bb22cc33'
branch_labels = None
depends_on = None

table_name = 'password_reset_token'


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, primary_key=True, comment='Token identifier'),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False, comment='Associated user'),
        sa.Column('token', sa.String(255), nullable=False, unique=True, comment='UUID reset token'),
        sa.Column('expires_at', sa.DateTime, nullable=False, comment='Token expiry timestamp'),
        sa.Column('used', sa.Boolean, nullable=False, server_default='0', comment='Whether the token was already used'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Creation timestamp'),
    )


def downgrade() -> None:
    op.drop_table(table_name)
