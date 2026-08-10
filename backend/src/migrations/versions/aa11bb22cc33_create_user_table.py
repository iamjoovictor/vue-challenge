"""create_user_table

Revision ID: aa11bb22cc33
Revises: dd9499ba0c30
Create Date: 2026-08-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import bcrypt

# revision identifiers, used by Alembic.
revision = 'aa11bb22cc33'
down_revision = 'dd9499ba0c30'
branch_labels = None
depends_on = None

table_name = 'user'


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, primary_key=True, comment='User identifier'),
        sa.Column('username', sa.String(100), nullable=False, unique=True, comment='Username'),
        sa.Column('email', sa.String(255), nullable=False, unique=True, comment='User email'),
        sa.Column('hashed_password', sa.String(255), nullable=False, comment='Bcrypt hashed password'),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='1', comment='Whether the user is active'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), comment='Creation timestamp'),
    )

    admin_hash = bcrypt.hashpw(b"@Test2026", bcrypt.gensalt()).decode('utf-8')

    connection = op.get_bind()
    connection.execute(
        sa.text(
            "INSERT INTO `user` (username, email, hashed_password, is_active) "
            "VALUES (:username, :email, :hashed_password, :is_active)"
        ),
        {"username": "admin", "email": "admin@example.com", "hashed_password": admin_hash, "is_active": 1}
    )


def downgrade() -> None:
    op.drop_table(table_name)
