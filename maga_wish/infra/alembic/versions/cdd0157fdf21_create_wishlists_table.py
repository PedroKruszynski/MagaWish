"""create wishlists table

Revision ID: cdd0157fdf21
Revises: c0858e1d8d64
Create Date: 2025-03-10 18:58:26.805149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdd0157fdf21'
down_revision: Union[str, None] = 'd2ce70739f1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'wishlists',
        sa.Column('id', sa.UUID(), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('product_id', sa.UUID(), nullable=False),
        sa.Column('added_at', sa.DateTime(), nullable=False, default=sa.func.now()),
    )

    op.create_unique_constraint('uq_user_product', 'wishlists', ['user_id', 'product_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('wishlists')
