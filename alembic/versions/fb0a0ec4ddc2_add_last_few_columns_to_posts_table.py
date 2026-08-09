"""add last few columns to posts table

Revision ID: fb0a0ec4ddc2
Revises: c77fc1ea565e
Create Date: 2026-08-09 04:55:14.132230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb0a0ec4ddc2'
down_revision: Union[str, Sequence[str], None] = 'c77fc1ea565e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column(
    'published', sa.Boolean(), nullable=False, server_default='TRUE'),)\
        
    op.add_column('posts', sa.Column(
    'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
    ('NOW()')),)
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
