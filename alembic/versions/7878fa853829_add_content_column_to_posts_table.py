"""add content column to posts table

Revision ID: 7878fa853829
Revises: 0195ea878ea4
Create Date: 2026-08-09 02:38:05.090564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7878fa853829'
down_revision: Union[str, Sequence[str], None] = '0195ea878ea4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
