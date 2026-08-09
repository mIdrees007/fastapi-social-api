"""add foreign-key to posts table

Revision ID: c77fc1ea565e
Revises: 507e279f54b5
Create Date: 2026-08-09 04:38:25.746729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c77fc1ea565e'
down_revision: Union[str, Sequence[str], None] = '507e279f54b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
