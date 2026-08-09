"""add user table 

Revision ID: 507e279f54b5
Revises: 7878fa853829
Create Date: 2026-08-09 02:54:02.578469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '507e279f54b5'
down_revision: Union[str, Sequence[str], None] = '7878fa853829'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
