"""create posts table

Revision ID: 3b6a8518529d
Revises: 
Create Date: 2026-04-27 12:24:22.585707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b6a8518529d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        #sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')

    pass
