"""Add foreignkey to posts

Revision ID: 19168e8e7913
Revises: 5253f87ddcaa
Create Date: 2026-04-27 13:49:32.511446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19168e8e7913'
down_revision: Union[str, Sequence[str], None] = '5253f87ddcaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_owner_id_fkey', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
